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
# The blessed fel2026_base_49_2015 run already exists (renamed v5), so base
# skips 2015 by default. CAUTION: if the input data changed since that run
# (e.g. the Canadian gas VariableCost regionalisation), set this to true so
# the base is recomputed consistently with the sensitivities.
const RERUN_BASE_2015 = true
# ----------------------------------------------------------------------------

for sens ∈ SENSITIVITIES
    wys = (sens == "base" && !RERUN_BASE_2015) ?
        filter(!=("2015"), WEATHER_YEARS) : WEATHER_YEARS
    run_sensitivity(sens; weather_years=wys,
                    daystep=DAYSTEP, hourstep=HOURSTEP, version=VERSION)
end

println("\n########## sensitivity suite complete: $(length(SENSITIVITIES)) sensitivities x $(length(WEATHER_YEARS)) weather years ##########")
