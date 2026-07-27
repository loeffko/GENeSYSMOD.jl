# Regions: North America

The North America application models the contiguous United States and Canada
in **ten regions**, chosen to follow the real electricity-market and
reliability geography (ISO/RTO footprints and interconnection structure)
rather than state borders.

## Regional setup

| Model region | Corresponds to |
|---|---|
| `California` | CAISO |
| `WECC` | Western Interconnection excl. California (NW, Mountain, Southwest) |
| `ERCOT` | Texas interconnection |
| `SPP` | Southwest Power Pool |
| `MISO` | Midcontinent ISO |
| `SERC` | Southeast (non-RTO SERC utilities, FRCC) |
| `PJM` | PJM Interconnection |
| `NewYork` | NYISO |
| `NewEngland` | ISO New England |
| `Canada` | Canada (aggregated) |

Regions are connected by net-transfer-capacity interconnectors with endogenous
expansion (see [Grid & trade](#grid-trade)). Within a region the model takes
a **busbar perspective**: a single zonal balance without intra-regional
network constraints.

## Scope

- **Power sector only (phase 1).** Demand for electricity is exogenous per
  region, year, and end-use carrier (general load, data centers, building
  heat electrification, electric vehicles, hydrogen production). Other sectors
  (heat, transport fuels, industry) are not co-optimized in this phase.
- **Busbar accounting.** The model balances utility-scale (busbar) supply and
  demand. Behind-the-meter generation that never crosses the meter — most
  prominently industrial/commercial gas CHP (≈ 270 TWh/yr in the US) — is
  outside the model boundary; benchmark comparisons against all-sector
  statistics are adjusted accordingly.
- **Horizon** 2025–2040 with every year modelled; perfect foresight.

## Assumptions

### Demand

- Start year ≈ **4,800 TWh** (US + Canada, busbar). The base path reaches
  ≈ **8,260 TWh in 2040**, driven by data-center growth, electrification of
  buildings and transport, and hydrogen production.
- Demand is decomposed into carriers (`Power_General`, `Power_DataCenter`,
  `Power_Buildings_Heat`, `Power_BEVs`, `Power_Hydrogen`) so that demand
  scenarios can scale a single driver — the DC-High / DC-Low scenarios move
  2040 demand to +22 % / −14 % of base almost entirely via the data-center
  carrier (see [Scenarios](scenarios.md)).
- Hourly demand shape follows the weather-year profile per region.

### Thermal fleets

- **Existing fleets** enter as residual capacities with technology-specific
  lifetimes; retirements are endogenous (economic) unless pinned by policy
  assumptions.
- **Coal**: the annual availability factor is set to the observed **fleet
  capacity factor (~45 %)** rather than technical availability. In a linear
  model the availability factor acts as the annual fleet-CF cap, and technical
  availability (~80 %) would let coal displace gas far beyond observed
  operation. This single assumption aligns the start-year coal/gas split with
  statistics (without it, ~600 TWh migrate from gas to coal).
- **Gas** is represented by four technologies (CCGT, OCGT, steam, engines)
  with separate cost/efficiency profiles; new-build corridors keep expansion
  within observed construction pipelines in the early years.
- **Nuclear** runs quasi-must-run in dispatch (92 % minimum activity);
  **biomass** is modelled as a CHP-anchored fleet: capacity fixed at the
  observed US fleet (≈ 11 GW net summer), 50 % availability, and a minimum
  activity floor reflecting that most of the fleet is industrial CHP that
  runs regardless of wholesale prices.

### Renewables

- PV and wind are split into **resource classes** (optimal / average /
  inferior sites, plus commercial rooftop PV) with class-specific profiles
  and potentials; offshore wind into shallow / transitional / deep water.
- **Offshore wind build-out floors**: New York, New England, and PJM carry
  minimum offshore trajectories from state/regional procurement plans — the
  conservative (Low) case until 2030 and the Central case from 2031 — totaling
  ≈ 20 GW US offshore by 2040. Offshore, geothermal, and biomass are treated
  as policy/externally-driven technologies and exempted from the economic
  capacity corridors.
- **Enhanced geothermal (EGS)** enters in four supply-cost tiers with
  region-specific potentials.

### Storage

- Four technologies: Li-ion batteries (power and energy sized separately),
  redox-flow, CAES, pumped hydro (existing).
- **Battery duration is data-driven**: an energy-to-power ratio path pins the
  fleet-average duration (≈ 1.5 h in 2025 → 3.5 h in 2040 in the base case)
  with ±10 % flexibility. Storage-cost scenarios move this path (7 h
  optimistic, ≈ 2.9 h pessimistic).
- In **dispatch**, the aggregate battery fleet is split into 1/2/4/8-hour
  duration bins with year-specific shares (2025: 70/20/10/0 → 2035:
  45/25/20/10 → 2040: 30/20/30/20 %), each tranche with an independent state
  of charge. This reproduces the observed duration mix and prevents the
  aggregate fleet from behaving like a single long-duration battery.

### Grid & trade

- Interconnector capacities start from today's transfer capabilities and can
  be expanded endogenously subject to growth-rate limits reflecting
  permitting and construction reality.
- Grid scenarios vary this: a **low-grid** variant caps expansion at
  0.75 %/yr; a **high-grid** variant replaces per-corridor growth limits with
  an **aggregate national wire budget** (interconnector capacity may double
  by 2040, allocated freely across corridors by the optimizer).

### Capacity corridors ("funnels")

To keep near-term expansion within industrial reality, each major
technology-region pair carries a **capacity corridor**: minimum and maximum
trajectories around reference expectations that widen over time. The base
corridor encodes announced pipelines and conservative continuation; scenario
variants widen it (economic build: min ×0.75 / max ×1.5 by 2035) or reshape
it (grid-oriented builds). Externally-driven technologies (offshore wind,
EGS, biomass) sit outside the corridors.

### Dispatch market layer

- **Must-run minimums** (share of available capacity): nuclear 92 %; coal
  50/40/20 % (MISO / SPP / other regions); hydro 15 %.
- **Bid adders**: production-incentive (PTC-style) adders let subsidized wind
  and solar bid negative; curtailment is priced at the deepest adder, so
  negative price hours emerge endogenously (≈ 2–4 % of hours in 2040 runs).
- **Scarcity pricing**: regional VoLL for unserved energy plus an ORDC-lite
  stepped reserve-scarcity adder (tightest in ERCOT), tied to dispatchable +
  storage headroom.
- **Gas price path**: Henry-Hub-based trajectory
  (≈ 11.9 → 12.8 → 11.2 → 9.5 → 9.5 → 10.2 €/MWh(th) at the 2025–2040
  milestones) with monthly shape factors; other fuels use annual prices with
  monthly factors.

### Emissions & policy

- CO₂ accounting per region and technology with weighted emission factors;
  the coal fleet distinguishes hard coal and lignite.
- Technology-push policies are represented structurally (PTC bid adders in
  dispatch, offshore procurement floors, corridor minimums) rather than as a
  single carbon-price trajectory.

## Sources

| Area | Source |
|---|---|
| US generation, capacity, fleet CFs, fuel use | EIA (Electric Power Annual, Form EIA-860/923, Short-Term Energy Outlook) |
| Canada | CER — Canada's Energy Future |
| Benchmark start-year mix (2024) | EIA / CER published statistics (see repository `Benchmarks/`) |
| Storage technology costs | DEA Technology Data catalogue (converted to model units), cross-checked against US cost studies |
| Offshore wind trajectories | State/regional procurement plans and project pipelines (NY, NE, PJM; Central/Low build-out cases) |
| Gas prices | Henry Hub futures/outlook-based projection (converted to €/MWh thermal) |
| Bid adders | US production tax credit (IRA) levels |
| Market-layer calibration | Historic ISO price statistics (ERCOT, CAISO, PJM day-ahead LMPs: levels, spread, negative-hour frequency) |
| Hourly profiles | Region-specific weather-year timeseries (2012/2015/2017/2018) for demand shape, PV, wind, hydro |

## Methods (region-specific)

### Calibration and benchmarking

The start year is calibrated against observed 2024 statistics: generation by
fuel (gas ≈ 1,950 TWh, coal ≈ 670 TWh, nuclear ≈ 850 TWh, hydro ≈ 580 TWh,
wind ≈ 490 TWh, solar ≈ 310 TWh for the US) and capacity by fuel. After every
base-case rerun, both are re-checked automatically and **any fuel deviating
by more than 15 % is investigated** before the run is used. Known scope
differences (behind-the-meter CHP under the busbar boundary) are documented
as explicit benchmark adjustments rather than hidden in calibration.

### Fleet-level representation

The model works with regional fleets, not units. Fleet behaviour that emerges
from unit commitment in reality (must-run, minimum stable generation,
self-scheduling) is represented by linear minimum-activity constraints
calibrated to observed fleet operation — the coal availability-as-CF
assumption and the dispatch must-run shares are the two main instances.

### Weather sensitivity

All scenario results are produced against the 2015 weather year; selected
scenarios are re-run against 2012, 2017, and 2018 to separate weather-driven
variance (hydro, wind droughts, demand shape) from structural scenario
differences.

### Known limitations

- Busbar scope: behind-the-meter generation and distribution-level effects
  are outside the model.
- Copper-plate regions: intra-regional congestion is not represented; interface
  limits exist only between the ten regions.
- Linear fleets: no unit commitment, start costs, or minimum up/down times in
  the LP; the dispatch market layer approximates their price effects.
- The peaking-capacity adequacy constraint is calibrated for corridor-shaped
  fleets; strongly cost-optimized fleets can carry dispatch-level scarcity
  (visible as unserved-energy tails in stress scenarios).
