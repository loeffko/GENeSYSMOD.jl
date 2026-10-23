#!/bin/bash
# Climate-adaptation chain: Climate Base investment (gate), the three thermal-CF investment cases,
# then the full-year dispatch of the Climate Base fleet under all four input sets.
# Serial (single DuckDB writer), restartable via done-files.
cd "C:/Users/testbed/Documents/GENeSYSMOD.jl_SE"
export PATH="/c/Users/testbed/AppData/Local/Microsoft/WindowsApps:$PATH"
JULIA="/c/Users/testbed/AppData/Local/Microsoft/WindowsApps/julia.exe"
run() { k=$1
  [ -f "_climate/run_done_$k" ] && return 0
  echo "=== run $k $(date +%H:%M)"
  "$JULIA" --project=. "_climate/run_$k.jl" > "Results/_climate_run_$k.log" 2>&1
  st=$(grep -o "post-optimize: status=[A-Z_]*" "Results/_climate_run_$k.log" | tail -1)
  echo "    $k -> ${st:-NO STATUS (crash?)}"
  if grep -q "Processed results written" "Results/_climate_run_$k.log" && [ "$st" = "post-optimize: status=OPTIMAL" ]; then
    touch "_climate/run_done_$k"; return 0
  fi
  return 1
}
disp() { k=$1
  [ -f "_climate/disp_done_$k" ] && return 0
  echo "=== dispatch $k $(date +%H:%M)"
  "$JULIA" --project=. "_climate/dispatch_$k.jl" > "Results/_climate_dispatch_$k.log" 2>&1
  n=$(grep -c "solve: OPTIMAL" "Results/_climate_dispatch_$k.log")
  echo "    dispatch $k -> $n optimal years"
  grep -q "NA CLIMATE DISPATCH" "Results/_climate_dispatch_$k.log" && touch "_climate/disp_done_$k"
}
run base || { echo "Climate Base failed - chain stopped (gate)"; exit 1; }
for k in central extreme severe; do run $k; done
for k in base central extreme severe; do disp $k; done
echo "CLIMATE RUNS DONE"
