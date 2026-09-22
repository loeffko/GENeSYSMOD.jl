# SE scenario set - wave 1 results (2026-09-22)

14 scenarios, one variant each (plan v3, `../NA_scenario_plan_2026-09-18_v3.xlsx`), all on the v6 freeze.
Reference: `fel2026_base_49_2015_v6d` (= v6c physically; same CO2 accounting as the scenario runs).
All 14 runs OPTIMAL at 49-hour resolution; infeasibility slack 2.4-6.1 TWh vs 4.5 in the base (INF gate passed).
Table: `Scripts/analyze_s14.py fel2026_base_49_2015_v6d` -> `Results/s14_summary.csv`. Deltas below are 2040 vs base.

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) |
|---|---|---|---|---|---|---|---|---|---|---|
| base | v6d | 8,242 TWh | 2,771 | 1,852 | 1,349 | 1,150 | 851 | 305 | 1,162 Mt | 2,668 |
| 1 | EV comeback (s01_ev) | +245 | +72 | +50 | +124 | 0 | +6 | 0 | +31 | +64 |
| 2 | H2 comeback (s02_h2) | +399 | +188 | +86 | +124 | 0 | +13 | 0 | +66 | +55 |
| 3 | Age of compute (s03_compute) | +754 | +355 | +194 | +205 | 0 | +24 | 0 | +132 | +138 |
| 4 | Space race, terrestrial (s04_space) | +155 | +83 | +35 | +37 | 0 | +9 | 0 | +30 | +14 |
| 5 | Political brakes (s05_brakes) | -518 | -492 | -66 | +28 | 0 | -215 | 0 | -163 | -210 |
| 6 | Hormuz 6C (s06_hormuz) | 0 (2026-32 only) | +27 | -23 | -5 | 0 | 0 | -2 | +9 | -35 |
| 7 | Tech breakthrough (s07_tech) | 0 | -101 | +35 | +11 | 0 (+73 fusion) | -24 | +31 (+36 iron-air) | -38 | -1 |
| 8 | Canada DC, pipeline-consistent (s08_canada) | -49 | -3 | -3 | -43 | 0 | +3 | 0 | -2 | -10 |
| 9 | Water boom (s09_water) | +36 | +8 | +9 | +19 | 0 | +1 | 0 | +3 | +4 |
| 10 | Climate reshuffle (s10_climate) | +216 | -35 | +129 | +143 | -27 | -10 | +5 | -6 | +44 |
| 11 | FEOC (s11_feoc) | 0 | +5 | -4 | -2 | 0 | 0 | 0 | +2 | +8 |
| 12 | AI overbuild (s12_overbuild) | -1,294 | -741 | -333 | -222 | 0 | -23 | -5 | -267 | -201 |
| 13 | Reindustrialization (s13_reindustrial) | +163 | +84 | +42 | +36 | 0 | +12 | 0 | +30 | +50 |
| 14 | Decarbonization (s14_decarb, v3) | 0 | -690 | +268 | +305 | +254 | +16 (+40 CCS) | +2 | -524 | +264 (incl. CO2 payments) |

Units: TWh unless stated; storage = D_ power capacity; cost = total discounted system cost delta (the
scenario objective includes any extra demand it serves, so demand-adding scenarios are not "cost of policy").

## Reading by scenario

1. **EV** - +245 TWh (AEO2026 policy path) is met two-thirds by wind and solar, one-third by gas; gas fleet +6 GW.
2. **Hydrogen** - 413 TWh of flat electrolysis load is served mostly by gas (+188 TWh) because the load is inflexible; a
   flexible-electrolyser formulation (2D) would shift it to renewables.
3. **Compute** - +754 TWh: gas +355 TWh (+24 GW), solar +194, wind +205; CO2 +132 Mt; cost +138 bEUR.
4. **Space** - +155 TWh of e-propellant/manufacturing load: gas +83, small RES; cost +14 bEUR.
5. **Political brakes** - the DC haircut removes 518 TWh; without forced gas builds the gas fleet ends 215 GW smaller
   (233 vs 448 GW of new gas 2026-40) and CO2 -163 Mt; system cost -210 bEUR.
6. **Hormuz** - almost entirely transient: recession demand 2026-30 outweighs the capex/WACC uplift (-35 bEUR); by 2040 the
   mix is back to base (gas +27, solar -23).
7. **Tech breakthrough** - fusion 9.5 GW / 73 TWh (forced ramp), iron-air 36 GW by 2040 (build cap nearly binding),
   Li-ion +31 GW; gas -101 TWh and -24 GW; SMR stays at the base 2.8 GW even at 3,330 EUR/kW (not competitive vs
   PV + storage at 5 %); cost neutral.
8. **Canada DC** - below the FEL base by construction (user rule): -49 TWh, wind -43 TWh; no Alberta gas build beyond the
   forced minimum (the base already forces 15 GW of Canadian CCGT by 2040).
