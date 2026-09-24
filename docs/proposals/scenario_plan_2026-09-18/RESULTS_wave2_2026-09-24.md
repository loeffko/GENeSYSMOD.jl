# SE scenario set - wave 2 results (2026-09-24)

Wave 2 = the 14 scenarios and the base rerun on **one identical setup**: the v6 freeze with the biogas co-firing
mode disabled in the base data (the s14 v3 fix, review item 1), plus the four definition fixes from the wave-1 review
(s03 crypto growth-only, s05 gas-engines window cap, s06 uplift from 2028, s14 ITC phase-in; see
`../scenario_results/REVIEW_RESPONSE_2026-09-23.md` and the `Wave2_changes` sheet of
`../NA_scenario_plan_2026-09-18_v4.xlsx`).
Reference: `fel2026_base_49_2015_v6e`. Labels `fel2026_sNN_<name>_49_2015_v6_v2` (s14 `_v4`; s03 and s06 `_v3`, see run notes).
All runs at 49-hour resolution; infeasibility slack 2.4-5.1 TWh vs 4.5 in the base (INF gate passed).
Table: `Scripts/analyze_s14.py fel2026_base_49_2015_v6e 2` -> `s14_summary_wave2.csv`. Deltas are 2040 vs base.

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CF solar/wind 2040 | curtailed 2040 | cost per MWh of extra demand | CO2 payments (bEUR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | v6e | 8,242 TWh | 2,770 | 1,853 | 1,349 | 1,150 | 851 | 305 | 1,161 Mt | 2,675 | 0.20/0.36 | 189 TWh | - | 0 |
| 1 | EV comeback (s01_ev, v2) | +245 | +73 | +49 | +124 | 0 | +6 | 0 | +31 | +64 | 0.20/0.35 | +15 | 27.6 EUR | 0 |
| 2 | H2 comeback (s02_h2, v2) | +399 | +189 | +86 | +123 | 0 | +13 | 0 | +67 | +55 | 0.20/0.36 | +4 | 22.9 EUR | 0 |
| 3 | Age of compute (s03_compute, v3) | +694 | +327 | +174 | +193 | 0 | +21 | 0 | +122 | +77 | 0.20/0.35 | +12 | 22.4 EUR | 0 |
| 4 | Space race, terrestrial (s04_space, v2) | +155 | +83 | +34 | +37 | 0 | +9 | 0 | +30 | +15 | 0.20/0.36 | 0 | 22.1 EUR | 0 |
| 5 | Political brakes (s05_brakes, v2) | -518 | -491 | -67 | +28 | 0 | -215 | -0 | -163 | -210 | 0.19/0.35 | +36 | 48.2 EUR | 0 |
| 6 | Hormuz 6C (s06_hormuz, v3) | 0 | +20 | -21 | 0 | 0 | 0 | -2 | +7 | -18 | 0.20/0.36 | -5 | 10.9 EUR | 0 |
| 7 | Tech breakthrough (s07_tech, v2) | 0 | -101 | +35 | +10 | 0 (+73 fusion) | -24 | +31 (+36 iron-air) | -40 | -1 | 0.20/0.36 | -15 | - | 0 |
| 8 | Canada DC, pipeline-consistent (s08_canada, v2) | -49 | -2 | -4 | -43 | 0 | +3 | 0 | -2 | -10 | 0.20/0.36 | -1 | 20.0 EUR | 0 |
| 9 | Water boom (s09_water, v2) | +36 | +8 | +9 | +19 | 0 | +1 | 0 | +3 | +4 | 0.20/0.36 | +2 | 21.0 EUR | 0 |
| 10 | Climate reshuffle (s10_climate, v2) | +216 | -35 | +128 | +143 | -27 | -10 | +5 | -6 | +44 | 0.19/0.35 | +45 | 30.6 EUR | 0 |
| 11 | FEOC (s11_feoc, v2) | 0 | +4 | -4 | -2 | 0 | 0 | 0 | +2 | +8 | 0.20/0.36 | -1 | - | 0 |
| 12 | AI overbuild (s12_overbuild, v2) | -1,294 | -741 | -332 | -222 | 0 | -23 | -5 | -267 | -202 | 0.20/0.36 | -11 | 22.8 EUR | 0 |
| 13 | Reindustrialization (s13_reindustrial, v2) | +163 | +85 | +41 | +36 | 0 | +12 | 0 | +30 | +50 | 0.20/0.36 | +2 | 34.5 EUR | 0 |
| 14 | Decarbonization (s14_decarb, v4) | 0 | -690 | +269 | +304 | +254 | +16 (+40 CCS) | +2 | -524 | +271 | 0.18/0.31 | +373 | - | 322 |

Units: TWh unless stated; storage = D_ power capacity; cost = total discounted system cost delta 2025-40. The
objective of a demand-adding scenario includes serving the extra demand, so "cost per MWh of extra demand" (delta
cost / delta demand 2025-40, undiscounted TWh) is the comparable number; for s14 the delta includes the CO2 payments
(a transfer, 322 bEUR discounted) and the ITC capex reduction (a transfer the other way), so it is not a resource cost.
CF = implied fleet capacity factor 2040 (generation / capacity); curtailed = `CurtailedEnergyAnnual`, Power, 2040.

## What changed against wave 1

- **Nothing in the 2040 picture for the ten unchanged scenarios.** With the biogas artefact removed from base and
  scenario alike, every 2040 delta (generation, capacity, CO2, cost) of s01, s02, s04, s05, s07-s13 reproduces the
  wave-1 value to within +-2 TWh / +-2 Mt / +-1 bEUR. The wave-1 tables stay valid for 2040.
- **2030 CO2 is now right everywhere.** Base 1,317 Mt (was 718 with the artefact); every scenario 1,235-1,347 Mt
  (was 676-769). The base's 2030 gas generation is unchanged (1,821 TWh), it just burns natural gas in mode 1.
- **s06 Hormuz is the one scenario the artefact had muted.** In wave 1 the whole gas fleet ran in the free "biogas"
  mode from 2026 on (1,371 TWh in 2026, 1,570 in 2027 ...), so the Henry-Hub shock never hit the objective and the
  scenario looked like a net saving (-35 bEUR). With the mode gone the shock bites in 2026-27 (+27 bEUR: the fleet burns
  natural gas at the shock price instead of free "biogas") and again in 2032-33 (+15, catch-up builds after the uplift
  window); the recession demand 2028-31 saves 62 bEUR. Net -18 bEUR (wave 1: -35). The 2040 mix is back to base
  (gas +20, solar -21, CO2 +7 Mt).
- **s03** is smaller by construction (crypto no longer double-counted: +694 instead of +754 TWh in 2040):
  gas +327 (was +355), solar +174, wind +193, CO2 +122 Mt, cost +77 bEUR (was +138; 22.4 EUR/MWh).
- **s05**: the new engines cap holds - gas additions 2027-31 are at most 10 GW/yr of plants plus 1 GW/yr of
  engines (2028: 9.9 + 1.0; 2031: 10.0 + 0); wave-1 2028 had 11.5 GW through engines outside the subset. 2040
  unchanged (-215 GW gas, -163 Mt, -210 bEUR).
- **s14**: the ITC phase-in removes the 2029 spike - new solar 2029/30/31 = 102/115/121 GW (v3: 130/120/107;
  base: 86/76/79). The end state is identical to v3 (CO2 637 Mt, CCS at the 40 GW cap, SMR 22 GW, coal ~0, nuclear
  +254 TWh, EGS 24 GW). Regional caps 2040: PJM 144 vs 147 Mt and New York at its cap (both carry a shadow price),
  California 37 vs 55, New England 6 vs 20. Curtailment 562 TWh (base 189), solar CF 0.18 / wind 0.31.

## Reading by scenario (wave 2)

1. **EV** - +245 TWh (AEO2026 policy path): wind +124, gas +73, solar +49; +6 GW gas; +31 Mt; 27.6 EUR/MWh.
2. **Hydrogen** - 413 TWh of flat electrolysis load: gas +189, wind +123, solar +86; +67 Mt; 22.9 EUR/MWh
   (inflexible load -> gas; a flexible-electrolyser variant would shift it to renewables).
3. **Compute** - +694 TWh (second-wave adders above the FEL base, crypto as growth only): gas +327 TWh (+21 GW),
   solar +174, wind +193; +122 Mt; +77 bEUR (22.4 EUR/MWh).
4. **Space** - +155 TWh: gas +83, solar +34, wind +37; +15 bEUR (22.1 EUR/MWh).
5. **Political brakes** - -518 TWh and the gas minima removed: gas -491 TWh / -215 GW, CO2 -163 Mt, -210 bEUR
   (48 EUR per MWh of avoided demand, because the forced gas build disappears with it).
6. **Hormuz** - transient: shock cost 2026-27 and 2032-33 (+42 bEUR) against recession savings 2028-31 (-62);
   net -18 bEUR; 2040 mix back to base (gas +20, solar -21, CO2 +7 Mt).
7. **Tech breakthrough** - fusion 73 TWh, iron-air 36 GW, Li-ion +31 GW; gas -101 TWh / -24 GW; CO2 -40 Mt;
   cost neutral (-1 bEUR); SMR stays at the base 2.8 GW.
8. **Canada DC** - -49 TWh (pipeline-consistent, below the FEL base by construction): wind -43 TWh; -10 bEUR.
9. **Water** - +36 TWh, immaterial (+4 bEUR).
10. **Climate reshuffle** - +216 TWh and the north-shift: wind +143, solar +128, gas -35, nuclear -27; +44 bEUR.
11. **FEOC** - transient cost premium, 2040 mix unchanged, +8 bEUR.
12. **AI overbuild** - -1,294 TWh: gas -741, solar -332, wind -222; CO2 -267 Mt; -202 bEUR.
13. **Reindustrialization** - +163 TWh flat load: gas +85, solar +41, wind +36; +50 bEUR (34.5 EUR/MWh).
14. **Decarbonization** - CO2 price 30/60/90 USD/t + ITC phase-in + 45Q + announced nuclear + state caps: power CO2
    1,161 -> 637 Mt (-45 %; 2030 1,198 vs base 1,317), gas -690 TWh with the fleet roughly unchanged, CCPP+CCUS at
    the 40 GW cap (294 TWh), coal ~0, nuclear +254 TWh (SMR 22 GW), EGS +12 GW, solar +269, wind +304 TWh;
    objective +271 bEUR of which 322 bEUR are CO2 payments.

## Base v6e vs the previous base (v6d)

Same v6 data except the biogas co-firing mode (mode 2, Gas_Bio) of every gas plant, which is now disabled in
the base data (OutputActivityRatio = 0; data repo commit 7269329). Effect on the base run:

| | v6d | v6e |
|---|---|---|
| objective (bEUR, discounted 2025-40) | 2,668.3 | 2,675.3 (+0.26 %) |
| power CO2 2025 / 2030 / 2035 / 2040 (Mt) | 1,557 / 718 / 1,238 / 1,162 | 1,557 / 1,317 / 1,238 / 1,161 |
| gas generation 2030 in mode 2 "biogas" (TWh) | 1,710 | 0 |
| gas generation 2030 total (TWh) | 1,824 | 1,821 |
| capacities, generation mix 2025-40, trade | reference | identical (largest deviation 1.4 % in a small group) |

Everything physical is unchanged; only the 2030 CO2 artefact (-600 Mt) disappears and the objective rises by the
fuel-cost difference of the 2030 Henry-Hub peak year. `Scripts/compare_base_regression.py fel2026_base_49_2015_v6e
fel2026_base_49_2015_v6d` reproduces the comparison.

## Run notes

- **Solver status.** all 15 reported runs terminated `OPTIMAL` (Gurobi barrier, crossover off). The superseded s03 `_v2`
  run (stale rows) had stalled in the barrier (`Sub-optimal termination`, relative gap 2e-7, `LOCALLY_SOLVED`); the
  clean `_v3` run solves to optimality.
- **Label incident (s02).** The wave-2 driver of s02 carried the wave-1 label, so the rerun purged the wave-1
  scenario `fel2026_s02_h2_49_2015_v6` from the database and wrote the new results under that name. The rows were
  renamed in place to `..._v2`; the wave-1 s02 numbers survive only in `s14_summary_wave1.csv` /
  `RESULTS_wave1_2026-09-22.md`. All other wave-1 runs are still in the database.
- **Stale overlay rows (s03, s06).** The overlay writer of the scenario generator merges into an existing
  overlay file (row-upsert) and keeps rows whose keys the new definition no longer writes. The first wave-2 runs of
  s03 (`_v2`) and s06 (`_v2`) therefore still carried wave-1 rows: 60 TWh of crypto load in 2025-26 (s03) and the
  1.35 capex uplift in 2026-27 (s06). Both overlays were regenerated from an empty folder (the regenerated files are
  pure subsets of the old ones), the two workbooks reconverted and both scenarios rerun as `_v3`; the table above
  shows the `_v3` runs. s05 (overlay deleted before regeneration) and s14 (ITC path verified in the input dump:
  x1.0/0.9/0.8/0.7 for 2028-31) were clean; the other ten definitions did not change between the waves.
- **INF gate.** Infeasibility-technology generation 2.4-5.1 TWh per run (base 4.5); wave 1: 2.4-6.1.

## Reproduction

- Data: data repo `NA_inputs/build_14_scenarios.py --apply --repo C:/v6wt` (wave-2 definitions), conversion
  `C:/v6wt/Conversion Script/_s14_convert.py`; base workbook `InputData/RegularParameters_NorthAmerica_v6e.xlsx`,
  scenario workbooks `InputData/RegularParameters_NorthAmerica_sNN_<name>.xlsx` (+ `..._allFuels_v6_s06.xlsx`).
- Runs: `_s14/run_base_v6e.jl`, `_s14/run_sNN_v2.jl`, `_s14/run_s14_v4.jl`; chain `_s14/run_all_v2.sh`
  (log `Results/_s14_runs_w2.log`, per-run logs `Results/_s14_run_<k>_v2.log`).
- Table: `python Scripts/analyze_s14.py fel2026_base_49_2015_v6e 2` -> `Results/s14_summary.csv`;
  markdown via `python Scripts/s14_results_md.py`. Copy of the csv: `s14_summary_wave2.csv`.
- `output_emission` mixes physical emissions (Type `Emissions` / `ExogenousEmissions`) with the regional cap shadow
  prices; filter on Type when summing.
