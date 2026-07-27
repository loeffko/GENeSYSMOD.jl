# Model & Methods

## Framework

The North America model is built on **GENeSYS-MOD.jl**, the Julia/JuMP port of
the Global Energy System Model (GENeSYS-MOD, originally implemented in GAMS and
based on the OSeMOSYS framework). The model is a **linear program**: it
minimizes total discounted system cost over the full horizon subject to energy
balances, capacity constraints, ramping, storage dynamics, trade, emission
accounting, and policy constraints.

Key structural properties:

- **Perfect foresight** over 2025–2040 with every year modelled.
- **Technology-rich**: thermal fleets (gas CCGT/OCGT/steam/engines, hard coal,
  lignite, nuclear incl. SMR, oil, biomass), renewables in resource classes
  (utility PV optimal/average/inferior + commercial rooftop; onshore wind in
  three classes; offshore wind shallow/transitional/deep; hydro run-of-river
  and reservoir; enhanced geothermal in four supply-cost tiers), and four
  storage technologies (Li-ion battery, redox-flow battery, CAES,
  pumped hydro).
- **Trade** between regions via net-transfer-capacity interconnectors with
  endogenous expansion.
- **Feasibility slack**: a high-cost backstop technology (`Infeasibility_Power`)
  keeps the LP feasible under extreme stress; runs are validated against its
  usage (see below).

## Two-stage setup: investment + dispatch

The North America workflow separates capacity expansion from operational
analysis:

1. **Investment model** — full horizon (2025–2040), reduced chronological time
   resolution (every 49th hour of the weather year, preserving the diurnal and
   seasonal structure). Decides capacity expansion, storage build-out,
   interconnector expansion, and yearly operation. Solved with Gurobi
   (barrier).
2. **Dispatch model** — takes the investment model's fleet (capacities,
   storage, interconnectors, demand) for selected years and re-solves the
   operation at **full hourly resolution (8,760 h)** with a market-realism
   layer:
     - **Must-run / minimum activity** shares for nuclear, coal, and hydro
       fleets (fleet inflexibility, self-scheduling).
     - **Production-incentive bid adders** (PTC-style): subsidized renewables
       bid at negative prices; curtailment is priced at the deepest adder.
     - **Regional value of lost load (VoLL)** for unserved energy.
     - **Operating-reserve demand curves (ORDC-lite)**: stepped scarcity
       adders tied to reserve headroom of dispatchable and storage capacity.
     - **Fuel price structure**: monthly shape factors plus a year-specific
       fuel-price path (Henry-Hub-based for gas).
     - **Storage duration bins**: the aggregate battery fleet is split into
       1/2/4/8-hour duration tranches with year-specific shares, each with an
       independent state of charge (see
       [Regions: North America](regions-north-america.md#storage)).

Hourly zonal prices are read from the duals of the energy balance; scarcity and
reserve events appear as price spikes, PTC bidding as negative price hours.

## Validation & quality gates

Every production run passes through a fixed validation pipeline:

- **Input error checking** — an automated pre-solve check of the input data
  (missing mappings, inconsistent parameter combinations, unit plausibility);
  hard violations abort the run.
- **Feasibility gate** — a run only counts as clean if the solver reports
  optimality **and** the infeasibility backstop generation stays below a small
  threshold (a few TWh, attributable to known start-year artifacts). This
  guards against formally optimal solutions that hide infeasibility in the
  slack technology.
- **Historic benchmarking** — after every base-case rerun, the start-year
  generation mix and capacities by fuel are compared against published
  statistics (EIA for the US, CER for Canada); any fuel deviating by more than
  15 % is investigated before results are used. See
  [Regions: North America](regions-north-america.md#calibration-and-benchmarking).
- **Infeasibility diagnosis** — when a configuration is infeasible, a
  low-resolution probe (same workbook, coarse timeseries) reproduces the
  conflict in minutes and computes an irreducible infeasible subsystem (IIS)
  to locate the conflicting constraints.

## Solver configuration

- **Gurobi** barrier method, parallelized; crossover enabled for runs where
  clean basis solutions / duals matter (price analysis), disabled for speed
  otherwise.
- Model sizes: the investment LP solves in the order of hours; a full-year
  dispatch solves in the order of 15–60 minutes per year depending on
  configuration.
