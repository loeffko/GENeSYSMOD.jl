# SE scenario set - wave 4 results (2026-10-02)

Wave 4 = the hub's market-intelligence feedback (`../scenario_results/Input Scenarios (v3) 2.docx`; plan and decisions in
`FEEDBACK_PLAN_wave4_2026-10-02.md`) applied to the set, on the unchanged base v6f (July freeze): six scenarios re-sized or
re-defined, s07 split, three new cases (affordability, transmission supercycle, flexible loads as a diagnostic), the gas
funnel removed inside the four cases where forced gas contradicts the story, Hormuz as a fuel-price channel on s06 and
as a variant of s03/s05/s12/s14, and s02/s04/s09 dropped as runs. Canada is ignored for now (US portion; the Canada
document is rights-protected). 18 runs, all `OPTIMAL`, infeasibility slack 2.1-5.7 TWh (base 4.4).
Tables: `Scripts/analyze_s14.py fel2026_base_49_2015_v6f 4` -> `s14_summary_wave4.csv`. Deltas are 2040 vs base v6f.

## Main set

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CF solar/wind 2040 | curtailed 2040 | resource cost net of transfers (bEUR) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| base | v6f | 8,242 TWh | 2,798 | 1,788 | 1,384 | 1,150 | 844 | 305 | 1,171 Mt | 2,677 | 0.20/0.36 | 175 TWh | - |
| 1 | EV comeback (s01_ev, v4) | +49 | +18 | +12 | +19 | 0 | +1 | 0 | +7 | +15 | 0.20/0.36 | +4 | +15 |
| 3 | Age of compute (s03_compute, v4) | +694 | +363 | +124 | +205 | 0 | +21 | +1 | +141 | +81 | 0.20/0.35 | +6 | +81 |
| 5 | Political brakes (s05_brakes, v4) | -783 | -651 | -135 | -3 | 0 | -235 | 0 | -222 | -305 | 0.20/0.35 | +27 | -305 |

TWh unless stated; storage = D_ power capacity; cost = discounted system cost delta 2025-40; cost per MWh = delta
cost / delta demand 2025-40; resource cost backs out CO2 payments and capex / variable-cost reductions vs base (relevant
for s14). "Funnel released" cases (s07a, s07b, s12, s14) have no forced gas builds after 2030.

## Hormuz as a cross-scenario fuel sensitivity

Henry-Hub uplift 2026-30 (the s06 allFuels workbook) on the base and on four scenarios; everything else as the parent.

| scenario | parent cost (bEUR) | with Hormuz fuel | fuel-shock cost | gas 2040 TWh parent / Hormuz | CO2 2040 parent / Hormuz |
|---|---|---|---|---|---|
| base (= s06 v5) | 0 | +64 | +64 | 2,798 / 2,797 | 1,171 / 1,170 |
| s03 compute | +81 | +146 | +65 | 3,161 / 3,160 | 1,311 / 1,311 |
| s05 brakes | -305 | -250 | +56 | 2,147 / 2,148 | 949 / 949 |
| s12 overbuild | -196 | -136 | +60 | 2,282 / 2,282 | 1,000 / 1,000 |
| s14 decarb | +264 | +327 | +62 | 2,155 / 2,155 | 682 / 682 |

The fuel shock costs 55-65 bEUR discounted wherever it is applied, leaves the 2040 mix untouched and shifts nothing
between scenarios: it is a level, not a lens. The capex-freeze channel the hub rates as "risk to watch" is not modelled
(their observation: utility capex plans have risen, not frozen).

## Wave 3 -> wave 4: what the redefinitions changed (2040 deltas vs base v6f)

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

Reading:
- s01 EV at the hub's sizing is immaterial (+49 TWh, +15 bEUR); the wave-3 AEO path was ~4x larger.
- s05 "delay + credible tranche" is the harshest demand case of the set after s12: -783 TWh by 2040, gas -651 TWh /
  -235 GW, -305 bEUR.
- s12 at "speculative tranche only" is milder than wave 3 (-476 vs -1,294 TWh of 2040 load) but with the funnel released
  it still drops 185 GW of gas and 196 bEUR.
- s13 at 30 GW + point loads: +279 TWh, gas +144, solar +76, wind +58, +97 bEUR (36 EUR/MWh).
- s07a (LDES, funnel released): iron-air 54 GW, gas -224 TWh / -172 GW, -49 bEUR; s07b (fusion/SMR): fusion 73 TWh,
  gas -238 TWh / -146 GW, -10 bEUR. Both erode gas more than the bundled wave-3 twin because each is unconstrained by
  the other's capital.
