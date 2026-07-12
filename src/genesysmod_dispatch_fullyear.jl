"""
Full-year (8760 h) multi-region economic dispatch — a Julia port of the
standalone GAMS `genesysmod_dispatch.gms`.

It FIXES capacities from a prior investment run (read from
`genesysmod_db.duckdb`, scenario- + year-keyed; falls back to the pre-merge
`genesysmod_results_db.duckdb`), pulls the hourly
profiles + merged demand from a full-resolution data load (`elmod_nthhour=1`),
builds an hourly LP over ALL regions, solves it, and writes the hourly
dispatch (generation by tech, storage in/out/SoC, net trade flow, curtailment,
unserved energy and the nodal price = energy-balance dual) to
`genesysmod_dispatch_results.duckdb`, keyed by (Scenario, Year, Region, Hour).

Differences from the GAMS original, by design (see the port plan):
  * data-driven tech classes, ramping (Par_RampingUp/DownFactor) and storage
    sizing (actual S_ energy + D_ power from the run), not hard-coded lists;
  * one merged Power demand (Σ of the Power_* segments × hourly profile), not
    the GAMS single-'power' carrier (NA splits demand across segments);
  * cyclic storage (SoC[end] = SoC[1]); everything internal in GWh;
  * price/quantity-curve + base-file two-stage machinery dropped.

Entry point: `genesysmod_dispatch_fullyear(; years, scenario, ...)`.
"""

const DISPATCH_RESULTS_DB_FILENAME = "genesysmod_dispatch_results.duckdb"
const PJ_TO_GWH = 1000.0 / 3.6        # 277.78 — PJ → GWh (model energy is PJ; caps are GW)
const DISP_EPS = 1e-6                  # tie-break weight (suppress idle cycling/curtailment/wheeling)
const DISP_VOLL = 10.0                 # legacy/World-default value of lost load, MEUR/GWh (= 10 000
                                       # EUR/MWh); per-region override via Par_DispatchVoLL
# (must-run shares moved to data: Par_DispatchMinActivity in DispatchData_<region>.xlsx)
# storage round-trip efficiency split convention (mirrors GAMS NE3: charge gains
# (1+eff)/2, discharge pays 2/(1+eff)); StorageLosses = per-hour self-discharge.
const DISP_STORAGE_LOSSES = Dict("S_Battery_Li-Ion" => 0.00417)   # ≈10%/day; others 0

_dispatch_db_path(resultdir) = joinpath(resultdir, DISPATCH_RESULTS_DB_FILENAME)
# Investment results live in the merged genesysmod_db.duckdb; fall back to the
# pre-merge results-only file so dispatch still runs on older investment runs.
function _results_db_path_from(resultdir)
    path = joinpath(resultdir, DB_FILENAME)
    legacy = joinpath(resultdir, LEGACY_RESULTS_DB_FILENAME)
    if !isfile(path) && isfile(legacy)
        println("  dispatch: $(DB_FILENAME) not found, using legacy $(LEGACY_RESULTS_DB_FILENAME)")
        return legacy
    end
    return path
end

# ---------------------------------------------------------------------------
# Dispatch cost configuration (merit-order realism) — fully DATA-DRIVEN.
# Read from DispatchData_<region>.xlsx in inputdir (built by the data repo's
# Conversion Script/convert_dispatch_data.py from Data/Dispatch/*.csv):
#   Par_DispatchTechClass      Technology -> Class + Fuel (region-agnostic)
#   Par_DispatchCostBins       Class, Bin, Share, CostMultiplier (fleet tranches)
#   Par_DispatchFuelCostFactor Region, Fuel, Value (regional fuel-price basis;
#                              'World' row = default)
#   Par_DispatchCO2Price       Region, Year, Value [EUR/tCO2] (milestones,
#                              linearly interpolated; absent region = 0)
# NO numbers live in this code. A missing file or unmatched tech/region/fuel
# falls back to neutral defaults (single bin, factor 1.0, CO2 price 0), so the
# feature is opt-in per dataset and portable to any region.
# ---------------------------------------------------------------------------
struct DispatchCostConfig
    techclass  ::Dict{String,Tuple{String,String}}        # tech -> (class, fuel)
    bins       ::Dict{String,Vector{Tuple{Float64,Float64}}}  # class -> [(share, mult)]
    # (region, fuel) -> [(months, multiplier)]; months === nothing is the
    # all-year/default row, a Set{Int} row applies only in those months
    # (seasonal hub basis, e.g. Algonquin winter premium)
    fuelfactor ::Dict{Tuple{String,String},Vector{Tuple{Union{Nothing,Set{Int}},Float64}}}
    co2price   ::Dict{String,Vector{Tuple{Int,Float64}}}  # region -> [(year, EUR/t)] sorted
    co2bench   ::Dict{String,Float64}                     # region -> free-allocation benchmark
                                                          # (tCO2/MWh; OBPS-style: only
                                                          # emissions ABOVE it pay the price)
    # market-realism layer (all optional; absent sheets = neutral / legacy behavior)
    minactivity ::Dict{Tuple{String,String},Float64}      # (region|World, tech) -> must-run share
                                                          # of hourly available capacity (self-
                                                          # committed coal, nuclear, cogen, hydro
                                                          # min-flow)
    bidadder   ::Dict{Tuple{String,String},Vector{Tuple{Int,Float64}}}
                                                          # (region|World, tech) -> [(year, EUR/MWh)]
                                                          # milestone-interpolated offer adder;
                                                          # negative = production subsidy (PTC), sets
                                                          # the curtailment-hour price floor
    voll       ::Dict{String,Float64}                     # region -> value of lost load EUR/MWh
                                                          # (World/absent -> DISP_VOLL)
    reservereq ::Dict{String,Tuple{Float64,Float64}}      # region -> (share of hourly demand, GW floor)
    ordc       ::Dict{String,Vector{Tuple{Float64,Float64}}} # region -> [(width share of req, EUR/MWh)]
                                                          # piecewise reserve-shortage penalty
    storagebins ::Dict{Tuple{String,Float64},Vector{Tuple{Int,Float64}}}
                                                          # (storage, duration h) -> [(year, power
                                                          # share)] milestones: split one aggregate
                                                          # storage into duration tranches with
                                                          # independent SoC (fleet duration mix,
                                                          # e.g. 1h/2h/4h/8h BESS, evolving by
                                                          # year); bin energy = share x power x
                                                          # hours, OVERRIDING the investment S_
                                                          # energy. Year absent/0 = all years.
end
const _NEUTRAL_DISPATCH_CONFIG = DispatchCostConfig(Dict(), Dict(), Dict(), Dict(), Dict(),
                                                    Dict(), Dict(), Dict(), Dict(), Dict(), Dict())

# month of an hour-of-year (1..8760, non-leap); clamped for safety
const _MONTH_END_HOUR = cumsum([31,28,31,30,31,30,31,31,30,31,30,31] .* 24)
_month_of_hour(h) = searchsortedfirst(_MONTH_END_HOUR, clamp(h, 1, 8760))

