# Canada scenario set - priority-1 results (2026-10-06)

Nine runs of the Canada scenario plan (`../CA_scenario_plan_2026-10-04.xlsx`, sheet "Run plan", priority 1), all on
the frozen base `fel2026_base_49_2015_v6f`, 49-hour-step investment runs, weather year 2015. Scenario 5 (northern and
remote power systems) is a side calculation, see below. All nine runs are OPTIMAL; the infeasibility-slack generation
equals the base (4.4 TWh, all of it in US pools, none in Canada). Run time about 20 minutes each; chain 22:53-01:56.

Tables: `python Scripts/analyze_canada.py md` (deltas against the base, Canada node); full KPI set in `ca_summary_p1.csv`.

## Headline

| run | scenario (central variant) | Canada 2040, change against the base | system cost 2025-40, bEUR discounted |
|---|---|---|---|
| c01a | S1 Unleash generation - grid mix (gas fleet kept at CER level, SMR, batteries) | gas +9.4 GW (+44 TWh), wind -20.9 GW, nuclear +1.8 GW (SMR), battery +2.1 GW; CO2 +15.5 Mt | +6.4 (Canada +8.0) |
| c02a | S2 Local content - scored preference (capex premium 5-8 % from 2028) | wind build shifted from 2032-35 to 2037-39; 2040 wind -2.5 GW, gas +9 TWh; CO2 +2.8 Mt | +2.0 |
| c03b | S3 Nuclear growth - Siemens Energy outlook (23.4 GW large + 4.2 GW SMR) | nuclear +11.7 GW (+82 TWh), wind -22 GW, solar -3.6 GW, exports +7 TWh; CO2 -2.7 Mt | +8.9 (Canada +9.4) |
| c04a | S4 Indigenous partnership as the norm (financing factor, paths earlier) | solar +5.3 GW, gas -4 TWh, exports +4 TWh; CO2 -1.5 Mt | +0.1 |
| c06b | S6 Data centres - named pipeline (177 TWh instead of 269) | demand -92 TWh, wind -25.4 GW, solar -3.6 GW, exports +10 TWh; CO2 -2.2 Mt | -14.6 |
| c07a | S7 Wind - procurement-paced ceiling (55.7 GW) with headwind cost | wind -31.5 GW (-94 TWh), gas +9.3 GW (+78 TWh), hydro +2.6 GW; CO2 +26.4 Mt (doubling) | +3.8 |
| c07b | S7 Wind - accelerated floor (45 / 70 / 87 GW), lower cost | wind +11.0 GW (+30 TWh), solar -7.9 GW, gas -15 TWh; CO2 -4.8 Mt | -1.2 |
| c08b | S8 Critical minerals - planning view (+21.7 TWh flat) | wind +6.6 GW (+18 TWh); exports -1 TWh; CO2 +0.5 Mt | +4.5 |
| c09a | S9 EU associate member - export projects (+65 TWh: hydrogen +36, industry +29) | wind +18.9 GW (+52 TWh), gas +4 TWh, exports -7 TWh; CO2 +1.3 Mt | +10.4 |

Reading across the set:

- **Wind is the swing technology of the Canada node.** Every scenario that adds or removes load, or forces another
  technology, is balanced by onshore wind (-31 to +19 GW in 2040); solar, hydro and gas move much less. The base wind
  path (31 / 62 / 87 GW) therefore sits above the corridor minimum in most years and below the ceiling - it is a
  genuine model choice, not a guardrail.
- **Gas only grows where it is forced or where wind is capped.** Forced gas (c01a) or a wind ceiling (c07a) lifts the
  new-CCGT fleet to 20-25 GW with capacity factors of 0.39-0.63 in 2040 (base 15 GW at 0.31) and raises Canadian power
  CO2 by 15-26 Mt. Additional load (c08b, c09a) is met with wind, not gas: new CCGT stays on its forced minimum.
- **US spill-over is small.** US gas generation changes by at most 5 TWh in 2040, US new gas capacity by at most 0.8 GW
  (c07a), US system cost by -2.2 to +2.7 bEUR, mostly through the Canada-US interconnectors (net exports move by -7 to
  +10 TWh, New York and MISO first).
- **Costs are modest**: +0.1 to +10.4 bEUR discounted (0.0-0.4 % of the North American system cost); the two cases
  below the base are the lower data-centre path (-14.6) and accelerated wind with the lower CanREA cost path (-1.2).
- **Flags from the plan hold**: c06b and c07a sit below the base by construction (sourced numbers used, base above
  the signals); c04a is close to the base, as announced.

## Results by year (Canada node)

