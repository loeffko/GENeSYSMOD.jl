#!/bin/bash
cd "C:/Users/testbed/Documents/GENeSYSMOD.jl_SE"
JULIA="/c/Users/testbed/.julia/juliaup/julia-1.12.6+0.x64.w64.mingw32/bin/julia.exe"
for k in base_nofossil extreme_nofossil severe_nofossil; do
  echo "=== probe $k $(date +%H:%M)"
  "$JULIA" --project=. "_climate/probe_$k.jl" > "Results/scen_probe/_climate_probe_$k.log" 2>&1
  echo "    $k -> $(grep -o "post-optimize: status=[A-Z_]*" "Results/scen_probe/_climate_probe_$k.log" | tail -1)"
  f=$(ls InputData/input_reduced_timeserie_north_america_*_1924.xlsx 2>/dev/null | head -1); [ -n "$f" ] && mv "$f" "Results/scen_probe/reduced_ts_climate_${k}_1924.xlsx"
done
echo "NOFOSSIL PROBES DONE"