function read_dispatch_config(inputdir, dispatch_data_file)
    isempty(dispatch_data_file) && return _NEUTRAL_DISPATCH_CONFIG
    path = joinpath(inputdir, dispatch_data_file * ".xlsx")
    if !isfile(path)
        println("  dispatch: no $(basename(path)) — running with a flat merit order " *
                "(no cost bins / regional fuel / regional CO2)")
        return _NEUTRAL_DISPATCH_CONFIG
    end
    xf = XLSX.readxlsx(path)
    sheet(n) = n ∈ XLSX.sheetnames(xf) ? DataFrame(XLSX.gettable(xf[n])) : DataFrame()
    techclass = Dict{String,Tuple{String,String}}()
    for r ∈ eachrow(sheet("Par_DispatchTechClass"))
        techclass[string(r.Technology)] = (string(r.Class), string(r.Fuel))
    end
    bins = Dict{String,Vector{Tuple{Float64,Float64}}}()
    for r ∈ eachrow(sheet("Par_DispatchCostBins"))
        push!(get!(bins, string(r.Class), Tuple{Float64,Float64}[]),
              (Float64(r.Share), Float64(r.CostMultiplier)))
    end
    for (c, v) ∈ bins
        tot = sum(first.(v))
        abs(tot - 1.0) > 1e-6 && @warn "DispatchCostBins: shares for class $(c) sum to $(tot), renormalising"
        tot > 0 && (bins[c] = [(s/tot, m) for (s,m) ∈ v])
        wavg = sum(s*m for (s,m) ∈ bins[c])
        abs(wavg - 1.0) > 0.02 && @warn "DispatchCostBins: class $(c) capacity-weighted multiplier is $(round(wavg,digits=3)) (should be ~1.0 to preserve the fleet-mean cost)"
    end
    fuelfactor = Dict{Tuple{String,String},Vector{Tuple{Union{Nothing,Set{Int}},Float64}}}()
    ffsheet = sheet("Par_DispatchFuelCostFactor")
    for r ∈ eachrow(ffsheet)
        months = nothing   # all-year/default row
        if "Months" ∈ names(ffsheet) && !ismissing(r.Months) && !isempty(strip(string(r.Months)))
            months = Set(parse(Int, m) for m ∈ split(string(r.Months), ",") if !isempty(strip(m)))
        end
        push!(get!(fuelfactor, (string(r.Region), string(r.Fuel)),
                   Tuple{Union{Nothing,Set{Int}},Float64}[]), (months, Float64(r.Value)))
    end
    co2price = Dict{String,Vector{Tuple{Int,Float64}}}()
    co2bench = Dict{String,Float64}()
    co2sheet = sheet("Par_DispatchCO2Price")
    for r ∈ eachrow(co2sheet)
        push!(get!(co2price, string(r.Region), Tuple{Int,Float64}[]), (Int(r.Year), Float64(r.Value)))
        # optional output-based free-allocation benchmark (tCO2/MWh); only
        # emissions above it pay the price (e.g. Canada's federal OBPS)
        if "FreeAllocBenchmark" ∈ names(co2sheet) && !ismissing(r.FreeAllocBenchmark)
            b = Float64(r.FreeAllocBenchmark)
            b > 0 && (co2bench[string(r.Region)] = b)
        end
    end
    foreach(v -> sort!(v, by=first), values(co2price))
    # optional Region column helper: missing/empty -> 'World' default row
    _reg(row, nms) = ("Region" ∈ nms && !ismissing(row.Region) &&
                      !isempty(strip(string(row.Region)))) ? string(row.Region) : "World"
    minactivity = Dict{Tuple{String,String},Float64}()
    masheet = sheet("Par_DispatchMinActivity")
    for r ∈ eachrow(masheet)
        minactivity[(_reg(r, names(masheet)), string(r.Technology))] = Float64(r.Share)
    end
    bidadder = Dict{Tuple{String,String},Vector{Tuple{Int,Float64}}}()
    basheet = sheet("Par_DispatchBidAdder")
    for r ∈ eachrow(basheet)
        push!(get!(bidadder, (_reg(r, names(basheet)), string(r.Technology)),
                   Tuple{Int,Float64}[]), (Int(r.Year), Float64(r.Value)))
    end
    foreach(v -> sort!(v, by=first), values(bidadder))
    voll = Dict{String,Float64}()
    for r ∈ eachrow(sheet("Par_DispatchVoLL"))
        voll[string(r.Region)] = Float64(r.Value)
    end
    reservereq = Dict{String,Tuple{Float64,Float64}}()
    rrsheet = sheet("Par_DispatchReserveReq")
    for r ∈ eachrow(rrsheet)
        share = "ShareOfDemand" ∈ names(rrsheet) && !ismissing(r.ShareOfDemand) ? Float64(r.ShareOfDemand) : 0.0
        gwfloor = "MinGW" ∈ names(rrsheet) && !ismissing(r.MinGW) ? Float64(r.MinGW) : 0.0
        reservereq[string(r.Region)] = (share, gwfloor)
    end
    ordc = Dict{String,Vector{Tuple{Float64,Float64}}}()
    for r ∈ eachrow(sheet("Par_DispatchORDC"))
        push!(get!(ordc, string(r.Region), Tuple{Float64,Float64}[]),
              (Float64(r.WidthShare), Float64(r.Price)))
    end
    storagebins = Dict{Tuple{String,Float64},Vector{Tuple{Int,Float64}}}()
    sbsheet = sheet("Par_DispatchStorageBins")
    for r ∈ eachrow(sbsheet)
        y = "Year" ∈ names(sbsheet) && !ismissing(r.Year) ? Int(r.Year) : 0   # 0 = all-year row
        push!(get!(storagebins, (string(r.Storage), Float64(r.Hours)), Tuple{Int,Float64}[]),
              (y, Float64(r.PowerShare)))
    end
    foreach(v -> sort!(v, by=first), values(storagebins))
    println("  dispatch: cost config from $(basename(path)) — " *
            "$(length(techclass)) tech classes, $(length(bins)) bin sets, " *
            "$(length(fuelfactor)) fuel factors, $(length(co2price)) CO2 regions, " *
            "$(length(minactivity)) must-run rows, $(length(bidadder)) bid adders, " *
            "$(length(voll)) VoLL rows, $(length(ordc)) ORDC curves, " *
            "$(length(unique(first.(collect(keys(storagebins)))))) binned storages")
    return DispatchCostConfig(techclass, bins, fuelfactor, co2price, co2bench,
                              minactivity, bidadder, voll, reservereq, ordc, storagebins)
end

# class/fuel of a tech ("", "") when unmapped; bins for a tech (nothing = single)
_dc_class(cfg, t) = get(cfg.techclass, t, ("", ""))
_dc_bins(cfg, t)  = get(cfg.bins, _dc_class(cfg, t)[1], nothing)
# regional fuel-cost multiplier at month `mon`: a month-specific row wins over
# the all-year row; exact region -> World default -> 1.0
function _dc_fuelmult(cfg, r, t, mon)
    fuel = _dc_class(cfg, t)[2]
    isempty(fuel) && return 1.0
    for key ∈ ((r, fuel), ("World", fuel))
        rows = get(cfg.fuelfactor, key, nothing)
        rows === nothing && continue
        for (months, v) ∈ rows          # month-specific rows first
            months !== nothing && mon ∈ months && return v
        end
        for (months, v) ∈ rows          # then the all-year/default row
            months === nothing && return v
        end
    end
    return 1.0
end
# linear interpolation between sorted (year, value) milestones, clamped at the ends
function _interp_milestones(ms, year)
    isempty(ms) && return 0.0
    year <= ms[1][1] && return ms[1][2]
    year >= ms[end][1] && return ms[end][2]
    for i ∈ 2:length(ms)
        y1, v1 = ms[i-1]; y2, v2 = ms[i]
        y1 <= year <= y2 && return v1 + (v2 - v1) * (year - y1) / (y2 - y1)
    end
    return ms[end][2]
end
# regional CO2 price (EUR/t) at `year`; region absent -> World -> 0.
_dc_co2(cfg, r, year) =
    _interp_milestones(get(cfg.co2price, r, get(cfg.co2price, "World", Tuple{Int,Float64}[])), year)
# must-run share of hourly available capacity; exact region -> World -> 0
_dc_minact(cfg, r, t) = get(cfg.minactivity, (r, t), get(cfg.minactivity, ("World", t), 0.0))
# offer adder EUR/MWh at `year` (negative = subsidy); (region, tech) -> World -> 0
_dc_bidadder(cfg, r, t, year) =
    _interp_milestones(get(cfg.bidadder, (r, t),
                           get(cfg.bidadder, ("World", t), Tuple{Int,Float64}[])), year)
