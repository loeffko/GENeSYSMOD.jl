# NA sensitivity 'dc_low' — all four weather years.
# Options: run_sensitivity("dc_low"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("dc_low")
