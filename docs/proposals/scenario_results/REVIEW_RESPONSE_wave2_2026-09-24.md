# Response to the wave-2 review (2026-09-24)

Reviewer material: `REVIEW_wave2_2026-09-24.md` (status of the 16 wave-1 items, six new findings N1-N6).
Every number below was checked against the wave-2 input dumps and results in the model database
(base `fel2026_base_49_2015_v6e`). Action taken: **wave 3** - two base-data fixes (rooftop build-rate cap, gas-steam
floor), one definition refinement (s10 derate ramp), the base and all 14 scenarios rerun on the fixed data
(`fel2026_base_49_2015_v6f`, scenario labels `_v3`; s03/s06 `_v4`, s14 `_v5`), plus a **funnel-released twin** of every
scenario except s05 (`fel2026_sNN_<name>_open_49_2015_v6`). Results: `../scenario_plan_2026-09-18/RESULTS_wave3_2026-09-25.md`.

## Wave-1 items (reviewer's status table)

Agree with all 16 verdicts. Nothing to contest. Open item 13 (2025 gas calibration, power burn 27.9 vs 36.9 Bcf/d)
stays a v7 item; the caveat on absolute gas TWh remains on every table.

## New findings

### N1 (Serious) rooftop PV - confirmed, mechanism found, fixed in wave 3

| Check | Finding |
|---|---|
| Cost | Not the problem. Rooftop commercial capex 720 / 570 / 460 MEUR/GW (2025/30/40) vs utility 470 / 380 / 320 = 1.5x (LCOE model V1.4); fixed O&M similar. Residential rooftop is forbidden in the NA data (max 0.001 GW). |
| Funnel membership | **Rooftop is an uncapped bypass of the utility-PV pipeline funnel.** Utility PV carries the announced-pipeline maximum (PJM 19 / 30 / 46 GW in 2027 / 29 / 31, binding) until the funnel opens after 2031 (88 GW in 2033). Rooftop has no pipeline minimum, no build-rate limit (per-technology investment caps are not a data sheet; the parameter is hard-wired to 999999) and only the flat restool potential as maximum (PJM 168, SERC 127 GW). It therefore builds exactly while the utility maximum binds (PJM 16.8 and SERC 12.7 GW/yr in 2026-31) and stops when it opens (0.8 GW in 2032, ~0 after). The same mechanism makes it the first responder in s05 (+88 GW rooftop / -109 utility), s10 (+89), s12 (-72) and s14 (+240 / +22). |
| Potentials, CA/WECC/ERCOT | Potentials are not the reason (CA 68, ERCOT 86, WECC 132 GW). The three regions have the largest capacity-factor penalty of rooftop vs utility (0.16-0.20 vs 0.20-0.22 from the timeseries), in the East the gap is below 0.01, so rooftop at 1.5x the cost is only worth building where utility PV is capped. |
| Behind-the-meter treatment | Consistent: the FEL demand is busbar demand net of behind-the-meter PV (`NA_inputs/canada_demand_assessment.md`), so a 0 GW rooftop residual is correct. New rooftop selling at busbar is a simplification, not an error. |
| s05 rule | The s05 "RES max = pipeline" rule covered utility PV and wind only, so rooftop bypassed it too. |

Fix (wave 3, base data, region-agnostic): a build-rate cap on `P_PV_Rooftop_Commercial` via a group limit
(`RooftopPV x USA` in `Par_GroupTotalAnnualMaxNewCap`): 7 GW/yr 2026-30 rising to 10 GW/yr by 2040. Source: EIA
small-scale solar additions 6.4 GW in 2022 (record; 39.5 GW total) and the STEO path 44 GW (Jun-2023) -> 55 GW
(end-2024) = ~7.7 GW/yr; the growth to 10 GW/yr is an assumption and is flagged in the data repo. National cap, regional
split left to the model; Canada keeps its CER path. Documented in `Par_GroupTotalAnnualMaxNewCap/Assumptions.txt`,
sources saved and registered.