# value of lost load EUR/MWh; region -> World -> legacy DISP_VOLL (10 000)
_dc_voll(cfg, r) = get(cfg.voll, r, get(cfg.voll, "World", DISP_VOLL * 1000.0))
# duration-bin set for storage `s` at `year`: per-duration power shares are
# milestone-interpolated (Year 0 rows apply to all years), zero-share bins are
# dropped and the rest renormalised. Returns nothing when `s` has no bin rows.
function _dc_storagebins(cfg, s, year)
    hrs = sort!([h for (st, h) ∈ keys(cfg.storagebins) if st == s])
    isempty(hrs) && return nothing
    out = Tuple{Float64,Float64}[]
    for h ∈ hrs
        sh = _interp_milestones(cfg.storagebins[(s, h)], year)
        sh > 1e-9 && push!(out, (sh, h))
    end
    isempty(out) && return nothing
    tot = sum(first.(out))
    return [(sh / tot, h) for (sh, h) ∈ out]
end

# ---------------------------------------------------------------------------
# Build a Switch for a full-resolution (elmod_nthhour=1) all-region data load.
# Mirrors genesysmod_main's Switch construction; NoDispatch so dataload keeps
# all regions, errorcheck off (8760-timeslice load trips full-year invariants).
# ---------------------------------------------------------------------------
function _make_dispatch_switch(; year, model_region, data_base_region, data_file, hourly_data_file,
        allfuels_data_file, switch_power_only_mode, inputdir, resultdir, emissionPathway,
        emissionScenario, threads, DNLPsolver, elmod_nthhour, extr_str)
    isdir(resultdir) || mkdir(resultdir)
    daystep = elmod_nthhour ÷ 24
    hourstep = elmod_nthhour % 24
    return Switch(Int16(year), DNLPsolver, model_region, data_base_region, data_file, hourly_data_file,
        threads, emissionPathway, emissionScenario, 0.05, inputdir, resultdir,
        WithInfeasibilityTechs(), 0, 1, 1, 1, 0.9, 1, 0.75, 0.25, 2, 0,
        0, 0, 0, 1.0, 0.15, 0.5, 0.25, 2030, 1, 1, 0, 0, 0, "",
        NoDispatch(), Int16(elmod_nthhour), Int16(1), 0, Int16(daystep), Int16(hourstep),
        NoRawResult(), 0, 0, 0, 0, extr_str, "dispatch", 0,
        switch_power_only_mode, allfuels_data_file, 0, 0, 0)
end

# ---------------------------------------------------------------------------
# Read the fixed investment results from genesysmod_db.duckdb
# ---------------------------------------------------------------------------
"""
Return (cap, scap, ntc) for one (scenario, year):
  cap[t,r]  GW  — TotalCapacityAnnual            (raw_TotalCapacityAnnual)
  scap[s,r] PJ  — TotalStorageCapacityAnnual     (raw_TotalStorageCapacityAnnual, S_ storages)
  ntc[r,rr] GW  — TotalTradeCapacity for 'Power'  (raw_TotalTradeCapacity, sparse x1..x4)
as DenseAxisArrays over the dispatch Sets.
"""
function read_investments_db(results_db, scenario, year, Sets)
    # READ-ONLY, non-cached connection, closed as soon as the three frames are
    # read: the dispatch only ever reads the investment database, so a
    # multi-hour dispatch run must not hold a (write-mode) lock on it — that
    # blocked every external reader/writer for the whole run. A read-only
    # handle also coexists with other readers even while briefly open.
    con = DuckDB.DB(results_db; readonly=true)
    sc = String(scenario); yr = Int(year)
    function df_or_empty(sql, params)
        try
            return DataFrame(DBInterface.execute(con, sql, params))
        catch e
            @warn "dispatch: query failed" sql exception=e
            return DataFrame()
        end
    end
    capdf = df_or_empty("SELECT Technology, Region, Value FROM raw_TotalCapacityAnnual " *
                        "WHERE Scenario = ? AND Year = ?", [sc, yr])
    scapdf = df_or_empty("SELECT Storage, Region, Value FROM raw_TotalStorageCapacityAnnual " *
                         "WHERE Scenario = ? AND Year = ?", [sc, yr])
    # sparse trade table: x1=Year, x2=Fuel, x3=Region, x4=Region2, y=Value
    ntcdf = df_or_empty("SELECT x3, x4, y FROM raw_TotalTradeCapacity " *
                        "WHERE Scenario = ? AND x1 = ? AND lower(x2) = 'power'", [sc, yr])
    try
        DBInterface.close!(con)
    catch e
        @warn "dispatch: could not close read-only investment-db handle" exception=e
    end
    GC.gc()   # drop query-result finalizers so the file handle is really released
    cap = create_daa(capdf, "", Sets.Technology, Sets.Region_full)
    scap = create_daa(scapdf, "", Sets.Storage, Sets.Region_full)
    ntc = create_daa(ntcdf, "", Sets.Region_full, Sets.Region_full)
    return cap, scap, ntc
end

# ---------------------------------------------------------------------------
# Tech classification (data-driven) + merged demand
# ---------------------------------------------------------------------------
"Power-producing techs split into (dispatchable, variable, storage_power_map)."
function classify_dispatch_techs(Sets, Params, Maps)
    𝓛 = Sets.Timeslice
    # techs that output Power in some (mode, year)
    outputs_power(t) = any(Params.OutputActivityRatio[r,t,"Power",m,y] > 0
                           for r ∈ Sets.Region_full for m ∈ Sets.Mode_of_operation for y ∈ Sets.Year)
    excl = Set(get(Params.Tags.TagTechnologyToSubsets, "DummyTechnology", String[]))
    is_storage_D(t) = startswith(t, "D_")
    is_aux(t) = startswith(t, "X_") || startswith(t, "Infeasibility") || startswith(t, "R_") || startswith(t, "Z_")
    # VARIABLE RE = Solar ∪ Wind ∪ {P_Hydro_RoR} — exactly the set genesysmod_bounds
    # zeroes TagDispatchableTechnology for (bounds.jl:218). We can't read the runtime
    # tag here (dataload inits it to 1 for all; only bounds zeroes the variable set,
    # and we don't run bounds), so we replicate that subset directly. Everything else
    # that outputs Power (thermal, hydro reservoir, geothermal, EGS, ocean) is
    # DISPATCHABLE. D_ storage / X_Convert / Infeasibility / R_,Z_ excluded.
    varset = Set(vcat(intersect(Sets.Technology, get(Params.Tags.TagTechnologyToSubsets, "Solar", String[])),
                      intersect(Sets.Technology, get(Params.Tags.TagTechnologyToSubsets, "Wind", String[])),
                      ["P_Hydro_RoR"]))
    disp = String[]; var = String[]
    for t ∈ Sets.Technology
        (t ∈ excl || is_aux(t) || is_storage_D(t)) && continue
        outputs_power(t) || continue
        (t ∈ varset ? push!(var, t) : push!(disp, t))
    end
    # storage S_ -> its D_ power tech (name pairing S_X -> D_X)
    storage_power = Dict(s => replace(s, r"^S_" => "D_") for s ∈ Sets.Storage)
    return disp, var, storage_power
end

"Merged hourly Power demand[r,h] in GWh = Σ over Power_* segments of Params.Demand (PJ).
Params.Demand is indexed [Year, Timeslice, Fuel, Region]."
function merged_power_demand(Sets, Params, y0)
    𝓛 = Sets.Timeslice
    demand_fuels = [f for f ∈ Sets.Fuel if startswith(f, "Power") &&
                    any(Params.SpecifiedAnnualDemand[r,f,y] != 0 for r ∈ Sets.Region_full for y ∈ Sets.Year)]
    d = Dict{Tuple{String,Any},Float64}()
    for r ∈ Sets.Region_full, l ∈ 𝓛
        d[(r,l)] = sum(Params.Demand[y0,l,f,r] for f ∈ demand_fuels; init=0.0) * PJ_TO_GWH
    end
    return d, demand_fuels