Base in absolute numbers, scenarios as change against the base. CF = fleet capacity factor.

**2030**

| run | demand TWh | wind GW | solar GW | hydro GW | nuclear GW | gas GW | battery GW | wind TWh | solar TWh | nuclear TWh | gas TWh | net export TWh | CO2 Mt | new-CCGT CF | wind CF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base v6f | 624 | 31.0 | 14.4 | 91.3 | 12.9 | 30.6 | 4.1 | 86 | 21 | 88 | 98 | 96 | 41.9 | 0.68 | 0.32 |
| c01a | +0 | +0.0 | +0.0 | +0.0 | +0.3 | +3.6 | +0.4 | +0 | +0 | +2 | +2 | +4 | +1.1 | 0.46 | 0.32 |
| c02a | +0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | -0 | +0 | +0 | +0 | +0 | +0.0 | 0.68 | 0.32 |
| c03b | +0 | +0.0 | +0.0 | +0.0 | +0.6 | +0.0 | +0.0 | +0 | +0 | +5 | -3 | +1 | -1.0 | 0.61 | 0.32 |
| c04a | +0 | +0.0 | +0.5 | +0.6 | +0.0 | +0.0 | +0.0 | -0 | +1 | +0 | -2 | +1 | -0.8 | 0.63 | 0.32 |
| c06b | -24 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0 | +0 | +0 | -19 | +5 | -6.5 | 0.41 | 0.32 |
| c07a | +0 | -3.0 | +0.1 | +0.0 | +0.0 | +0.0 | +0.0 | -8 | +0 | +0 | +5 | -3 | +1.7 | 0.79 | 0.32 |
| c07b | +0 | +14.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +39 | +0 | +0 | -36 | +3 | -12.5 | 0.33 | 0.32 |
| c08b | +8 | +0.2 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +1 | +0 | +0 | +4 | -3 | +1.3 | 0.77 | 0.32 |
| c09a | +12 | +0.6 | +0.1 | +0.0 | +0.0 | +0.0 | +0.0 | +2 | +0 | +0 | +6 | -4 | +1.9 | 0.80 | 0.32 |

**2035**

| run | demand TWh | wind GW | solar GW | hydro GW | nuclear GW | gas GW | battery GW | wind TWh | solar TWh | nuclear TWh | gas TWh | net export TWh | CO2 Mt | new-CCGT CF | wind CF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base v6f | 768 | 62.2 | 30.4 | 97.4 | 15.3 | 28.9 | 5.2 | 175 | 44 | 105 | 70 | 77 | 28.5 | 0.37 | 0.32 |
| c01a | +0 | -8.9 | +0.0 | +0.0 | +1.2 | +4.5 | +1.3 | -25 | +0 | +9 | +19 | +3 | +6.8 | 0.39 | 0.32 |
| c02a | +0 | -16.0 | +0.5 | +0.0 | +0.0 | +0.0 | +0.0 | -44 | +1 | -0 | +38 | -5 | +13.2 | 0.70 | 0.32 |
| c03b | +0 | -3.1 | +0.0 | +0.0 | +2.1 | +0.0 | +0.0 | -8 | +0 | +15 | -5 | +2 | -1.7 | 0.35 | 0.32 |
| c04a | +0 | +0.8 | +4.9 | +0.2 | +0.3 | +0.0 | +0.0 | +4 | +7 | +2 | -9 | +4 | -3.3 | 0.33 | 0.32 |
| c06b | -57 | -14.3 | -0.3 | +0.0 | +0.0 | +0.0 | +0.0 | -40 | -0 | +0 | -11 | +6 | -3.7 | 0.32 | 0.32 |
| c07a | +0 | -18.7 | +1.6 | +0.0 | +0.0 | +0.0 | +0.0 | -54 | +2 | -0 | +43 | -8 | +14.9 | 0.76 | 0.32 |
| c07b | +0 | +9.7 | -0.1 | +0.0 | +0.0 | +0.0 | +0.0 | +27 | -0 | +0 | -22 | +5 | -7.3 | 0.27 | 0.32 |
| c08b | +20 | +3.4 | +0.5 | +0.0 | +0.0 | +0.0 | +0.0 | +9 | +1 | +0 | +8 | -2 | +2.7 | 0.42 | 0.32 |
| c09a | +45 | +3.8 | +0.8 | +0.0 | +0.0 | +0.0 | +0.0 | +10 | +1 | +0 | +29 | -4 | +10.0 | 0.60 | 0.32 |

**2040**

