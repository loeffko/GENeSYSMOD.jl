# Natural gas infrastructure in the North America model - design proposal

Status: PROPOSAL for review (2026-09-12). Nothing implemented yet except research.
All research items resolved (last gaps closed 2026-09-12); remaining proxies are flagged inline.
Data basis: EIA (state-to-state capacity Jan-2026, ARR 2024, consumption 2024,
liquefaction Q2-2026, pipeline projects Aug-2026, AEO2026), CER Canada Energy
Future 2026, FERC filings. Units: 1 Bcf = 1.094 PJ (1,037 Btu/cf, EIA consumed-gas
heat content); 1 Bcf/d = 399.4 PJ/yr = 12.66 GW-th. Currency EUR2023 at 1.0813.

## 1. What changes, in one picture

```
today (power-only):   [gas plants] <- fuel cost + CO2 folded from Henry-Hub path
proposed:             R_Gas(region) --+
                      Z_Import_Gas   --+--> [Gas_Natural balance, per timeslice, per region]
                      pipelines (10 nodes, 30 corridors) <-> storage S/D_Gas_Methane
                                                |--> gas plants (IAR, CO2 on the plant)
                                                |--> non-power demand (res/com/ind, heating-shaped)
                                                |--> LNG export terminals + Mexico (exogenous sinks)
                      deliverability cap per region/timeslice (New England / California winter)
```

The fuel becomes explicit; price formation becomes endogenous (hourly regional gas
price = EB2 dual of the Gas_Natural balance, recorded automatically in `duals_*`).

## 2. Model-side changes (code, all region-agnostic, data-gated)

| # | Change | Where | Why |
|---|---|---|---|
| C1 | Power-only precompute skips any fuel present in the workbook's fuel set (per input fuel, not per tech) | `genesysmod_precompute_powerOnly.jl` | otherwise fuel cost and CO2 are counted twice (folded + explicit). Diff drafted by the code analysis. Companion: apply the CCS residual fraction in the fold (today CCS plants are charged 100% CO2 in power-only) |
| C2 | Un-fence the non-power trade blocks: corridor growth `TrC4a` (use `InitialMaxNewTradeCapacity`, drop the hardcoded 100/50), annual flow cap `TrC7`, per-timeslice pipeline accounting `TrPA1a`, flat-import rule `TrPA2b` | `genesysmod_equ.jl:520-627` | today they are inside `#= =#` for the NA build; without them pipeline capacity is decorative. Gate on data presence (a tradable non-power fuel in `Set_Fuel_Regions`), never on region |
| C3 | Deliverability cap: new optional `Par_FuelUseRateLimit[Region, Fuel, Year]` (GW-th, 999999 = none) + `Par_FuelUseRateLimitMonth[Region, Fuel, Month]` (factor, default 1): per timeslice, sum of RateOfUse of that fuel by all consuming techs <= limit x month factor | equ (new CA6), dataload (optional sheet, `create_daa_init`), datastructures, errorcheck | single-node ISO regions need an intra-regional pipeline/storage takeaway limit; the reliability reports quote it in Bcf/d, which is exactly GW-th. Same wiring pattern as the existing group caps. Alternative (fuel-agnostic, tech-subset keyed activity cap) documented in the analysis; the fuel-use form is cleaner once gas is explicit |
| C4 | Fuel -> timeseries binding made data-driven (`Par_TagFuelToTimeseries`, fallback = the current hardcoded dict) | `genesysmod_timeseries_reduction.jl` | non-power gas demand needs its own profile; today the map is a code constant |
| C5 | Infeasibility slack for explicitly-demanded fuels (Gas_Natural gets `Infeasibility_Gas_Natural` like Power) | dataload `update_inftechs_params!` | development safety: a gas-balance conflict otherwise hard-infeasible with no diagnostic |
| C6 | Dispatch layer: NOT touched in phase 1. Flag: the full-year dispatch assumes folded fuel cost; phase 2 should read the investment run's hourly regional gas price (EB2 dual) instead of the regional basis multipliers | `genesysmod_dispatch_fullyear.jl:417-462` | avoid double pricing |

