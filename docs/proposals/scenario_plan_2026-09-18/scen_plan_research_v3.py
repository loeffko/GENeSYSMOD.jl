# -*- coding: utf-8 -*-
"""Plan v3 (2026-09-22): v2 + user decisions (v6 basis; scenario numbers used even where the base is
already higher, flagged; existing sensitivities reused for numbers only - the 14 are separate runs),
fusion from Fusion_Market_Model_v09.xlsx, and the implemented wave-1 variant per scenario."""
import copy
from scen_plan_research_v2 import SCENARIOS as _S2, ASSUMPTIONS as _A2, SOURCES as _SRC2, OPEN_QUESTIONS as _Q2

# --- implementation record per scenario (wave 1)
IMPL = {
 1: ('1A', 'NorthAmerica_s01_ev', 'fel2026_s01_ev_49_2015_v6', 'Power_BEVs rescaled to the AEO2026 path (base regional shares), Canada CER net-zero.'),
 2: ('2A', 'NorthAmerica_s02_h2', 'fel2026_s02_h2_49_2015_v6', 'Power_Hydrogen 10/27/165/333 TWh by hub shares (ERCOT 35, PJM 25, MISO 20, CA 10, SPP 5, WECC 5 %); Canada 25/52/80. Flat profile (2D flexible electrolysers not built).'),
 3: ('3A', 'NorthAmerica_s03_compute', 'fel2026_s03_compute_49_2015_v6', 'DC base->1,450 (2035)->2,230 TWh (2040), Canada by ratio; new flat fuel Power_LargeLoads for crypto/robotics/telecom adders (X_Convert_Power mode 7, profile POWER_DATACENTER).'),
 4: ('4C (terrestrial only)', 'NorthAmerica_s04_space', 'fel2026_s04_space_49_2015_v6', 'Power_LargeLoads 5/35/155 TWh (2030/35/40) in ERCOT 50 / CA 20 / SERC 20 / WECC 10 %; orbital-compute displacement NOT applied (space_dc trio stays a separate analysis).'),
 5: ('5A', 'NorthAmerica_s05_brakes', 'fel2026_s05_brakes_49_2015_v6', 'Regional DC multipliers on the post-2026 increment; GasPlants USA new-build cap 10 GW/yr 2027-31 (group cap); gas guardrail minimum = residual; RES rep funnel max without the x1.30 widening.'),
 6: ('6C', 'NorthAmerica_s06_hormuz', 'fel2026_s06_hormuz_49_2015_v6', 'Fuel leg via a scenario allFuels workbook (Z_Import_Gas +10 % 2026, +2 USD/MMBtu 2027-29, +1 in 2030); macro leg: capex x1.35 (2026-28) / x1.18 (2029-30) / x1.09 (2031) - equipment +15 % and WACC +150 bp folded via CRF (TechnologyDiscountRate has no year dimension); IC max = grid_low rows 2026-30; recession-FEL demand 2026-30 blended back by 2033.'),
 7: ('7C', 'NorthAmerica_s07_tech', 'fel2026_s07_tech_49_2015_v6', 'SMR max 2/5/15/40 GW (2030/32/35/40), capex 5,090->3,330 EUR/kW; iron-air D_IronAir/S_IronAir (100 h, RTE 45 %, 60->20 USD/kWh, NA build cap 0.5->5 GW/yr); Li-ion optimistic rows reused; P_Fusion bull ramp min = max = 2.0/4.25/6.75/9.5 GW (2034/36/38/40).'),
 8: ('8A (flagged below base)', 'NorthAmerica_s08_canada', 'fel2026_s08_canada_49_2015_v6', 'Canada DC 41/130/220 TWh (pipeline-consistent) - BELOW the FEL base 71/178/269; used as instructed and flagged. BYOP CCGT minimum +0.25/+1.18/+2.58 GW (2028/30/33) on the base Canada minimum (which already forces 15 GW by 2040).'),
 9: ('9C', 'NorthAmerica_s09_water', 'fel2026_s09_water_49_2015_v6', 'Power_LargeLoads 4/18/36 TWh (2030/35/40) WECC 40 / CA 30 / ERCOT 20 / SERC 10 %.'),
 10: ('10C', 'NorthAmerica_s10_climate', 'fel2026_s10_climate_49_2015_v6', '10 % (2035) / 20 % (2040) of SERC+ERCOT+CA General and DC load moved to MISO/PJM/NE/NY/WECC by load share; Sunbelt cooling +8 % by 2040; rebuild +1 %; coastal IC cost x1.5; coastal gas+nuclear availability -5 pp from 2030. Peaking-reserve uplift not applied (global switch).'),
 11: ('11A', 'NorthAmerica_s11_feoc', 'fel2026_s11_feoc_49_2015_v6', 'Li-ion capex x1.44 (2026) -> x1.05 (2035); PV x1.02 2026-30; IC cost x1.2 whole horizon (no year dimension); LiIon USA cap 17 GW/yr 2026-27 (group cap).'),
 12: ('12A', 'NorthAmerica_s12_overbuild', 'fel2026_s12_overbuild_49_2015_v6', 'DC 540/620/690 TWh (2030/35/40), Canada by ratio.'),
 13: ('13A', 'NorthAmerica_s13_reindustrial', 'fel2026_s13_reindustrial_49_2015_v6', 'Power_LargeLoads by project (fabs WECC/NY/ERCOT/PJM, smelter SPP, ERCOT non-DC queue 25 %, stylised MISO/SERC).'),
 14: ('14A', 'NorthAmerica_s14_decarb', 'fel2026_s14_decarb_49_2015_v6', 'US CO2 price 30/60/90 USD/t (2029/35/40) with the penalty tag extended to gas plants; RES+storage capex x0.7 from 2029; P_Gas_CCS 2/15/40 GW with 45Q as -7.95 MEUR/PJ; nuclear_announced minima + UPRISE uprates; regional CO2 caps NY/NE/CA/PJM.'),
}

