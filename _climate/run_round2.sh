#!/bin/bash
# Round 2: no-fossil-expansion investment variants (base/extreme/severe), then hourly dispatch of the
# regular v6f fleet under the four climate input sets. Serial, restartable via done-files.
cd "C:/Users/testbed/Documents/GENeSYSMOD.jl_SE"
JULIA="/c/Users/testbed/.julia/juliaup/julia-1.12.6+0.x64.w64.mingw32/bin/julia.exe"
run() { k=$1
  [ -f "_climate/run_done_$k" ] && return 0
  echo "=== run $k $(date +%H:%M)"
  "$JULIA" --project=. "_climate/run_$k.jl" > "Results/_climate_run_$k.log" 2>&1
  st=$(grep -o "post-optimize: status=[A-Z_]*" "Results/_climate_run_$k.log" | tail -1)
  echo "    $k -> ${st:-NO STATUS (crash?)}"
  grep -q "Processed results written" "Results/_climate_run_$k.log" && [ "$st" = "post-optimize: status=OPTIMAL" ] && touch "_climate/run_done_$k"
}
disp() { k=$1
  [ -f "_climate/disp_done_$k" ] && return 0
  echo "=== dispatch $k $(date +%H:%M)"
  "$JULIA" --project=. "_climate/dispatch_$k.jl" > "Results/_climate_dispatch_$k.log" 2>&1
  echo "    dispatch $k -> $(grep -c "solve: OPTIMAL" "Results/_climate_dispatch_$k.log") optimal years"
  grep -q "NA CLIMATE DISPATCH" "Results/_climate_dispatch_$k.log" && touch "_climate/disp_done_$k"
}
for k in base_nofossil extreme_nofossil severe_nofossil; do run $k; done
for k in v6f_base v6f_central v6f_extreme v6f_severe; do disp $k; done
echo "ROUND 2 DONE"
