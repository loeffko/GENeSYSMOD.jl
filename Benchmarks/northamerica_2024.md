# Benchmark: North America (US + Canada) — actuals 2024

Reference for the standing base-case sanity check (CLAUDE.md `## Benchmarks`):
compare start-year model generation AND capacity by fuel group against this
table; flag deviations >15%. Model 2025 vs actuals 2024 => ~+2-3% growth is
inside the tolerance. Assembled 2026-07-13.

## Generation (TWh/yr)

| Group   | US 2024 | Canada 2024 | NA total | Source |
|---------|--------:|------------:|---------:|--------|
| Gas     |   1,851 |         102 |    1,953 | EIA EPM 2024; StatCan 2024 |
| Coal    |     653 |          18 |      671 | EIA EPM 2024; StatCan |
| Nuclear |     765 |          86 |      851 | EIA; WNA/StatCan |
| Hydro   |     236 |         343 |      579 | EIA; StatCan/CER |
| Wind    |    ~440 |          47 |     ~487 | EIA (wind+solar 17.2% share); CER |
| Solar   |     303 (incl ~80 small-scale) | 8 | ~311 | EIA |
| Other (bio/oil/geo) | ~67 | ~16 | ~83 | EIA; StatCan |
| **Total** | 4,304 | 623 | **4,927** | EIA; StatCan preliminary |

## Capacity (GW, end-2023/2024)

| Group   | US | Canada | NA total | Source |
|---------|---:|-------:|---------:|--------|
| Gas     | 507.5 | ~23 | ~530 | EIA (2023); CER residual |
| Coal    | 180.8 | ~6  | ~187 | EIA; CER |
| Nuclear |  95.1 | 12.7 | 107.8 | EIA; WNA |
| Hydro   |  79.7 | 83   | 162.7 | EIA; StatCan |
| Wind    | ~153  | 18.4 | ~171 | EIA/ACP 2024; CER |
| Solar (utility) | ~128 | ~7 | ~135 | EIA 2024 |

## Fleet capacity factors (sanity anchors)

| Fleet | Real CF | Note |
|---|---|---|
| US coal | ~42% | EIA 2023-24; old fleet, economics + maintenance — an AF near 0.8 lets the model run coal as baseload |
| US gas (all types) | ~42% | 1,953 TWh / ~530 GW |
| Nuclear | ~90% | |
| Hydro | ~41% | |
| Wind | ~33-34% | US fleet avg 2024 |
| Solar utility | ~24% | |

## Known model-vs-history caveats (v5a-era)

- Model omits: US biomass (~47 TWh), petroleum (~20), most geothermal, and
  residential rooftop PV beyond the commercial class -> "Other" always reads low.
- Wind gen runs ~+15% hot (Opt-class CF 39.5% vs fleet 34%).
- 2026-07 incident: World coal AF 0.80 let coal run at 78% CF (real ~42%),
  displacing ~570-600 TWh of gas. Fixed via US-pool coal AF rows (0.45).


## Scope adjustment — behind-the-meter generation (compare like-for-like!)

The model's FEL demand is BUSBAR (net of BTM), so grid-scale model generation
must be compared against EIA all-sector values MINUS the BTM part
(BTM_Generation_Mix_Capacity_v06.xlsx, Calc, 2025, regional rows):

| BTM 2025 | TWh |
|---|---|
| gas-fired CHP (chp_gas + process gas + DC gensets) | ~269 |
| industrial biomass CHP | ~64 |
| rooftop solar+BESS (beyond commercial) + industrial solar | ~127 |
| coal CHP | ~16 |
| all BTM | ~499 |

Scope-adjusted 2025 targets: gas ~1,684 TWh (v6 model: 1,661, -1.4% OK);
biomass grid-visible well below the 55 all-sector value (model 42 OK);
solar benchmark ex small-scale ~240 (model 272, +13% OK).