Nothing hardcoded: every number below lives in the data repo under a scenario
subfolder `NorthAmerica_gas` (own filter file `Set_filter_file_NorthAmerica_gas.xlsx`),
so the existing power-only base is untouched until the feature is adopted.

## 3. Data (scenario NorthAmerica_gas)

### 3.1 Set flips (filter file)
Fuel `Gas_Natural`; technologies `R_Gas`, `Z_Import_Gas`, `D_Gas_Methane`; storage
`S_Gas_Methane`; timeseries `TS_GAS_NONPOWER` (new). `Gas_Natural` stays
timeslice-resolved (no `TagTimeIndependentFuel` row) - the annual form has no demand
term and free disposal.

### 3.2 Inter-regional pipelines (Par_TradeCapacity, Gas_Natural, PJ/yr, 2025)
EIA state-to-state capacity 2025, county-level ISO mapping, EIA's own
`flows_to_remove` applied, transit loops removed (MEP/Gulf Crossing OK->TX),
Golden Pass feed line dropped, California capped at utility receipt capability.

| from -> to | Bcf/d | PJ/yr | from -> to | Bcf/d | PJ/yr |
|---|--:|--:|---|--:|--:|
| WECC -> California | 7.30 | 2915 | California -> WECC | 0.87 | 348 |
| WECC -> SPP | 8.22 | 3281 | SPP -> WECC | 1.53 | 611 |
| SPP -> ERCOT | 2.19 | 873 | ERCOT -> SPP | 1.26 | 503 |
| ERCOT -> MISO | 5.78 | 2309 | MISO -> ERCOT | 3.96 | 1582 |
| SPP -> MISO | 8.25 | 3295 | MISO -> SPP | 0.23 | 91 |
| PJM -> MISO | 18.07 | 7214 | MISO -> PJM | 7.93 | 3167 |
| MISO -> SERC | 11.37 | 4541 | SERC -> MISO | 3.05 | 1219 |
| PJM -> SERC | 2.69 | 1074 | SERC -> PJM | 3.81 | 1522 |
| PJM -> NewYork | 10.19 | 4067 | NewYork -> PJM | 1.78 | 712 |
| NewYork -> NewEngland | 4.09 | 1632 | NewEngland -> NewYork | 0.90 | 357 |
| Canada -> WECC | 7.25 | 2895 | WECC -> Canada | 0.13 | 53 |
| Canada -> SPP | 1.92 | 768 | SPP -> Canada | 0.03 | 12 |
| Canada -> MISO | 6.10 | 2435 | MISO -> Canada | 4.93 | 1971 |
| Canada -> NewYork | 3.31 | 1324 | NewYork -> Canada | 1.35 | 539 |
| Canada -> NewEngland | 1.45 | 579 | NewEngland -> Canada | 1.14 | 456 |

No physical connection (no route row): California with anything but WECC;
ERCOT with SERC/PJM/NY/NE/Canada; SPP with SERC/PJM/NY/NE; MISO with NY/NE;
SERC with NY/NE/Canada; PJM with NE/Canada. Total inter-regional 131 Bcf/d.
Caveat: the Northern Border chain (Canada->WECC->SPP->MISO) is transit; WECC has
almost no injection into it - a `GroupAnnualMaxTradeCapacity` on the chain or a
lower WECC->SPP value is the fix if the model abuses it.

### 3.3 Corridor expansion (growth, cost, distance)
- `GrowthRateTradeCapacity` per corridor class (evidence: EIA project tracker
  1996-2026, FERC dockets): Gulf/LNG corridors 15 %/yr to 2030 then 8 %; Appalachia
  takeaway (PJM out) 6 %; Northeast demand corridors (into NY/NE) 3 % / 2 % with
  zero before 2027; California import 0 %; Canada border 1 %; interior West/Plains
  4 %; Midwest interchange 5 %. Plus absolute caps via `AnnualMaxTradeCapacity`
  (class abs adds 0.2-3.0 Bcf/d/yr) and a national envelope of 8 Bcf/d/yr via
  `GroupAnnualMaxTradeCapacity`.
