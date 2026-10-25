# Climate-adaptation scenario set (SU Climate inputs) - implementation note

Date: 2026-10-23. Branches: `dev/fel-x-su-climate-adaptation` in the code repository (from `dev/se`) and in the
data repository (from the v6 freeze, see "Data basis"). Status: inputs built and verified, probes run, the 49-hour
chain is prepared and **not** started.

## Cases

| case | scenario option | label | content |
|---|---|---|---|
| Climate Base | `NorthAmerica_climate_base` | `fel2026_climate_base_49_2015_v1` | v6f data + FEL demand with the cooling split and the climate adjustment of heating / cooling + SSP2-4.5 heating and cooling profiles from 2030 on; thermal capacity factors untouched |
| central | `NorthAmerica_climate_central` | `fel2026_climate_central_49_2015_v1` | Climate Base + thermal-plant derates, temperature only |
| extreme | `NorthAmerica_climate_extreme` | `fel2026_climate_extreme_49_2015_v1` | Climate Base + derates from temperature and river temperature / flow |
| severe | `NorthAmerica_climate_severe` | `fel2026_climate_severe_49_2015_v1` | extreme with the historic drought years baked in |

Comparison partners: Climate Base against the regular base `fel2026_base_49_2015_v6f` (effect of the demand and
profile changes); the three CF cases against Climate Base (effect of the derates). "Climate Base" is a separate
case and does not replace the regular v6 base.

## Data basis

The data branch starts at the v6-freeze commit (`a00d5d9`) plus the base fixes that were sitting uncommitted in the
freeze worktree (commit `81f4576`). A conversion of that state reproduces `RegularParameters_NorthAmerica_v6f.xlsx`
and `Timeseries_NorthAmerica_2015.xlsx` sheet for sheet (checked with a full value comparison), so Climate Base and
v6f differ only in the climate inputs. `se_northamerica` HEAD was not used: it carries the v7 LCOE import and other
post-freeze changes that have never been run as a base, which would mix a data-vintage effect into every comparison.
Switching the branch onto HEAD later is a rebase plus one conversion run.

## Inputs and where they went

| input (`NA_inputs/SU Climate/`) | use | target |
|---|---|---|
| `base_fel_v261023_cooling_climate.xlsx` | FEL demand run with the new `cooling` busbar sector (buildings sector shrinks accordingly) and the climate adjustments `Cooling_Climate_Adj` / `Heating_Climate_Adj` | `Par_SpecifiedAnnualDemand/NorthAmerica_climate_<case>/` via `convert_fel_to_demand.py` (extended: `cooling` -> `Power_Buildings_Cooling`; `--source/--date` arguments). Other sectors are identical to the v6 FEL file. |
| `2026-10-14 - Climate projections SSP2-45 for US.xlsx` | hourly region-mean temperature 2030 and 2035, nine US ISO regions, UTC | `TS_POWER_BUILDINGS_HEAT_2030/2035`, `TS_POWER_BUILDINGS_COOLING_2030/2035` (US columns; Canada and other regions copy the regular profile) |
| `GENeSYS_CapacityFactor_thermal_stress_<central/extreme/severe>.csv` | hourly thermal-plant capacity factors, 28 technologies, nine US regions, years 2030-2050, summer hours 3622-6478 | `TS_CF_THERMAL_<STEAM/CCGT/OCGT>_2030/NorthAmerica_climate_<case>/` + `Par_TagTechnologyToTimeseries/NorthAmerica_climate_<case>/` |
| `2018_temperature_northamerica.csv` (copied from the tools repository) | calibration of the sub-regional spread | not a model input |

Demand check (all NA regions, TWh): Power_Buildings_Cooling 449 (2025) -> 571 (2040); Power_Buildings_Heat 776 -> 743;
Power_General 3375 -> 4357. Regional totals move by -2.5 to +7 TWh against the v6 demand (the FEL climate
adjustment), the cooling share is carved out of the former Power_General. Cooling 2025 by region: SERC 161, ERCOT 79,
PJM 48, MISO 39, WECC 32, SPP 30, Canada 26, California 20, New York 8, New England 5.

## Heating and cooling profiles