9. **Water** - +36 TWh, immaterial.
10. **Climate reshuffle** - +216 TWh (cooling + rebuild) and the north-shift: wind +143, solar +129, gas -35; coastal
    availability cut lowers nuclear -27 TWh; cost +44 bEUR.
11. **FEOC** - cost premium is transient; 2040 mix unchanged, +8 bEUR.
12. **AI overbuild** - -1,294 TWh: gas -741, solar -333, wind -222; -201 bEUR.
13. **Reindustrialization** - +163 TWh flat load: gas +84, solar +42, wind +36; +50 bEUR.
14. **Decarbonization (v3 = planned case)** - CO2 price 30/60/90 USD/t + restored ITC + 45Q + announced nuclear/uprates
    + state caps: power CO2 1,162 -> 638 Mt by 2040 (-45 %; 2030 1,172 vs the base's artefact-affected 718, see below),
    gas generation -690 TWh with the fleet roughly unchanged (CCGT 917 vs 1,580 TWh), coal to ~0, CCPP+CCUS at the
    40 GW cap (295 TWh), nuclear +254 TWh (SMR 22 GW, uprates), EGS 22 GW, solar +268, wind +305 TWh. Regional caps:
    PJM 144 vs cap 147 Mt (binding), NY 9 vs 12, CA 44 vs 55, NE 3 vs 20. The +264 bEUR objective delta includes
    the CO2 payments themselves (a transfer), so it overstates the resource cost. v2 (CCS unconstrained) is the
    sensitivity in the findings section.

## Model findings from this wave (act on before v7)

- **Biogas co-firing mode artifact (all v6 runs).** The NA gas plants keep the EU mode 2 (Gas_Bio, folded from
  R_Biogas at ~5.8 MEUR/PJ, no CO2, no resource limit in the power-only data). In the v6 base and every scenario
  the entire gas fleet runs in that mode in 2030 (the Henry-Hub peak year, 4.8 MEUR/PJ): 1,710 TWh of "biogas"
  generation, so the published v6 2030 power CO2 (762 Mt) is understated by roughly 600 Mt. Capacities and other
  years are unaffected. Under a CO2 price the mode absorbs all gas generation in every year (first s14 run: 26 Mt
  CO2 in 2040 with 1,212 TWh of CCGT output). s14 v2 disables mode 2 for the gas plants; the base should get the
  same fix (or a biogas resource limit) in v7.
- The CO2-price / regional-cap machinery works on NA data (E1-E8, penalty booked in the cost tables) once the
  penalty tag covers the gas plants (base tag file only tagged coal/oil/CCS).
- **CCS caps cannot be set per region in data.** With `switch_ccs = 1` the bounds code lifts every CCS
  TotalAnnualMaxCapacity above the 0.001 GW forbid-marker to 999999 (blanket enable). The first s14 runs therefore
  built 304 GW of gas CCS by 2040 instead of the planned 40 GW; s14 v3 uses a `GasCCS`/USA group cap
  (Par_GroupTotalAnnualMaxCapacity), which the blanket does not touch. s14 v2 is kept as the "unconstrained CCS"
  sensitivity: at 90 USD/t with 45Q the model wants ~300 GW of CCPP+CCUS (2,134 TWh in 2040), coal to zero,
  nuclear +104 TWh, SMR 22 GW, EGS 20 GW; power CO2 1,162 -> 237 Mt; system cost +206 bEUR.
- The probes caught three overlay/funnel clashes (offshore and onshore RES max below their pipeline minima in
  s05, SMR max below the committed Darlington minimum in s07, FEOC build cap below the base Li-ion minimum path
  in s11) - all fixed in the generator with floors against the base rows.
- The new demand fuel (`Power_LargeLoads`, X_Convert_Power mode 7, flat profile), P_Fusion and D_IronAir/S_IronAir
  work as plain data additions; no code change was needed.

## Reproduction

- Data: data repo `NA_inputs/build_14_scenarios.py --apply --repo C:/v6wt` (+ `--apply` in HEAD), conversion
  `C:/v6wt/Conversion Script/_s14_convert.py`, workbooks `InputData/RegularParameters_NorthAmerica_sNN_<name>.xlsx`
  (+ `RegularParameters_NorthAmerica_allFuels_v6_s06.xlsx`).
- Runs: `_s14/run_sNN.jl` (49-hour), `_s14/probe_sNN.jl` (1924 probes), chains `_s14/run_all.sh` / `probe_all.sh`.
- Labels `fel2026_sNN_<name>_49_2015_v6` (s14: `_v3` = planned case with the biogas mode disabled and the 40 GW CCS
  group cap; `_v2` = CCS unconstrained; v1 = broken by the biogas mode); input dumps are in the DB (`input_*`).
- `output_emission` mixes physical emissions (Type `Emissions` / `ExogenousEmissions`) with the regional cap shadow
  prices (`Regional Endogenous CO2 Price`); filter on Type when summing.
