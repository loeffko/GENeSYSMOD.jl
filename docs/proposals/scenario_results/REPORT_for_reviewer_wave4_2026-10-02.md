# Wave 4 - report for the reviewer (2026-10-02)

Scope: wave 4 applies the North America hub's market-intelligence feedback on the 14 scenarios (their "Input
Scenarios (v3)" note: likelihood/impact ratings, re-sizing arguments, proposed additions A-G) to the set. The base is
unchanged (v6f, the July freeze; the hub's "move nuclear life extension and Alberta into the base" asks are recorded as
baseline items for the next version). This report gives (1) what changed in each scenario and why, (2) the results,
(3) what the results say about each piece of feedback, (4) a diagnostic on the firm-capacity constraint, and (5) export
notes. All figures come from the model database (input dumps `input_*`, results `output_*`), 2040 deltas vs base v6f
unless stated. Wave-3 numbers quoted for comparison are from `s14_summary_wave3.csv` / `..._wave3_open.csv` (same base).

## 1. What changed

| run | definition | funnel |
|---|---|---|
| s01 EV (v4) | re-sized to the hub's upside: +20 TWh of BEV load in 2030 (BEV share 23 % vs 10 % baseline), AEO2026-shaped after (+49 TWh in 2040); Canada base | kept |
| s03 compute (wave-3 v4, unchanged) | second-wave adders above the FEL base | kept |
| s05 brakes (v4) | DC increment above 2026 delayed 2 years (ERCOT, New York 3) and cut to the credible tranche (55 %, ERCOT 66 %); gas minimum = residual from 2027, RES max = pipeline, gas cap window as before | released 2027 |
| s06 Hormuz (v5) | fuel-price channel only: Henry-Hub uplift 2026-30 (base workbook + allFuels_v6_s06); capex/WACC uplift, IC cap and recession demand dropped | kept |
| s07a LDES (new) | iron-air from 2027 (0.5/1/2/3/4/5 GW/yr cap) + optimistic Li-ion (cost, 7 h); SMR and fusion at base | released 2031 |
| s07b fusion/SMR (new) | fusion backed ramp 2034-40 (9.5 GW), SMR 2/5/15/40 GW path at 5,500 -> 3,600 USD/kW; storage at base | released 2031 |
| s08 Canada (wave-3 v3, unchanged) | pipeline-consistent Canada DC path; Canada document pending | kept |
| s10 climate (v4) | relocation 0 % (2035) / 5 % (2040) instead of 10/20 %; cooling uplift, coastal derate ramp, +50 % coastal IC cost kept | kept |
| s11 FEOC + tariffs (v4) | FEOC premium and Li-ion cap as before, IC expansion cost x1.2 x1.15 (Section 232 transformers) | kept |
| s12 overbuild (v4) | credible tranche only: DC = 2026 + 55 % of the FEL increment to 2030 (ERCOT 66 %), flat 2031-32, FEL growth after; Canada base | released 2031 |
| s13 reindustrial (v4) | ~30 GW by 2035 (236 TWh at 90 % LF, flat after) on the wave-3 regional pattern + Starbase Louisiana 2 GW (SERC), Starbase TX + chip plant 2 GW (ERCOT), Permian O&G electrification 1.6 GW (SPP) | kept |
| s14 decarb (v6) | CO2 price 30/60/90 USD/t, ITC phase-in, 45Q, CCS 40 GW cap, announced nuclear, state caps (unchanged) | released 2031 |
| s15 affordability (new) | grid-connected DC increment delayed one year (large-load tariffs, deposits, ramp schedules); interconnector growth = v6 grid_low path; the BYOG leg (40 % of the DC increment) is an ownership shift and is reported as a metric | kept |
| s16 transmission supercycle (new) | v6 grid_high interconnector path (aggregate IC budget 2x the 2025 installed by 2040, corridor funnel); gas funnel as base | kept |
| s03/s05/s12/s14 _hormuz | parent definition + the Hormuz fuel uplift (allFuels_v6_s06) | as parent |
| base_peaking / base_peaking_flexdc | diagnostics: base v6f with the peaking constraint switched on (`set_peaking_slack` 1.0) and with 10 % of the data-center peak curtailable (slack 0.975) | kept |