Method as in the tools repository (`GIS_&_Timeseries_Tool/functions.py::temperature_timeseries`): heating demand
`max(20 - T, 0)` normalised per region to `(x / mean + 0.25) / 1.25`; cooling demand `max(T - 22, 0)`. The tool
evaluates the formula on every grid point and averages afterwards; the projections only provide the region mean.
Applying the formula to the mean sharpens the profiles (2018 test: cooling non-zero hours 0.65 -> 0.24 of the year,
cooling peak/mean +40 to +75 %, WECC 11.3 -> 19.9). The sub-regional spread is therefore restored analytically,
`E[max(X - a, 0)]` with `X ~ N(T_mean, sigma_r)`, and `sigma_r` (heating and cooling separately, per region, 1.7 to
6.3 K) is fitted so that the 2018 region-mean temperature reproduces the point-based 2018 profile in the repository
(shape correlation 0.98 to 1.00, peaks within 1-2 %; table in `NA_inputs/SU Climate/derived/spread_calibration_2018.csv`).

Year banding is a new, general model mechanism (no run-specific code): a sheet `TS_<NAME>_<YYYY>` next to `TS_<NAME>`
replaces that profile from model year YYYY on (latest YYYY <= y wins), so the runs use the regular profile for
2025-2029, the 2030 sheet for 2030-2034 and the 2035 sheet for 2035-2040. The variants pass through the same hour
selection, smoothing and scaling as every other series.

What the projections say (region-mean degree hours against 2018; single weather years, see the caveat):

| | heating degree hours 2030 / 2035 | cooling degree hours 2030 / 2035 |
|---|---|---|
| California | +1 % / +5 % | -22 % / -9 % |
| ERCOT | -16 % / -8 % | -8 % / -18 % |
| MISO | -15 % / -14 % | -23 % / +32 % |
| New England | -9 % / -16 % | -25 % / +41 % |
| New York | -6 % / -11 % | -31 % / +29 % |
| PJM | -9 % / -10 % | 0 % / +52 % |
| SERC | -1 % / 0 % | -5 % / +14 % |
| SPP | -14 % / -15 % | -35 % / +19 % |
| WECC | -8 % / -4 % | -5 % / -5 % |

Only the shape enters the model (annual energy comes from the FEL demand), but the shape of 2030 is milder than
2018 in most regions and 2035 is hotter. That is weather, not trend, and is inherited from the one-year projections;
the user's temperature outlook page says the same.

## Thermal-plant capacity factors

The three CSVs carry identical hourly values for every year 2030-2050 (asserted by the builder), so one `_2030`
variant per class suffices. The 28 technologies fall into three groups with identical series in every region:
STEAM (nuclear, SMR, coal, lignite, biomass, oil, waste, gas steam and the non-gas CHPs; 18 members), CCGT
(P_Gas_CCGT, _Residual, P_Gas_CCS and the gas CHPs; 8) and OCGT (P_Gas_OCGT, P_H2_OCGT). Hours outside the summer
window, Canada and untagged technologies keep 1.

| annual-mean capacity factor, 2030+ | central | extreme | severe |
|---|---|---|---|
| STEAM, range over the nine regions | 0.992-0.999 | 0.929-0.985 | 0.961-0.990 |
| CCGT | 0.999-1.000 | 0.984-0.995 | 0.991-0.997 |
| OCGT | 1.000 | 0.998-1.000 | 1.000 |
| worst hour (STEAM, California) | 0.80 | 0.44 | 0.44 |

Two general model additions carry this: `Par_TagTechnologyToTimeseries` (Technology, Profile) binds a technology's
capacity factor to a `TS_<Profile>` sheet exactly like a renewable (absent sheet = no binding), and the peaking
constraint credits a tagged plant with its worst-timeslice capacity factor. Without the second change any firm
plant with a CF below 1 would fall into the variable-RES branch of the peaking constraint and lose half its credit
for a derate of a few percent. Untagged technologies and the regular base are unaffected by both.

## Files

