# NA sensitivity 'dc_high_limitless' — dc_high demand with the build limits
# mostly gone (data: gas cap 100 GW/yr, EGS 4 GW/yr, funnel max x2 for
# PV/onshore/BESS, P_SOFC enabled 3->9 GW/yr; model: looser SC1/SC2 pacing
# via SENS_MODEL_KWARGS). All four weather years.
# Options: run_sensitivity("dc_high_limitless"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("dc_high_limitless")