| run | demand TWh | wind GW | solar GW | hydro GW | nuclear GW | gas GW | battery GW | wind TWh | solar TWh | nuclear TWh | gas TWh | net export TWh | CO2 Mt | new-CCGT CF | wind CF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| base v6f | 899 | 87.2 | 61.9 | 97.9 | 15.9 | 27.2 | 8.4 | 254 | 90 | 109 | 58 | 66 | 23.8 | 0.31 | 0.33 |
| c01a | +0 | -20.9 | +0.0 | +0.0 | +1.8 | +9.4 | +2.1 | -58 | +0 | +13 | +44 | -1 | +15.5 | 0.39 | 0.34 |
| c02a | +0 | -2.5 | -1.5 | +0.0 | +0.0 | +0.0 | +0.0 | -7 | -2 | +0 | +9 | -1 | +2.8 | 0.36 | 0.33 |
| c03b | +0 | -22.0 | -3.6 | +0.0 | +11.7 | +0.0 | +0.0 | -61 | -5 | +82 | -9 | +7 | -2.7 | 0.27 | 0.34 |
| c04a | +0 | -1.1 | +5.3 | +0.0 | +0.0 | +0.0 | +0.0 | -0 | +8 | +0 | -4 | +4 | -1.5 | 0.29 | 0.34 |
| c06b | -92 | -25.4 | -3.6 | +0.0 | +0.0 | +0.0 | +0.0 | -70 | -5 | -0 | -7 | +10 | -2.2 | 0.28 | 0.34 |
| c07a | +0 | -31.5 | +1.6 | +2.6 | +0.0 | +9.3 | +0.0 | -94 | +2 | -0 | +78 | -7 | +26.4 | 0.63 | 0.33 |
| c07b | +0 | +11.0 | -7.9 | +0.0 | +0.0 | +0.0 | +0.0 | +30 | -10 | -0 | -15 | +5 | -4.8 | 0.24 | 0.33 |
| c08b | +22 | +6.6 | +0.5 | +0.0 | +0.0 | +0.0 | +0.0 | +18 | +1 | +0 | +1 | -1 | +0.5 | 0.33 | 0.33 |
| c09a | +65 | +18.9 | +0.8 | +0.0 | +0.0 | +0.0 | +0.0 | +52 | +1 | +0 | +4 | -7 | +1.3 | 0.34 | 0.33 |

**System cost and US spill-over** (discounted 2025-2040, bEUR; generation TWh, capacity GW)

| run | status | slack TWh | cost Canada | cost US pools | cost total | US gas generation 2040 | US new gas capacity 2026-40 | Canada curtailment 2040 TWh |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| base v6f | OPTIMAL | 4.4 | 220.3 | 2456.9 | 2677.2 | 2740 | 421.4 | 15.5 |
| c01a | OPTIMAL | 4.4 | +8.0 | -1.6 | +6.4 | -2 | -0.0 | -1.8 |
| c02a | OPTIMAL | 4.4 | +1.3 | +0.7 | +2.0 | -2 | -0.0 | -0.2 |
| c03b | OPTIMAL | 4.4 | +9.4 | -0.5 | +8.9 | -5 | +0.0 | -1.9 |
| c04a | OPTIMAL | 4.4 | +1.5 | -1.4 | +0.1 | +1 | +0.0 | -0.0 |
| c06b | OPTIMAL | 4.4 | -12.4 | -2.2 | -14.6 | -4 | +0.0 | -2.2 |
| c07a | OPTIMAL | 4.4 | +1.1 | +2.7 | +3.8 | -5 | +0.8 | -2.2 |
| c07b | OPTIMAL | 4.4 | +0.1 | -1.3 | -1.2 | +1 | +0.0 | +0.9 |
| c08b | OPTIMAL | 4.4 | +3.5 | +1.0 | +4.5 | -1 | -0.0 | +0.6 |
| c09a | OPTIMAL | 4.4 | +7.9 | +2.5 | +10.4 | -0 | -0.0 | +1.6 |

## Notes by scenario

**c01a - grid mix (S1).** The gas fleet is held at the CER Current Measures level (34.2 / 33.4 / 36.6 GW) by raising
the new-CCGT minimum to 8.6 / 14.5 / 24.5 GW (2030 / 2035 / 2040; in 2027-28 the base corridor ceiling binds, so the
path is held just under it), SMR 0.3 / 1.5 / 2.1 GW and batteries 4.5 / 6.5 / 10.5 GW. The forced CCGT runs at 0.39-0.46
and displaces 21 GW of wind by 2040 (-58 TWh); CO2 +15.5 Mt. Canada pays +8.0 bEUR, the US saves 1.6 bEUR through
cheaper imports. The "doubling" itself does not appear - the base already has 297 GW in 2040.

