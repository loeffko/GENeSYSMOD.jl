# -*- coding: utf-8 -*-
"""Model-side content for the Canada scenario plan (2026-10-04): baseline of the frozen base run
fel2026_base_49_2015_v6f for the Canada node, the CER EF2026 comparison paths, model facts and levers.
All numbers were read from the model database (input_* / output_* tables) and from
GENeSYS-MOD.data/NA_inputs/canada_power_ef2026.xlsx on 2026-10-04."""

BASE_LABEL = 'fel2026_base_49_2015_v6f'
YEARS = (2025, 2030, 2035, 2040)

# busbar TWh, Canada node
DEMAND = [
    ('Power_General (industry + buildings)', 513.1, 518.1, 522.1, 525.2),
    ('Power_DataCenter', 17.1, 70.9, 177.9, 269.3),
    ('Power_BEVs', 3.2, 14.4, 37.0, 62.0),
    ('Power_Buildings_Heat', 11.8, 17.6, 25.4, 34.4),
    ('Power_Hydrogen (electrolysis)', 0.0, 2.5, 5.3, 8.5),
    ('TOTAL', 545.2, 623.7, 767.6, 899.4),
]

# GW: model result 2025/2030/2035/2040, corridor 2040 (min, max) from CER Current Measures x margins
CAPACITY = [
    ('Onshore wind (Avg class)', 19.1, 31.0, 60.3, 76.0, 50.6, 101.2),
    ('Onshore wind (Opt class)', 0.0, 0.0, 1.9, 11.2, 0.0, 24.8),
    ('Offshore wind (shallow / transitional / deep)', 0.0, 0.0, 0.0, 0.0, 0.0, '49 / 56 / 200 (potential, no minimum)'),
    ('Hydro reservoir', 59.3, 65.7, 70.1, 70.4, 64.0, 70.4),
    ('Hydro run-of-river', 25.4, 25.6, 27.3, 27.4, 27.4, 30.2),
    ('Solar utility (Avg + Inf + Opt)', 5.4, 11.1, 26.3, 58.2, 11.5, 95.0),
    ('Solar rooftop', 1.7, 3.4, 4.1, 3.6, 3.6, 7.3),
    ('Nuclear (large)', 12.9, 12.9, 15.0, 15.6, 15.6, 25.0),
    ('Nuclear SMR', 0.0, 0.0, 0.32, 0.32, 0.32, 0.32),
    ('Gas CCGT new', 0.0, 5.0, 10.0, 15.1, 15.1, 31.6),
    ('Gas CCGT existing', 20.1, 15.1, 10.0, 5.0, 0.0, 5.0),
    ('Gas OCGT', 5.2, 5.2, 5.2, 5.2, 5.2, 9.5),
    ('Gas steam + engines', 7.1, 5.4, 3.6, 1.9, 1.9, 13.0),
    ('Oil-fired', 3.8, 3.8, 3.0, 2.6, 2.6, 5.2),
    ('Biomass', 3.1, 3.1, 2.7, 2.7, 2.7, 5.4),
    ('Coal (lignite + hard coal)', 4.1, 2.9, 1.5, 1.5, 0.0, 1.5),
    ('Gas with CCS / hydrogen turbines / EGS', 0.0, 0.0, 0.0, 0.0, 0.0, 'forbidden in the base data (0.001 marker / 0)'),
    ('TOTAL generation', 167.2, 190.1, 241.4, 296.8, '', ''),
    ('Battery storage (Li-ion, power)', 1.6, 4.1, 5.2, 8.4, 8.4, 16.8),
]

GENERATION = [  # TWh
    ('Hydro', 386, 421, 449, 451), ('Wind', 53, 86, 175, 254), ('Nuclear', 88, 88, 105, 109), ('Solar', 10, 21, 44, 90),
    ('Gas', 91, 98, 70, 58), ('Coal', 13, 9, 5, 5), ('Net export to the US', 93, 96, 77, 66), ('Power-sector CO2, physical (Mt)', 43, 42, 29, 24),
]

INTERTIES = [  # partner, GW 2025, GW 2040 (maximum), net export TWh 2025, 2040
    ('MISO', 6.85, 6.85, 37.1, 19.0), ('NewYork', 4.63, 4.97, 36.1, 21.6), ('NewEngland', 2.40, 4.31, 17.6, 14.5),
    ('WECC', 3.15, 3.45, 1.8, 7.2), ('PJM', 0.0, 1.0, 0.0, 3.7), ('SPP', 0.20, 0.36, 0.4, -0.3),
]

