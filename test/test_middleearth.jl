using Pkg
Pkg.develop(path="C:/Users/testbed/Documents/GENeSYS_MOD.jl")
using GENeSYSMOD
using HiGHS
using Ipopt

solver = HiGHS.Optimizer

const TEST_RESULTS_DIR = joinpath(pkgdir(GENeSYSMOD),"Results")

macro track(name, expr)
    quote
        GC.gc()
        pre_rss = Sys.maxrss()
        stats = @timed $(esc(expr))
        post_rss = Sys.maxrss()
        @info $name time_s=round(stats.time, digits=2) alloc_MiB=round(stats.bytes/1024^2, digits=1) peak_rss_MiB=round(post_rss/1024^2, digits=1) rss_delta_MiB=round((post_rss-pre_rss)/1024^2, digits=1)
        stats.value
    end
end

model, data = @track "MiddleEarth run" genesysmod(;elmod_daystep = 10, elmod_hourstep = 3, solver=solver, DNLPsolver = Ipopt.Optimizer, threads=0,
inputdir = joinpath(pkgdir(GENeSYSMOD),"InputData"),
resultdir = TEST_RESULTS_DIR,
data_file="RegularParameters_MiddleEarth",
hourly_data_file = "Timeseries_MiddleEarth",
switch_infeasibility_tech = NoInfeasibilityTechs(),
switch_investLimit=1,
switch_ccs=1,
switch_ramping=0,
switch_weighted_emissions=1,
switch_intertemporal=0,
switch_base_year_bounds = 0,
switch_peaking_capacity = 0,
set_peaking_slack = 0,
set_peaking_minrun_share = 0,
set_peaking_res_cf = 0,
set_peaking_startyear = 2025,
switch_peaking_with_storages = 0,
switch_peaking_with_trade = 0,
switch_peaking_minrun = 0,
switch_employment_calculation = 0,
switch_endogenous_employment = 0,
employment_data_file = "",
elmod_starthour = 8,
elmod_dunkelflaute= 0,
switch_raw_results = NoRawResult(),
switch_processed_results = 1,
write_reduced_timeserie = 1,
model_region="middleearth",
data_base_region="Gondor",
);