**c02a - local content (S2).** Capital cost +8 % (wind), +6 % (utility PV, batteries), +5 % (CCGT) from 2028 does not
change the 2040 fleet much (wind -2.5 GW) but shifts the wind build-out: 2032-2035 additions fall from 6.3-9.8 GW/yr
to 1.8-4.6 GW/yr and come back at 11-12 GW/yr in 2037-38. In between, gas covers the gap (2035: gas +38 TWh,
CO2 +13 Mt). Cost +2.0 bEUR. The core SE item - gas-turbine lead times and prices - is still not in the scenario
(no data).

**c03b - nuclear, SE outlook (S3).** Large reactors 23.4 GW and SMR 4.2 GW by 2040 (fleet 27.6 GW, +11.7 GW against
the base). The 82 TWh of extra nuclear replaces wind (-22 GW, -61 TWh), some solar and gas, and lifts exports by 7 TWh
(New York, MISO, WECC). Cost +8.9 bEUR at the model's 10,000 EUR/kW; CO2 -2.7 Mt only, because the base is already
hydro- and wind-dominated by 2040.

**c04a - Indigenous partnership (S4).** Capital-cost factors 0.971-0.982 (blended WACC 4.83 % against 5 %), wind and
PV ceiling one year earlier, hydro and nuclear paths two years earlier. The visible effect is +5 GW of solar (ceiling
earlier) and slightly less gas; total cost +0.1 bEUR (Canada +1.5 from the earlier hydro / nuclear builds, US -1.4).
As flagged in the plan, the tailwind variant is close to the base; the stretch 4C would show the range.

**c06b - data centres, named pipeline (S6).** Demand 47 / 121 / 177 TWh instead of 71 / 178 / 269: the whole gap is
taken out of wind (-25 GW) and a little solar; forced gas is unchanged, so the new CCGT fleet runs at 0.28 instead of
0.31 and exports rise by 10 TWh. Cost -14.6 bEUR. The existing run `fel2026_s08_canada_49_2015_v6_v3`
(41 / 130 / 220 TWh) sits between this run and the base.

**c07a - wind procurement-paced (S7, Mixed reading).** Onshore wind capped at the announced path (28 / 43.5 / 55.7 GW,
all classes together) with headwind cost x1.13. The model fills the gap with gas: new CCGT 20 GW and OCGT 9.4 GW in
2040 (base 15.1 / 5.2), new-CCGT capacity factor 0.63, gas generation +78 TWh, CO2 +26 Mt (50 Mt instead of 24); hydro
reservoir +2.6 GW on its ceiling; exports -7 TWh. Cost +3.8 bEUR. The only run with extra US gas capacity (+0.8 GW).

**c07b - wind accelerated (S7, Tailwind reading).** Floor 45 / 70 / 87 GW on the average class, cost x0.95-0.91. Wind
additions of 8.8 GW/yr in 2028-30 (base 1.9-4.0); 2040 wind reaches 98 GW because the model keeps adding the better
class on top of the forced average class. Gas -36 TWh in 2030, CO2 -12.5 Mt; solar -8 GW in 2040. Cost -1.2 bEUR: the
lower cost path pays for the earlier build.

**c08b - critical minerals (S8).** +7.5 / +19.7 / +21.7 TWh flat load, met almost entirely with wind (+6.6 GW in 2040)
and, in 2030-35, with gas at the margin (+4 / +8 TWh). Cost +4.5 bEUR (about 70 EUR/MWh of added demand, discounted).

**c09a - EU associate member (S9).** +65 TWh in 2040 (hydrogen +36 as flat electrolysis, industry +29): wind +18.9 GW,
gas +29 TWh in 2035 (CO2 +10 Mt) before the wind catches up, exports -7 TWh. Cost +10.4 bEUR. The flat electrolyser
load overstates the firm-capacity need, as noted in the plan.

## Scenario 5 - northern and remote power systems (side calculation)

The territories generate 1.7 TWh (0.3 % of the Canada node) and are isolated grids; a one-node model cannot
represent them, so the plan's variants A and B are reported as a side calculation (research note
`B_nuclear_north.md`, section S5; all values relative to 2025, own arithmetic marked there).

| lever | variant A - committed projects | variant B - corridors and mines |
|---|---|---|
| demand added, TWh (2030 / 2035 / 2040) | +0.2 / +0.5 / +0.9 | +0.2 / +1.5 / +2.5 |
| diesel generation displaced, TWh/yr | 0.0 / 0.5 / 0.8 | 0.03 / 0.85 / 1.2 |
| hydro added, GW | 0 / 0.02 / 0.09 (Iqaluit 15-30 MW, Taltson 60 MW, Atlin 8 MW) | 0.01 / 0.03 / 0.10 |
| microreactors, GW | 0 / 0.005 / 0.02 | 0.001 / 0.01 / 0.05 |
| share of Canada node demand 2040 | 0.1 % | 0.3 % |