# CER "Canada's Energy Future 2026", national, GW: 2025, 2030, 2035, 2040, 2050
CER_CAPACITY = {
    'Current Measures': [('TOTAL', 168.7, 193.7, 225.8, 243.7, 308.3), ('Wind', 19.1, 33.9, 55.2, 63.3, 91.5), ('Solar', 7.2, 14.5, 18.0, 18.9, 30.5),
                         ('Hydro', 84.7, 85.3, 91.1, 91.5, 91.5), ('Nuclear incl. SMR', 12.9, 11.0, 15.0, 15.6, 19.6), ('of which SMR', 0.0, 0.3, 1.5, 2.1, 6.1),
                         ('Natural gas incl. CCUS', 32.4, 34.2, 33.4, 36.6, 42.0), ('of which gas with CCUS', 0.0, 0.0, 0.5, 0.9, 7.4), ('Battery storage', 1.6, 4.5, 6.5, 10.5, 23.6)],
    'Higher': [('TOTAL', 168.7, 196.8, 244.8, 278.6, 359.5), ('Wind', 19.1, 36.4, 68.2, 87.2, 115.2), ('Solar', 7.2, 14.6, 20.1, 21.6, 37.8),
               ('Nuclear incl. SMR', 12.9, 11.0, 15.0, 15.6, 30.8), ('of which SMR', 0.0, 0.3, 1.5, 2.1, 17.3), ('Natural gas incl. CCUS', 32.4, 34.6, 36.2, 41.3, 45.9), ('Battery storage', 1.6, 4.5, 7.5, 14.0, 25.7)],
    'Lower': [('TOTAL', 168.7, 192.6, 217.4, 226.9, 269.6), ('Wind', 19.1, 32.6, 49.3, 55.2, 71.9), ('Nuclear incl. SMR', 12.9, 11.0, 15.0, 15.6, 16.5), ('Natural gas incl. CCUS', 32.4, 34.3, 32.8, 31.6, 38.4)],
    'Canada Net-zero': [('TOTAL', 168.9, 200.4, 252.4, 302.1, 402.4), ('Wind', 19.1, 39.6, 77.6, 113.5, 167.0), ('Solar', 7.4, 14.9, 17.5, 19.0, 32.0),
                        ('Nuclear incl. SMR', 12.9, 11.0, 15.0, 15.6, 24.8), ('of which SMR', 0.0, 0.3, 1.5, 2.1, 11.3), ('Natural gas incl. CCUS', 32.4, 34.4, 37.4, 38.7, 42.3), ('Battery storage', 1.6, 4.8, 7.0, 15.3, 29.0)],
}
CER_DEMAND = [  # electricity end-use demand TWh (gross end use, not busbar): 2025, 2030, 2035, 2040, 2050
    ('Current Measures', 567, 604, 661, 723, 814), ('Higher', 567, 627, 710, 806, 982), ('Lower', 567, 588, 624, 657, 713), ('Canada Net-zero', 567, 619, 719, 832, 1042),
    ('Current Measures: industrial', 229, 253, 283, 309, 337), ('Higher: industrial', 230, 262, 302, 338, 398),
    ('Current Measures: transport', 5, 13, 29, 45, 68), ('Canada Net-zero: transport', 6, 29, 72, 125, 203),
]
CER_GENERATION = [('Current Measures', 651, 704, 800, 881, 975), ('Higher', 651, 725, 860, 971, 1156), ('Canada Net-zero', 651, 726, 872, 1031, 1323)]
# CER Current Measures by province, GW: total 2025/2040/2050 | wind 2025/2040/2050 | nuclear | gas
CER_PROVINCES = [
    ('Quebec', '47.2 / 58.2 / 68.4', '4.1 / 10.3 / 15.3', '0 / 0 / 0.8', '0.6 / 0.6 / 0.1'),
    ('Ontario', '44.6 / 50.1 / 73.2', '5.8 / 5.8 / 16.3', '12.2 / 14.1 / 16.2', '11.8 / 12.7 / 12.1'),
    ('Alberta', '26.6 / 41.8 / 60.5', '5.8 / 13.4 / 21.8', '0 / 0 / 1.0', '15.0 / 16.3 / 21.6'),
    ('British Columbia', '20.2 / 36.5 / 41.0', '0.7 / 10.9 / 10.9', '0', '0.7 / 0.3 / 0.3'),
    ('Saskatchewan', '6.0 / 9.4 / 14.6', '0.8 / 3.0 / 5.2', '0 / 0.6 / 0.7', '2.7 / 3.9 / 4.2'),
    ('Manitoba', '6.6 / 7.3 / 7.5', '0.3 / 0.4 / 0.4', '0', '0.3 / 0.5 / 0.6'),
    ('Newfoundland and Labrador', '8.8 / 25.8 / 26.3', '0.1 / 13.1 / 13.5', '0', '0.3 / 0.3 / 0.3'),
    ('Nova Scotia', '3.3 / 7.8 / 9.3', '0.8 / 5.0 / 6.1', '0', '0.5 / 1.3 / 1.6'),
    ('New Brunswick', '4.6 / 5.2 / 5.3', '0.5 / 1.0 / 1.4', '0.7 / 0.9 / 0.9', '0.4 / 0.7 / 1.2'),
    ('Prince Edward Island', '0.4 / 0.8 / 1.4', '0.3 / 0.4 / 0.7', '0', '0'),
    ('Yukon + NWT + Nunavut', '0.6 / 0.7 / 0.7', '0', '0', '~0'),
]