Dropped as runs: s02 hydrogen (hub: electrolytic H2 below the FEL flat case, activity is CCS-backed), s04 space (point
loads now inside s13), s09 water (immaterial, siting constraint). Their wave-3 results remain citable. "Funnel
released" = gas guardrail minimum (CCGT, OCGT, steam, engines) set to the residual fleet from 2031 inside the
definition; announced projects through 2030 and the turbine-supply caps are kept. There are no "twin" runs in wave 4.

## 2. Results

### 2a. Main set (2040 vs base v6f)

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CF solar/wind 2040 | curtailed 2040 | resource cost net of transfers (bEUR) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | v6f | 8,242 TWh | 2,798 | 1,788 | 1,384 | 1,150 | 844 | 305 | 1,171 Mt | 2,677 | 0.20/0.36 | 175 TWh | - |
| 1 | EV comeback (s01_ev, v4) | +49 | +18 | +12 | +19 | 0 | +1 | 0 | +7 | +15 | 0.20/0.36 | +4 | +15 |
| 3 | Age of compute (s03_compute, v4) | +694 | +363 | +124 | +205 | 0 | +21 | +1 | +141 | +81 | 0.20/0.35 | +6 | +81 |
| 5 | Political brakes (s05_brakes, v4) | -783 | -651 | -135 | -3 | 0 | -235 | 0 | -222 | -305 | 0.20/0.35 | +27 | -305 |

TWh unless stated; storage = D_ power capacity; cost = discounted system cost delta 2025-40; resource cost backs out CO2
payments and capex / variable-cost reductions vs base (relevant for s14 only).

### 2b. Hormuz as a fuel sensitivity

| scenario | parent cost (bEUR) | with Hormuz fuel | fuel-shock cost | gas 2040 TWh parent / Hormuz | CO2 2040 parent / Hormuz |
|---|---|---|---|---|---|
| base (= s06 v5) | 0 | +64 | +64 | 2,798 / 2,797 | 1,171 / 1,170 |
| s03 compute | +81 | +146 | +65 | 3,161 / 3,160 | 1,311 / 1,311 |
| s05 brakes | -305 | -250 | +56 | 2,147 / 2,148 | 949 / 949 |
| s12 overbuild | -196 | -136 | +60 | 2,282 / 2,282 | 1,000 / 1,000 |
| s14 decarb | +264 | +327 | +62 | 2,155 / 2,155 | 682 / 682 |

### 2c. Wave 3 -> wave 4 (2040 deltas vs base v6f; "twin" = the wave-3 funnel-released run)

| scenario | wave-3 run | gas TWh w3 / w4 | solar | wind | gas GW | CO2 Mt | cost bEUR | demand 2040 |
|---|---|---|---|---|---|---|---|---|
| s01 EV | s01_ev | +58 / +18 | +39 / +12 | +150 / +19 | +5 / +1 | +22 / +7 | +67 / +15 | +245 / +49 |
| s03 compute | s03_compute | +363 / +363 | +124 / +124 | +205 / +205 | +21 / +21 | +141 / +141 | +81 / +81 | +694 / +694 |
| s05 brakes | s05_brakes | -461 / -651 | -72 / -135 | +2 / -3 | -210 / -235 | -154 / -222 | -201 / -305 | -518 / -783 |
| s06 Hormuz (fuel) | s06_hormuz | +3 / -1 | +1 / -0 | -3 / +0 | +0 / -0 | +1 / -1 | -16 / +64 | +0 / +0 |
| s07a LDES | s07_tech twin | -287 / -224 | +80 / +91 | +160 / +161 | -179 / -172 | -93 / -72 | -27 / -49 | +0 / +0 |
| s07b fusion/SMR | s07_tech twin | -287 / -238 | +80 / +27 | +160 / +132 | -179 / -146 | -93 / -74 | -27 / -10 | +0 / +0 |
| s08 Canada DC | s08_canada | +10 / +10 | +1 / +1 | -60 / -60 | +3 / +3 | +4 / +4 | -11 / -11 | -49 / -49 |
| s10 climate | s10_climate | +38 / +31 | +66 / +61 | +134 / +149 | -7 / +1 | +27 / +23 | +49 / +46 | +216 / +216 |
| s11 FEOC+tariffs | s11_feoc | +4 / +3 | -1 / -1 | -3 / -2 | +0 / +0 | +1 / +1 | +7 / +7 | +0 / +0 |
| s12 overbuild | s12_overbuild twin | -946 / -516 | -263 / -54 | -83 / +89 | -242 / -185 | -325 / -170 | -255 / -196 | -1294 / -476 |
| s13 reindustrial | s13_reindustrial | +84 / +144 | +45 / +76 | +34 / +58 | +12 / +19 | +30 / +52 | +51 / +97 | +163 / +279 |
| s14 decarb | s14_decarb twin | -643 / -643 | +206 / +206 | +278 / +278 | -180 / -180 | -488 / -488 | +264 / +264 | +0 / +0 |
| s15 affordability | - | - / +12 | - / -14 | - / -67 | - / +7 | - / +5 | - / -83 | - / -67 |
| s16 transmission | - | - / +8 | - / +6 | - / -11 | - / -28 | - / -2 | - / -70 | - / +0 |