Anchors: Yukon +90 GWh renewable winter energy needed by 2030 and +45 dependable MW by 2035 (Yukon Energy); Nunavut
diesel generation +5.7 %/yr 2018-2025 (383 GWh in 2025); Kivalliq Hydro-Fibre Link 150 MW (50 MW firm from Manitoba);
Taltson +60 MW by about 2036; Iqaluit hydro 2033; DND microreactor demonstration aim 2028-30. The stretch variant 5C
(+5 TWh, 0.3 GW of microreactors at 16,000 -> 10,000 EUR/kW) is runnable as `fel2026_c05c_north_49_2015_v6` if a
model number is wanted; against 899 TWh of demand it would not move national results.

## Implementation record

- Data: `NA_inputs/build_canada_scenarios.py` (data repo, branch se_northamerica, commits c9bbe7e, c03eefd, 8fbd6e9),
  built on the v6-freeze worktree (`--repo C:/v6wt --apply`), overlay folders `Par_X/NorthAmerica_cNN<v>_<name>/`
  copied unchanged to the HEAD checkout. Only Canada rows; the US side is identical to the base.
- Workbooks: `C:/v6wt/Conversion Script/_ca_convert.py` -> `InputData/RegularParameters_NorthAmerica_cNN<v>_<name>.xlsx`;
  c08b and c09a use their own filter files (fuel Power_LargeLoads, mode 7). Sheet-level diff against the base workbook
  shows only the intended parameters.
- Probes: 1924-resolution feasibility probes (`_s14/probe_ca.sh`) for all nine before the chain; c01a was infeasible
  because the rounded new-CCGT minimum exceeded the corridor ceiling by 0.1 MW in 2027-28 - fixed by holding the
  minimum 0.1 % under the ceiling.
- Runs: drivers `_s14/run_cNN<v>.jl`, chain `_s14/run_all_c1.sh` (serial, done-files), gate per run in
  `Results/_ca_gate.log`, labels `fel2026_cNN<v>_<name>_49_2015_v6`. Same switches as the base v6f run.
- Corridor edits inside the definitions (no separate released runs): c01a raises the new-CCGT, SMR (min = max) and
  battery minima; c03b takes the Canada rows of the existing `NorthAmerica_nuclear_announced` overlay; c04a shifts the
  wind / PV ceilings one year and the hydro / nuclear paths two years earlier; c07a lowers the wind minimum to the
  ceiling in 2030-2036 (base minimum carries the cancelled Newfoundland wind-hydrogen capacity); c07b lifts the wind
  ceiling to the floor +2 % in 2028-2030. Capital-cost factors are written as Canada rows for every year the World rows
  carry (c02a, c04a, c07a, c07b).
- Analysis: `Scripts/analyze_canada.py` (table, `md`, `gate <key>`); results also in `Results/ca_summary.csv`
  (copy `ca_summary_p1.csv` here). `scenario_results/scenario_mapping.csv` carries the nine new labels.

## Caveats

- One Canada node: Alberta gas, Quebec hydro and the hydro-rich provinces that ration data centres share one copper
  plate; dedicated (behind-the-meter) gas cannot be told apart from grid supply. Provincial statements in the notes are
  composition only.
- No active firm-capacity constraint in the NA investment runs (peaking constraint vacuous, reserve margin off):
  the wind-heavy answers of c08b, c09a and c07b rest on the 49-hour energy balance, not on an adequacy rule.
- The base is above several signals (297 GW of capacity, 269 TWh of data centres, 87 GW of wind in 2040); c06b and
  c07a are therefore lower-than-base cases by construction, as agreed in the plan.
- Capital costs are the model's overnight values (nuclear 10,000 EUR/kW flat); announced Canadian all-in budgets are
  higher (see plan, sheet Assumptions). Forced capacities move cost, not builds.

## Next

Stretch set (priority 2 in the run plan) after review: 1C firm doubling, 2C fortress Canada, 3A public schedules
(cross-check), 3C tripling by 2040, 4C consent failure, 6C full queue with 28 GW dedicated gas, 7C net-zero pace plus
offshore wind, 8C whole pipeline, 9C preferred partner with export cable. Open inputs from Siemens Energy: Crossfield
timing and customer, gas-turbine lead times and prices, source of "28 CANDU" and "221 licences / $1.1B".
