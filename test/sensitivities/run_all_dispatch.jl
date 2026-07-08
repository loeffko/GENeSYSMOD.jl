# META-RUNNER: full-year dispatch for every sensitivity (weather year 2015 only
# for now — add years / cross-weather-year combinations here when needed).
#
# Prereq: the matching investment runs exist in the results DB (run_all.jl) and
# DispatchData_NorthAmerica.xlsx is in InputData (merit-order cost config).
include(joinpath(@__DIR__, "common.jl"))

# ---- options ---------------------------------------------------------------
const DAYSTEP  = 2
const HOURSTEP = 1
const VERSION  = ""
const DISPATCH_WEATHER_YEARS = ["2015"]
const DISPATCH_YEARS = [2025, 2030, 2040]
const SENSITIVITIES = ["base", "dc_low", "dc_high", "dc_high_no_sofc", "dc_high_limitless", "recession",
                       "economic", "grid_low", "grid_high"]
# ----------------------------------------------------------------------------

for sens ∈ SENSITIVITIES, wy ∈ DISPATCH_WEATHER_YEARS
    label = sens_label(sens, DAYSTEP, HOURSTEP, wy, VERSION)
    println("\n########## dispatch: $(label) ##########")
    genesysmod_dispatch_fullyear(;
        years            = DISPATCH_YEARS,
        scenario         = label,
        dispatch_data_file = "DispatchData_NorthAmerica",
        model_region     = "north_america",
        data_base_region = "California",
        data_file        = sens_data_file(sens),
        hourly_data_file = "Timeseries_NorthAmerica_$(wy)",
        allfuels_data_file = "RegularParameters_NorthAmerica_allFuels",
        switch_power_only_mode = 1,
        inputdir         = joinpath(pkgdir(GENeSYSMOD), "InputData"),
        resultdir        = SENS_RESULTS_DIR,
        solver           = Gurobi.Optimizer,
        DNLPsolver       = Ipopt.Optimizer,
        threads          = 6,
        elmod_nthhour    = 1,
        cyclic_storage   = true,
        co2_price        = :endogenous,
        solver_attr      = Dict("Method"=>2, "Crossover"=>0, "BarHomogeneous"=>1,
                                "NumericFocus"=>2, "BarConvTol"=>1e-5))
end

println("\n########## dispatch suite complete ##########")