end

# ---------------------------------------------------------------------------
# Build + solve one dispatch year
# ---------------------------------------------------------------------------
function dispatch_build_solve_year(switch, solver, solver_attr, results_db, scenario,
                                   year, cyclic_storage, co2_price_mode,
                                   dcfg::DispatchCostConfig = _NEUTRAL_DISPATCH_CONFIG)
    Sets, Params, _ = genesysmod_dataload(switch)
    power_only_precompute!(Params, Sets, switch)
    Maps = make_mapping(Sets, Params)

    𝓡 = Sets.Region_full
    𝓛 = Sets.Timeslice                 # the hours (1:8760 at elmod_nthhour=1)
    # The data load (NoDispatch) keeps ALL modelled years, so index every per-year
    # parameter (demand, profiles, AF, VC, emissions) by the DISPATCH year — NOT
    # Sets.Year[1], which is always 2025 and would freeze demand/weather there.
    y0 = Int(year) ∈ Sets.Year ? Int(year) : Sets.Year[1]
    disp, var, storage_power = classify_dispatch_techs(Sets, Params, Maps)
    demand, demand_fuels = merged_power_demand(Sets, Params, y0)
    println("  dispatch $(year): regions=$(length(𝓡)) hours=$(length(𝓛)) " *
            "disp=$(length(disp)) var=$(length(var)) storage=$(length(Sets.Storage)) " *
            "demandfuels=$(demand_fuels)")

    cap, scap, ntc = read_investments_db(results_db, scenario, year, Sets)

    # --- per-(r,tech) coefficients ---
    af(r,d) = Params.AvailabilityFactor[r,d,y0]
    # variable cost MEUR/GWh (VariableCost is MEUR/PJ, fuel already baked in power-only)
    vc(r,d) = sum(Params.VariableCost[r,d,m,y0] for m ∈ Sets.Mode_of_operation; init=0.0) / PJ_TO_GWH
    # CO2 intensity tCO2/GWh via OutputEmissionRatio (power-only emission side), summed over modes
    emisCO2(r,d) = ("CO2" ∈ Sets.Emission) ?
        sum(Params.OutputEmissionRatio[r,d,"CO2",m,y0] for m ∈ Sets.Mode_of_operation; init=0.0) * PJ_TO_GWH : 0.0
    # variable RE capacity factor per timeslice (the resource fraction; the model's
    # variable production is cap×CF, no AF — matches genesysmod_equ).
    cf(r,v,l) = Params.CapacityFactor[r,v,l,y0]
    # hours represented by timeslice l (= 1 at full hourly resolution). Converts
    # power (GW) limits to per-timeslice energy (GWh); demand is already GWh/ts.
    dur(l) = Params.YearSplit[l,y0] * 8760.0
    # ramping fraction of capacity per hour (our researched hour-level factors)
    rup(d)  = Params.RampingUpFactor   === nothing ? 1.0 : Params.RampingUpFactor[d,y0]
    rdn(d)  = Params.RampingDownFactor === nothing ? 1.0 : Params.RampingDownFactor[d,y0]
    # storage: power (GW) from D_ cap, energy (GWh) from S_ cap (PJ→GWh), RTE from discharge OAR (mode 2)
    spow(r,s) = cap[storage_power[s], r]
    sene(r,s) = scap[s, r] * PJ_TO_GWH
    # real round-trip efficiency from the charge/discharge ratios (GAMS used OAR
    # mode-2 = 1.0, i.e. lossless — we use the actual To/FromStorage instead).
    # To is nonzero only in the charge mode, From only in the discharge mode, so
    # max-over-modes picks the right value. Guard against 0 (-> lossless).
    ceff(s) = (e=maximum(Params.TechnologyToStorage[storage_power[s],s,m,y0]   for m ∈ Sets.Mode_of_operation; init=0.0); e>0 ? e : 1.0)
    deff(s) = (e=maximum(Params.TechnologyFromStorage[storage_power[s],s,m,y0] for m ∈ Sets.Mode_of_operation; init=0.0); e>0 ? e : 1.0)
    sloss(s)  = get(DISP_STORAGE_LOSSES, s, 0.0)
    # CO2 price per region (endogenous = EmissionsPenalty; else a scalar)
    co2price(r) = co2_price_mode === :endogenous ?
        (hasproperty(Params, :EmissionsPenalty) && "CO2" ∈ Sets.Emission ?
            Params.EmissionsPenalty[r,"CO2",y0] : 0.0) : Float64(co2_price_mode)

    # --- merit-order cost config (data-driven; see read_dispatch_config) ---
    # CO2 intensity in t/GWh: OutputEmissionRatio is Gt/PJ -> x1e9 [t/Gt] / 277.8 [GWh/PJ]
    co2_t_per_GWh(r,d) = ("CO2" ∈ Sets.Emission) ?
        sum(Params.OutputEmissionRatio[r,d,"CO2",m,y0] for m ∈ Sets.Mode_of_operation; init=0.0) * 1.0e9 / PJ_TO_GWH : 0.0
    # regional carbon price (EUR/t) from the dispatch config, per region at this year
    regco2 = Dict(r => _dc_co2(dcfg, r, Int(year)) for r ∈ 𝓡)
    # marginal cost basis MEUR/GWh: fuel-basis-scaled VC + regional carbon cost
    # (t/GWh x EUR/t x 1e-6 -> MEUR/GWh). The fuel factor is month-aware
    # (seasonal hub basis, e.g. Algonquin winter premium), so basecost takes the
    # timeslice h; the month comes from the hour-of-year (position-scaled if the
    # run is not at full 8760 resolution). Where a free-allocation benchmark is
    # set (output-based systems, e.g. Canada OBPS), only the intensity ABOVE the
    # benchmark pays. Neutral (== vc) when the tech/region is not in the config.
    co2part(r,d) = max(0.0, co2_t_per_GWh(r,d) - get(dcfg.co2bench, r, 0.0) * 1000.0) * regco2[r] * 1.0e-6
    nts = length(𝓛)
    month_of_ts = Dict(h => _month_of_hour(ceil(Int, i * 8760 / nts)) for (i,h) ∈ enumerate(𝓛))
    basecost(r,d,h) = vc(r,d) * _dc_fuelmult(dcfg, r, d, month_of_ts[h]) + co2part(r,d)

    # per-region value of lost load (MEUR/GWh conversion: EUR/MWh x 1e-3); the
    # nodal price cap in unserved hours (data-driven, Par_DispatchVoLL)
    infeas_pen(r) = _dc_voll(dcfg, r) * 1.0e-3
    # offer adder (subsidy) per (region, tech), MEUR/GWh; negative = PTC-style
    # revenue. Applied to dispatchable AND variable techs.
    adder = Dict((r,t) => _dc_bidadder(dcfg, r, t, Int(year)) * 1.0e-3
                 for r ∈ 𝓡 for t ∈ vcat(disp, var))
    has_adders = any(v != 0.0 for v ∈ values(adder))
    # curtailment cost: the deepest subsidy present (spilling subsidized RE
    # forgoes it), so the generic dump variable never undercuts the subsidized
    # resources' own spill; neutral (= tie-break EPS) when no adders configured.
    curt_cost = has_adders ? maximum(abs(v) for v ∈ values(adder)) : DISP_EPS

    model = JuMP.Model(solver)
    H = collect(𝓛); nH = length(H)
    hidx = Dict(h => i for (i,h) ∈ enumerate(H))   # chronological order

    # --- storage duration bins (Par_DispatchStorageBins): a configured storage
    #     is split into tranches with independent SoC ("s#k"); bin energy =
    #     power share x total power x duration hours, OVERRIDING the investment
    #     S_ energy (fleet duration-mix realism). Unconfigured storages keep one
    #     tranche with the investment energy (hours sentinel < 0). ---
    sbins = String[]
    sbmap = Dict{String,Tuple{String,Float64,Float64}}()   # sid -> (parent, power share, hours; <0 = investment energy)
    for s ∈ Sets.Storage
        binsdef = _dc_storagebins(dcfg, s, Int(year))
        if binsdef === nothing
            push!(sbins, s); sbmap[s] = (s, 1.0, -1.0)
        else
            for (k,(sh,hrs)) ∈ enumerate(binsdef)
                sid = "$(s)#$(k)"; push!(sbins, sid); sbmap[sid] = (s, sh, hrs)
            end
        end
    end
    spowb(r,sid) = sbmap[sid][2] * spow(r, sbmap[sid][1])
    seneb(r,sid) = sbmap[sid][3] < 0 ? sbmap[sid][2] * sene(r, sbmap[sid][1]) :
                                       sbmap[sid][3] * sbmap[sid][2] * spow(r, sbmap[sid][1])
    any(v -> haskey(dcfg.storagebins, v[1]), values(sbmap)) &&
        println("  dispatch: storage duration bins active — $(length(sbins)) tranches over $(length(Sets.Storage)) storages")

    # --- variables ---
    @variable(model, g[r ∈ 𝓡, d ∈ disp, H] >= 0)            # dispatchable gen (GWh)
    @variable(model, gup[r ∈ 𝓡, d ∈ disp, H] >= 0)
    @variable(model, gdn[r ∈ 𝓡, d ∈ disp, H] >= 0)
    @variable(model, vg[r ∈ 𝓡, v ∈ var, H] >= 0)            # variable gen (GWh)
    @variable(model, sin[r ∈ 𝓡, s ∈ sbins, H] >= 0)         # storage charge (GWh)
    @variable(model, sout[r ∈ 𝓡, s ∈ sbins, H] >= 0)        # storage discharge (GWh)
    @variable(model, soc[r ∈ 𝓡, s ∈ sbins, H] >= 0)         # state of charge (GWh)
    @variable(model, curt[r ∈ 𝓡, H] >= 0)                   # curtailment (GWh)
    @variable(model, flow[r ∈ 𝓡, rr ∈ 𝓡, H])                # net flow r->rr (GWh), free
    @variable(model, fpos[r ∈ 𝓡, rr ∈ 𝓡, H] >= 0)
    @variable(model, fneg[r ∈ 𝓡, rr ∈ 𝓡, H] >= 0)
    @variable(model, infe[r ∈ 𝓡, H] >= 0)                   # unserved (GWh)

    # --- merit-order cost bins: split each configured thermal fleet into
    #     tranches gb (sum = g) with per-tranche cost multipliers. Everything
    #     else (per-hour cap, AF, ramping, min-run, balance, outputs) stays on
    #     the total g, so the bins only shape the marginal-cost curve. ---
    binned = [(r,d) for r ∈ 𝓡 for d ∈ disp
              if _dc_bins(dcfg, d) !== nothing && cap[d,r] > 0 && af(r,d) > 0]
    binnedset = Set(binned)
    @variable(model, gb[p ∈ binned, k ∈ 1:length(_dc_bins(dcfg, p[2])), h ∈ H] >= 0)
    for (r,d) ∈ binned
        tranches = _dc_bins(dcfg, d)
        for h ∈ H
            capE = cap[d,r] * cf(r,d,h) * dur(h)
            for (k,(share,_)) ∈ enumerate(tranches)
                set_upper_bound(gb[(r,d),k,h], share * capE)
            end
            @constraint(model, sum(gb[(r,d),k,h] for k ∈ 1:length(tranches)) == g[r,d,h])
        end
    end
    isempty(binned) || println("  dispatch: cost bins active on $(length(binned)) (region, tech) fleets")

    has_route(r,rr) = ntc[r,rr] > 0

    # --- dispatchable: per-hour cap cap×CF (CF=1 for thermal, <1 for hydro etc.;
    #     matches investment CA3b -> full nameplate available at the peak hour),
    #     annual energy cap cap×CF×AF (matches CA5 -> AvailabilityFactor limits
    #     yearly utilisation, NOT the peak hour), must-run, fix-zero.
    #     (Earlier this derated every hour by AF, capping firm at 0.8×nameplate and
    #     overstating scarcity vs the fleet the investment actually built.) ---
    for r ∈ 𝓡, d ∈ disp
        if cap[d,r] > 0 && af(r,d) > 0
            # must-run share from Par_DispatchMinActivity (self-committed coal,
            # nuclear, cogen, hydro min-flow); capped at AF so the hourly floor
            # can never conflict with the annual availability budget
            mar = min(_dc_minact(dcfg, r, d), af(r,d))
            for h ∈ H
                capE = cap[d,r] * cf(r,d,h) * dur(h)   # GWh available in timeslice h
                @constraint(model, g[r,d,h] <= capE)
                mar > 0 && @constraint(model, g[r,d,h] >= mar * capE)
            end
            @constraint(model, sum(g[r,d,h] for h ∈ H) <=
                af(r,d) * sum(cap[d,r] * cf(r,d,h) * dur(h) for h ∈ H))
        else
            for h ∈ H; fix(g[r,d,h], 0.0; force=true); end
        end
    end

    # --- variable RE: without bid adders, fixed to capacity × CF × hours (spill
    #     via the generic curt variable — legacy behavior). With adders, vg is
    #     upper-bounded instead: spilling a subsidized resource then forgoes its
    #     adder revenue, so the curtailment-hour price floor lands at −adder
    #     (PTC-style negative pricing) and unsubsidized RE spills first. ---
    for r ∈ 𝓡, v ∈ var, h ∈ H
        pot = max(0.0, cap[v,r] * cf(r,v,h) * dur(h))
        if has_adders
            set_upper_bound(vg[r,v,h], pot)
        else
            fix(vg[r,v,h], pot; force=true)
        end
    end

    # --- ramping (chronological): Δgen between consecutive timeslices ---
    for r ∈ 𝓡, d ∈ disp
        (cap[d,r] > 0 && af(r,d) > 0) || continue
        for i ∈ 2:nH
            h = H[i]; hp = H[i-1]
            @constraint(model, g[r,d,h] - g[r,d,hp] == gup[r,d,h] - gdn[r,d,h])
            @constraint(model, gup[r,d,h] <= rup(d) * cap[d,r] * dur(h))
            @constraint(model, gdn[r,d,h] <= rdn(d) * cap[d,r] * dur(h))
        end
        fix(gup[r,d,H[1]], 0.0; force=true); fix(gdn[r,d,H[1]], 0.0; force=true)
    end

    # --- storage (cyclic SoC; per duration tranche) ---
    for r ∈ 𝓡, s ∈ sbins
        par = sbmap[s][1]
        p = spowb(r,s); e = seneb(r,s); ce = ceff(par); de = deff(par); loss = sloss(par)
        if p > 0 && e > 0
            for i ∈ 1:nH
                h = H[i]
                @constraint(model, sin[r,s,h]  <= p * dur(h))   # GW power -> GWh per timeslice
                @constraint(model, sout[r,s,h] <= p * dur(h))
                @constraint(model, soc[r,s,h]  <= e)            # energy capacity (GWh)
                if i == 1 && !cyclic_storage
                    continue        # non-cyclic: SoC[1] free start (bounded [0,e]), no predecessor link
                end
                hp = H[i == 1 ? nH : i-1]   # cyclic wrap: hour 1 follows hour 8760
                @constraint(model, soc[r,s,h] ==
                    soc[r,s,hp]*(1-loss) + sin[r,s,h]*ce - sout[r,s,h]/de)
                @constraint(model, sout[r,s,h] <= soc[r,s,hp])
            end
        else
            for h ∈ H
                fix(sin[r,s,h], 0.0; force=true); fix(sout[r,s,h], 0.0; force=true); fix(soc[r,s,h], 0.0; force=true)
            end
        end
    end

    # --- trade: antisymmetry, NTC, abs split, fix-zero off-routes ---
    for r ∈ 𝓡, rr ∈ 𝓡, h ∈ H
        if has_route(r,rr)
            @constraint(model, flow[r,rr,h] == -flow[rr,r,h])
            @constraint(model, flow[r,rr,h] <=  ntc[r,rr])
            @constraint(model, flow[r,rr,h] >= -ntc[r,rr])
            @constraint(model, flow[r,rr,h] == fpos[r,rr,h] - fneg[r,rr,h])
        else
            fix(flow[r,rr,h], 0.0; force=true); fix(fpos[r,rr,h], 0.0; force=true); fix(fneg[r,rr,h], 0.0; force=true)
        end
    end

    # --- energy balance (its dual = nodal price) ---
    @constraint(model, balance[r ∈ 𝓡, h ∈ H],
        sum(g[r,d,h] for d ∈ disp) + sum(vg[r,v,h] for v ∈ var) + infe[r,h]
        + sum(sout[r,s,h] - sin[r,s,h] for s ∈ sbins)
        + sum(flow[rr,r,h] for rr ∈ 𝓡)
        == demand[(r,h)] + curt[r,h])

    # --- operating-reserve shortage (ORDC-lite; Par_DispatchReserveReq +
    #     Par_DispatchORDC). Hourly requirement = max(share x demand, GW floor);
    #     provided by dispatchable headroom (cap x CF - g) + storage discharge
    #     headroom; the piecewise shortage slacks price scarcity into the energy
    #     dual via co-optimization (the missing $200-2000 mid-tail). Regions
    #     without config rows get no constraint (neutral default). ---
    resregs = [r for r ∈ 𝓡 if haskey(dcfg.reservereq, r) && haskey(dcfg.ordc, r) &&
                              !isempty(dcfg.ordc[r])]
    @variable(model, rshort[r ∈ resregs, k ∈ 1:length(dcfg.ordc[r]), h ∈ H] >= 0)
    for r ∈ resregs
        share, gwfloor = dcfg.reservereq[r]
        segs = dcfg.ordc[r]
        for h ∈ H
            req = max(share * demand[(r,h)], gwfloor * dur(h))
            req <= 0 && continue
            for (k,(w,_)) ∈ enumerate(segs)
                set_upper_bound(rshort[r,k,h], w * req)
            end
            @constraint(model,
                sum(cap[d,r]*cf(r,d,h)*dur(h) - g[r,d,h] for d ∈ disp
                    if cap[d,r] > 0 && af(r,d) > 0; init=0.0)
              + sum(spowb(r,s)*dur(h) - sout[r,s,h] + sin[r,s,h] for s ∈ sbins; init=0.0)
              + sum(rshort[r,k,h] for k ∈ 1:length(segs))
              >= req)
        end
    end
    isempty(resregs) || println("  dispatch: ORDC-lite reserve curves active in $(length(resregs)) regions")

    # --- objective ---
    # unbinned fleets pay basecost on g; binned fleets pay basecost x tranche
    # multiplier on gb (their g carries no direct cost — it equals sum(gb)).
    # The endogenous-emission term below stays on g for ALL fleets (it is the
    # model's own EmissionsPenalty machinery, separate from the regional
    # dispatch-config carbon price inside basecost).
    # Market-realism terms: offer adders on g and vg (negative = subsidy),
    # curtailment priced at the deepest subsidy, per-region VoLL, and the
    # ORDC shortage penalties (EUR/MWh x 1e-3 -> MEUR/GWh).
    @objective(model, Min,
        sum(g[r,d,h]*basecost(r,d,h) for r ∈ 𝓡 for d ∈ disp for h ∈ H if (r,d) ∉ binnedset)
      + sum(gb[(r,d),k,h]*basecost(r,d,h)*_dc_bins(dcfg,d)[k][2]
            for (r,d) ∈ binned for k ∈ 1:length(_dc_bins(dcfg,d)) for h ∈ H)
      + sum(g[r,d,h]*emisCO2(r,d)*co2price(r) for r ∈ 𝓡 for d ∈ disp for h ∈ H)
      + sum(g[r,d,h]*adder[(r,d)] for r ∈ 𝓡 for d ∈ disp for h ∈ H if adder[(r,d)] != 0.0)
      + sum(vg[r,v,h]*adder[(r,v)] for r ∈ 𝓡 for v ∈ var for h ∈ H if adder[(r,v)] != 0.0)
      + DISP_EPS*sum(sout[r,s,h] for r ∈ 𝓡 for s ∈ sbins for h ∈ H)
      + curt_cost*sum(curt[r,h] for r ∈ 𝓡 for h ∈ H)
      + DISP_EPS*sum(fpos[r,rr,h]+fneg[r,rr,h] for r ∈ 𝓡 for rr ∈ 𝓡 for h ∈ H)
      + sum(infeas_pen(r)*infe[r,h] for r ∈ 𝓡 for h ∈ H)
      + 1.0e-3*sum(dcfg.ordc[r][k][2]*rshort[r,k,h]
                   for r ∈ resregs for k ∈ 1:length(dcfg.ordc[r]) for h ∈ H))

    for (k,v) ∈ solver_attr
        try; set_optimizer_attribute(model, k, v); catch e; @warn "attr $k=$v" exception=e; end
    end
    optimize!(model)
    return model, Sets, Params, disp, var, storage_power, H, hidx, demand, balance,
           (g=g, vg=vg, sin=sin, sout=sout, soc=soc, curt=curt, flow=flow, infe=infe,
            sbins=sbins, sbmap=sbmap)