- `CommissionedTradeCapacity`: the under-construction/approved list (CP Express
  4.0 Bcf/d ERCOT->MISO 2027, SSE 1.6 PJM->SERC 2027, MSX 2.1 + SSE4 1.3
  MISO->SERC 2028, NESE 0.4 PJM->NY 2027, Heartland 0.47 PJM->MISO 2027, ...).
- `TradeCapacityGrowthCosts` (M EUR per PJ/yr per km) from 63 EIA-tracked projects
  with cost, length, capacity: median 0.0086; by region: South Central 0.006,
  Mountain/West 0.007, Southeast 0.011, Northeast 0.025 (MVP/SSE/NESE class),
  Midwest small-loop projects 0.04 -> use 0.012 for large corridors. EU value in
  the data today: 0.003.
- `TradeRoute` distances: hub-to-hub pipeline route km (Dominion South, Henry Hub,
  Katy, Waha, Chicago Citygate, Opal, SoCal border, Transco Z6, Algonquin, Dawn,
  AECO); 35 pairs computed (great-circle x 1.25 or actual line length).
- `InitialMaxNewTradeCapacity` Gas 300 PJ/yr already present for NA pairs.
- `TradeLossFactor` 9.45e-7/km, `TradeCostFactor` 0.000054 M EUR/PJ/km already present.

### 3.4 Supply: R_Gas per region (dry-equivalent, EIA ARR 2024)

| region | 2024 production PJ | Bcf/d | proved reserves PJ | R/P yrs |
|---|--:|--:|--:|--:|
| PJM (Appalachia) | 13,120 | 32.9 | 172,600 | 13 |
| SPP (Anadarko, Permian-NM, Panhandle, Bakken) | 10,270 | 25.7 | 119,500 | 12 |
| ERCOT (Permian-TX, Eagle Ford, E-Texas, 30 % GOM) | 9,270 | 23.2 | 100,100 | 11 |
| WECC (Rockies, San Juan, TX-El Paso) | 5,650 | 14.2 | 65,500 | 12 |
| MISO (Haynesville-LA, 70 % GOM, AR) | 4,040 | 10.1 | 27,300 | 7 |
| California / SERC / NewYork / NewEngland | ~90 / ~90 / 8 / 0 | | | |
| Canada (CER 2026, marketable) | 7,320 | 18.3 | (2040: 26.5 Bcf/d Current Measures) | |
| US total | 42,540 | 106.5 | 486,700 | 11.4 |

Model parameters: `TotalAnnualMaxActivity` = 2024 production scaled with the AEO2026
national path (39.2 -> 41.4 -> 44.9 -> 47.1 Tcf in 2025/30/35/40) per region, Canada with
CER Current Measures; `ModelPeriodActivityMaxLimit` = proved reserves x 2 (reserve
growth); `VariableCost` = extraction cost from basin breakevens (USD/MMBtu -> M EUR/PJ at
0.8766; sources: Stanwich 2025 regional breakevens cross-checked with EIA Haynesville
behaviour and Dallas Fed surveys; associated-gas basins are oil-driven and priced as a
by-product):

| region | dominant basins | breakeven USD/MMBtu | R_Gas VariableCost M EUR/PJ |
|---|---|--:|--:|
| PJM | Marcellus/Utica | 1.75-2.50 | 1.9 |
| ERCOT | Permian associated (~by-product), Eagle Ford 2.75-3.50, East Texas | blend | 1.6 |
| SPP | Anadarko/SCOOP-STACK >= 2.50, Permian-NM associated, Bakken associated | blend | 2.4 |
| MISO | Haynesville 3.75-4.25, Gulf offshore (n/a), Arkansas | blend | 3.3 |
| WECC | Rockies (Piceance/Green River dry gas; DJ oil-linked) - proxy 2.5-3.0 | proxy | 2.6 |
| Canada | Montney/Duvernay - AECO-price proxy (< C$2/GJ) | proxy | 1.5 |
| California / SERC / NY (marginal fields) | | | 3.0 |

