#!/bin/bash
# 1924-hour probes of the four climate cases (feasibility + mechanism check), serial, no DB writes.
# After each probe the reduced-timeseries export is moved aside so the four do not overwrite each other.
cd "C:/Users/testbed/Documents/GENeSYSMOD.jl_SE"
export PATH="/c/Users/testbed/AppData/Local/Microsoft/WindowsApps:$PATH"
for k in base central extreme severe; do
  echo "=== probe $k $(date +%H:%M)"
  julia --project=. "_climate/probe_$k.jl" > "Results/scen_probe/_climate_probe_$k.log" 2>&1
  st=$(grep -o "post-optimize: status=[A-Z_]*" "Results/scen_probe/_climate_probe_$k.log" | tail -1)
  echo "    $k -> ${st:-NO STATUS (crash?)}"
  f=$(ls InputData/input_reduced_timeserie_north_america_*_1924.xlsx 2>/dev/null | head -1)
  [ -n "$f" ] && mv "$f" "Results/scen_probe/reduced_ts_climate_${k}_1924.xlsx"
done
echo "CLIMATE PROBES DONE"
