# NA sensitivity 'grid_high' — all four weather years.
# Options: run_sensitivity("grid_high"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("grid_high")