MODEL_FACTS = [
    ('Geography', 'Canada is ONE node next to 9 US pools. No provinces, no territories, no off-grid systems: Alberta gas, Quebec hydro and northern diesel grids share one copper plate. Anything provincial enters as a national total.'),
    ('Horizon / resolution', 'Annual 2025-2040, 49-hour-step dispatch, weather year 2015. Nothing after 2040 is visible, so 2050 targets enter only through their 2040 waypoint.'),
    ('Base run', 'fel2026_base_49_2015_v6f = the July-2026 freeze (v6) plus bug fixes only. It is NOT changed by scenario work (user rule).'),
    ('Demand', 'FEL 2026 Power Demand Model, busbar TWh, five categories with their own hourly profiles (general, data centers flat, BEV charging, building heat, hydrogen flat). A sixth flat category Power_LargeLoads exists for scenario adders. Canada 2040: 899 TWh, of which data centers 269 TWh (30 %). CER EF2026 Current Measures end-use demand 2040: 723 TWh, i.e. the base is ~25 % above CER.'),
    ('Supply guardrails', 'Canada capacities follow CER EF2026 Current Measures inside a corridor: +-4 % to 2028, widening to -20 % / +60 % at 2035 (hydro +20 %), held to 2040. Minimum = forced build, maximum = cap. New CCGT (15 GW by 2040), nuclear (15.6 GW) and SMR (0.32 GW) sit exactly on their minimum, wind (87 GW) and solar (62 GW) are chosen inside the corridor.'),
    ('Base vs CER', 'Because the FEL demand is higher than CER, the base builds 297 GW of generation by 2040 (305 GW with batteries) against 244 GW in CER Current Measures and 302 GW in CER Net-zero. CER Current Measures reaches 308 GW only in 2050: the base already "doubles the grid" by 2040.'),
    ('Costs', 'LCOE-model capex in EUR2023/kW (2030): nuclear and SMR 10,000 (flat), onshore wind 1,150, offshore wind 2,393, CCGT 883, utility PV 380, hydro reservoir 2,100, Li-ion 160 /kW + energy part. Overnight capex x new capacity, discounted at 5 %; salvage value at the horizon end.'),
    ('Financing cost is not a lever', 'The technology discount rate only discounts cash flows (a higher rate makes a technology look cheaper). A WACC change must be converted into a capex multiplier via the annuity ratio CRF(new WACC, life) / CRF(5 %, life), e.g. 5 % -> 4.5 % over 30 years = x0.944.'),
    ('Build-rate limits', 'Per-technology annual investment caps are not a data sheet; build-rate caps are set as group limits (Par_GroupTotalAnnualMaxNewCap) with a technology subset and the region subset "Canada" (exists).'),
    ('Interconnectors', 'Canada-US: MISO 6.9, New York 4.6 -> 5.0, New England 2.4 -> 4.3, WECC 3.2 -> 3.5, PJM 0 -> 1.0, SPP 0.2 -> 0.4 GW (2025 -> 2040 maximum). No east-west grid inside Canada (one node).'),
    ('Policy', 'No CO2 price, no Clean Electricity Regulations constraint, no emission cap for Canada in the base (parameters exist, values are neutral). Gas with CCS, hydrogen turbines and EGS are switched off for Canada in the data.'),
    ('Adequacy', 'No active firm-capacity constraint (peaking constraint vacuous, reserve margin off); adequacy rests on the 49-hour energy balance. Capacity results of supply-push scenarios are therefore set by the minimum paths, not by a reliability rule.'),
    ('Run cost', '~25 min per investment run, serial (single database writer). A Canada set of 9 scenarios x 1-2 variants = 10-18 runs = 4-8 h.'),
]

LEVERS = [
    ('Demand path', 'Par_SpecifiedAnnualDemand rows for region Canada (Power_General, Power_DataCenter, Power_BEVs, Power_Hydrogen, Power_LargeLoads flat)', 'S1, S5, S6, S8, S9'),
    ('Forced capacity (minimum path)', 'Par_TotalAnnualMinCapacity Canada x technology x year (nuclear, SMR, wind, offshore wind, gas CCGT, hydro)', 'S1, S3, S5, S6, S7'),
    ('Capacity cap (maximum path)', 'Par_TotalAnnualMaxCapacity Canada x technology x year (corridor ceiling; removing it = "unleash")', 'S1, S3, S7'),
    ('Build-rate cap', 'Par_GroupTotalAnnualMaxNewCap (technology subset x region subset Canada x year)', 'S2, S4'),
    ('Capital cost', 'Par_CapitalCost Canada x technology x year (premium or discount; WACC effects via the annuity ratio)', 'S2, S3, S4, S7'),
    ('Timing shift', 'Corridor minimum/maximum paths shifted by N years for the affected technologies', 'S2, S4'),
    ('Interconnector capacity', 'Par_AnnualMaxTradeCapacity / Par_AnnualMinTradeCapacity Canada-US pairs', 'S1, S9'),
    ('Technology enable', 'Maximum capacity above the forbid marker for gas with CCS, hydrogen turbines, offshore wind minimum', 'S1, S7, S9'),
    ('CO2 price / cap', 'Par_EmissionsPenalty, Par_RegionalAnnualEmissionLimit for Canada (tested on the US in s14)', 'S1 (Clean Electricity Regulations variant)'),
]
