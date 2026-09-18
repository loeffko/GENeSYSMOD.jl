# -*- coding: utf-8 -*-
"""Model-side content for the 14-scenario plan (levers, routes, feasibility). Research data is added separately."""

BASELINE = {
 # US = 9 US pools (busbar TWh, FEL26 base as loaded in fel2026_base_49_2015_v6c); CA = Canada
 'Power_General':          {'US': {2025: 3316, 2030: 3492, 2035: 3944, 2040: 4369}, 'CA': {2025: 513, 2030: 518, 2035: 522, 2040: 525}},
 'Power_DataCenter':       {'US': {2025: 133, 2030: 726, 2035: 1344, 2040: 1817},  'CA': {2025: 17, 2030: 71, 2035: 178, 2040: 269}},
 'Power_Buildings_Heat':   {'US': {2025: 764, 2030: 735, 2035: 710, 2040: 709},    'CA': {2025: 12, 2030: 18, 2035: 25, 2040: 34}},
 'Power_Hydrogen':         {'US': {2025: 2, 2030: 6, 2035: 6, 2040: 6},            'CA': {2025: 0, 2030: 3, 2035: 5, 2040: 9}},
 'Power_BEVs':             {'US': {2025: 25, 2030: 71, 2035: 213, 2040: 442},      'CA': {2025: 3, 2030: 14, 2035: 37, 2040: 62}},
}
DC_BY_REGION = {'California': (4.7, 9.2, 26.8), 'Canada': (17.1, 70.9, 269.3), 'ERCOT': (15.6, 268.6, 630.5), 'MISO': (14.2, 53.8, 146.2),
 'NewEngland': (0.7, 0.7, 1.2), 'NewYork': (0.0, 5.4, 12.8), 'PJM': (46.4, 205.9, 552.9), 'SERC': (13.3, 63.4, 167.8), 'SPP': (9.2, 72.9, 171.3), 'WECC': (29.3, 46.0, 107.7)}
EXISTING = {
 'dc_high': 'DC US 2035/2040 = 2188/3585 TWh; funnel max raised with ratio', 'dc_low': 'DC US 2035/2040 = 805/874 TWh; gas min floor 0',
 'recession': 'GDP-recession FEL demand: DC 1048/1563, General -1..2 %', 'btm_lag': 'DC 1526/2163 (BTM lag -> more grid load)',
 'economic': 'funnel widened after 2030 (min x0.75, max x1.5)', 'grid_high/grid_low': 'IC growth 2x budget / capped 0.75 %/yr',
 'bess_optimistic/pessimistic': 'Li-ion cost x0.4 by 2040 + 7 h / min blend x0.53', 'nuclear_announced (+ccgtrelax)': '+19.1 GW announced nuclear (large+SMR) by 2035 on top of the corridor, CCGT min relaxed',
 'space_dc / disruptive / spacex': 'orbital compute REMOVES 5 / 13 / 27 % of US DC load by 2040 (1724/1585/1353 TWh)',
 'gas (NorthAmerica_gas)': 'explicit gas supply, pipelines, LNG exports, storage, deliverability caps; endogenous regional gas prices',
}
MODEL_FACTS = [
 ('Geography', '9 US pools (California, WECC, ERCOT, SPP, MISO, SERC, PJM, NewYork, NewEngland) + Canada as ONE node; no state or province resolution.'),
 ('Horizon / resolution', 'Annual 2025-2040, 49-hour-step dispatch (179 slices), one weather year (2015). Nothing after 2040 is visible.'),
 ('Demand categories', 'Power_General, Power_DataCenter, Power_Buildings_Heat, Power_Hydrogen, Power_BEVs (Power_Buildings_Cooling exists but is empty). Each has its own hourly profile: BEV (charging shape), Buildings_Heat and Buildings_Cooling are real profiles; DataCenter and Hydrogen are FLAT (no electrolysis flexibility, no DC load-following).'),
 ('Demand source', 'FEL 2026 Power Demand Model workbook (base_fel_v260707_v2.xlsx: sectors buildings / industry / transport / hydrogen / data_centers, sub-segments, busbar TWh per pool) converted by NA_inputs/convert_fel_to_demand.py. Demand scenarios are best produced as FEL presets (bev_share, dc_scenario, hydrogen_scenario, industry_electrification_*, gdp_growth); fallback = scaling sub-segments on our side.'),
 ('Supply guardrails', 'Capacity funnels from the US Pools announced pipeline (TotalAnnualMin/MaxCapacity, +-2 % to 2028 widening to -10 %/+30 % at 2035), gas retirement schedule, IC trade growth 4 %/yr, RES potentials (restool). SMR: 0 before 2033, 2.9 GW 2035, 18.7 GW 2040 max. P_Gas_CCS, P_Geothermal (conventional), P_CSP, P_H2_OCGT: capacity max 0 (disabled). EGS classes, Li-ion (max 120->404 GW), Redox flow (from 2030), CAES, PHS available.'),
 ('Costs', 'LCOE model v1.4 capex/FOM/WACC-as-discount-rate (5 % uniform). Capex 2025 EUR/kW: CCGT 827, OCGT 691, nuclear and SMR 9091 (flat), gas CCS 2593, PV 427, onshore 1073, Li-ion 195 /kW + 964 M EUR/PJ. Fuel: Henry-Hub path folded into gas VariableCost (3.7/4.8/4.8/4.4 EUR/GJ 2025/30/35/40), regional hub factors (Canada).'),
 ('Emissions / policy', 'No CO2 price and no emission cap in the NA data (parameters EmissionsPenalty, AnnualEmissionLimit, RegionalAnnualEmissionLimit exist but are sentinels). No RPS/CES constraints. 45Q/45V/45Y not represented.'),
 ('Gas infrastructure', 'Optional NorthAmerica_gas data scenario (2026-09-15): R_Gas regional supply curves, 30 pipeline corridors, LNG export demand, storage, deliverability caps -> endogenous regional gas prices (2.3-3.3 EUR/GJ, i.e. below the folded HH path).'),
 ('Run cost', '~1 h per 49-hour-step investment run (build 15 min + solve 12-55 min), single DuckDB writer -> serial runs. 14 scenarios x 1-2 variants = 20-30 runs = 1-2 days.'),
 ('Basis', 'v6 (frozen July 2026, code-consistent baseline fel2026_base_49_2015_v6c) or v7 (LCOE v1.4 costs, RES cost re-anchoring; user still reviewing RES capacity shifts). Decision needed before implementation.'),
]
