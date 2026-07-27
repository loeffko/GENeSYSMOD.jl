# Results & Databases

## Output formats

Model results are written to **DuckDB databases** (plus optional CSV exports):

- `genesysmod_db.duckdb` — investment-model results and processed input data,
- `genesysmod_dispatch_results.duckdb` — full-year dispatch results (hourly).

Every table carries a `Scenario` column; re-running a scenario replaces its
rows, a new scenario name appends. Tables use real dimension names
(Region, Technology, Fuel, Year, …).

## Scenario labels

```
fel2026_<scenario>_<resolution>_<weatheryear>[_<version>]
        │           │            │             └ model generation (v6)
        │           │            └ weather year (2012/2015/2017/2018)
        │           └ time resolution key (49 = every 49th hour)
        └ scenario name (base, dc_high, dch_eco_gridhigh, …)
```

Reruns with changed inputs always get a fresh version suffix; labels are never
reused for different inputs.

## Main investment-result tables

| Table | Content |
|---|---|
| `output_capacity` | capacities by region/technology/year (total, new, residual) |
| `output_production` / `output_annual_production` | generation and use by technology and fuel |
| `output_trade` | interregional flows |
| `output_emission` | CO₂ by region/technology |
| `output_technology_costs_detailed`, `output_exogenous_costs` | cost breakdown |
| `output_energydemandstatistics` | demand by carrier, generation statistics |
| `output_switches` | the full run configuration of every scenario |
| `input_*` | the processed input parameters (when the input dump is enabled) |
| `raw_*`, `duals_*` | raw variable values and selected shadow prices |

## Main dispatch-result tables

The dispatch database stores hourly results per scenario / weather year /
dispatch year: zonal balances (demand, generation by fleet, storage operation,
trade, curtailment, unserved energy) and **hourly zonal prices** from the
energy-balance duals, including scarcity and negative-price hours from the
market-realism layer.

## Reproducibility

- Every result row is keyed to its scenario label; `output_switches` records
  the exact model configuration per label.
- Input workbooks are generated deterministically from the versioned data
  repository; a scenario label plus data-repository commit fully determines a
  run.
- Validation artifacts (error-check reports, benchmark comparisons) are stored
  alongside the result databases.