end

# ---------------------------------------------------------------------------
# Write one year's results to genesysmod_dispatch_results.duckdb
# ---------------------------------------------------------------------------

"""
One-time in-place migration of a pre-Unit-column dispatch database: adds the
`Unit` column to the dispatch tables and rescales legacy price rows from the
old raw dual unit (MEUR/GWh) to EUR/MWh (x1000). Legacy rows are identified by
`Unit IS NULL`, so the migration is idempotent and never touches new rows.
"""
function _migrate_dispatch_weatheryear!(con)
    # Cross-weather-year dispatch: hourly + summary tables carry a WeatherYear
    # column (the timeseries year the dispatch ran against). Old rows are
    # backfilled from the scenario label (fel2026_<sens>_<step>_<wy>[_vN]),
    # whose weather year the pre-column runs always used.
    for t in ("dispatch_generation", "dispatch_storage", "dispatch_trade",
              "dispatch_balance", "dispatch_combined", "dispatch_summary",
              "dispatch_gen_annual")
        _table_exists(con, t) || continue
        cols = DataFrame(DBInterface.execute(con,
            "SELECT column_name FROM information_schema.columns WHERE table_name = ?", [t])).column_name
        "WeatherYear" ∈ cols && continue
        DBInterface.execute(con, "ALTER TABLE $(_quote_ident(t)) ADD COLUMN WeatherYear VARCHAR")
        DBInterface.execute(con, "UPDATE $(_quote_ident(t)) SET WeatherYear = " *
            "regexp_extract(Scenario, '_(20[0-9][0-9])(_v[0-9]+)?\$', 1) WHERE WeatherYear IS NULL")
        println("  dispatch db: migrated $(t) (added WeatherYear, backfilled from scenario label)")
    end
