using Pkg
Pkg.develop(path="C:/Users/testbed/Documents/GENeSYSMOD.jl_SE")
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

model, data = @track "NorthAmerica run" genesysmod(;solver=solver, DNLPsolver = Ipopt.Optimizer,
elmod_daystep = 3, 
elmod_hourstep = 2, 
threads=6,
inputdir = joinpath(pkgdir(GENeSYSMOD),"InputData"),
resultdir = TEST_RESULTS_DIR,
data_file="RegularParameters_NorthAmerica",
hourly_data_file = "Timeseries_NorthAmerica",
switch_infeasibility_tech = NoInfeasibilityTechs(),
switch_investLimit=0,
switch_ccs=1,
switch_ramping=0,
switch_weighted_emissions=1,
switch_intertemporal=0,
switch_base_year_bounds = 0,
switch_peaking_capacity = 1,
set_peaking_slack = 0,
set_peaking_minrun_share = 0,
set_peaking_res_cf = 0.5,
set_peaking_startyear = 2025,
switch_peaking_with_storages = 1,
switch_peaking_with_trade = 1,
switch_peaking_minrun = 0,
switch_employment_calculation = 0,
switch_endogenous_employment = 0,
employment_data_file = "",
elmod_starthour = 8,
elmod_dunkelflaute= 0,
switch_raw_results = NoRawResult(),
switch_processed_results = 1,
write_reduced_timeserie = 0,
model_region="north_america",
data_base_region="California",
);