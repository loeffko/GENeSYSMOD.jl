# Climate severe: extreme with the historic drought baked in - 1924-hour feasibility/mechanism probe, no DB writes
# Data: v6-freeze base (identical to RegularParameters_NorthAmerica_v6f) + NorthAmerica_climate_severe overlays,
# weather year 2015, v6-era allFuels. Comparison partners: fel2026_base_49_2015_v6f (regular base) and
# fel2026_climate_base_49_2015_v1 (climate base) for the CF sensitivities.
using GENeSYSMOD
using Gurobi
using Ipopt
label = "fel2026_climate_severe_1924probe_v1"
println("
########## NA climate severe @ nthhour 1924 (probe): $(label) ##########")
genesysmod(; set_new_res_capacity = 0.1,
    solver=Gurobi.Optimizer, DNLPsolver=Ipopt.Optimizer,
    year=2025, elmod_daystep=80, elmod_hourstep=4, threads=6,
    inputdir=joinpath(pkgdir(GENeSYSMOD), "InputData"),
    resultdir=joinpath(pkgdir(GENeSYSMOD), "Results", "scen_probe"),
    data_file="RegularParameters_NorthAmerica_climate_severe",
    hourly_data_file="Timeseries_NorthAmerica_climate_severe_2015",
    switch_power_only_mode=1,
    allfuels_data_file="RegularParameters_NorthAmerica_allFuels_v6",
    switch_infeasibility_tech=WithInfeasibilityTechs(),
    switch_investLimit=1, switch_ccs=1, switch_ramping=1,
    E2P_ratio_deviation_factor=1.1,
    switch_weighted_emissions=1, switch_intertemporal=0,
    switch_base_year_bounds=0, switch_peaking_capacity=1,
    set_peaking_slack=0, set_peaking_minrun_share=0, set_peaking_res_cf=0.5,
    set_peaking_startyear=2025, switch_peaking_with_storages=1,
    switch_peaking_with_trade=1, switch_peaking_minrun=0,
    switch_employment_calculation=0, switch_endogenous_employment=0,
    employment_data_file="", elmod_starthour=8, elmod_dunkelflaute=0,
    switch_raw_results=NoRawResult(), switch_processed_results=1,
    write_reduced_timeserie=1, model_region="north_america",
    data_base_region="California", extr_str_results=label,
    switch_test_data_load=0, switch_results_db=0, switch_dump_input_data=0, switch_errorcheck=1)
println("NA CLIMATE SEVERE DONE")