- s15 affordability (ramp delay + grid_low wires): -67 TWh of 2040 load, -83 bEUR, wind -67 TWh, CO2 +5 Mt; the BYOG
  leg is an ownership shift (metric `byog_gw_equiv` in the csv: 40 % of the DC increment at 0.8 LF).
- s16 transmission supercycle: -70 bEUR, gas -28 GW, curtailment -14 TWh, CO2 flat - wires beat peakers, as in v6.
- s10 lighter relocation: within +-30 TWh of wave 3; s11 tariffs: +7 bEUR, immaterial.

## Flexible large loads (s17) - diagnostic, not a scenario

The investment model has no active firm-capacity requirement (next section), so a curtailable-load lever has nothing to
act on. The pair `fel2026_base_peaking_49_2015_v6f` (peaking constraint on, slack 1.0) and `..._flexdc` (slack 0.975 =
10 % of the data-center peak curtailable) therefore tests the constraint itself on the frozen data: see the adequacy
section. Outcome at 49-hour resolution:

| run | INF slack (TWh) | objective (bEUR) | of which slack capex | 2040 GW gas / nuclear / wind / storage | slack "capacity" bought (GW, max over years) |
|---|---|---|---|---|---|
| base v6f (peaking off) | 4.4 | 2,677 | 61 (ERCOT 2025-26 base-year gap) | 844 / 148 / 441 / 305 | ERCOT 17 |
| peaking on, slack 1.0 | 5.6 | 5,059 | 1,182 | 955 / 165 / 531 / 462 | PJM 74, SERC 56, Canada 26, SPP 21, ERCOT 21, NY 6, NE 5 |
| peaking on, 10 % of DC peak curtailable (0.975) | 5.6 | 4,752 | 1,030 | 936 / 164 / 503 / 451 | PJM 68, SERC 51, Canada 23, SPP 19, ERCOT 20, NY 5, NE 5 |

With the constraint on, the frozen regional build limits cannot deliver the required firm capacity: the model buys the
999 MEUR/GW penalty technology as "capacity" (1.2 trillion EUR of it) and expensive firm options elsewhere (nuclear +14
GW, EGS R3 +22 GW, offshore +26 GW, oil, coal, 88 GW of redox storage). The curtailable-load variant lowers the slack
bill by 150 bEUR but changes nothing structurally. Conclusion: the peaking machinery as parameterised (peak from the
hourly profile, RES credited at 0.5 x CF, storage at full power, trade credited) is not usable on the v6 data without
re-parameterising the near-term caps and the capacity credits; this is why it is switched off and it stays a v7
baseline item. s17 therefore has no scenario result.

## Definitions (what changed against wave 3)

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

Dropped as runs (hub assessment): s02 hydrogen (electrolytic H2 below the FEL flat case), s04 space (point loads
now inside s13), s09 water (immaterial; siting constraint). Their wave-3 results remain citable. Base v6f is the
July freeze and is not changed; the nuclear-wave and named-CCS asks are v7 baseline items.

## Adequacy finding (2026-10-02)

All NA investment runs, the v6 freeze included, pass `set_peaking_slack = 0`, which makes the peaking constraints
vacuous (`PeakingCapacity >= PeakingDemand x 0`); the reserve-margin switch is off. Adequacy rests on the 49-hour
energy balance alone. The two diagnostic runs switch the constraint on for the base. Treat gas GW in the
funnel-released cases as a lower bound until a firm-capacity rule is part of the baseline (v7).

## Reproduction

- Data: data repo `NA_inputs/build_14_scenarios.py --apply --repo C:/v6wt --only s01,s05,s06,s07a,s07b,s10,s11,s12,s13,s14,s15,s16`
  (commit 16c53bd; overlays regenerated from empty folders; Assumptions.txt entries; the hub document registered in
  `Overview_Sources.csv`); conversion `C:/v6wt/Conversion Script/_s14_convert.py s01 s05 s07a s07b s10 s11 s12 s13 s14 s15 s16`.
- Runs: `_s14/run_sNN_v4.jl` (s06 `_v5`, s14 `_v6`), `_s14/run_s07a.jl`, `run_s07b.jl`, `run_s15.jl`, `run_s16.jl`,
  `run_sNN_hormuz.jl`, `run_base_peaking.jl`, `run_base_peaking_flexdc.jl`; chain `_s14/run_all_v4.sh`
  (log `Results/_s14_runs_w4.log`); 1924-hour probe of the peaking-on base `_s14/probe_base_peaking.jl`.
- Tables: `python Scripts/analyze_s14.py fel2026_base_49_2015_v6f 4` -> `s14_summary_wave4.csv`; markdown via
  `Scripts/s14_results_md.py`; storage tables `Scripts/export_storage_tables.py`.