- Data repository: `NA_inputs/build_climate_scenarios.py` (idempotent builder, `--apply`), `NA_inputs/convert_fel_to_demand.py`,
  `Conversion Script/_climate_convert.py`, `Conversion Script/Set_filter_file_NorthAmerica_climate.xlsx`, the TS folders and
  overlays listed above, `Par_TagTechnologyToTimeseries/`, registry rows in `Overview_GENeSYS-MOD.csv` and `Overview_Sources.csv`,
  `Assumptions.txt` notes in every new folder, compact derived inputs in `NA_inputs/SU Climate/derived/` (the raw 140 MB
  stress CSVs stay untracked).
- Code repository: `src/genesysmod_timeseries_reduction.jl` (tag reader, year-banded variants, exported demand profiles),
  `src/genesysmod_equ.jl` (peaking credit), `CLAUDE.md`, `_climate/` (run and probe drivers, `run_all.sh`, `probe_all.sh`,
  `check_probe.py`), the four converted workbook pairs in `InputData/`.

## Verification

- Base conversion from the data branch equals the v6f workbooks sheet for sheet (84 shared sheets; v6f additionally has
  three header-only sheets of parameters that did not exist at the freeze).
- Climate Base workbook vs v6f: only `Par_SpecifiedAnnualDemand` differs (+160 cooling rows, heat / general resplit) plus the
  new timeseries sheets; CF-case workbooks vs Climate Base: only the 28 tag rows and the three `_2030` stress sheets.
- Probe runs (1924-hour resolution, Gurobi, no DB writes): see below.

## Probe results

1924-hour probes (`_climate/probe_all.sh`, `check_probe.py`): all four cases load, the build announces the year-banded
variants, the heating / cooling profiles of the US regions change in 2030 and 2035 and stay constant in Canada, the
tagged plants carry CF 1 before 2030 and the derates from 2030 on (extreme: steam class 0.56 in the worst slice of the
coarse probe, CCGT 0.89, OCGT 0.94). Climate Base and central solve; extreme and severe were infeasible: the IIS
named the P_Biomass fleet floor (`Par_TotalAnnualMinActivity`, 61-95 % of the availability ceiling) that the derate
cuts under. Fix in data: the CF overlays scale those floors from 2030 on by the annual-mean stress CF of the class
in that region (central x0.992-0.999, extreme x0.929-0.985, severe x0.961-0.990; `build_activity_floors` in the builder).

49-hour probe of the extreme case (the harshest), no DB writes: OPTIMAL after the floor fix, but with 242 PJ of
infeasibility slack over the horizon against 16 PJ in v6f, 190 PJ of it in Canada and 22 PJ already in 2025, i.e.
before any climate input applies. Cause: the cooling carve-out. In v6 the cooling energy sat inside Power_General and
followed the load shape (peak/mean about 2). Power_Buildings_Cooling follows the temperature-derived cooling profile,
whose peak/mean is 30 in Canada, 28 in New England and 25 in New York (`max(T - 22, 0)` is zero for 65-75 % of the
hours there), against 5-10 in the southern pools. Change made: Canada's cooling stays in Power_General
(`COOLING_IN_GENERAL` in `convert_fel_to_demand.py`; Canada has no temperature projection anyway, its climate
adjustment still enters through the annual FEL energy). The US regions keep the split as requested.

Second 49-hour probe of the extreme case with Canada's cooling in the load shape: OPTIMAL, slack 35 PJ over the
horizon (v6f: 16 PJ): 2025-2029 at v6f level (0.5-3.6 PJ/yr), a 15 PJ step in 2030 when the 2030 profiles and the
derates kick in, falling to zero by 2035. By region: New York 13, New England 7, SERC 6, ERCOT 5, PJM 4 PJ. The
remaining slack is the 2030 climate kick plus the peaky cooling shape of the two northeastern pools (open point 0).
The chain is ready to fire; its gate stops after Climate Base if that run is not OPTIMAL.

## Residual load shape and the ISO benchmark (added after the user review)

