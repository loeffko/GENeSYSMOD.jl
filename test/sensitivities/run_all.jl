# META-RUNNER: the full NA sensitivity workflow (investment runs).
# Order: base case first, then the sensitivities — each across all weather years.
#
# Prereq: the sensitivity input workbooks exist in InputData (built by the data
# repo's  python NA_inputs/build_sensitivity_inputs.py).
#
# Naming: fel2026_<sensitivity>_<nthhour>_<weatheryear>[_<version>]
include(joinpath(@__DIR__, "common.jl"))

# ---- options ---------------------------------------------------------------
const DAYSTEP  = 2          # nthhour = DAYSTEP*24 + HOURSTEP  (2/1 -> 49)
const HOURSTEP = 1
const VERSION  = ""         # rerun tag ("v2", "v3", ...); "" for the first run
const WEATHER_YEARS = SENS_WEATHER_YEARS            # ["2012","2015","2017","2018"]
const SENSITIVITIES = ["base", "dc_low", "dc_high", "dc_high_no_sofc", "dc_high_limitless", "recession",
                       "bess_e2p_6h", "bess_e2p_8h", "bess_cost_low", "bess_cost_low_6h", "bess_cost_low_8h",
                       "economic", "grid_low", "grid_high"]
# The blessed fel2026_base_49_2015 run (v7: Canadian gas price + AF calibration,
# identical inputs to the sensitivity workbooks) already exists, so base skips
# 2015. Set true whenever the input data changes again.
const RERUN_BASE_2015 = false
# ----------------------------------------------------------------------------

for sens ∈ SENSITIVITIES
    wys = (sens == "base" && !RERUN_BASE_2015) ?
        filter(!=("2015"), WEATHER_YEARS) : WEATHER_YEARS
    run_sensitivity(sens; weather_years=wys,
                    daystep=DAYSTEP, hourstep=HOURSTEP, version=VERSION)
end

println("\n########## sensitivity suite complete: $(length(SENSITIVITIES)) sensitivities x $(length(WEATHER_YEARS)) weather years ##########")