Sanity: the HH-based `Z_Import_Gas` rows now in the NA data are 2.83-3.31 M EUR/PJ -
i.e. Henry Hub sits at the Haynesville marginal cost, which is exactly what the
supply curve above reproduces. Flagged proxies: Rockies dry-gas, WCSB, Gulf offshore.
`TotalAnnualMaxCapacity` = peak daily production capability (production / 0.9).

### 3.5 Demand: non-power (new SpecifiedAnnualDemand rows) - EIA 2024, PJ/yr

| region | res+com+ind (non-power) | electric-gen (calibration only) |
|---|--:|--:|
| MISO | 4,300 | 2,030 |
| PJM | 3,300 | 2,890 |
| ERCOT | 2,260 | 1,970 |
| SERC | 1,940 | 3,670 |
| SPP | 1,580 | 960 |
| WECC | 1,570 | 1,550 |
| California | 1,450 | 620 |
| NewYork | 840 | 560 |
| NewEngland | 540 | 470 |
| US total | 17,770 | 14,710 (36.9 Bcf/d, matches EIA) |

Profile: monthly non-power shape from the same EIA series (New England Jan 16 % /
Jul 4 %; SERC Jan 14 % / Jun 6 %), flat within each month, as the new
`TS_GAS_NONPOWER` sheet (Canada = MISO shape proxy). Implementation note: `TS_HEAT_LOW`
carries only zero placeholders in its NA columns, so the originally planned hourly
heating blend was not possible; an hourly ERA5 heating shape for NA is a later refinement. Trajectory to 2040: flat (AEO2026 reference
is flat-to-slightly-down for res/com, up for industrial) - scenario lever later.
Canada non-power: CER (pending; proxy ~2,400 PJ).

Calibration flag: the model's own 2025 power burn is 27.9 Bcf/d (v6c) vs EIA 36.9 - the
v6 fleet efficiency (CCGT IAR 1.79 = 56 % LHV) and gas generation are both above/below
reality; supply-side sizing anchors on EIA, not the model.

### 3.6 Exogenous sinks: LNG exports + Mexico
LNG baseload capacity (EIA liquefaction Q2-2026, existing + under construction):

| year | MISO (LA) | ERCOT (TX) | PJM (Cove Point) | SERC (Elba) | total Bcf/d |
|---|--:|--:|--:|--:|--:|
| 2025 | 9.3 | 5.1 | 0.7 | 0.3 | 15.4 |
| 2027 | 11.9 | 10.1 | 0.7 | 0.3 | 23.1 |
| 2030 | 15.7 | 12.0 | 0.7 | 0.3 | 28.7 |
| 2032+ | 15.7 | 14.3 | 0.7 | 0.3 | 31.0 |

Represented as `SpecifiedAnnualDemand` rows for a new demand fuel `Gas_LNG_Export`
served by a 1:1 conversion tech from `Gas_Natural` (so pipelines see the feedgas), at
90 % utilisation, flat profile; approved-not-FID (LA 2.4, TX 1.0, MS 0.7 Bcf/d) as a
scenario. Mexico pipeline exports: ~6.5 Bcf/d (2024 actual; ERCOT ~70 %, WECC ~20 %,
California ~10 %) as a flat exogenous demand; capacity is 14.5 Bcf/d, not binding.

### 3.7 Storage (EIA-191 2024, per region)

| region | working gas PJ | deliverability Bcf/d | GW-th | salt share |
|---|--:|--:|--:|--:|
| MISO | 1,366 | 38.7 | 472 | 0.14 |
| PJM | 1,177 | 23.3 | 285 | 0.00 |
| SPP | 668 | 12.2 | 149 | 0.04 |
| ERCOT | 566 | 17.8 | 217 | 0.32 |
| WECC | 478 | 5.4 | 66 | 0.00 |
| California | 341 | 8.5 | 104 | 0.00 |
| SERC | 187 | 9.3 | 114 | 0.52 |
| NewYork | 130 | 2.9 | 35 | 0.01 |
| NewEngland | 0 (LNG peak-shaving only) | | | |
| Canada | 1,038 (CER: 949 Bcf total; Ontario 248-353, Alberta ~500-550, BC 95) | Dawn 7.6 (others n/a) | 96+ | 0.00 |

