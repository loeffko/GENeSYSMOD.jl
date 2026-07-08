# NA sensitivity 'btm_lag' — behind-the-meter data-center capacity + demand
# grid-connect with a 4-year lag (pinned residual fleet incl. P_SOFC; demand
# joins Power_DataCenter). All four weather years.
# Options: run_sensitivity("btm_lag"; daystep=2, hourstep=1, version="", weather_years=[...])
include(joinpath(@__DIR__, "common.jl"))
run_sensitivity("btm_lag")