### N2 (Serious) s06 foresight pre-build - confirmed, same root cause

s06 v3 builds 43 / 51 GW of rooftop in 2026 / 27 (base 15.6 / 28.4), then ~0 in 2028-30; utility PV is unchanged because
it is pipeline-capped. The pre-build runs through the only uncapped PV class, so the rooftop cap bounds it to the
cap. Pinning 2026-27 builds to base values is kept as a second lever in case the rerun still shows a visible pre-build.

### N3 (Check) s14 cost - agreed, transfers quantified

| Component (discounted 2025-40, bEUR) | Value |
|---|---|
| Objective delta vs base | +271 |
| CO2 payments (in the objective) | 322 |
| ITC value (capex reduction x new capacity, 2029-40) | 193 (319 undiscounted) |
| 45Q credit (variable-cost reduction x CCS output) | 24 |
| **Resource cost = delta - CO2 + ITC + 45Q** | **+166 (+6 % of the 2,675 base)** |

The results tables now carry `itc_value`, `q45_value` and `resource_cost` next to the objective delta; no statement
"decarbonization is cheaper than the base" is made.

### N4 (Check) new gas steam - confirmed, data artefact, fixed in wave 3

The funnel minimum for `P_Gas_Steam` is held flat at its 2035 value (40 GW US) while the residual steam fleet keeps
retiring (30.6 GW in 2040); the difference is forced as new steam units (12 GW 2026-40: Canada, New York, SPP, ERCOT,
New England) at a placeholder 1,100 MEUR/GW whose own source comment says no new steam is expected. Steam also sits in
the GasPlants group and consumed part of the turbine-supply budget. Fix: the minimum is clamped to the residual
capacity of the same region and year (31 rows), so no new steam can be forced; the export label can stay.
Residual effect found in the v6f probe: New York still builds 1-4 GW of steam after 2037 on its own, because its
OCGT/CCGT/engine pipeline maxima are essentially the residual fleet (OCGT 2.8, CCGT 1.0 GW) and steam (max 10 GW) is
the only firm option left for the peaking constraint. Not a floor artefact any more; v7 item (New York gas pipeline
maxima vs peaking requirement).

### N5 (Note) geothermal label - export only

The EGS row includes the existing conventional fleet (4.1 GW / 32 TWh in 2025). Label "Geothermal (incl. EGS)" in
the export; no model change.

### N6 (Check) s10 2030 peaker jump - explained, derate ramped in wave 3

The derate is coastal as designed (SERC, ERCOT, New York, New England, California; gas and nuclear; -5 pp from
2030). The jump comes from the residual CCGT fleet, whose availability factor (0.50) is its fleet capacity-factor
cap: 0.45 removes 10 % of its energy in one step (-91 TWh residual CCGT in 2030, +97 TWh OCGT). The relocated load
already ramps (53 / 67 / 81 TWh in 2030-32). Wave 3 ramps the derate -1 pp/yr from 2030 to -5 pp in 2034.

### Item 4 - storage sheet

`Scripts/export_storage_tables.py <scenario labels>` writes D_* power (GW) and S_* energy (GWh) capacity per
scenario, region and year (`Results/storage_capacity_wave.csv`) for the export.

## The funnel: assessment and decision

The funnel has two sides that deserve different answers.

