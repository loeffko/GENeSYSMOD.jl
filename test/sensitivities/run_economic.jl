# NA sensitivity 'economic' — all four weather years.
# Options: run_sensitivity("economic"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("economic")