end

function _migrate_dispatch_units!(con)
    for t in ("dispatch_generation", "dispatch_storage", "dispatch_trade",
              "dispatch_balance", "dispatch_combined")
        _table_exists(con, t) || continue
        cols = DataFrame(DBInterface.execute(con,
            "SELECT column_name FROM information_schema.columns WHERE table_name = ?", [t])).column_name
        "Unit" ∈ cols && continue
        DBInterface.execute(con, "ALTER TABLE $(_quote_ident(t)) ADD COLUMN Unit VARCHAR")
        if t == "dispatch_balance"
            DBInterface.execute(con, "UPDATE dispatch_balance SET Price = Price*1000 WHERE Unit IS NULL")
            DBInterface.execute(con, "UPDATE dispatch_balance SET Unit = 'GWh (Price: EUR/MWh)' WHERE Unit IS NULL")
        elseif t == "dispatch_combined"
            DBInterface.execute(con, "UPDATE dispatch_combined SET Value = Value*1000 WHERE Category = 'price' AND Unit IS NULL")
            DBInterface.execute(con, "UPDATE dispatch_combined SET Unit = CASE WHEN Category = 'price' THEN 'EUR/MWh' ELSE 'GWh' END WHERE Unit IS NULL")
        else
            DBInterface.execute(con, "UPDATE $(_quote_ident(t)) SET Unit = 'GWh' WHERE Unit IS NULL")
        end
        println("  dispatch db: migrated $(t) (added Unit; legacy prices -> EUR/MWh)")
    end