- **Lower side = forced minima** (announced pipeline as `TotalAnnualMinCapacity`; CCGT is pinned to its minimum
  from 2032 on, 263 GW US in 2040, OCGT within 10 % of it). Binding in every run except s05. In s14 (90 USD/t), s07
  (cheap fusion and iron-air) and s12 (-1.3 PWh) it forces 366 GW of new CCGT+OCGT in 2029-40 that the model would not
  build on its own: new-CCGT capacity factor 36-40 % against 65 % in the base, ~196 bEUR of discounted overnight capex
  sunk. It distorts the cost deltas (s14 pays for gas it does not run, s12's saving is understated) and contradicts
  the stories (a 90 USD/t world cancels gas projects). s05 shows the mechanism works: minimum = residual from 2027
  gives 198 GW instead of 390.
- **Upper side = build-rate caps** (GasPlants 6 / 9 / 10 / 35 / 35 GW/yr 2026-30, GasEngines 2.5 GW/yr, utility PV and
  wind pipeline maxima to ~2031). Binding in every scenario 2026-30 (all runs build exactly the cap), i.e. the demand
  booms (s02, s03, s13) cannot add gas before 2031 and add it later. These caps encode real turbine backlogs and
  interconnection queues and stay in every run. Their PV side effect was the rooftop bypass (N1), fixed by the cap.
- **Against opening broadly**: near-term minima are projects under construction; funnel-freed fleets rely on the
  peaking constraint, which under-secured winter VRE droughts in the v6 `economic` dispatch (VoLL hours, unserved
  energy; open v7 topic); and the "one identical setup" rule for the 14.

**Decision (user, 2026-09-24):** the wave-3 main set keeps the funnel (base and all 14, reference); every scenario
except s05 gets a **funnel-released twin** with the gas guardrail minimum = residual capacity from 2031 (announced
projects through 2030 kept, build-rate caps unchanged, everything else as in the main run). The base itself is not
released, so the twins' deltas vs base contain the release effect; the results doc reports each twin against its own
funnel run as well. Peaking caveat stated with the twins.

## Wave-3 verification (filled from the runs)

- Base v6f vs v6e (run 2026-09-24 12:16, OPTIMAL, INF 4.4 TWh, objective +0.07 %): rooftop additions sit exactly on the
  cap every year (7.0 GW 2026-30 -> 9.7 GW 2039; rooftop fleet 46 GW in 2031 instead of 188, 115 GW in 2040 instead
  of 188); no forced steam (New York builds 0.7-1.5 GW on its own 2038-40, see N4). Consequence of the cap: the base
  has less solar and more gas in the 2030s - 2030 solar 700 vs 885 TWh, gas 2,003 vs 1,821; 2035 solar 1,281 vs 1,423,
  gas 2,495 vs 2,385; 2040 solar 1,788 vs 1,853, gas 2,798 vs 2,770, wind 1,384 vs 1,349; CO2 2040 1,171 vs 1,161 Mt.
  2025 identical. Largest regional shifts in the funnel years (PJM 2029 solar 54 vs 119 TWh, New England 2030 8 vs 22).
- s10 v3 (OPTIMAL, INF 4.4): the 2030 step is gone - OCGT +18 TWh in 2030 (was +97), rising with the ramp to +125 in
  2034 while the residual CCGT loses -96 TWh; the shift itself remains, as it is the residual fleet's CF cap.
- s06 v4 (OPTIMAL, INF 2.5): the pre-build is gone - 2026/27 new capacity equals the base (rooftop 7.8 / 7.3 GW on the
  cap, utility 29.8 / 35.8 identical, wind +0.3 / +1.6, storage 0 / +2.4 GW). Cost by year: +1.6 / +11.0 (2026-27
  shock), -9.6 / -13.1 / -8.7 / -4.1 (recession 2028-31), +3.9 / +3.0 (2032-33); net -16 bEUR; 2040 mix = base.
- Twins (13, all OPTIMAL, INF 2.5-5.0): release worth -18 to -27 bEUR per scenario (s14 -40, s12 -50), 90-216 GW less
  gas capacity, new CCGT+OCGT 2031-40 = 108 GW in the s14 twin vs 306 with the funnel; s14 twin resource cost +106
  bEUR (funnel run +149), CO2 682 vs 670 Mt (residual CCGT runs harder). Details in the wave-3 results doc.
