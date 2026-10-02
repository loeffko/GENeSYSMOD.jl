# Wave 3 - report for the reviewer (2026-09-25)

Scope: your wave-2 review (`REVIEW_wave2_2026-09-24.md`) triggered two base-data fixes, one definition refinement and a
funnel-released variant of every scenario. Everything was rerun on one setup. This report gives (1) what changed and why,
(2) the answer to each of your findings with the verifying numbers, (3) the wave-3 results, (4) what to check in the
export and what remains open. Model database labels are listed at the end; every figure here comes from the DB
(input dumps `input_*`, results `output_*`), not from the workbook.

## 1. What changed since wave 2

| Change | Where | Why |
|---|---|---|
| **Rooftop PV build-rate cap**: subset `RooftopPV` = `P_PV_Rooftop_Commercial`, `Par_GroupTotalAnnualMaxNewCap` `RooftopPV x USA` = 7.0 GW/yr 2026-30, linear to 10.0 GW/yr in 2040 | base data (all runs) | N1. Source: EIA small-scale solar additions 6.4 GW in 2022 (record, 39.5 GW total) and the STEO path 44 GW (Jun-2023) -> 55 GW (end-2024), i.e. ~7.7 GW/yr. The growth to 10 GW/yr is an assumption and is flagged in the data repo. National cap; Canada keeps its CER path. |
| **Gas-steam floor**: `TotalAnnualMinCapacity` of `P_Gas_Steam` clamped to the residual fleet (31 rows) | base data | N4 |
| **s10 derate ramp**: coastal availability cut -1 pp/yr 2030-34 instead of -5 pp in 2030 | s10 | N6 |
| **Funnel-released twins**: gas guardrail minimum (CCGT, OCGT, steam, engines) = residual capacity from 2031; announced projects through 2030, build-rate caps and everything else unchanged | 13 twins (all but s05) | your item 2; see section 4 |
| New reference base `fel2026_base_49_2015_v6f`; scenario labels `_v3` (s03/s06 `_v4`, s14 `_v5`); twins `_open` | DB | wave-2 rows (`v6e`, `_v2`, ...) remain in the DB |

Not changed: forced gas minima in the main set (by design, the twins answer it), coal/nuclear pinning, hydro 2026,
2025 gas calibration (v7 items, caveats stay).

## 2. Your findings, verified

**N1 rooftop PV (serious) - confirmed, mechanism found, fixed.** Cost is not the problem: rooftop commercial capex
720 / 570 / 460 MEUR/GW (2025/30/40) vs utility 470 / 380 / 320, i.e. 1.5x (residential rooftop is forbidden in the
NA data). Rooftop was an **uncapped bypass of the utility-PV pipeline funnel**: utility PV carries the announced-pipeline
maximum until it opens after 2031 (PJM 19 / 30 / 46 GW in 2027 / 29 / 31, binding; 88 GW in 2033), while rooftop had no
pipeline minimum, no build-rate limit (the per-technology investment cap is not a data sheet in the model, it is
hard-wired to 999999) and only the flat restool potential as maximum (PJM 168, SERC 127 GW). It therefore built exactly
while the utility maximum bound (PJM 16.8 and SERC 12.7 GW/yr, 2026-31) and stopped when it opened (0.8 GW in 2032).
No CA/WECC/ERCOT because the rooftop capacity factor there is 0.16-0.20 vs 0.20-0.22 for utility (largest gap of all
regions); in the East the gap is below 0.01. Behind-the-meter treatment is consistent: the FEL demand is busbar demand
net of BTM PV, so a 0 GW residual is correct; new rooftop selling at busbar is a simplification. With the cap the
rooftop fleet is 46 GW in 2031 (was 188) and 115 GW in 2040.

**N2 s06 pre-build (serious) - confirmed, same root cause, gone.** s06 v3 had built 43 / 51 GW of rooftop in 2026 / 27
(base 15.6 / 28.4). In s06 v4 the 2026-27 additions equal the base (rooftop 7.8 / 7.3 GW on the cap, utility identical,
wind +0.3 / +1.6, storage 0 / +2.4 GW). No pinning was needed.

