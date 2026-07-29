"""
Power-only mode (Switch.switch_power_only_mode == 1) precompute.

For each thermal tech kept in the filtered power-only model, derive an effective per-
activity VariableCost and a per-PJ-power OutputEmissionRatio from the *allFuels* Excel,
where the fossil supply chain (Z_Import_*, fuel IAR, EmissionContentPerFuel) is still
present. The power-only model itself stays small and fast; the precompute injects what
the missing supply chain would have contributed.

Formula (per the user's overall-efficiency rule):
    OAR_total = sum over all output fuels of OAR[r,t,f,m,y]   (PJ output per unit activity)
    OAR_power = OAR[r,t,"Power",m,y]                          (PJ power per unit activity)
    upstream_VC[r,f,y] = VariableCost[r, "Z_Import_<f>", 1, y]  (M EUR / PJ fuel)
    fuel_cost_pa = sum_f IAR[r,t,f,m,y] * upstream_VC[r,f,y]    (M EUR per unit activity)
    emission_pa  = sum_f IAR[r,t,f,m,y] * EmissionContentPerFuel[f,e]  (Gt per activity)

    Params.VariableCost[r,t,m,y]        += fuel_cost_pa
    Params.OutputEmissionRatio[r,t,e,m,y] = emission_pa / OAR_power

For pure thermal (OAR_Power = OAR_total) these reproduce the full model's per-PJ-act
fuel cost + emission exactly. For CHP cogen modes there is no heat credit in pwr-only
(no heat sink), so cogen modes pay the full fuel cost — they no longer look
artificially cheap and the model picks pure-P_ techs over CHP cogen when only power
demand is active. Emission is charged in FULL against power output (heat is an unused
bonus; atmosphere does not credit cogen). Tech's existing non-fuel O&M VariableCost
is preserved (we ADD).

If CHP needs to be made attractive again, add a virtual negative cost term against
the heat OAR (simulating heat sale revenue) rather than reintroducing the heat
discount on fuel cost.

Only mode 1 is used (suitable for the single-mode thermal + CHP techs in scope). Modes
where OAR_Power == 0 (heat-only modes) are skipped — they're irrelevant in power-only.
"""

using XLSX, DataFrames