SCENARIOS = []
for s in copy.deepcopy(_S2):
    var, folder, label, how = IMPL[s['id']]
    s['implemented'] = f'{var} -> data scenario {folder}, run {label}. {how}'
    SCENARIOS.append(s)

# scenario 7: fusion now from the user's workbook
for s in SCENARIOS:
    if s['id'] == 7:
        s['meaning'] = s['meaning'].replace('FUSION CAPEX: to be supplied by the user (placeholder rows in Assumptions).',
            'FUSION from Fusion_Market_Model_v09.xlsx (SE, 2026-07-27): bull case = FOAK 2034, 5 developers, Class IV x0.7, capex 21,700 (N1) -> 9,229 EUR/kW (N4, 2040), FOM 2 %/yr, VOM 10 EUR/MWh, CF 0.88, life 60 yr, WACC 7 %; backed ramp 2.0/4.25/6.75/9.5 GW by 2034/36/38/40 (base case: FOAK 2036, 4.05 GW by 2040).')
        s['evidence'] = 'Medium-High for SMR/LDES (INL/ATB cost bands, project pipeline, Form/Eos numbers); fusion = SE market model v09 (all shipped numbers marked placeholders by its author)'
        s['concerns'] = [c for c in s['concerns'] if 'come from the user' not in c[2]]
    if s['id'] == 8:
        s['flag_summary'] += ' USER RULE: the scenario numbers are used even though the FEL base is higher; flagged in the results.'

