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
