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
const SENSITIVITIES = ["base", "dc_low", "dc_high", "recession",
                       "economic", "grid_low", "grid_high"]
# ----------------------------------------------------------------------------

for sens ∈ SENSITIVITIES
    run_sensitivity(sens; weather_years=WEATHER_YEARS,
                    daystep=DAYSTEP, hourstep=HOURSTEP, version=VERSION)
end

println("\n########## sensitivity suite complete: $(length(SENSITIVITIES)) sensitivities x $(length(WEATHER_YEARS)) weather years ##########")
