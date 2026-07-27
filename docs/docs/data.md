# Data & Workflow

## Data pipeline

Input data is maintained in a separate **data repository** as one CSV file per
model parameter (capital costs, availability factors, demand, potentials,
efficiencies, …). A conversion toolchain combines these into the Excel
workbooks the model reads:

```
Data repository (per-parameter CSVs)
        │  conversion scripts (Python)
        ▼
RegularParameters_NorthAmerica[_<scenario>].xlsx   ← scenario data
Timeseries_NorthAmerica_<weatheryear>.xlsx         ← hourly profiles
DispatchData_NorthAmerica[_<variant>].xlsx         ← dispatch market layer
        │
        ▼
GENeSYS-MOD.jl  (investment → dispatch → result databases)
```

Two rules keep this reproducible:

1. **No data in code.** All numbers — costs, factors, caps, price paths,
   technology lists — live in the data pipeline, never in the model equations.
   New features are designed region-agnostic and data-driven with neutral
   defaults when rows are absent.
2. **Set registration.** Every technology, fuel, region, or emission used in a
   parameter must be registered in the set-filter workbook; unregistered
   members are dropped by the conversion.

## Scenario variants

Scenario input variants are managed as **overlay folders**: a scenario folder
contains only the parameter CSVs that differ from the base; the conversion
merges them over the base data (row-level upsert) and emits a separate
workbook `RegularParameters_NorthAmerica_<scenario>.xlsx`. Base data is never
mutated for a scenario. The same mechanism builds combined variants
(e.g. a demand path × grid × storage cross) by stacking overlays.

Automated build scripts generate the full scenario workbook set, including:

- demand-path variants (data-center growth paths),
- capacity-corridor (“funnel”) variants,
- interconnector expansion variants,
- storage cost/duration variants.

## Timeseries

Hourly profiles (demand shape, PV, wind onshore/offshore, hydro inflows) are
provided per **weather year** — 2012, 2015, 2017 and 2018 — as separate
timeseries workbooks. 2015 is the primary reporting weather year; the others
are used for weather-sensitivity analysis. The investment model samples every
49th hour of the chosen weather year; the dispatch model uses all 8,760 hours.

## Run configuration

Every run records its full switch configuration into the result database
(`output_switches`), so any result table can be traced back to the exact model
setup that produced it. Reruns with changed inputs receive a fresh scenario
label (versioned suffix) rather than overwriting an existing one.
