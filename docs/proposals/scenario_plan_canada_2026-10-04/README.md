# Canada scenario quantification plan (2026-10-04)

Plan for the nine Canada scenarios requested by Siemens Energy Canada (`canada_scenarios_request.txt`,
copy of `../canada.txt`). **Status: PLAN only - nothing is implemented or run.** Open decisions are in the
workbook (sheet "Open questions").

Deliverable: `../CA_scenario_plan_2026-10-04.xlsx` (sheets: README, Overview, Signal check, Assumptions,
Feasibility, Run plan, Sources, Model baseline, CER comparison, Open questions).

Rebuild: `python build_ca_plan_xlsx.py` (writes `../CA_scenario_plan_2026-10-04.xlsx`).

## Files

- `ca_plan_content.py` - model side: Canada node of the frozen base `fel2026_base_49_2015_v6f` (demand,
  capacity result and corridor, generation, interconnectors), CER "Canada's Energy Future 2026" paths,
  model facts and levers.
- `ca_plan_part1.py` ... `ca_plan_part5.py` - scenario rows, signal checks, assumptions and sources, one file
  per research note (1: scenarios 1 and 9; 2: scenarios 3 and 5; 3: scenarios 2 and 4; 4: scenario 6;
  5: scenarios 7 and 8).
- `ca_plan_research.py` - merges the parts, adds the SE-internal / model sources, the run plan and the open
  questions; checks that every cited source id exists.
- `ca_plan_sources.py` - `U(key)` returns the URL from the research notes, so that no link is retyped.
- `build_ca_plan_xlsx.py` - writes the workbook.

Research notes (web research of 2026-10-04, one file per research agent; every figure carries its source,
figures that could not be sourced are marked NOT FOUND, own conversions are marked):

- `A_grid_doubling_eu.md` - scenario 1 (unleash generation potential) and scenario 9 (EU associate member)
- `B_nuclear_north.md` - scenario 3 (nuclear growth) and scenario 5 (northern territories, remote power)
- `C_datacenters.md` - scenario 6 (data sovereignty, data centres)
- `D_wind_minerals.md` - scenario 7 (wind re-acceleration) and scenario 8 (critical minerals)
- `E_localcontent_indigenous.md` - scenario 2 (local content) and scenario 4 (Indigenous equity)

## Rules carried over from the North America set

- Runs are always based on the frozen v6 base (`fel2026_base_49_2015_v6f`); the base is not changed.
- Where the base is already higher than the scenario input, this is flagged and the scenario numbers are used.
- Judgement calls and far-fetched what-ifs are legitimate scenario content; the flag only says whether the
  model can represent the scenario. Every scenario has a stretch variant. As few data points as possible
  are invented (column "Invented?" in the Assumptions sheet).
- No separate "funnel released" twin runs: a scenario edits the Canadian capacity corridor inside its own
  definition where the storyline contradicts it.

## Main findings of the signal check

- **The frozen base is already above several of the signals.** Generation capacity reaches 297 GW in 2040
  (the "310 GW by 2050" of scenario 1 is the CER Current Measures path, 244 GW in 2040); data-centre demand
  (269 TWh in 2040) is above every sourced forecast and the named project pipeline (177 TWh); onshore wind
  (87 GW in 2040) is above the announced procurement (56 GW). In these scenarios the content is the mix or
  the pace, not the level, and some central variants are lower than the base.
- "150 to 310 GW by 2050" is the CER Energy Future 2026 Current Measures path; the federal strategy
  "Powering Canada Strong" (May 2026) has no capacity target.
- "22 GW of announced nuclear" matches the Siemens Energy Canadian Nuclear Review list; public schedules
  support 18.5 GW large reactors and 1.8 GW SMR by 2040. "28 new CANDU reactors by 2050" was not found.
- The TC Energy Crossfield concept (3 x 465 MW) is not in any public source or in the Alberta connection
  list; the unit size matches one H-class combined-cycle block.
- Hydro-Quebec: more than 10 GW of new wind by 2035 on top of 4 GW (total about 14 GW), part of it after 2035.
- The Williams Treaties First Nations CAD 700 million Darlington partnership is confirmed (loan converting
  to equity).
- "EU associate member" is a proposal of 16 September 2026, without a quantified energy programme.
- Local content is mostly a scored preference (10 % price preference federally and in Ontario, 65 % Quebec
  content target in the Hydro-Quebec wind tender), not a mandate; it enters the model as a cost premium,
  a build-rate cap and a delay.
- Northern and remote systems are 0.3 % of the Canada node (1.7 TWh); a side calculation is proposed
  instead of a model run.
