"""
Expand a year-keyed `Dict` of anchor values so it covers every year in `years`.
Values between anchors are linearly interpolated; years outside the anchor
range are clamped to the nearest anchor. This lets year-keyed settings work
with any time resolution (e.g. individual years), not only 5-year steps.
"""
function _fill_year_dict(anchors::Dict, years)
    ks = sort(collect(keys(anchors)))
    out = Dict{Int,Float64}()
    for y in years
        yi = Int(y)
        if haskey(anchors, yi)
            out[yi] = anchors[yi]
        elseif yi <= ks[1]
            out[yi] = anchors[ks[1]]
        elseif yi >= ks[end]
            out[yi] = anchors[ks[end]]
        else
            lo = maximum(k for k in ks if k <= yi)
            hi = minimum(k for k in ks if k >= yi)
            frac = (yi - lo) / (hi - lo)
            out[yi] = anchors[lo] + frac * (anchors[hi] - anchors[lo])
        end
    end
    return out
end

"""
Internal function used in the run process to set run settings such as dicount rates.
"""
function genesysmod_settings(Sets, Params, socialdiscountrate)

    DepreciationMethod=JuMP.Containers.DenseAxisArray(zeros(length(Sets.Region_full)), Sets.Region_full)
    GeneralDiscountRate=JuMP.Containers.DenseAxisArray(zeros(length(Sets.Region_full)), Sets.Region_full)
    TechnologyDiscountRate=JuMP.Containers.DenseAxisArray(zeros(length(Sets.Region_full), length(Sets.Technology)), Sets.Region_full, Sets.Technology)
    SocialDiscountRate=JuMP.Containers.DenseAxisArray(zeros(length(Sets.Region_full)), Sets.Region_full)
    for r ∈ Sets.Region_full
        DepreciationMethod[r] = 1
        GeneralDiscountRate[r] = Float64(0.05)
        for t ∈ setdiff(Sets.Technology,Params.Tags.TagTechnologyToSubsets["Households"])
            TechnologyDiscountRate[r,t] = Float64(0.05)
        end
        for t ∈ intersect(Sets.Technology, Params.Tags.TagTechnologyToSubsets["Households"])
            TechnologyDiscountRate[r,t] = Float64(0.05)
        end
        SocialDiscountRate[r] = socialdiscountrate
    end

    InvestmentLimit = Float64(1.9)  #Freedom for investment choices to spread across periods. A value of 1 would mean equal share for each period.
    NewRESCapacity = Float64(0.1)
    #ProductionGrowthLimit=JuMP.Containers.DenseAxisArray(zeros(length(Sets.Year), length(Sets.Fuel)), Sets.Year, Sets.Fuel)
    #= for y ∈ Sets.Year for f ∈ Sets.Fuel
        if f ∈ vcat(["Power"],Params.Tags.TagFuelToSubsets["HeatFuels"],Params.Tags.TagFuelToSubsets["TransportFuels"])
            Params.ProductionGrowthLimit[y,f] = Float64(0.05)
        end
        if f == "Air"
            Params.ProductionGrowthLimit[y,f] = Float64(0.025)
        end
    end end =#
    StorageLimitOffset = Float64(0.015)

    Trajectory2020UpperLimit = 3
    Trajectory2020LowerLimit = Float64(0.7)

    BaseYearSlack = JuMP.Containers.DenseAxisArray(zeros(length(Sets.Fuel)), Sets.Fuel)
    BaseYearSlack[Sets.Fuel] .= 0.035
    BaseYearSlack["Power"] = 0.035

    # Anchor values defined at 5-year steps; interpolated to every modelled year
    # via _fill_year_dict so the model also runs at finer time resolution.
    # NOTE: these are per-modelled-step multipliers (relative to the previous
    # modelled year). They were calibrated for 5-year steps - revisit the
    # anchor values if running at a different resolution.
    PhaseOut = _fill_year_dict(Dict(2020=>3.0, 2025=>3.0, 2030=>3.0, 2035=>2.5, 2040=>2.5, 2045=>2.0, 2050=>2.0, 2055=>1.5, 2060=>1.25), Sets.Year)# upper limit for fossil generation based on the previous year - to remove choose large value

    PhaseIn = _fill_year_dict(Dict(2020=>1.0, 2025=>0.8, 2030=>0.8, 2035=>0.8, 2040=>0.8, 2045=>0.8, 2050=>0.6, 2055=>0.5, 2060=>0.5), Sets.Year) # lower bound for renewable integration based on the previous year - to remove choose 0

    #StorageLevelYearStartUpperLimit = Switch.set_storagelevelstart_up
    #StorageLevelYearStartLowerLimit = Switch.set_storagelevelstart_down


    Settings=GENeSYSMOD.Settings(DepreciationMethod,GeneralDiscountRate,TechnologyDiscountRate,SocialDiscountRate,InvestmentLimit,NewRESCapacity,
    StorageLimitOffset,Trajectory2020UpperLimit,Trajectory2020LowerLimit, BaseYearSlack, PhaseIn, PhaseOut)
    return Settings
end