end

function write_dispatch_year_db(dispatch_db, scenario, year, weather_year, Switch, Sets, disp, var,
                                H, demand, balance, V)
    con = _db_connect(dispatch_db)
    sc = String(scenario); yr = Int(year); wy = String(weather_year)
    _migrate_dispatch_units!(con)
    _migrate_dispatch_weatheryear!(con)
    function put(table, df)
        isempty(df) && return
        out = _with_run_context(df, Switch, sc)
        insertcols!(out, 5, :Year => fill(yr, nrow(out)))
        insertcols!(out, 6, :WeatherYear => fill(wy, nrow(out)))
        tq = _quote_ident(table); reg = "df_" * table
        DuckDB.register_data_frame(con, out, reg)
        try
            DBInterface.execute(con, "BEGIN TRANSACTION")
            if _table_exists(con, table)
                DBInterface.execute(con, "DELETE FROM $tq WHERE Scenario = ? AND Year = ? AND WeatherYear = ?", [sc, yr, wy])
                DBInterface.execute(con, "INSERT INTO $tq BY NAME SELECT * FROM $(_quote_ident(reg))")
            else
                DBInterface.execute(con, "CREATE TABLE $tq AS SELECT * FROM $(_quote_ident(reg))")
            end
            DBInterface.execute(con, "COMMIT")
        catch; DBInterface.execute(con, "ROLLBACK"); rethrow()
        finally; DuckDB.unregister_data_frame(con, reg); end
    end
    # generation (dispatchable + variable)
    gen = DataFrame(Region=String[], Technology=String[], Hour=Int[], Value=Float64[])
    for r ∈ Sets.Region_full
        for d ∈ disp, h ∈ H
            v = value(V.g[r,d,h]); abs(v) > 1e-6 && push!(gen, (r, d, Int(h), round(v, digits=4)))
        end
        for vt ∈ var, h ∈ H
            v = value(V.vg[r,vt,h]); abs(v) > 1e-6 && push!(gen, (r, vt, Int(h), round(v, digits=4)))
        end
    end
    gen[!, :Unit] .= "GWh"
    put("dispatch_generation", gen)
    # storage operation
    sto = DataFrame(Region=String[], Storage=String[], Hour=Int[], Charge=Float64[], Discharge=Float64[], SoC=Float64[])
    # duration tranches ("s#k") aggregate back to their parent storage
    sids_of = Dict(s => [sid for sid ∈ V.sbins if V.sbmap[sid][1] == s] for s ∈ Sets.Storage)
    for r ∈ Sets.Region_full, s ∈ Sets.Storage, h ∈ H
        ci = sum(value(V.sin[r,sid,h])  for sid ∈ sids_of[s]; init=0.0)
        di = sum(value(V.sout[r,sid,h]) for sid ∈ sids_of[s]; init=0.0)
        sc_ = sum(value(V.soc[r,sid,h]) for sid ∈ sids_of[s]; init=0.0)
        (abs(ci)>1e-6 || abs(di)>1e-6 || abs(sc_)>1e-6) && push!(sto, (r, s, Int(h), round(ci,digits=4), round(di,digits=4), round(sc_,digits=4)))
    end
    sto[!, :Unit] .= "GWh"
    put("dispatch_storage", sto)
    # nodal balance: demand, curtailment, unserved, net import, price (dual)
    bal = DataFrame(Region=String[], Hour=Int[], Demand=Float64[], Curtailment=Float64[],
                    Unserved=Float64[], NetImport=Float64[], Price=Float64[])
    for r ∈ Sets.Region_full, h ∈ H
        netimp = sum(value(V.flow[rr,r,h]) for rr ∈ Sets.Region_full; init=0.0)
        # dual is MEUR/GWh (objective MEUR, balance GWh); x1000 -> EUR/MWh
        price = dual(balance[r,h]) * 1000.0
        # curtailment = generic dump + variable-RE spill (vg below its potential;
        # nonzero only when bid adders un-fix vg — legacy runs report curt alone)
        respill = sum(is_fixed(V.vg[r,v,h]) ? 0.0 :
                      max(0.0, upper_bound(V.vg[r,v,h]) - value(V.vg[r,v,h]))
                      for v ∈ var; init=0.0)
        push!(bal, (r, Int(h), round(demand[(r,h)],digits=4),
                    round(value(V.curt[r,h]) + respill,digits=4),
                    round(value(V.infe[r,h]),digits=4), round(netimp,digits=4), round(price,digits=4)))
    end
    bal[!, :Unit] .= "GWh (Price: EUR/MWh)"
    put("dispatch_balance", bal)
    # bilateral trade flows (signed, r -> rr), nonzero only
    trd = DataFrame(Region=String[], Region2=String[], Hour=Int[], Flow=Float64[])
    for r ∈ Sets.Region_full, rr ∈ Sets.Region_full, h ∈ H
        f = value(V.flow[r,rr,h]); abs(f) > 1e-6 && push!(trd, (r, rr, Int(h), round(f, digits=4)))
    end
    trd[!, :Unit] .= "GWh"
    put("dispatch_trade", trd)
    # combined long table (GAMS `output`/`stor_oper`/`dual_price` merged into one) for
    # easy charting: every quantity as (Category, Name, Value) per Region/Hour. Sign
    # conventions mirror the GAMS output: charging (s_in) and curtailment (cur) negative.
    comb = DataFrame(Region=String[], Hour=Int[], Category=String[], Name=String[], Value=Float64[], Unit=String[])
    for row ∈ eachrow(gen)                                   # generation (disp + var), nonzero
        push!(comb, (row.Region, row.Hour, "prod", row.Technology, row.Value, "GWh"))
    end
    for row ∈ eachrow(sto)                                   # storage operation
        push!(comb, (row.Region, row.Hour, "s_in",      row.Storage, round(-row.Charge, digits=4), "GWh"))
        push!(comb, (row.Region, row.Hour, "s_out",     row.Storage, row.Discharge, "GWh"))
        push!(comb, (row.Region, row.Hour, "s_soc",     row.Storage, row.SoC, "GWh"))
        push!(comb, (row.Region, row.Hour, "s_net_out", row.Storage, round(row.Discharge - row.Charge, digits=4), "GWh"))
    end
    for row ∈ eachrow(bal)                                   # demand + price every hour; rest nonzero
        push!(comb, (row.Region, row.Hour, "dem",   "Demand", row.Demand, "GWh"))
        push!(comb, (row.Region, row.Hour, "price", "Price",  row.Price, "EUR/MWh"))
        row.Curtailment != 0 && push!(comb, (row.Region, row.Hour, "cur",  "Curtailment",   round(-row.Curtailment, digits=4), "GWh"))
        row.Unserved    != 0 && push!(comb, (row.Region, row.Hour, "inf",  "Infeasibility", row.Unserved, "GWh"))
        row.NetImport   != 0 && push!(comb, (row.Region, row.Hour, "flow", "NetImport",     row.NetImport, "GWh"))
    end
    put("dispatch_combined", comb)
    println("  dispatch_combined: ", nrow(comb), " rows")
    return nrow(gen), nrow(sto), nrow(bal), nrow(trd)
