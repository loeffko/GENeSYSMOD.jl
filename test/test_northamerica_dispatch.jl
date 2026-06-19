using Pkg
Pkg.develop(path="C:/Users/testbed/Documents/GENeSYSMOD.jl_SE")
using GENeSYSMOD
using Gurobi
using Ipopt

# Full-year (8760 h) multi-region hourly DISPATCH for the North America power-only
# model. Reads the fixed investment capacities of an existing scenario from
# genesysmod_results_db.duckdb and computes the hourly dispatch for each year,
# writing generation / storage / nodal-price / trade to
# genesysmod_dispatch_results.duckdb (keyed Scenario/Year/Region/Hour).
#
# Prereq: the investment run for `scenario` must already be in the results DB
# (run test_northamerica.jl with switch_results_db=1 + the matching extr_str_results).

solver = Gurobi.Optimizer
const RES = joinpath(pkgdir(GENeSYSMOD), "Results")
const SCENARIO = "73_ramping_invlimit"

summary = genesysmod_dispatch_fullyear(;
    years          = [2025, 2030, 2040],
    scenario       = SCENARIO,
    model_region   = "north_america",
    data_base_region = "California",
    data_file      = "RegularParameters_NorthAmerica",
    hourly_data_file = "Timeseries_NorthAmerica",
    allfuels_data_file = "RegularParameters_NorthAmerica_allFuels",
    switch_power_only_mode = 1,
    inputdir       = joinpath(pkgdir(GENeSYSMOD), "InputData"),
    resultdir      = RES,
    solver         = solver,
    DNLPsolver     = Ipopt.Optimizer,
    threads        = 6,
    elmod_nthhour  = 1,          # full 8760-hour resolution
    cyclic_storage = true,       # SoC[end] = SoC[1]
    co2_price      = :endogenous,
    solver_attr    = Dict("Method"=>2, "Crossover"=>0, "BarHomogeneous"=>1,
                          "NumericFocus"=>2, "BarConvTol"=>1e-5),
)

println("\n=== DISPATCH SUMMARY ($(SCENARIO)) ===")
for y in sort(collect(keys(summary)))
    println("  $y => ", summary[y])
end