**N3 s14 transfers (check) - agreed, quantified.** Discounted 2025-40, funnel run (v5): objective delta +304 bEUR =
resource cost + CO2 payments 361 - ITC value 180 - 45Q credit 26, so **resource cost = +149 bEUR (+5.6 % of the 2,677
base)**. Wave-2 figures for reference: +271 = resource +166 + 322 - 193 - 24. The tables now carry `itc_value`,
`q45_value` and `resource_cost`; no "cheaper than base" statement is made.

**N4 new gas steam (check) - confirmed data artefact, fixed; one residual.** The funnel minimum for steam was held flat
at its 2035 value (40 GW US) while the residual fleet retires (30.6 GW in 2040); the gap was forced as new units (12 GW
2026-40) at a placeholder 1,100 MEUR/GW. Clamped to the residual. Residual effect: **New York** still builds 0.7-1.5
GW/yr of steam in 2038-40 on its own, because its OCGT / CCGT / engine pipeline maxima are essentially the residual
fleet (OCGT 2.8, CCGT 1.0 GW) and steam (max 10 GW) is the only firm option left for the peaking constraint. Not a
floor artefact; v7 item (New York pipeline maxima vs peaking requirement). Please keep the "Gas Steam" row label.

**N5 geothermal label (note)** - export only: the EGS row carries the existing conventional fleet (4.1 GW / 32 TWh in
2025). Suggested label "Geothermal (incl. EGS)".

**N6 s10 2030 peaker jump (check) - explained, ramped.** The derate is coastal as designed (SERC, ERCOT, NY, NE, CA; gas
and nuclear). The jump came from the residual CCGT fleet, whose availability factor (0.50) is its fleet capacity-factor
cap: 0.45 removes 10 % of its energy in one step (-91 TWh residual CCGT, +97 TWh OCGT in 2030). With the ramp, s10 v3
shows OCGT +18 TWh in 2030 (was +97), rising to +125 in 2034 while the residual CCGT loses -96 TWh; the shift itself is
structural and remains.

**Item 4 storage sheet** - `storage_capacity_wave3.csv` (next to this report) holds D_* power capacity (GW) and S_*
energy capacity (GWh) per scenario, region and year for all 28 runs.

**Item 2 gas GW is an input** - correct for the main set; the twins are the answer, see section 4.

## 3. Base v6f vs v6e

| | v6e | v6f |
|---|---|---|
| objective (bEUR, discounted 2025-40) | 2,675.3 | 2,677.2 (+0.07 %) |
| rooftop additions 2026-31 (US, GW/yr) | 15.6 / 28.4 / 38.4 / 33.2 / 35.7 / 34.9 | 7.0 (on the cap), then 7.3-9.7 to 2039 |
| rooftop fleet 2031 / 2040 (GW) | 188 / 188 | 46 / 115 |
| new gas steam 2026-40 | 12 GW forced | 0.1 GW + New York 0.7-1.5 GW/yr 2038-40 (see N4) |
| generation 2030: solar / gas (TWh) | 885 / 1,821 | 700 / 2,003 |
| generation 2035: solar / gas / wind | 1,423 / 2,385 / 1,006 | 1,281 / 2,495 / 1,032 |
| generation 2040: solar / gas / wind | 1,853 / 2,770 / 1,349 | 1,788 / 2,798 / 1,384 |
| CO2 2030 / 2035 / 2040 (Mt) | 1,317 / 1,238 / 1,161 | 1,398 / 1,277 / 1,171 |
| 2025 | identical | identical |

Expect the base to lean more on gas in the 2030s: the ~140 GW of rooftop the model had used as the escape valve are
filled by gas in the funnel years and by wind later. INF slack 4.4 TWh (v6e 4.5). Input dumps differ only in the two
fixed parameters and the new subset tag.

## 4. Results

