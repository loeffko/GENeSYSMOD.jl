# Full-year hourly dispatch of the Climate Base fleet (investment run fel2026_climate_base_49_2015_v1)
# under the base input set: NorthAmerica_climate_base demand profiles and thermal-stress capacity factors (none in the base case).
# Results keyed fel2026_climate_base_dispatch_v1 in genesysmod_dispatch_results.duckdb.
using GENeSYSMOD
using Gurobi
using Ipopt
const FLEET = "fel2026_climate_base_49_2015_v1"
const LABEL = "fel2026_climate_base_dispatch_v1"
println("
########## NA climate dispatch base: fleet $(FLEET) -> $(LABEL) ##########")
summary = genesysmod_dispatch_fullyear(;
    years = [2025, 2030, 2035, 2040],
    scenario = FLEET, result_label = LABEL,
    dispatch_data_file = "DispatchData_NorthAmerica",
    model_region = "north_america", data_base_region = "California",
    data_file = "RegularParameters_NorthAmerica_climate_base",
    hourly_data_file = "Timeseries_NorthAmerica_climate_base_2015",
    allfuels_data_file = "RegularParameters_NorthAmerica_allFuels_v6",
    switch_power_only_mode = 1,
    inputdir = joinpath(pkgdir(GENeSYSMOD), "InputData"),
    resultdir = joinpath(pkgdir(GENeSYSMOD), "Results"),
    solver = Gurobi.Optimizer, DNLPsolver = Ipopt.Optimizer, threads = 6,
    elmod_nthhour = 1, cyclic_storage = true, co2_price = :endogenous,
    solver_attr = Dict("Method"=>2, "Crossover"=>0, "BarHomogeneous"=>1, "NumericFocus"=>2, "BarConvTol"=>1e-5))
println("
=== DISPATCH SUMMARY ($(LABEL)) ===")
for y in sort(collect(keys(summary)))
    println("  $y => ", summary[y])
end
println("NA CLIMATE DISPATCH BASE DONE")
