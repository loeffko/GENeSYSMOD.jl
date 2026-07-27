# Scenarios & Sensitivities

The scenario tree is built from a **base case** plus orthogonal levers that
can be combined. Every scenario is a separate input workbook produced by the
overlay mechanism (see [Data & Workflow](data.md)); model code is identical
across scenarios.

## Base case

Central demand path (≈ 8,260 TWh in 2040), base capacity corridors, historic
interconnector growth limits, base storage duration path (3.5 h by 2040),
central fuel prices. Calibrated and benchmarked against 2024 statistics.

## Demand levers

| Scenario | Definition | 2040 demand vs base |
|---|---|---|
| `dc_high` | accelerated data-center growth | +22 % |
| `dc_low` | data-center slowdown | −14 % |
| `recession` | macroeconomic slowdown | reduced across carriers |
| `btm_lag` | behind-the-meter/self-supply lag variant | demand-side timing shift |

## Build / corridor levers

| Scenario | Definition |
|---|---|
| `economic` | relaxed capacity corridors (min ×0.75 / max ×1.5 by 2035) — the optimizer chooses the fleet more freely |
| `grid_high` | aggregate national wire budget (interconnector capacity may double by 2040) + grid-oriented corridor widening + accelerated coal phase-down |
| `grid_low` | interconnector expansion capped at 0.75 %/yr |

## Storage levers

| Scenario | Definition |
|---|---|
| `bess_optimistic` | battery capex ×0.4 and 7-hour duration path |
| `bess_pessimistic` | battery build-out reduced (≈ 53 % of base power path), duration ≈ 2.9 h |

## Cross-sensitivities

The demand levers are crossed with the build and storage levers to separate
demand effects from flexibility effects — e.g. `dch_eco_bessopt_gridhigh` is
DC-High demand × economic corridors × optimistic batteries × high grid. A
wires-only variant (`gridhigh_nf`, wire budget without corridor changes)
isolates the pure transmission effect from the fleet-corridor effect.

## Dispatch-side variants

Operational sensitivities re-run the full-year dispatch on a fixed investment
fleet:

- **Gas price shock** (fuel price ×1.75),
- **Hydro drought** (Canada + WECC low-hydro conditions),
- **Grid swaps** (base fleet with high/low-grid interconnectors),
- **Storage stress** (reduced/removed storage energy),
- storage-duration and no-subsidy (no-PTC) variants.

## Weather years

All scenarios run against weather year 2015; selected scenarios additionally
against 2012, 2017, and 2018.