Gas build timing (new CCGT+OCGT+steam, US, GW): base 95 in 2026-30 / 309 in 2031-40; s03 95 / 330; s13 95 / 328;
s12 91 / 135; s05 30 / 150; s14 95 / 96; s07a 95 / 143. Gas capacity change 2040 by type: s07a CCGT -74, OCGT -88,
engines -7; s07b CCGT -78, OCGT -61; s12 CCGT -116, OCGT -61; s14 CCGT -141, OCGT -68. Storage energy 2040 in s07a:
iron-air 5.9 TWh, Li-ion 2.1 TWh (base 1.1).

## 3. What the results say about the feedback

| Hub position | Model result (wave 4) | Verdict |
|---|---|---|
| #1 EVs immaterial to 2030 load (+16-21 TWh) | at that sizing: +49 TWh in 2040, +15 bEUR, +7 Mt, gas +18 TWh | confirmed, demote |
| #2 hydrogen: keep out of the base | dropped as a run; the wave-3 run (+399 TWh flat electrolysis, +56 bEUR, served 40 % by gas) is the "if 45V/offtake reignite" lens | agreed |
| #3 compute: contracted load, deliverability is the ceiling | s03 adds +694 TWh and the model cannot pull gas forward: every scenario builds exactly the turbine cap in 2026-30 (95 GW), the extra gas comes in 2031-40 (330 vs 309 GW) and the existing CCGTs run harder; +81 bEUR, 24 EUR/MWh | confirmed; the ceiling is the binding constraint in every run |
| #4 space = Gulf-Coast named account | folded into s13 as 2 GW SERC + 2 GW ERCOT point loads | agreed |
| #5 brakes High/Strong, "delay not destruction" | with the hub's own reading (2-yr delay, ERCOT/NY 3, credible tranche only) s05 is now the largest downside of the set: -783 TWh in 2040, gas -651 TWh / -235 GW, new gas 2026-30 30 GW instead of 95, -305 bEUR | confirmed and larger than the hub's "delay" wording suggests: a delay plus a credibility cut removes more load than the wave-3 haircut |
| #6 Hormuz live condition, capex freeze not observed | fuel channel only: +64 bEUR on the base and +55-65 on every scenario, 2040 mix untouched; it is a level, not a lens | agreed; apply as a column, not a scenario |
| #7 LDES erodes peakers first, fusion/SMR baseload later | s07a (LDES): gas -172 GW, of which OCGT -88 and CCGT -74, iron-air 54 GW / 5.9 TWh, -49 bEUR; s07b (fusion/SMR): gas -146 GW (CCGT -78, OCGT -61), -10 bEUR | partly: LDES hits peakers and mid-merit alike once the gas minimum is released; fusion/SMR displace CCGT more than OCGT |
| #8 Alberta = base input | unchanged (inside the CER gas path); Canada document still rights-protected | pending |
| #9 water = siting constraint | dropped as a run | agreed |
| #10 relocation lags, resilience capex | with 5 % relocation by 2040 the case is cooling + coastal costs: +216 TWh, +46 bEUR, wind +149, CO2 +23 | agreed |
| #11 FEOC = share shift, tariffs = cost | +7 bEUR with the tariff add-on; no share-shift representation possible | agreed, immaterial for the system |
| #12 overbuild: speculative tranche only, timing risk 2028-31 | -476 TWh in 2040 (was -1,294), -196 bEUR; the 2026-30 gas build is untouched (91 vs 95 GW), the hit is 2031-40 (135 vs 309 GW new gas) | confirmed: order-book risk is post-2030, not 2028-31 |
| #13 reindustrialization toward the base | at 30 GW + point loads: +279 TWh, +97 bEUR (36 EUR/MWh), 52 % served by gas, gas +19 GW | confirmed as the most bankable load; whether it enters the base is a FEL26 decision |
| #14 CCUS-on-gas + nuclear | s14 with the funnel released: CO2 682 Mt (-488), CCS at the 40 GW cap (329 TWh), nuclear +254 TWh, resource cost +106 bEUR; new unabated gas 2031-40 = 96 GW instead of 309 | the policy case stops paying for gas it does not need; CCS fills the cap |
| A #15 affordability / cost allocation | ramp delay + limited socialised wires: -67 TWh, -83 bEUR, CO2 +5 Mt; BYOG is an ownership shift (metric only) | representable in two of three legs; mild |
| B supply ceiling | the turbine caps bind in every scenario 2026-30 - identical gas additions across the set | confirmed; it is the model's main structural constraint |
| E nuclear wave into the base | not done (base frozen); carried inside s14 | deferred |
| F transmission supercycle | -70 bEUR, gas -28 GW, curtailment -14 TWh, CO2 flat | wires beat peakers, as in v6 |
| G flexible loads | no lever: the investment runs carry no active firm-capacity constraint; the diagnostic pair (section 4) shows the constraint cannot be switched on as parameterised | deferred to the next baseline |