function power_only_precompute!(Params, Sets, Switch)
    Switch.switch_power_only_mode == 1 || return
    isempty(Switch.allfuels_data_file) && error(
        "switch_power_only_mode == 1 requires `allfuels_data_file` (no extension) " *
        "pointing at the allFuels Excel in inputdir")

    path = joinpath(Switch.inputdir, Switch.allfuels_data_file * ".xlsx")
    isfile(path) || error("allFuels Excel not found: $path")
    print("Power-only precompute: reading $(basename(path))\n")
    xl = XLSX.readxlsx(path)

    # ---- pull the parameter sheets we need ----
    iar  = DataFrame(XLSX.gettable(xl["Par_InputActivityRatio"]))
    oar  = DataFrame(XLSX.gettable(xl["Par_OutputActivityRatio"]))
    vc   = DataFrame(XLSX.gettable(xl["Par_VariableCost"]))
    ecpf = DataFrame(XLSX.gettable(xl["Par_EmissionContentPerFuel"]))

    # ---- group IAR / OAR by (Region, Technology, Mode, Year) -> [(Fuel, Value), ...] ----
    function group_by_rtmy(df)
        g = Dict{Tuple{String,String,Int,Int}, Vector{Tuple{String,Float64}}}()
        for row in eachrow(df)
            k = (String(row.Region), String(row.Technology),
                 Int(row.Mode_of_operation), Int(row.Year))
            push!(get!(g, k, Tuple{String,Float64}[]),
                  (String(row.Fuel), Float64(row.Value)))
        end
        g
    end
    iar_g = group_by_rtmy(iar)
    oar_g = group_by_rtmy(oar)

    # ---- VariableCost lookup: (Region, Technology, Mode, Year) -> Value ----
    vc_d = Dict{Tuple{String,String,Int,Int}, Float64}()
    for row in eachrow(vc)
        vc_d[(String(row.Region), String(row.Technology),
              Int(row.Mode_of_operation), Int(row.Year))] = Float64(row.Value)
    end

    # ---- EmissionContentPerFuel lookup: (Fuel, Emission) -> Value ----
    ecpf_d = Dict{Tuple{String,String}, Float64}()
    for row in eachrow(ecpf)
        ecpf_d[(String(row.Fuel), String(row.Emission))] = Float64(row.Value)
    end

    # ---- upstream fuel cost + emission per input fuel ----
    # Default: each fuel f is supplied by Z_Import_<f> (cost) and uses
    # EmissionContentPerFuel[<f>, e] (emission). Many "renewable carrier" fuels
    # (Gas_Bio, Gas_Synth, LBG, LSG, H2_Blend) are produced internally in the full
    # model by chains that are stripped in power-only. Without explicit handling
    # those modes would be free of cost AND emissions, so the model would short-
    # circuit emissions by switching mode.
    #
    # Handling per user direction:
    #  - Gas_Synth: SKIP (mode dropped; complex H2+DAC chain not modelled here)
    #  - Gas_Bio:   cost from R_Biogas (mode 1), emission = 0 (treated biogenic)
    #  - LBG/LSG:   alias to LNG (fossil proxy)
    #  - H2_Blend:  alias to H2
    SKIP_FUELS = Set(["Gas_Synth"])
    UPSTREAM_TECH = Dict(  # fuel => (tech_name_for_vc_lookup, emission_factor)
        "Gas_Bio" => ("R_Biogas", 0.0),
        # No Z_Import_Nuclear exists — uranium cost comes from R_Nuclear.
        # Without this entry the lookup missed and nuclear fuel cost was 0.
        "Nuclear" => ("R_Nuclear", 0.0),
    )
    # Fuel name → Z_Import_<suffix> name (so the lookup `Z_Import_` * alias(f) hits
    # an actual import tech). Without these the gas/blended-H2 modes would have
    # zero added fuel cost — making them artificially cheap and dominating dispatch.
    FUEL_ALIAS = Dict(
        "Gas_Natural" => "Gas",     # Z_Import_Gas (not Z_Import_Gas_Natural)
        "LBG"         => "LNG",
        "LSG"         => "LNG",
        "H2_Blend"    => "H2",
    )
    alias(f) = get(FUEL_ALIAS, f, f)
    allfuels_techs = Set(String.(unique(skipmissing(vc.Technology))))
    function upstream_vc(r, f, y)
        if haskey(UPSTREAM_TECH, f)
            z, _ = UPSTREAM_TECH[f]
            z in allfuels_techs || return 0.0
            return get(vc_d, (String(r), z, 1, Int(y)), 0.0)
        end
        z = "Z_Import_" * alias(f)
        z in allfuels_techs || return 0.0
        get(vc_d, (String(r), z, 1, Int(y)), 0.0)
    end
    function ec_lookup(f, e)
        if haskey(UPSTREAM_TECH, f)
            _, ec = UPSTREAM_TECH[f]
            return ec
        end
        get(ecpf_d, (alias(f), String(e)), get(ecpf_d, (f, String(e)), 0.0))
    end

    # ---- main loop: iterate IAR groups, apply formulas to power-only Params ----
    techs_pwr = Set(String.(Sets.Technology))
    regions   = Set(String.(Sets.Region_full))
    years     = Set(Int.(Sets.Year))
    n_techs_touched = Set{String}()
    n_rows_vc = n_rows_ear = 0

    for ((r, t, m, y), fuel_in_vals_raw) in iar_g
        (t in techs_pwr && r in regions && y in years) || continue
        # Block dispatch of modes that rely on a SKIP fuel (e.g. Gas_Synth chain not
        # modelled in pwr-only — without a Z_Import_Gas_Synth this mode would have
        # near-zero cost and emissions and dominate, so we zero its Power OAR so the
        # model literally cannot produce Power from it).
        if any(f in SKIP_FUELS for (f, _) in fuel_in_vals_raw)
            try
                Params.OutputActivityRatio[r, t, "Power", m, y] = 0.0
            catch
            end
            continue
        end
        fuel_in_vals = fuel_in_vals_raw
        oar_list = get(oar_g, (r, t, m, y), Tuple{String,Float64}[])
        oar_total = sum(v for (_, v) in oar_list; init=0.0)
        oar_power = 0.0
        for (f, v) in oar_list
            if f == "Power"
                oar_power = v
                break
            end
        end
        (oar_total > 0 && oar_power > 0) || continue

        fuel_cost_pa = sum(v * upstream_vc(r, f, y) for (f, v) in fuel_in_vals; init=0.0)
        # Charge ALL input-fuel cost against the activity (no heat credit). In
        # power-only mode there is no heat sink so the cogen "heat" output is
        # waste — CHP cogen modes should pay the full fuel cost per PJ_act, same
        # as the equivalent P_ tech. If you want CHP back in the mix later, add a
        # negative virtual heat-sale term against the heat OAR rather than
        # discounting fuel cost here.
        Params.VariableCost[r, t, m, y] += fuel_cost_pa
        n_rows_vc += 1

        for e in Sets.Emission
            emission_pa = sum(v * ec_lookup(f, e) for (f, v) in fuel_in_vals; init=0.0)
            # Emission per PJ_power: charge ALL input-fuel emission against power
            # output (heat is an unused bonus in power-only and the atmosphere does
            # not care about the cogen credit). For pure-thermal techs this equals
            # the input-emission rate. For CHP it now matches the equivalent P_ tech
            # rather than being scaled down by the heat share.
            Params.OutputEmissionRatio[r, t, e, m, y] = emission_pa / oar_power
            n_rows_ear += 1
        end
        push!(n_techs_touched, t)
    end

    print("Power-only precompute: $(length(n_techs_touched)) techs touched, " *
          "$(n_rows_vc) VariableCost adds, $(n_rows_ear) OutputEmissionRatio sets\n")

    return nothing
end
