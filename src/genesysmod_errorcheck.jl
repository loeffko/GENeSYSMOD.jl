"""
Input-data error checks, mirroring genesysmod_errorcheck.gms.

Runs right after data load (before the model is built) so obvious data
problems abort with a named list of offenders instead of surfacing later as
an infeasible or misbehaving model.

Hard checks (model aborts, like the GAMS `abort`):
  1. Technology missing from TagTechnologyToSector
  2. TradeCosts missing for a traded fuel with a defined TradeRoute
     (TradeCosts is derived from TradeCostFactor × TradeRoute, so the
      Par_TradeCostFactor input is what is actually missing)
  3. ModalSplit sums > 1 per ModalGroup / ModalSubgroup
  4. OperationalLife missing for a Technology (dummy/infeasibility techs are
     exempt — their parameters are filled programmatically later)
  5. CapacityFactor zero across all timeslices although AvailabilityFactor
     and TotalAnnualMaxCapacity are set
  6. CapacityToActivityUnit missing although AvailabilityFactor is set
  7. TradeCapacity / CommissionedTradeCapacity set without a TradeRoute

Warnings (printed, run continues):
  8. AvailabilityFactor missing although ResidualCapacity is set
  9. Technology efficiency > 1 (input sum < output sum) outside the
     Resources / Transportation sectors

`Switch.switch_errorcheck`:
  0 = skip all checks
  1 = run and REPORT everything, but continue (default — some legacy/test
      datasets have known gaps that the model tolerates, e.g. zero-CF techs)
  2 = strict GAMS behaviour: abort the run when a hard check fails
"""
function genesysmod_errorcheck(Sets, Params, Switch)
    Switch.switch_errorcheck != 0 || return

    𝓡 = Sets.Region_full
    𝓣 = Sets.Technology
    𝓕 = Sets.Fuel
    𝓨 = Sets.Year
    𝓛 = Sets.Timeslice
    𝓜 = Sets.Mode_of_operation
    𝓜𝓽 = Sets.ModalType
    𝓢𝓮 = Sets.Sector

    nerrors = 0
    # print at most this many offenders per check; the count is always exact
    maxshow = 20
    function report!(kind, name, offenders, msg)
        isempty(offenders) && return
        shown = first(offenders, maxshow)
        if kind === :error
            @error "$(name): $(msg)" offenders=shown total=length(offenders)
            nerrors += 1
        else
            @warn "$(name): $(msg)" offenders=shown total=length(offenders)
        end
    end

    dummy_techs = Set(get(Params.Tags.TagTechnologyToSubsets, "DummyTechnology", String[]))

    # 1 — Technology missing from Sector list
    off = [t for t ∈ 𝓣 if t ∉ dummy_techs && all(Params.Tags.TagTechnologyToSector[t,se] == 0 for se ∈ 𝓢𝓮)]
    report!(:error, "TechMissingFromSectorList", off,
        "Technology missing from the Sector list. Check Par_TagTechnologyToSector.")

    # 2 — TradeCosts missing for a traded fuel with a TradeRoute
    # (TradeCosts = TradeCostFactor × TradeRoute, so a zero here means the
    #  Par_TradeCostFactor input is missing for that fuel)
    off = Tuple{String,String,String}[]
    for f ∈ 𝓕
        Params.Tags.TagCanFuelBeTraded[f] != 0 || continue
        for r ∈ 𝓡, rr ∈ 𝓡
            if any(Params.TradeRoute[r,rr,f,y] != 0 for y ∈ 𝓨) &&
               all(Params.TradeCosts[r,f,y,rr] == 0 for y ∈ 𝓨)
                push!(off, (r, f, rr))
            end
        end
    end
    report!(:error, "TradeCostsMissingFromTradeRoute", off,
        "TradeCosts missing for a traded fuel with a defined TradeRoute. Check Par_TradeCostFactor.")

    # 3 — ModalSplit definition (sum over group must be <= 1)
    if !isempty(𝓜𝓽)
        for (group, label) ∈ (("TransportModes", "ModalGroup"), ("ModalSubgroups", "SubGroup"))
            mts = [mt for mt ∈ 𝓜𝓽 if Params.Tags.TagModalTypeToModalGroups[mt,group] != 0]
            isempty(mts) && continue
            off = [(f, r, y) for f ∈ 𝓕 for r ∈ 𝓡 for y ∈ 𝓨
                   if round(sum(Params.ModalSplitByFuelAndModalType[r,f,y,mt] for mt ∈ mts), digits=4) > 1]
            report!(:error, "ModalSplitByModalTypeDefinition ($label)", off,
                "Sum of ModalTypes in a $(label) exceeds 1. Check Par_ModalSplitByFuel.")
        end
    end

    # 4 — OperationalLife missing
    off = [t for t ∈ 𝓣 if t ∉ dummy_techs && Params.OperationalLife[t] == 0]
    report!(:error, "OperationalLifeMissing", off,
        "OperationalLife missing for a Technology. Check Par_OperationalLife.")

    # 5 — CapacityFactor zero everywhere although AF + MaxCapacity set
    off = Tuple{String,String,Int}[]
    for r ∈ 𝓡, t ∈ 𝓣, y ∈ 𝓨
        if Params.AvailabilityFactor[r,t,y] != 0 && Params.TotalAnnualMaxCapacity[r,t,y] != 0 &&
           all(Params.CapacityFactor[r,t,l,y] == 0 for l ∈ 𝓛)
            push!(off, (r, t, y))
        end
    end
    report!(:error, "CapacityFactorDataMissing", off,
        "CapacityFactor is zero in every timeslice for an available technology. Check the hourly data file.")

    # 6 — CapacityToActivityUnit missing although AF set
    off = [(r, t) for r ∈ 𝓡 for t ∈ 𝓣
           if t ∉ dummy_techs && Params.CapacityToActivityUnit[t] == 0 &&
              any(Params.AvailabilityFactor[r,t,y] != 0 for y ∈ 𝓨)]
    report!(:error, "CapacityToActivityUnitDataMissing", off,
        "CapacityToActivityUnit missing for a Technology. Check Par_CapacityToActivityUnit.")

    # 7 — Trade capacities without a TradeRoute
    off = Tuple{String,String,String,Int,String}[]
    for r ∈ 𝓡, rr ∈ 𝓡, f ∈ 𝓕, y ∈ 𝓨
        if Params.TradeRoute[r,rr,f,y] == 0
            Params.TradeCapacity[r,rr,f,y] != 0 && push!(off, ("TradeCapacity", r, f, y, rr))
            Params.CommissionedTradeCapacity[r,rr,f,y] != 0 && push!(off, ("CommissionedTradeCapacity", r, f, y, rr))
        end
    end
    report!(:error, "TradeCapacityMismatch", off,
        "TradeCapacity/CommissionedTradeCapacity set without a TradeRoute. Check the trade input data.")

    # 8 — WARNING: AvailabilityFactor missing although ResidualCapacity set
    off = [(r, t, y) for r ∈ 𝓡 for t ∈ 𝓣 for y ∈ 𝓨
           if Params.ResidualCapacity[r,t,y] != 0 && Params.AvailabilityFactor[r,t,y] == 0]
    report!(:warn, "AvailabilityFactorMissing", off,
        "AvailabilityFactor missing for a Technology with ResidualCapacity. Check Par_AvailabilityFactor.")

    # 9 — WARNING: efficiency > 1 outside Resources/Transportation
    off = Tuple{String,String,Int,Int}[]
    for t ∈ 𝓣
        (Params.Tags.TagTechnologyToSector[t,"Resources"] != 0 ||
         Params.Tags.TagTechnologyToSector[t,"Transportation"] != 0) && continue
        for r ∈ 𝓡, m ∈ 𝓜, y ∈ 𝓨
            sout = sum(Params.OutputActivityRatio[r,t,f,m,y] for f ∈ 𝓕)
            sin  = sum(Params.InputActivityRatio[r,t,f,m,y] for f ∈ 𝓕)
            if sout != 0 && sin != 0 && sin / sout < 1
                push!(off, (r, t, m, y))
            end
        end
    end
    report!(:warn, "TechnologyEfficiencies", off,
        "Technology efficiency above 1 (input sum < output sum) outside Resources/Transportation.")

    if nerrors > 0
        if Switch.switch_errorcheck == 2
            error("genesysmod_errorcheck: $(nerrors) input-data check(s) failed — see the error log above. " *
                  "Fix the input data, or lower switch_errorcheck to continue anyway.")
        else
            @warn "genesysmod_errorcheck: $(nerrors) input-data check(s) failed (continuing; set switch_errorcheck=2 to abort on these)"
        end
    else
        println("Build:   errorcheck : no hard input-data errors")
    end
    return
end
