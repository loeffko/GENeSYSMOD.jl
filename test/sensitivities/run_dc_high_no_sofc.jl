# NA sensitivity 'dc_high_no_sofc' — dc_high demand and build limits, but the
# P_SOFC technology is deselected (own filter file): does the (BTM-reduced)
# data-center boom clear without the SOFC option? All four weather years.
# Options: run_sensitivity("dc_high_no_sofc"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("dc_high_no_sofc")