end

# ---------------------------------------------------------------------------
# Per-run summary: scalar metrics + annual generation by tech -> print, DB, CSV
# ---------------------------------------------------------------------------
"""
Build a short per-year summary for `scenario` from the just-written dispatch
tables, print it, and persist it to `genesysmod_dispatch_results.duckdb`
(`dispatch_summary`, `dispatch_gen_annual`) and to CSV in `resultdir`.
"""
function write_dispatch_summary(dispatch_db, resultdir, scenario, weather_year, model_region, emissionPathway, emissionScenario)
    con = _db_connect(dispatch_db)
    sc = String(scenario); wy = String(weather_year)
    _migrate_dispatch_weatheryear!(con)
    q(s) = DataFrame(DBInterface.execute(con, s, [sc, wy]))
    summ = q("SELECT Year, round(sum(Demand),0) AS Demand_GWh, " *
             "round(sum(Curtailment),0) AS Curtailment_GWh, round(sum(Unserved),1) AS Unserved_GWh, " *
             "round(100*sum(Unserved)/nullif(sum(Demand),0),3) AS Unserved_pct, " *
             # Price column is already EUR/MWh (converted at write; legacy rows migrated)
             "round(avg(Price),1) AS AvgPrice_EURMWh, round(max(Price),0) AS MaxPrice_EURMWh " *
             "FROM dispatch_balance WHERE Scenario = ? AND WeatherYear = ? GROUP BY Year ORDER BY Year")
    if isempty(summ)
        @warn "dispatch summary: no rows for scenario $(sc)"; return summ
    end
    gentot = q("SELECT Year, round(sum(Value),0) AS Generation_GWh FROM dispatch_generation WHERE Scenario = ? AND WeatherYear = ? GROUP BY Year")
    summ = sort!(leftjoin(summ, gentot, on=:Year), :Year)
    genann = q("SELECT Year, Technology, round(sum(Value),0) AS Generation_GWh " *
               "FROM dispatch_generation WHERE Scenario = ? AND WeatherYear = ? GROUP BY Year, Technology ORDER BY Year, Generation_GWh DESC")
    # CSV (clean — no context columns)
    lbl_wy = something(match(r"_(20\d\d)(?:_v\d+)?$", sc), (; captures=[""])).captures[1]
    fsuf = (isempty(wy) || wy == lbl_wy) ? "" : "_wy$(wy)"
    CSV.write(joinpath(resultdir, "dispatch_summary_$(sc)$(fsuf).csv"), summ)
    CSV.write(joinpath(resultdir, "dispatch_gen_annual_$(sc)$(fsuf).csv"), genann)
    # DB (scenario-keyed, with run-context columns)
    ctx(df) = (out = copy(df); insertcols!(out, 1,
        :Scenario => fill(sc, nrow(out)), :WeatherYear => fill(wy, nrow(out)),
        :ModelRegion => fill(model_region, nrow(out)),
        :Pathway => fill(emissionPathway, nrow(out)),
        :PathwayScenario => fill("$(emissionPathway)_$(emissionScenario)", nrow(out))); out)
    _db_attempt(() -> _db_write_scenario!(con, "dispatch_summary", ctx(summ), sc; extra_key=("WeatherYear" => wy,)), "dispatch_summary")
    _db_attempt(() -> _db_write_scenario!(con, "dispatch_gen_annual", ctx(genann), sc; extra_key=("WeatherYear" => wy,)), "dispatch_gen_annual")
    # print
    println("\n=== DISPATCH SUMMARY ($(sc)) ===")
    show(summ, allrows=true, allcols=true); println()
    for y in summ.Year
        top = first(eachrow(filter(:Year => ==(y), genann)), 8)
        println("  $(y) top (GWh): ", join(["$(r.Technology) $(r.Generation_GWh)" for r in top], " · "))
    end
    return summ
end

# ---------------------------------------------------------------------------
# Entry point — loop years
# ---------------------------------------------------------------------------
"""
    genesysmod_dispatch_fullyear(; years, scenario, ...)

Run the full-year hourly multi-region dispatch for each year in `years`, reading
fixed capacities from the investment scenario `scenario` in
`genesysmod_db.duckdb`, and writing results to
`genesysmod_dispatch_results.duckdb` (keyed Scenario/Year/Region/Hour).
"""
function genesysmod_dispatch_fullyear(; years=[2025,2030,2040], scenario,
        weather_year="",
        model_region="north_america", data_base_region="California",
        data_file, hourly_data_file, allfuels_data_file="", switch_power_only_mode=1,
        inputdir, resultdir, solver, DNLPsolver,
        emissionPathway="MinimalExample", emissionScenario="globalLimit",
        threads=6, elmod_nthhour=1, cyclic_storage=true, co2_price=:endogenous,
        dispatch_data_file="",
        solver_attr=Dict("Method"=>2, "Crossover"=>0, "BarHomogeneous"=>1))

    results_db  = _results_db_path_from(resultdir)
    dispatch_db = _dispatch_db_path(resultdir)
    # Weather year of THIS dispatch (the hourly file's year) - the investment
    # solution in `scenario` may have been built on a different one
    # (cross-weather-year dispatch). Derived from hourly_data_file if not given;
    # keyed into every dispatch table as the WeatherYear column.
    wy = String(weather_year)
    if isempty(wy)
        m = match(r"_(20\d\d)$", String(hourly_data_file))
        wy = m === nothing ? "" : String(m.captures[1])
    end
    dcfg = read_dispatch_config(inputdir, dispatch_data_file)
    summary = Dict{Int,Any}()
    for year ∈ years
        println("\n=== dispatch_fullyear: year $(year), scenario $(scenario) ===")
        switch = _make_dispatch_switch(; year=year, model_region=model_region,
            data_base_region=data_base_region, data_file=data_file, hourly_data_file=hourly_data_file,
            allfuels_data_file=allfuels_data_file, switch_power_only_mode=switch_power_only_mode,
            inputdir=inputdir, resultdir=resultdir, emissionPathway=emissionPathway,
            emissionScenario=emissionScenario, threads=threads, DNLPsolver=DNLPsolver,
            elmod_nthhour=elmod_nthhour, extr_str=string(scenario))
        model, Sets, Params, disp, var, storage_power, H, hidx, demand, balance, V =
            dispatch_build_solve_year(switch, solver, solver_attr, results_db, scenario,
                                      year, cyclic_storage, co2_price, dcfg)
        st = termination_status(model)
        feasible = primal_status(model) == MOI.FEASIBLE_POINT
        println("  solve: $(st)  obj=$(feasible ? objective_value(model) : NaN)")
        st == MOI.OPTIMAL || !feasible ||
            @warn "year $(year): solver did not certify optimality ($(st)); writing the feasible solution."
        if feasible   # write whenever a feasible solution exists (incl. sub-optimal barrier)
            try
                ng, ns, nb, nt = write_dispatch_year_db(dispatch_db, scenario, year, wy,
                    switch, Sets, disp, var, H, demand, balance, V)
                summary[year] = (status=st, generation_rows=ng, storage_rows=ns, balance_rows=nb, trade_rows=nt)
                println("  wrote: $(ng) gen, $(ns) storage, $(nb) balance, $(nt) trade rows")
            catch e
                @warn "dispatch DB write failed for $(year)" exception=e
                summary[year] = (status=st, write_error=true)
            end
        else
            summary[year] = (status=st,)
        end
    end
    # short per-run summary -> console + dispatch DB + CSV
    try
        write_dispatch_summary(dispatch_db, resultdir, scenario, wy, model_region, emissionPathway, emissionScenario)
    catch e
        @warn "dispatch summary failed" exception=e
    end
    release_dbs()
    return summary
end