### 4a. Main set (funnel kept), 2040 deltas vs base v6f

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CO2 payments (bEUR) | resource cost net of transfers (bEUR) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | v6f | 8,242 TWh | 2,798 | 1,788 | 1,384 | 1,150 | 844 | 305 | 1,171 Mt | 2,677 | 0 | - |
| 1 | EV comeback (s01_ev, v3) | +245 | +58 | +39 | +150 | 0 | +5 | +1 | +22 | +67 | 0 | +67 |
| 2 | H2 comeback (s02_h2, v3) | +399 | +161 | +84 | +155 | 0 | +12 | 0 | +58 | +56 | 0 | +56 |
| 3 | Age of compute (s03_compute, v4) | +694 | +363 | +124 | +205 | 0 | +21 | +1 | +141 | +81 | 0 | +81 |
| 4 | Space race, terrestrial (s04_space, v3) | +155 | +79 | +41 | +35 | 0 | +9 | 0 | +29 | +15 | 0 | +15 |
| 5 | Political brakes (s05_brakes, v3) | -518 | -461 | -72 | +2 | 0 | -210 | -1 | -154 | -201 | 0 | -201 |
| 6 | Hormuz 6C (s06_hormuz, v4) | 0 | +3 | +1 | -3 | 0 | 0 | -2 | +1 | -16 | 0 | -16 |
| 7 | Tech breakthrough (s07_tech, v3) | 0 | -80 | +42 | -14 | 0 (+73 fusion) | -28 | +35 (+39 iron-air) | -31 | -1 | 0 | +12 |
| 8 | Canada DC, pipeline-consistent (s08_canada, v3) | -49 | +10 | +1 | -60 | 0 | +3 | 0 | +4 | -11 | 0 | -11 |
| 9 | Water boom (s09_water, v3) | +36 | +10 | +10 | +16 | 0 | +1 | 0 | +4 | +4 | 0 | +4 |
| 10 | Climate reshuffle (s10_climate, v3) | +216 | +38 | +66 | +134 | -27 | -7 | +1 | +27 | +49 | 0 | +49 |
| 11 | FEOC (s11_feoc, v3) | 0 | +4 | -1 | -3 | 0 | 0 | 0 | +1 | +7 | 0 | +7 |
| 12 | AI overbuild (s12_overbuild, v3) | -1,294 | -719 | -320 | -254 | 0 | -26 | -4 | -262 | -205 | 0 | -205 |
| 13 | Reindustrialization (s13_reindustrial, v3) | +163 | +84 | +45 | +34 | 0 | +12 | 0 | +30 | +51 | 0 | +51 |
| 14 | Decarbonization (s14_decarb, v5) | 0 | -606 | +193 | +284 | +254 | +25 (+40 CCS) | +1 | -501 | +304 | 361 | +149 |

TWh unless stated; storage = D_ power capacity; cost = discounted system cost delta 2025-40; cost per MWh = delta
cost / delta demand 2025-40. "Resource cost" backs out CO2 payments and the capex / variable-cost reductions vs base;
it is the relevant number for s14 only (for s07 / s11 the capex change is the scenario itself).

Against wave 2 the 2040 deltas keep their shape; the flexible PV response becomes wind and gas. s10's north-shift is
now wind-led and no longer lowers CO2 (+27 Mt instead of -6); s14 keeps less solar (+193 vs +269 TWh) and more gas
(-606 vs -690), 2040 CO2 670 Mt (was 637). s05 and s12 are unchanged in substance; s06 is now almost invisible in 2040.

### 4b. Funnel-released twins, 2040 deltas vs base v6f

