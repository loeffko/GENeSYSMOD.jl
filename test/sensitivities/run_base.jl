# NA sensitivity 'base' — all four weather years.
# Options: run_sensitivity("base"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("base")
