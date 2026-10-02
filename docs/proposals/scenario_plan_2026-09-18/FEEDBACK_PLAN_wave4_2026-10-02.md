# Colleague feedback on the scenario set - plan for wave 4 (2026-10-02)

## Sources

| File | Status | Content |
|---|---|---|
| `scenario_results/Input Scenarios (v3) 2.docx` | read in full (465 paragraphs, no tracked changes or comments) | Executive summary, likelihood/impact table for #1-#14, a page per scenario (assessment, customer signals, "what would change our mind"), seven proposed additions A-G, 10-year load cross-check table, sources, glossary. Market-intelligence view from the NA hub (Q2-2026 utility disclosures, sell-side research). |
| `scenario_results/Canada Scenarios_MEP27.docx` | **not readable**: the file is an IRM/DRM-protected package (`EncryptedPackage` + `DRMEncryptedDataSpace` streams), not a plain .docx. Word automation hangs on the rights check. | Needs an unprotected export: open in Word with the licensed account, remove the sensitivity label / restriction (File > Info > Protect Document) and save as .docx, or paste the text into a .md. The Canada items below are placeholders until then. |

## What the feedback asks, in one paragraph

The hub does not dispute the FEL26 load view; it reframes it: load is contracted and collateral-backed, deliverability
(turbine slots, interconnection) and affordability (who pays) pace the decade. Consequences for the set: elevate
reindustrialization (#13) and nuclear life extension (E) toward the base, treat Alberta (#8) as a base input, demote EVs
(#1) and hydrogen (#2) as load drivers, turn space (#4) into a Gulf-Coast named-account load, treat Hormuz (#6) as a
live condition (cross-scenario sensitivity, capex-freeze channel not yet visible), split the tech scenario (#7) into
LDES (near term, erodes peakers) and fusion/SMR (post-2032), stress only the speculative tranche in the overbuild case
(#12), recast climate (#10) as resilience capex, and add affordability/cost allocation as #15 plus a supply-side
ceiling overlay (B). Everything else (FEOC #11, water #9, A-G details) is messaging or narrative.

## Reading: narrative vs model

Half of the document is for the MEP27 text and does not touch the model (vendor share race, hyperscaler capex
reference 600 -> 732-877 bn USD, named customer signals, "what would change our mind" triggers). The model-relevant
part is: (1) which scenarios sit in the base, (2) the size and timing of six scenarios, (3) three new cases, (4) one
cross-scenario sensitivity, (5) how results are presented (contracted floor / supply ceiling band). The supply-side
ceiling they ask for as an overlay already exists in the model: the turbine-supply caps (6/9/10/35/35 GW/yr 2026-30)
and the PV/wind pipeline maxima bind in every scenario through 2030; wave 3 documents it.

## Item by item

| # | Feedback | Model implication | Proposed action | Effort / flag |
|---|---|---|---|---|
| 1 EV | Demote. Full snap-back adds only 16-21 TWh/yr by 2030 (BEV share 23 % vs 10 % baseline); hybrids add no load. | s01 (AEO2026 policy path) is ~4x their 2030 sizing. | Re-size s01 to their numbers: +20 TWh in 2030 on the FEL BEV path, share-based growth after (about +90-120 TWh by 2040), label "upside lens, immaterial". Keep one run. | small; number from the doc (Cox/Urban Science) |
| 2 H2 | Keep out of base; electrolytic H2 below the FEL flat case; activity is CCS-backed (belongs to #14). | s02 adds 413 TWh of electrolysis that the hub does not believe in. | Drop s02 from the run set (keep the wave-3 result as the "if 45V/offtake reignite" lens in the write-up). Blue ammonia/CCS has no power-model footprint. | saves a run; decision |
| 3 compute | Keep (High/Strong). Show a contracted-load floor and a supply-side ceiling around FEL26, not a point forecast. Deliverability binds. | Already the case: caps bind 2026-30 in every run. | Present base / s12' / s03 as the band (floor = credible tranche, ceiling = caps); report cap-binding years and the turbine budget use per scenario. Narrative: update the capex reference. | reporting only |
| 4 space | Low-Medium as a load driver; Gulf-Coast named-account play (Starbase Louisiana >= 100 bn USD, own methane production and power, construction 2027, first launch 2029; chip plant TX; Colossus DCs are DCs). | s04 spreads 155 TWh over ERCOT/CA/SERC/WECC - wrong geography and too big. | Fold into s13 as regional point loads: SERC (Louisiana) ~2-3 GW industrial load from 2029, ERCOT ~1-2 GW (Starbase TX + chip plant); drop CA/WECC. No standalone run. | small; decision |
| 5 brakes | High/Strong; now state executive action incl. BTM (Texas permit halt, 474 GW audit, NY moratorium). "Still delay, not destruction"; contracted tranche posts collateral. | s05 = permanent regional haircut + no forced gas + RES max = pipeline + gas window cap. | Keep s05; change the DC leg from haircut to **delay**: ERCOT (and NY) DC path shifted 2 years, national cut only on the speculative tranche (same split as s12'). Gas/RES legs unchanged. | medium; decision |
| 6 Hormuz | Live condition since March 2026; EIA sees restrictions into 2027; capex plans have risen, not frozen (freeze = risk to watch); LNG pull. Apply as baseline sensitivity across scenarios and as a lens. | s06's capex/WACC uplift and recession demand are not observed; the fuel-price channel is. | s06 v5 = fuel-price channel only (Henry-Hub uplift 2026-30 as now, optionally extended to 2032 for the LNG pull), capex/recession legs dropped. Plus a **cross-scenario sensitivity**: the fuel uplift applied to the base and selected scenarios. | medium; decision on scope (5 vs 15 runs) |
| 7 tech | Split: LDES 2027-31 erodes peakers (Form Energy 65 GWh pipeline); fusion/SMR post-2032 erodes baseload; near-term displacement is BTM fuel cells and recip engines. | s07 bundles fusion, iron-air, Li-ion optimistic, SMR. | s07a LDES (iron-air + Li-ion optimistic, from 2027), s07b fusion + SMR (as now, from 2032/34). BTM engines are in the data (P_Gas_Engines cap); fuel cells are not - v7 addition. | small; +1 run |
| 8 Canada | Alberta = base input: Greenlight 932 MW CCGT FID (SE turbines), in service 2H30, expandable to 1,864 MW; Capital Power 250 MW ESA from 2H28; Keephills 230 MW -> 1 GW; BC restricts DCs; BCE 1.2 GW Saskatchewan. | Canada is one node; base DC path (FEL, 269 TWh 2040) already above the pipeline; CER gas path (CCGT min 5 GW 2030 -> 15 GW 2040) contains Greenlight. | No base change needed; s08 stays the pipeline-consistent case. Add an Alberta note (Greenlight inside the CER minimum). Alberta node split = v7. **Await the Canada document** for anything beyond this. | none now |
| 9 water | Low-Medium; mainly a siting constraint; Permian produced-water desalination is real but small. | s09 is immaterial (+36 TWh). | Drop the standalone run; keep water as a siting note in #3/#10 and the Permian load inside s13 (O&G electrification). | saves a run; decision |
| 10 climate | Medium/Moderate; relocation lags beyond the MEP27 horizon; recast as resilience/adequacy capex (~50 bn USD/yr by 2030); El Nino 2026-27. | s10 moves 10-20 % of load; the hub sees little relocation before 2036. | s10 v4: relocation 0 to 2035, 5 % by 2040 (was 10/20 %); keep cooling uplift, coastal derate ramp and the +50 % coastal IC cost (the resilience capex proxy). | small |
| 11 FEOC | High/Strong; share shift and pricing first, replacement upside; transformers the bottleneck (900 -> 1,500 units/yr, 80 % imported). Tariffs (D) same channel. | s11 = transient cost premium + Li-ion build cap. | s11 v4 "FEOC + tariffs": add +10-15 % on transmission expansion cost 2027-32 (transformers, Section 232) to the existing premium. Replacement of the installed base is not representable (no vintage retirement in the model) - narrative. | small |
| 12 overbuild | Stress only the speculative tranche: of 182 GW planned 2026-30 only ~101 GW credible (55 %); ERCOT TSP 218 vs ERCOT 145 GW; digestion with negative capex growth 2031-32; contracted tranche protected by take-or-pay. | s12 cuts to the LBNL low path (-62 % of the DC increment by 2040, -1,294 TWh) - too deep for the hub's reading. | s12 v4: DC path = 2026 level + 55 % of the FEL increment through 2030, flat 2031-32 (digestion), growth resumes at the FEL rate after; ERCOT at 66 %. Roughly -45 % of the increment (2040 ~1,250 TWh instead of 2,086 base / 792 now). | medium; numbers from the doc (Currence/Jefferies, Greenwich) |
| 13 reindustrial | High/Strong; elevate toward base; up to ~30 GW new load (TransAlta), 1/3-1/2 of non-AI growth; Permian O&G electrification (+32 % peak SPS); fabs AZ/ID/NY/TX. | s13 adds 163 TWh flat by 2040. | s13 v4: size to 30 GW by 2035 (~235 TWh at 90 % LF, ~250 by 2040) with the named regions (ERCOT, WECC/AZ-ID, NY, SPP Permian) + the Starbase point loads from #4. Present as the "elevated base" candidate; moving it into the base is a FEL26 baseline decision, not ours. | medium |
| 14 decarb | Medium-High; CCUS-on-gas (45Q 85 USD/t; Exxon 1.5 GW FID by end-2026, NextEra/Exxon 1.2 GW, BKV) and nuclear restart/uprate/life extension (E) are base-case material. | s14 carries the announced-nuclear overlay (+19 GW by 2035) and the CCS cap; the base has neither. | Base v6g candidates: (a) announced nuclear restarts/uprates/license extensions into the base minima (SMR portion reviewed: Duke says no new nuclear without protection); (b) named CCS projects as a base minimum (~3 GW by 2032) with 45Q. s14 then = CO2 price + ITC + 45Q + CCS cap + state caps. | base change -> full rerun; decision |
| A #15 affordability | Add as formal #15 (Headwind): large-load tariffs with deposits/ramp schedules, Ratepayer Protection Act, FERC 206, utilities' cost-offset plans; accelerates BYOG/midstream/IPP ownership. | Not in the set. Judgement-call design. | s15 = three legs: (i) grid-connected DC ramp delayed 1 year (tariff/ramp schedules), (ii) socialised grid build limited: IC growth = v6 `grid_low` path, (iii) BYOG: 40 % of the DC increment served by dedicated gas (forced gas additions in the DC regions, sized at 0.8 load factor). Representable with existing parameters. | medium; decision + design review |
| B supply ceiling | Overlay on the 10-year snapshot: can the industry deliver; slot reservations 2026-27 set share. | = our caps. | Report the caps as the ceiling (binding years, turbine budget used per scenario). Optional two overlay runs on the base: tight supply (gas caps x0.5 2027-32) and loose (x1.5). | reporting + optional 2 runs |
| C BTM permanent | 25 % of DC under construction / 40 % of pipeline is BTM; new buyer universe; Texas halt covers islanded projects. | Nodal model cannot separate BTM from grid supply; the BYOG leg of s15 is the closest. | Narrative; BYOG share inside s15. | none |
| D tariffs | Transformers 15 % Section 232; cost and lead time, not demand destruction. | cost channel | merged into s11 v4 | - |
| E nuclear wave | Move to base. | see #14 | base v6g (a) | decision |
| F transmission supercycle | MISO Tranche 2.1 22 bn, PJM 11.8 bn, SPP 9-10 bn approved; ERCOT 474 GW of requests. | v6 has a `grid_high` IC path (funnel + wires). | s16 "transmission supercycle" = the v6 `grid_high` interconnector path as a scenario overlay on the base (1 run); mapping the approved programmes to corridors is v7 data work. | small; decision |
| G flexible large loads | Does flexibility cut capacity or just accelerate interconnection? Model as a sensitivity on reserve-margin/peaking, not on load. | Peaking demand comes from the load profile (no data parameter). | Cheap proxy: s17 = peaking slack lowered (10 % of DC peak curtailable -> set_peaking_slack on the DC share) as a sensitivity run; a proper curtailable-load technology is a v7 code item. | small; decision |

## Decisions taken (user, 2026-10-02)

1. **Base stays v6f** - the July freeze is the reference; nothing but bug fixes until a new baseline is committed.
   The nuclear-wave and named-CCS asks are recorded as v7 baseline items; both stay inside s14 for now.
2. **Set**: drop s02, s04 (folded into s13) and s09 as runs; add s15 affordability, s16 transmission supercycle, s17
   flexible large loads.
3. **Hormuz**: no base variant. s06 is redefined as the fuel-price channel alone, and the same fuel uplift is applied
   as a variant of s03, s05, s12 and s14 (`_hormuz`).
4. **No twins.** Where the gas guardrail contradicts the storyline the funnel is removed inside the scenario definition
   (gas minimum = residual from 2031, build-rate caps kept): s07a, s07b, s12, s14 (s05 keeps its own release from 2027).
   The Hormuz variants of s05/s12/s14 inherit it.

## Wave 4 run list (19 runs, ~8 h, all on base v6f)

| run | definition (changes vs wave 3 in bold) | funnel |
|---|---|---|
| s01 EV | **re-sized to the hub's upside: +20 TWh in 2030 (BEV share 23 % vs 10 %), share growth after (~+110 TWh 2040)** | kept |
| s03 compute | unchanged (contracted floor / ceiling band in the write-up) | kept |
| s05 brakes | **DC leg = delay, not destruction: DC increment shifted 2 years (ERCOT, NY 3 years), permanent cut only on the speculative tranche (same split as s12)**; gas and RES legs as before | released 2027 (as before) |
| s06 Hormuz | **fuel-price channel only** (Henry-Hub uplift 2026-30 via the s06 allFuels workbook); capex/WACC uplift and recession demand dropped | kept |
| s07a LDES | **iron-air + optimistic Li-ion from 2027; no fusion, SMR at base cost** | **removed** |
| s07b fusion/SMR | **fusion ramp from 2034 + SMR 3,330 EUR/kW; storage at base** | **removed** |
| s08 Canada | unchanged (pipeline-consistent); Alberta BYOP sits inside the CER gas path; **pending the Canada document** | kept |
| s10 climate | **relocation 0 to 2035, 5 % by 2040** (was 10/20 %); cooling, coastal derate ramp and +50 % coastal IC cost kept | kept |
| s11 FEOC + tariffs | **+15 % on transmission expansion cost** (transformers, Section 232) on top of the FEOC premium and Li-ion cap | kept |
| s12 overbuild | **speculative tranche only: DC = 2026 level + 55 % of the FEL increment to 2030 (ERCOT 66 %), flat 2031-32, FEL growth rate after** | **removed** |
| s13 reindustrial | **30 GW by 2035 (~235 TWh at 90 % LF), named regions, + Starbase LA (SERC) and TX point loads, + Permian O&G electrification (SPP/ERCOT)** | kept |
| s14 decarb | CO2 price, ITC, 45Q, CCS cap, state caps, announced nuclear (unchanged) | **removed** |
| s15 affordability | **new**: grid-connected DC ramp delayed 1 year; interconnector growth = v6 `grid_low` path (socialised build limited); 40 % of the DC increment served by dedicated gas (BYOG, forced gas additions in the DC regions at 0.8 LF) | kept |
| s16 transmission supercycle | **new**: v6 `grid_high` interconnector path (approved MISO/PJM/SPP programmes as the narrative anchor) | kept |
| s17 flexible loads | **new** (sensitivity): 10 % of data-center peak curtailable, implemented through the peaking-constraint margin in the run settings (code-level parameter; verify the slack semantics first) | kept |
| s03_hormuz, s05_hormuz, s12_hormuz, s14_hormuz | parent scenario + the s06 fuel uplift (allFuels_v6_s06 workbook; no new RegularParameters needed) | as parent |

Dropped from the run set: s02 (hub: electrolytic H2 below the FEL flat case), s04 (point loads inside s13), s09
(immaterial; water as a siting note). Their wave-3 results stay citable. Optional: supply-ceiling overlay (gas caps
x0.5 / x1.5 on the base) - not run unless asked.

## Implementation steps

1. Data repo `NA_inputs/build_14_scenarios.py`: new/changed scenario functions (s01 re-size, s05 delay leg, s06
   fuel-only, s07a/s07b, s10, s11, s12 tranche path, s13 sizing, s15, s16 via `copy_overlay` of `grid_low` /
   `grid_high`, funnel release via `release_gas_minima` inside s07a/s07b/s12/s14), registry update, overlay folders
   deleted before `--apply` (stale-row lesson), `Assumptions.txt` entries, the colleague document registered as a
   source. s17 needs no data (run setting).
2. Check first: what `set_peaking_slack` does in the equations (several drivers pass 0), and what the v6 `grid_high`
   overlay contains (IC path only vs the wires-for-gas swap) - use the IC part only.
3. Conversion: 15 RegularParameters workbooks (`_s14_convert.py` list updated); Hormuz variants reuse the parents.
4. Drivers: labels `fel2026_sNN_<name>_49_2015_v6_v4` (new cases `_v1`, Hormuz `_hormuz`); label grep before launch;
   chain `_s14/run_all_v4.sh` with the julia PATH export; gates per run (OPTIMAL, INF, input-dump diff).
5. Analysis: `analyze_s14.py` wave `4`; floor/ceiling band and cap-binding table; results doc
   `RESULTS_wave4_<date>.md`; `scenario_mapping.csv` update; plan workbook sheet `Wave4_changes`.
6. Canada: incorporate `Canada Scenarios_MEP27.docx` once an unprotected copy is available (s08 and possibly s15).