Definition: gas guardrail minimum = residual capacity from 2031 (announced projects through 2030 kept, build-rate
caps kept). **The base is not released**, so these deltas contain the release effect itself. s05 has no twin (it
already releases from 2027) and is shown with its main run.

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CO2 payments (bEUR) | resource cost net of transfers (bEUR) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | v6f | 8,242 TWh | 2,798 | 1,788 | 1,384 | 1,150 | 844 | 305 | 1,171 Mt | 2,677 | 0 | - |
| 1 | EV comeback (s01_ev, open) | +245 | -28 | +68 | +190 | 0 | -108 | +1 | +2 | +46 | 0 | +46 |
| 2 | H2 comeback (s02_h2, open) | +399 | +74 | +105 | +206 | 0 | -102 | +1 | +36 | +35 | 0 | +35 |
| 3 | Age of compute (s03_compute, open) | +694 | +323 | +141 | +219 | 0 | -67 | 0 | +127 | +62 | 0 | +62 |
| 4 | Space race, terrestrial (s04_space, open) | +155 | -65 | +70 | +140 | 0 | -120 | 0 | -13 | -9 | 0 | -9 |
| 5 | Political brakes (s05_brakes, v3) | -518 | -461 | -72 | +2 | 0 | -210 | -1 | -154 | -201 | 0 | -201 |
| 6 | Hormuz 6C (s06_hormuz, open) | 0 | -170 | +35 | +129 | 0 | -137 | -2 | -49 | -42 | 0 | -42 |
| 7 | Tech breakthrough (s07_tech, open) | 0 | -287 | +80 | +160 | 0 (+73 fusion) | -179 | +47 (+52 iron-air) | -93 | -27 | 0 | -15 |
| 8 | Canada DC, pipeline-consistent (s08_canada, open) | -49 | -164 | +32 | +79 | 0 | -135 | 0 | -47 | -36 | 0 | -36 |
| 9 | Water boom (s09_water, open) | +36 | -151 | +44 | +138 | 0 | -133 | 0 | -43 | -20 | 0 | -20 |
| 10 | Climate reshuffle (s10_climate, open) | +216 | +5 | +75 | +145 | -27 | -97 | +1 | +23 | +31 | 0 | +31 |
| 11 | FEOC (s11_feoc, open) | 0 | -171 | +33 | +133 | 0 | -137 | 0 | -50 | -18 | 0 | -18 |
| 12 | AI overbuild (s12_overbuild, open) | -1,294 | -946 | -263 | -83 | 0 | -242 | -2 | -325 | -255 | 0 | -255 |
| 13 | Reindustrialization (s13_reindustrial, open) | +163 | -60 | +74 | +144 | 0 | -118 | 0 | -11 | +28 | 0 | +28 |
| 14 | Decarbonization (s14_decarb, open) | 0 | -643 | +206 | +278 | +254 | -180 (+40 CCS) | +1 | -488 | +264 | 367 | +106 |

### 4c. Release effect = twin minus its own funnel run (2040)

| scenario | gas TWh | gas GW | new gas 2026-40 (GW) | solar TWh | wind TWh | CO2 Mt | cost bEUR |
|---|---|---|---|---|---|---|---|
| s01 EV | -86 | -113 | 446 -> 333 | +29 | +40 | -20 | -21 |
| s02 H2 | -88 | -114 | 453 -> 339 | +21 | +51 | -22 | -21 |
| s03 compute | -40 | -88 | 461 -> 373 | +17 | +14 | -14 | -20 |
| s04 space | -144 | -129 | 449 -> 320 | +29 | +105 | -42 | -24 |
| s06 Hormuz | -173 | -137 | 441 -> 304 | +34 | +133 | -50 | -26 |
| s07 tech | -207 | -151 | 412 -> 262 | +38 | +175 | -62 | -27 |
| s08 Canada DC | -175 | -137 | 443 -> 306 | +32 | +140 | -50 | -25 |
| s09 water | -161 | -134 | 441 -> 308 | +35 | +122 | -47 | -25 |
| s10 climate | -33 | -90 | 434 -> 344 | +9 | +10 | -4 | -18 |
| s11 FEOC | -174 | -137 | 441 -> 304 | +34 | +136 | -51 | -25 |
| s12 overbuild | -227 | -216 | 415 -> 199 | +56 | +171 | -63 | -50 |
| s13 reindustrial | -144 | -130 | 452 -> 322 | +28 | +110 | -41 | -23 |
| s14 decarb | -37 | -204 | 465 -> 261 | +13 | -6 | +12 | -40 |

Base new gas 2026-40: 440 GW. New CCGT+OCGT in 2031-40: base 318 GW, s14 funnel 306, s14 twin 108, s07 twin 149,
s12 twin 87.

Reading:
- The release is worth -18 to -27 bEUR in every ordinary scenario, -40 in s14 and -50 in s12; it removes 90-140 GW of
  gas capacity (s12 216, s14 204) and moves 30-230 TWh of gas generation to wind. CO2 falls 40-60 Mt where gas output
  drops; in the demand booms (s03, s10) little changes, the extra gas is wanted anyway (new CCGT still at 60-66 %).
- s14 twin: new CCGT 137 GW instead of 278, new-CCGT capacity factor 0.54 instead of 0.39, objective +264 bEUR,
  resource cost +106 bEUR (funnel run +149). CO2 2040 is 682 Mt vs 670 in the funnel run: with fewer new CCGTs the
  residual fleet runs harder (1,023 vs 888 TWh) and 22 TWh of coal survive. The policy case gets cheaper, not
  cleaner, when it stops paying for gas plants it does not need.
