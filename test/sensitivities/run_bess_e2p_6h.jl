# NA sensitivity 'bess_e2p_6h' — Li-Ion BESS variation (E2P duration and/or cost path via
# the scenario subfolders; base demand and funnels). All four weather years.
# Options: run_sensitivity("bess_e2p_6h"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("bess_e2p_6h")
