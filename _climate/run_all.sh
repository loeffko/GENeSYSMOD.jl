#!/bin/bash
# Climate-adaptation chain: Climate Base first (gate), then the three thermal-CF sensitivities.
# Serial (single DuckDB writer), restartable via done-files. Launch only on the user's command.
cd "C:/Users/testbed/Documents/GENeSYSMOD.jl_SE"
export PATH="/c/Users/testbed/AppData/Local/Microsoft/WindowsApps:$PATH"
run() { k=$1
  [ -f "_climate/run_done_$k" ] && return 0
  echo "=== run $k $(date +%H:%M)"
  julia --project=. "_climate/run_$k.jl" > "Results/_climate_run_$k.log" 2>&1
  st=$(grep -o "post-optimize: status=[A-Z_]*" "Results/_climate_run_$k.log" | tail -1)
  echo "    $k -> ${st:-NO STATUS (crash?)}"
  if grep -q "Processed results written" "Results/_climate_run_$k.log" && [ "$st" = "post-optimize: status=OPTIMAL" ]; then
    touch "_climate/run_done_$k"; return 0
  fi
  return 1
}
run base || { echo "Climate Base failed - chain stopped (gate)"; exit 1; }
for k in central extreme severe; do run $k; done
echo "CLIMATE RUNS DONE"