Maps to `ResidualStorageCapacity` (S_Gas_Methane, PJ) and `ResidualCapacity`
(D_Gas_Methane, GW-th) with `StorageE2PRatio` = working/deliverability (MISO ~120 h,
salt-heavy SERC ~50 h). `D_Gas_Methane` capex rows need every-year fill (milestone-only
today - the Redox trap).

### 3.8 Deliverability limit (C3 data)
`Par_FuelUseRateLimit[r, Gas_Natural, y]` = inbound pipeline capacity + in-region
peak production + storage deliverability, minus non-power peak-day demand, i.e. what is
left for power on a design day; month factor from the ISO winter studies. Evidence
found: ISO-NE total winter gas supply capability 3.86 Bcf/d pipeline + 2.04 Bcf/d LNG
regasification = ~5.9 Bcf/d (OFSA, still the reference frame; Algonquin winter basis
+5 USD/MMBtu 2025-26, Jan-2025 spot 16.4 USD/MMBtu); SoCalGas system receipt capacity
3.89 Bcf/d with Aliso Canyon, 3.33 without (CPUC 2022-2026); NYISO models 6.4 GW of
gas-only capacity unavailable at winter peak, two-thirds of gas capacity dual-fuel;
PJM Winter Storm Elliott: 11 GW (13 %) of gas capacity out at the peak-outage hour,
Lower-48 production -16 % (Marcellus -23 %). Firm-transport shares were not found
published for any ISO. Neutral default 999999 everywhere else, so only regions with
evidence (New England, California, New York) get a cap in the first cut; Elliott-type
production freeze-offs are a separate weather-year sensitivity, not a cap.

Transport cost note: published firm tariffs/spreads (Algonquin winter basis 4.4 M
EUR/PJ, Kingsgate->Malin 1.2, Waha discount -1.8) are capacity-rent, not variable
cost; the model prices new capacity through `TradeCapacityGrowthCosts` and charges
flow only the variable/fuel share via `TradeCostFactor` (0.000054 M EUR/PJ/km, i.e.
~0.08 M EUR/PJ per 1,500 km). Keeping that; the tariff evidence is a validation
target for the resulting corridor shadow prices, not an input.

## 4. Base-year mass balance check (2024, Bcf/d)
production 106.5 + Canada net imports ~6 = 112 supply;
consumption: non-power 44.5 + power 36.9 + LNG 12.8 (actual) + Mexico 6.5 + pipeline
fuel/losses ~3 + storage net 0 = ~104; residual ~8 Bcf/d = wet/dry basis and
lease/plant fuel - within the accounting noise of a first cut. Closes.

## 5. Decisions needed from you
1. Z_Import_Gas role: (a) physical only - LNG import terminals (Everett, ~0.1 Bcf/d)
   + Mexico-to-US (1.5 Bcf/d capacity) and otherwise zero, so price formation is fully
   endogenous from R_Gas supply curves (recommended); or (b) keep a Henry-Hub-priced
   backstop with limited capacity as a price anchor.
2. Deliverability representation: C3 fuel-use cap (recommended) vs the fuel-agnostic
   tech-subset activity cap; or defer C3 to a second step and start with pipelines +
   storage only.
3. Non-power demand trajectory: flat 2024 levels vs AEO2026 sectoral paths.
4. Basis: build on current HEAD (v7 costs, PV option B) - a new feature, not
   v6-comparable - with its own base run `fel2026_gas_49_2015_v7g`.
5. Scope check: the gas balance adds ~10 x 49 x 16 equalities + trade variables at
   nthhour 49 - negligible; the Northeast corridor rules and the transit-chain caveat are
   the two places where I would expect first-run surprises.