- s07 twin: the breakthrough displaces gas instead of idling it (gas -287 TWh / -179 GW vs base, iron-air 52 GW,
  CO2 -93 Mt, cost -27 bEUR; funnel run -80 TWh, -1 bEUR).
- s12 twin: the overbuild story with cancellations (new gas 199 GW instead of 415, CO2 -325 Mt, -255 bEUR).

## 5. Please check / known limits

1. **Rooftop cap level** (7 -> 10 GW/yr national): the only new number in wave 3. If you have a better distributed-PV
   build-rate series (SEIA / Wood Mackenzie by state), we can regionalise it; the model keeps the split free today.
2. **Twins are not dispatch-checked, and no firm-capacity constraint is active** (correction, 2026-10-02): all NA
   investment runs, the v6 freeze included, pass `set_peaking_slack = 0`, which makes the peaking constraints vacuous,
   and the reserve margin switch is off. Adequacy rests on the 49-hour energy balance only. Nominal firm capacity 2040
   (gas + nuclear + coal + hydro + storage): base 1,561 GW, s14 twin 1,437, s12 twin 1,319. The v6 `economic` dispatch
   showed that funnel-freed fleets can carry winter-drought scarcity. Treat twin gas GW as a lower bound; a firm-capacity
   requirement is a v7 baseline item.
3. **s14 twin CO2 above the funnel run** (682 vs 670 Mt) is real model behaviour (residual CCGT and coal run more), not
   a bug; worth a sentence in any messaging.
4. **New York steam** (N4 residual) and the general point that NY's gas pipeline maxima equal its residual fleet.
5. Base 2025 is unchanged; the 2025 gas calibration caveat (27.9 vs 36.9 Bcf/d) stays.

## 6. For the export

- Main set: `fel2026_base_49_2015_v6f`, `fel2026_s01_ev_49_2015_v6_v3`, `fel2026_s02_h2_49_2015_v6_v3`, `fel2026_s03_compute_49_2015_v6_v4`, `fel2026_s04_space_49_2015_v6_v3`, `fel2026_s05_brakes_49_2015_v6_v3`, `fel2026_s06_hormuz_49_2015_v6_v4`, `fel2026_s07_tech_49_2015_v6_v3`, `fel2026_s08_canada_49_2015_v6_v3`, `fel2026_s09_water_49_2015_v6_v3`, `fel2026_s10_climate_49_2015_v6_v3`, `fel2026_s11_feoc_49_2015_v6_v3`, `fel2026_s12_overbuild_49_2015_v6_v3`, `fel2026_s13_reindustrial_49_2015_v6_v3`, `fel2026_s14_decarb_49_2015_v6_v5`.
- Twins: `fel2026_s01_ev_open_49_2015_v6`, `fel2026_s02_h2_open_49_2015_v6`, `fel2026_s03_compute_open_49_2015_v6`, `fel2026_s04_space_open_49_2015_v6`, `fel2026_s06_hormuz_open_49_2015_v6`, `fel2026_s07_tech_open_49_2015_v6`, `fel2026_s08_canada_open_49_2015_v6`, `fel2026_s09_water_open_49_2015_v6`, `fel2026_s10_climate_open_49_2015_v6`, `fel2026_s11_feoc_open_49_2015_v6`, `fel2026_s12_overbuild_open_49_2015_v6`, `fel2026_s13_reindustrial_open_49_2015_v6`, `fel2026_s14_decarb_open_49_2015_v6`.
- Storage: `storage_capacity_wave3.csv` (Scenario, Region, Technology, Year, Quantity = power capacity [GW] for D_* /
  energy capacity [GWh] for S_*, Value, Unit).
- Mapping notes: `P_Fusion` (s07) is its own row; `D_IronAir` / `S_IronAir` are the iron-air storage;
  `P_PV_Rooftop_Commercial` is all US distributed PV; EGS row = `P_EGS_R1` + conventional geothermal; `P_Gas_Steam`
  additions after 2037 are New York only.
- Emissions: sum `output_emission` with Type in ('Emissions', 'ExogenousEmissions'); the 'Regional Endogenous CO2 Price'
  rows are cap shadow prices, not tonnes.

Full documents: `RESULTS_wave3_2026-09-25.md` (results), `REVIEW_RESPONSE_wave2_2026-09-24.md` (item-by-item response),
`NA_scenario_plan_2026-09-18_v4.xlsx` sheet `Wave3_changes` (definitions).