# --- assumptions: drop the fusion USER INPUT placeholders, add the workbook rows + implementation notes
ASSUMPTIONS = [a for a in _A2 if not (a[0] == 7 and ('P_Fusion' in str(a[3]) or str(a[11]).startswith('User')))]
ASSUMPTIONS += [
 (7,'Tech breakthrough','7C (implemented)','P_Fusion CapitalCost','World (all NA)','2034 / 2036 / 2038 / 2040','21,700 / 16,619 / 12,555 / 9,229 (flat 21,700 before 2034, interpolated between)','EUR/kW','Fusion_Market_Model_v09.xlsx capex sheet: all-in overnight N1 31,000, N2 23,742, N3 17,935, N4 13,184 EUR/kW x Class IV factor 0.7 (bull); reactor N at 2034/36/38/40 (bull commercialization 2034, one reactor per developer every 2 yr).','FUSION-V09','Medium','No'),
 (7,'Tech breakthrough','7C (implemented)','P_Fusion FixedCost / VariableCost / CF / life / WACC','World','2034-2040','FOM 2 % of capex per yr; VOM 10 EUR/MWh (2.78 MEUR/PJ); CF 0.88; 60 yr; discount rate 7 %','-','Fusion_Market_Model_v09.xlsx inputs sheet, bull column (fixed_om_pct_of_capex 0.02, variable_om 10, capacity_factor 0.88, plant_life 60; wacc base 0.07).','FUSION-V09','Medium','No'),
 (7,'Tech breakthrough','7C (implemented)','P_Fusion TotalAnnualMin = Max (backed ramp)','PJM 40 %, WECC 20 %, SERC 20 %, California 10 %, ERCOT 10 %','2034 / 2036 / 2038 / 2040','2.0 / 4.25 / 6.75 / 9.5 (cumulative)','GW','foak_ramp sheet: 5 developers x 400/450/500/550 MW; must-build (the ramp is "backed" in the workbook logic); 100 % located in NA at announced sites (assumption).','FUSION-V09','Medium','Partly (NA share, sites)'),
 (7,'Tech breakthrough','context','Fusion base case (not run)','-','2036-2040','FOAK 2036, 3 developers, capex x1.0: 1.2/2.55/4.05 GW by 2036/38/40 at 31,000 -> 17,935 EUR/kW','-','Fusion_Market_Model_v09.xlsx base column; bear = 2045 (outside the horizon).','FUSION-V09','Medium','No'),
 (6,'Hormuz','6C (implemented)','Capex multiplier (all generation + storage)','World + NA rows','2026-28 / 2029-30 / 2031','x1.35 / x1.18 / x1.09','factor','WACC +150 bp cannot be time-varied (Par_TechnologyDiscountRate has no year dimension) -> folded into capex via CRF(6.5 %, 30 yr)/CRF(5 %, 30 yr) = 1.18, on top of the +15 % equipment inflation 2026-28.','WM-TURB; GRIDLAB-25; OECD-26','Low','Partly'),
 (6,'Hormuz','6C (implemented)','Folded gas price (scenario allFuels workbook)','all','2026 / 2027-29 / 2030','+10 % / +2 USD/MMBtu (+1.754 MEUR/PJ) / +1 USD/MMBtu','-','Z_Import_Gas VariableCost in RegularParameters_NorthAmerica_allFuels_v6_s06.xlsx; base HH path 3.7/4.8/4.8/4.4 MEUR/PJ.','IMF-WEO26; EIA-STEO26','Low','Partly'),
 (11,'FEOC / BPS','11A (implemented)','TradeCapacityGrowthCosts (NA Power pairs)','all NA corridors','whole horizon','x1.2','factor','Parameter has no year dimension: mean of the intended x1.30 (2026-30) -> x1.10 (2035) path.','WM-TRAFO','Low','Partly'),
 (10,'Climate relocation','10C (implemented)','AvailabilityFactor coastal gas + nuclear','SERC, ERCOT, California, NewYork, NewEngland','2030-2040','-5 pp (regional rows derived from the World rows)','pp','Storm-outage proxy.','CC-26','Low','Yes'),
 (0,'all','implementation','Run basis','all','-','v6 freeze (RegularParameters_NorthAmerica_v6freeze + Timeseries_NorthAmerica_2015 + allFuels_v6), reference run fel2026_base_49_2015_v6c (= v6d regression)','-','User decision 2026-09-22: runs are always v6-based.','-','High','No'),
 (0,'all','implementation','Reuse of existing sensitivities','-','-','numbers reused (grid_low IC rows in s06, bess_optimistic rows in s07, nuclear_announced rows in s14, recession demand in s06); each of the 14 is its own data scenario and run','-','User rule 2026-09-22.','-','High','No'),
]

SOURCES = list(_SRC2) + [
 ('FUSION-V09','SE (user)','Fusion_Market_Model_v09.xlsx - Fusion Market Outlook, Excel mode (capex build-up, FOAK ramp, scenarios bear/base/bull)','2026-07-27','NA_inputs/Fusion_Market_Model_v09.xlsx','S7'),
]

OPEN_QUESTIONS = [
 (1,'all','Basis: v6 freeze - DECIDED (2026-09-22).','-'),
 (2,'all','Wave 1 = one variant per scenario (14 runs, serial, ~1 h each) - implemented; stretch/secondary variants (1B/1C, 2B/2C/2D, 3B/3C, 4B, 5B/5C, 6A/6B/6D, 7A/7B/7D, 8B/8C, 9A/9B, 10A/10B, 11B/11C, 12B/12C, 13B/13C, 14B/14C) on request.','Run budget.'),
 (3,'7','Fusion: bull case implemented (base case available as a variant); NA location share (100 %) and site split are assumptions.','Confirm if a different NA share is wanted.'),
 (4,'8','Canada DC: scenario numbers used although below the FEL base (user rule); results will show a demand cut vs base - to be read as "announcement-consistent".','-'),
 (5,'3 / 12','DC paths use the external-anchored numbers (not FEL presets).','Consistency with published FEL numbers.'),
 (6,'2','Flat electrolysis load (2A); flexible electrolysers (2D) not built.','Capacity results at 333 TWh flat.'),
 (7,'6','6C combined case implemented; the LNG-only / macro-only split (6A/6B) on request.','-'),
 (8,'10','10C dials implemented (10/20 % relocation).','-'),
 (9,'13','Overlap with FEL base industry growth unknown (FEL team) - adders applied on top.','Possible double counting in s13.'),
 (10,'14','CO2 price 30/60/90 USD/t; nuclear ITC not added (unknown whether LCOE v1.4 nets it); CCS retrofit technology only in 14C (not built).','-'),
 (11,'11','Exogenous rip-and-replace capex report (11C) not built.','-'),
 (12,'4','4C run without the orbital-compute reduction (tailwind reading); the space_dc trio remains the displacement analysis.','-'),
 (13,'1 / 6','Oil-shock/EV coupling only in 6D (not run).','-'),
 (14,'5','RES supply-side brake included in 5A (rep funnel without the x1.30 widening).','-'),
]
