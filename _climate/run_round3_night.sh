#!/bin/bash
# Round 3 (2026-10-25): no-fossil-AND-no-nuclear expansion variants, overriding the round-2 labels on the user's
# instruction. Waits until 23:00 local time before touching the solver (other model runs during the day).
cd "C:/Users/testbed/Documents/GENeSYSMOD.jl_SE"
JULIA="/c/Users/testbed/.julia/juliaup/julia-1.12.6+0.x64.w64.mingw32/bin/julia.exe"
target=$(date -d "23:00" +%s); now=$(date +%s)
[ $now -gt $target ] && target=$((target + 86400))
echo "waiting until $(date -d @$target '+%F %H:%M') ($(( (target-now)/60 )) min)"
while [ $(date +%s) -lt $target ]; do sleep 300; done
rm -f _climate/run_done_base_nofossil _climate/run_done_extreme_nofossil _climate/run_done_severe_nofossil
run() { k=$1
  echo "=== run $k $(date +%H:%M)"
  "$JULIA" --project=. "_climate/run_$k.jl" > "Results/_climate_run_$k.log" 2>&1
  st=$(grep -o "post-optimize: status=[A-Z_]*" "Results/_climate_run_$k.log" | tail -1)
  echo "    $k -> ${st:-NO STATUS (crash?)}"
  grep -q "Processed results written" "Results/_climate_run_$k.log" && [ "$st" = "post-optimize: status=OPTIMAL" ] && touch "_climate/run_done_$k"
}
for k in base_nofossil extreme_nofossil severe_nofossil; do run $k; done
echo "ROUND 3 DONE"
