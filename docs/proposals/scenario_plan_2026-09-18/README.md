# NA scenario quantification plan (2026-09-18)

**Current version: v3 (2026-09-22, implementation record)** - `../NA_scenario_plan_2026-09-18_v3.xlsx`:
user decisions applied (v6 basis; scenario numbers used even where the base is higher, flagged; existing
sensitivities reused for numbers only), fusion from `NA_inputs/Fusion_Market_Model_v09.xlsx` (bull), and an
"Implemented (wave 1)" column per scenario. Data: data repo `NA_inputs/build_14_scenarios.py` (overlays
`Par_X/NorthAmerica_sNN_*`), workbooks built on the v6-freeze worktree, drivers in `_s14/` (jl_SE root),
run labels `fel2026_sNN_<name>_49_2015_v6`, reference `fel2026_base_49_2015_v6c`.
Rebuild v3: `SCEN_RESEARCH=scen_plan_research_v3 python build_scen_plan_xlsx.py ../NA_scenario_plan_2026-09-18_v3.xlsx`

**v2 (superseded)** - `../NA_scenario_plan_2026-09-18_v2.xlsx`. v2 separates representability
(can the model do it - drives the flag) from evidence strength (informational). Judgement calls and
far-fetched what-ifs are legitimate scenario content and are not down-rated; every scenario has a
stretch variant (1C, 2C, 3C, 4C, 5C, 6D, 7D, 8C, 9C, 10C, 11C, 12C, 13C, 14C); fusion capex/FOM/first
year are USER INPUT rows in Assumptions. Rebuild v2:
`SCEN_RESEARCH=scen_plan_research_v2 python build_scen_plan_xlsx.py ../NA_scenario_plan_2026-09-18_v2.xlsx`

v1 (superseded): `../NA_scenario_plan_2026-09-18.xlsx`.

Deliverable: `../NA_scenario_plan_2026-09-18.xlsx` (sheets: README, Overview, Assumptions,
Feasibility, Sources, Model baseline, Existing sensitivities, Open questions).

Rebuild: `python build_scen_plan_xlsx.py ../NA_scenario_plan_2026-09-18.xlsx`
(content in `scen_plan_content.py` = model side, `scen_plan_research.py` = scenario rows,
assumptions, sources, open questions).

Research notes (web-sourced, 2025-2026 vintage, one file per research agent):
- `A_ev_hydrogen.md` - scenarios 1, 2
- `B_compute_dc.md` - scenarios 3, 12, 8
- `C_politics_feoc.md` - scenarios 5, 11
- `D_hormuz_decarb.md` - scenarios 6, 14
- `E_tech_space.md` - scenarios 7, 4
- `F_water_climate_industry.md` - scenario 9 complete; scenarios 10 and 13 were filled from
  the main session after the agent hit the account session limit (sources are in the workbook).

Status: PLAN only, nothing implemented. Open decisions are listed in the workbook.
