# Shared runner for the NA sensitivity suite.
#
# Naming: fel2026_<sensitivity>_<nthhour>_<weatheryear>[_<version>]
# Inputs: RegularParameters_NorthAmerica[_<sensitivity>].xlsx (built by the data
#         repo's NA_inputs/build_sensitivity_inputs.py) +
#         Timeseries_NorthAmerica_<weatheryear>.xlsx; the allFuels workbook is
#         demand-independent and shared by all sensitivities.
using Pkg
Pkg.develop(path="C:/Users/testbed/Documents/GENeSYSMOD.jl_SE")
using GENeSYSMOD
using Gurobi
using Ipopt

const SENS_RESULTS_DIR = joinpath(pkgdir(GENeSYSMOD), "Results")
const SENS_WEATHER_YEARS = ["2012", "2015", "2017", "2018"]

"Scenario label for a sensitivity run."
sens_label(sensitivity, daystep, hourstep, weather_year, version) =
    "fel2026_$(sensitivity)_$(daystep * 24 + hourstep)_$(weather_year)" *
    (isempty(version) ? "" : "_$(version)")

"Data file for a sensitivity ('base' uses the plain workbook)."
sens_data_file(sensitivity) = sensitivity == "base" ?
    "RegularParameters_NorthAmerica" : "RegularParameters_NorthAmerica_$(sensitivity)"

"""
One NA investment run. Options: daystep/hourstep set the time resolution
(nthhour = daystep*24 + hourstep; default 49), version tags reruns (v2, ...).
"""
function run_na_investment(; sensitivity="base", weather_year="2015",
                           daystep=2, hourstep=1, version="")
    label = sens_label(sensitivity, daystep, hourstep, weather_year, version)
    println("\n########## investment: $(label) ##########")
    genesysmod(; solver=Gurobi.Optimizer, DNLPsolver=Ipopt.Optimizer,
        year=2025, elmod_daystep=daystep, elmod_hourstep=hourstep, threads=6,
        inputdir=joinpath(pkgdir(GENeSYSMOD), "InputData"),
        resultdir=SENS_RESULTS_DIR,
        data_file=sens_data_file(sensitivity),
        hourly_data_file="Timeseries_NorthAmerica_$(weather_year)",
        switch_power_only_mode=1,
        allfuels_data_file="RegularParameters_NorthAmerica_allFuels",
        switch_infeasibility_tech=WithInfeasibilityTechs(),
        switch_investLimit=1, switch_ccs=1, switch_ramping=1,
        switch_weighted_emissions=1, switch_intertemporal=0,
        switch_base_year_bounds=0, switch_peaking_capacity=1,
        set_peaking_slack=0, set_peaking_minrun_share=0, set_peaking_res_cf=0.5,
        set_peaking_startyear=2025, switch_peaking_with_storages=1,
        switch_peaking_with_trade=1, switch_peaking_minrun=0,
        switch_employment_calculation=0, switch_endogenous_employment=0,
        employment_data_file="", elmod_starthour=8, elmod_dunkelflaute=0,
        switch_raw_results=NoRawResult(), switch_processed_results=1,
        write_reduced_timeserie=0, model_region="north_america",
        data_base_region="California", extr_str_results=label,
        switch_test_data_load=0, switch_results_db=1, switch_dump_input_data=0)
end

"All weather years for one sensitivity."
function run_sensitivity(sensitivity; weather_years=SENS_WEATHER_YEARS, kwargs...)
    for wy ∈ weather_years
        run_na_investment(; sensitivity=sensitivity, weather_year=wy, kwargs...)
    end
end