## 4. Firm-capacity diagnostic

Finding: every NA investment run (v6 freeze included) passes `set_peaking_slack = 0`, which makes the peaking constraints
vacuous, and the reserve-margin switch is off; adequacy rests on the 49-hour energy balance alone. Two diagnostic runs
switch the constraint on for the base:

| run | INF slack (TWh) | objective (bEUR) | of which slack capex | 2040 GW gas / nuclear / wind / storage | slack "capacity" bought (GW, max over years) |
|---|---|---|---|---|---|
| base v6f (peaking off) | 4.4 | 2,677 | 61 (ERCOT 2025-26 base-year gap) | 844 / 148 / 441 / 305 | ERCOT 17 |
| peaking on, slack 1.0 | 5.6 | 5,059 | 1,182 | 955 / 165 / 531 / 462 | PJM 74, SERC 56, Canada 26, SPP 21, ERCOT 21, NY 6, NE 5 |
| peaking on, 10 % of DC peak curtailable (0.975) | 5.6 | 4,752 | 1,030 | 936 / 164 / 503 / 451 | PJM 68, SERC 51, Canada 23, SPP 19, ERCOT 20, NY 5, NE 5 |

With the constraint on, the frozen regional build limits cannot deliver the required firm capacity; the model buys the
999 MEUR/GW penalty technology as "capacity" (1.2 trillion EUR of it) and expensive firm options elsewhere (nuclear
+14 GW, EGS R3 +22 GW, offshore +26 GW, 88 GW of redox storage). The machinery as parameterised (peak from the hourly
profile, variable RES credited at 0.5 x CF, storage at full power, trade credited) is not usable on the v6 data without
re-parameterising the near-term caps and the capacity credits. Until then: gas GW in the funnel-released cases is a
lower bound, and no scenario result should be read as adequacy-constrained.

## 5. For the export

- `scenario_mapping.csv` (21 runs): base, 14 main runs (labels `_v4`; s03 `_v4` and s08 `_v3` are the unchanged wave-3
  runs; s06 `_v5`; s14 `_v6`; s07a/s07b/s15/s16 first versions), the four Hormuz variants (`..._hormuz_49_2015_v6`), and
  the two peaking diagnostics (keep them out of scenario comparisons).
- Storage: `storage_capacity_wave4.csv` (D_* power GW, S_* energy GWh per scenario, region, year).
- s06 uses the base RegularParameters with the Hormuz fuel workbook; its only difference to the base is the gas price.
- `P_PV_Rooftop_Commercial` is all US distributed PV (capped at 7-10 GW/yr since wave 3); EGS row includes conventional
  geothermal; `P_Gas_Steam` additions after 2037 are New York only.
- Emissions: sum `output_emission` with Type in ('Emissions', 'ExogenousEmissions').

Documents: `RESULTS_wave4_2026-10-02.md` (results), `FEEDBACK_PLAN_wave4_2026-10-02.md` (item-by-item plan and
decisions), `NA_scenario_plan_2026-09-18_v4.xlsx` sheet `Wave4_changes` (definitions). Open: the Canada feedback
document (rights-protected, not yet readable).
