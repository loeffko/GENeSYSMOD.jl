# GENeSYS-MOD North America

This site documents the **North America application of GENeSYS-MOD.jl**, an
open-source linear energy system optimization model. The North America model
covers the contiguous US power system plus Canada in ten regions, optimizes
capacity expansion and dispatch from **2025 to 2040**, and is used to study
demand growth (in particular data-center-driven load), transmission expansion,
storage build-out, and market outcomes.

## Quick facts

| | |
|---|---|
| Framework | [GENeSYS-MOD.jl](https://github.com/GENeSYS-MOD/GENeSYS_MOD.jl) (Julia / JuMP, linear program) |
| Scope | Power sector (phase 1), busbar perspective |
| Regions | 10 — California, WECC, ERCOT, SPP, MISO, SERC, PJM, New York, New England, Canada |
| Horizon | 2025–2040, every year modelled (16 periods) |
| Time resolution | Investment: reduced chronological timeseries (every 49th hour); Dispatch: full 8,760 h |
| Weather years | 2012, 2015 (primary), 2017, 2018 |
| Demand 2025 | ≈ 4,800 TWh (US + Canada, busbar) |
| Demand 2040 | Base ≈ 8,260 TWh · DC-High +22 % · DC-Low −14 % |
| Solver | Gurobi (barrier); HiGHS supported |

## How this documentation is organised

- **[Model & Methods](model.md)** — the optimization framework, the two-stage
  investment/dispatch setup, and the validation pipeline.
- **[Data & Workflow](data.md)** — how input data flows from per-parameter CSV
  files to model workbooks, and how scenario variants are managed.
- **[Regions: North America](regions-north-america.md)** — the regional setup
  with all region-specific **assumptions, sources, and methods**.
- **[Scenarios & Sensitivities](scenarios.md)** — the scenario tree: demand
  paths, grid variants, storage variants, and their combinations.
- **[Results & Databases](results.md)** — output formats, database schema, and
  naming conventions.

!!! note "Model generation"
    This documentation describes the **v6** model generation (frozen July 2026).
    Scenario labels in the result databases follow the pattern
    `fel2026_<scenario>_<resolution>_<weatheryear>_v6`.