The cooling carve-out was checked against the 2024 ISO peaks (ERCOT 85.4 GW, PJM 152.7, MISO 122, SPP 54.4, NYISO 29.0,
ISO-NE 24.9, CAISO 48.4; all in summer; energies approximated from FERC's 2025 State of the Markets average loads),
scaled to the model's 2025 energy per pool. Findings (interactive page: Cooling Shape Check):

- v6 (heating carve-out on top of the load shape) matches the magnitudes (-13 to +2 %) but peaks in WINTER in seven of
  nine pools (ERCOT 94.6 GW in January against a measured winter peak of 78 GW): the load shape already contains the
  heating load. A base defect of v6 that shaped every v6 fleet.
- the cooling split restores the summer peak but double-counts cooling: +6 % PJM/MISO, +16 % ERCOT/SPP, +22 % New
  England, +42 % New York (cooling profile 25-28x its mean there).
- a residual load shape for Power_General (load minus the 2025 heating and cooling components, clipped at zero in 0-47
  hours per pool, renormalised) puts the base-year total on the measured FEL load shape: summer peaks everywhere,
  -4 % (ERCOT) to +17 % (New York; the FEL hourly load itself is spikier than NYISO's).

Decision (user, 2026-10-23): residual load shape. Implemented as `TS_POWER_GENERAL` (builder `build_residual_general`)
bound through `Par_TagFuelToTimeseries` overlays of the four climate options; Canada's cooling returned to
Power_Buildings_Cooling (`COOLING_IN_GENERAL` empty). Consequence: Climate Base differs from v6f in winter as well (the
v6 winter double count is gone), which the write-up has to state.

## Dispatch set

After the four investment runs the chain dispatches the Climate Base fleet (`fel2026_climate_base_49_2015_v1`) hourly
over 2025/2030/2035/2040 under each input set (`_climate/dispatch_<case>.jl`, results keyed
`fel2026_climate_<case>_dispatch_v1`, new `result_label` option of `genesysmod_dispatch_fullyear`), so the thermal-stress
effect is also seen on a fixed fleet. Investment runs of the stress cases stay in the chain for the adaptation view.


## Run results (chain of 2026-10-23/24)

Investment runs, all OPTIMAL (about 28 min each, 49-hour resolution, Gurobi):

| case | objective bEUR | vs Climate Base | INF slack PJ | gas CCGT / OCGT GW 2040 | coal GW 2040 | solar GW 2040 | battery GW 2040 |
|---|---|---|---|---|---|---|---|
| v6f (reference) | 2,684 | +1.0 % | 16 | 531 / 258 | 58 | 1,029 | 279 |
| Climate Base | 2,658 | - | 1.2 | 545 / 344 | 58 | 1,155 | 294 |
| central | 2,662 | +0.1 % | 1.2 | 546 / 349 | 62 | 1,156 | 295 |
| extreme | 3,000 | +12.9 % | 96 | 611 / 361 | 75 | 1,169 | 316 |
| severe | 2,911 | +9.5 % | 61 | 609 / 356 | 66 | 1,172 | 325 |

- Climate Base vs v6f: 2025 generation mix identical (benchmark check unchanged), no fuel group deviates by more than
  15 % in any year; 2040 carries +104 GW gas (mostly OCGT) and +126 GW solar for the summer peaks.
- central is indistinguishable from Climate Base (annual-mean derate below 1 %).
- extreme / severe: the slack sits in 2030-2032, PJM and SERC (extreme 50 + 35 PJ): the derate arrives as a step in
  2030 (the stress CSVs are identical from 2030 on) while the build-rate caps limit the response for about three years;
  by 2033 the fleet has adapted (+66 GW CCGT, +17 GW OCGT, +17 GW coal kept, +22 GW batteries in 2040 against Climate
  Base). The slack penalty (999 MEUR/PJ) accounts for roughly 70-95 bEUR of the +342 bEUR objective delta; the rest is
  real adaptation and fuel cost.

Full-year hourly dispatch of the Climate Base fleet (2025/2030/2035/2040) under the four input sets:

| case | 2030 unserved GWh | 2030 avg / max price EUR/MWh | 2035 unserved | gas OCGT TWh 2030/2035 | nuclear TWh 2030/2035 |
|---|---|---|---|---|---|
| base | 0 | 67 / 123 | 0 | 216 / 50 | 920 / 990 |
| central | 0 | 67 / 123 | 0 | 221 / 53 | 916 / 986 |
| extreme | 4,767 (0.08 %) | 718 / 4,500 | 0 | 275 / 93 | 877 / 945 |
| severe | 36 | 69 / 3,344 | 0 | 260 / 75 | 895 / 963 |

- extreme 2030 on the unadapted fleet: 4.7 TWh unserved, 4.69 TWh of it in PJM over 357 hours (New York 50 GWh,
  SPP 19, SERC 7); 2035 and 2040 are served (the fleet grows faster than the derate bites). Steam-class plants lose
  4-5 % of their energy (nuclear -42 TWh, coal -26 TWh in 2030), replaced by OCGT (+59 TWh) and CCGT.
- Two dispatch fixes were needed on the way: the positional Switch constructor of the dispatch module lacked the
  newer switch_districtheat field (every dispatch failed), and tagged plants now ramp on utilisation of the available
  capacity, g/CF, because a must-run plant at its availability cap cannot follow a derate step (up to 0.22/h in the
  steam profiles) within its ramp-down factor (nuclear 0.15/h) - 2030+ were infeasible otherwise.
- To check before quoting prices: the PJM and SERC annual average prices in the extreme 2030 dispatch sit at
  3,316 EUR/MWh in nearly every hour, far beyond the 357 scarcity hours; this looks like the dual of a binding annual
  constraint (availability budget or floor) leaking into the hourly price, not a physical signal.

## Round 2 (2026-10-24): no fossil expansion, and the v6f fleet under the climate inputs

Variants `NorthAmerica_climate_{base,extreme,severe}_nofossil`: TotalAnnualMaxCapacity of every gas, coal and oil
technology (incl. CCS and CHP) = the v6f total-capacity path per region and year (0.001 GW where v6f has none), so no
fossil capacity beyond the regular base can be built (labels `fel2026_climate_<case>_nofossil_49_2015_v1`).

| 2040, NA | extreme | extreme_nofossil | base | base_nofossil |
|---|---|---|---|---|
| objective bEUR | 3,000 | 4,278 | 2,658 | 2,904 |
| INF slack PJ (horizon) | 96 | 720 | 1.2 | 94 |
| gas CCGT / OCGT GW | 611 / 361 | 532 / 258 (= v6f) | 545 / 344 | 532 / 258 |
| coal GW | 75 | 58 | 58 | 58 |
| nuclear GW | 149 | 171 | 148 | 167 |
| solar GW | 1,169 | 1,369 | 1,155 | 1,233 |
| wind GW | 435 | 556 | 431 | 518 |
| battery GW | 316 | 506 | 294 | 475 |
| geothermal GW | 14 | 24 | 12 | 24 |

Why solar + storage barely move in the fossil-free-to-build extreme case (the user's question): renewables are not
derated (verified: PV, wind and hydro capacity factors identical between Climate Base and extreme, only the 28 tagged
thermal techs change). With fossil expansion open, the model answers the derate with OCGT/CCGT and keeps coal, because
the derate also removes firm capacity in the summer evenings where PV has no output. With fossil expansion shut, the
model adds +200 GW solar, +121 GW wind, +190 GW batteries, +22 GW nuclear and +10 GW geothermal, and then runs into the
installation ceilings of the data where the slack sits: in PJM and SERC the best PV class (68 / 51 GW), the best
onshore wind class (22 / 4 GW), Li-ion batteries (39 / 44 GW), large nuclear (42 / 48 GW) and SMRs (6 / 2 GW) are all
at their TotalAnnualMaxCapacity in 2040; the remaining headroom is the average / inferior PV and wind classes, which
cannot serve derated summer evenings. Slack therefore persists 2030-2040 (PJM 22-49 PJ/yr, SERC 11-29, MISO from
2035), 720 PJ in total (2040: 97 PJ = 27 TWh, 0.3 % of demand); the objective delta is mostly the slack penalty. The
battery ceilings (39 GW PJM, 44 GW SERC) are data potentials worth revisiting before reading this as a physical limit.
No per-technology annual build cap binds for PV; the rooftop group cap (8.8 GW/yr) does.

Dispatch of the regular v6f fleet under the climate input sets (`fel2026_v6f_climate_<case>_dispatch_v1`) against the
Climate Base fleet:

| unserved GWh | 2030 | 2035 | 2040 |
|---|---|---|---|
| v6f fleet, base inputs | 67 | 8 | 75 |
| v6f fleet, central | 80 | 8 | 79 |
| v6f fleet, extreme | 627 | 296 | 934 |
| v6f fleet, severe | 338 | 200 | 728 |
| Climate Base fleet, extreme | 4,767 | 0 | 0 |
| Climate Base fleet, severe | 36 | 0 | 0 |

The v6f fleet, built on the winter-peaking v6 demand, is short in New York in every year (66-75 GWh even with base
inputs) and under extreme stress loses 0.6-0.9 TWh per year in PJM, New York, New England, MISO and SERC, with hourly
prices up to 9,000 EUR/MWh in 2040; curtailment is lower than on the Climate Base fleet (74 vs 126 TWh in 2040) because
it holds 126 GW less solar. The Climate Base fleet is short only in 2030 (the step year) and only under extreme stress.

## Round 3 (2026-10-25/26): no fossil AND no nuclear expansion beyond v6f

User review of round 2: +22 GW nuclear in the no-fossil cases is not credible (few advanceable projects, nuclear is
derated too). P_Nuclear and P_Nuclear_SMR join the capped technologies; same scenario names, the rerun replaced the
round-2 rows (chain started 23:00 on the user's instruction, other runs during the day).

| 2040, NA | base | base_nofossil | extreme | extreme_nofossil | severe_nofossil |
|---|---|---|---|---|---|
| objective bEUR | 2,658 | 2,999 | 3,000 | 4,400 | 4,194 |
| INF slack PJ (horizon) | 1.2 | 149 | 96 | 811 | 691 |
| gas CCGT / OCGT GW | 545 / 344 | 532 / 258 | 611 / 361 | 532 / 258 | 532 / 258 |
| coal / nuclear GW | 58 / 148 | 58 / 148 | 75 / 149 | 58 / 148 | 58 / 148 |
| solar / wind GW | 1,155 / 431 | 1,233 / 516 | 1,169 / 435 | 1,371 / 556 | 1,355 / 540 |
| Li-ion / redox / CAES / PHS GW | 277 / 17 / 4 / 24 | 322 / 153 / 10 / 27 | 278 / 38 / 9 / 25 | 346 / 159 / 12 / 29 | 346 / 158 / 12 / 29 |
| geothermal GW | 12 | 24 | 14 | 24 | 24 |

With nuclear shut as well, the extreme case leaves 811 PJ unserved over the horizon, rising every year to 111 PJ
(31 TWh, 0.4 % of demand) in 2040, in PJM (378 PJ), SERC (283) and MISO (84). In those three pools every firm or
storage option is at its data ceiling in 2040: best PV class (PJM 68/68, SERC 51/51, MISO 123/123 GW), best onshore
wind class (22/22, 4/4, 39/39), Li-ion (39/39, 44/44, 37/37), redox flow (22/22 in each), CAES (9 of 10 pools), PHS
(8 of 10), biomass, hydro. What remains is the average / inferior PV and wind classes (half-used, lower CF, no evening
output) and enhanced geothermal (MISO 0 of 181 GW, too expensive at its cost path). Even base_nofossil, with no derate,
carries 149 PJ of slack: capping gas at the v6f path already denies the +104 GW the Climate Base builds for the
summer peaks. The binding limits are the storage and best-class RES potentials in Par_TotalAnnualMaxCapacity,
especially the per-pool Li-ion (37-44 GW) and redox (22 GW) ceilings; whether a RES + storage adaptation path exists
is a question about those data ceilings, not about cost.

## Open points for the user

0. Cooling profile shape in the cool pools: the tools formula gives New England / New York a cooling peak of 25-28
   times the annual mean (real AC loads peak at roughly 10x). Options: keep (slack stays small but non-zero there),
   lower the threshold to the 18.3 degC degree-day convention, add a baseline floor as the heating formula has, or treat
   those pools like Canada. The regular profile is affected as well (same formula), so any change applies to all years.
1. Data basis: v6 freeze (chosen, comparable to v6f) or `se_northamerica` HEAD (v7 costs, never run as a base).
2. Peaking credit of derated plants = worst-timeslice CF (conservative). Alternative: CF in the peak-demand timeslice.
3. The 2030 profiles are milder than 2018 in most regions (single weather years). A multi-year or delta-based profile
   would separate trend from weather; out of scope here.
4. Thermal stress data stop at the nine US regions; Canada keeps full availability.
