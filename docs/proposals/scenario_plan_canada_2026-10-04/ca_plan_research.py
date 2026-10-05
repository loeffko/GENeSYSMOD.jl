# -*- coding: utf-8 -*-
"""Scenario rows, signal checks, assumptions, sources, run plan and open questions for the Canada scenario plan
(2026-10-04). Built from the research notes A-E in this folder (web research of 2026-10-04) and the model baseline in
ca_plan_content.py. The scenario content lives in ca_plan_part1..5.py (one file per research note) and is merged here.
Source ids: A.. E.. = research notes; M.. = model / SE-internal files.
Assumption rows: (id, scenario, variant, parameter/lever, region, years, value, unit, basis, source ids, confidence, invented?)"""
import re
import ca_plan_part1 as P1
import ca_plan_part2 as P2
import ca_plan_part3 as P3
import ca_plan_part4 as P4
import ca_plan_part5 as P5

CAD_EUR = 0.685          # Bank of Canada annual average 2023 (1 EUR = 1.4597 CAD), consistent with 1 USD = 0.925 EUR in EUR2023

PARTS = (P1, P2, P3, P4, P5)

# =====================================================================================================================
# Sources: model / SE-internal first, then the research notes in id order
SOURCES = [
    ('M1', 'TU Berlin / SE model', 'GENeSYS-MOD North America, frozen base run fel2026_base_49_2015_v6f (input dump and results in the model database)', '2026-09', 'Results/genesysmod_db.duckdb', 'Canada baseline'),
    ('M2', 'Canada Energy Regulator', "Canada's Energy Future 2026 - consolidated power-sector workbook canada_power_ef2026.xlsx (capacity, generation, demand by province and scenario; from the CER open data)", '2026', 'GENeSYS-MOD.data/NA_inputs/canada_power_ef2026.xlsx ; https://www.cer-rec.gc.ca/open/energy/energyfutures2026/', 'S1, S3, S7, S9, base corridor'),
    ('M3', 'Siemens Energy (internal)', 'Canadian Nuclear Review_5.7.2026.xlsx - unit list of operating, announced and early-development Canadian reactors, uprates, IRP/RFP resources', '2026-05-07', 'GENeSYS-MOD.data/NA_inputs/Canadian Nuclear Review_5.7.2026.xlsx', 'S3'),
    ('M4', 'Siemens Energy NA Hub (internal)', 'Input Scenarios (v3) - market-intelligence note incl. Alberta customer signals (Greenlight, Capital Power, TransAlta, BCE)', '2026-10', 'docs/proposals/scenario_results/Input Scenarios (v3) 2.docx', 'S6'),
    ('M5', 'TU Berlin / SE model', 'Existing data overlay NorthAmerica_nuclear_announced (Canada rows from M3) and the s08 Canada data-centre case (wave 3)', '2026-09', 'GENeSYS-MOD.data/Data/Parameters/Par_TotalAnnualMinCapacity/NorthAmerica_nuclear_announced', 'S3, S6'),
]


def _sid(s):
    m = re.match(r'([A-Z])(\d+)', s[0])
    return (m.group(1), int(m.group(2)))


SOURCES += sorted([s for p in PARTS for s in p.SOURCES], key=_sid)
_ids = [s[0] for s in SOURCES]
assert len(_ids) == len(set(_ids)), 'duplicate source id'

SCENARIOS = sorted([s for p in PARTS for s in p.SCENARIOS], key=lambda s: s['id'])
SIGNALS = sorted([s for p in PARTS for s in p.SIGNALS], key=lambda s: s[0])                 # stable: keeps the order inside a scenario
ASSUMPTIONS = sorted([a for p in PARTS for a in p.ASSUMPTIONS], key=lambda a: a[0])

# every source id cited in signals / assumptions must exist
for _row, _col in [(r, 4) for r in SIGNALS] + [(r, 9) for r in ASSUMPTIONS]:
    for _tok in re.findall(r'\b[A-EM]\d+\b', str(_row[_col])):
        assert _tok in _ids, f'unknown source id {_tok} in {_row[:3]}'

# =====================================================================================================================
# Run plan: (label, scenario, variant, definition, corridor / funnel treatment, priority, note)
# Labels follow the North America set: fel2026_cNN<variant>_<name>_49_2015_v6 ; data folders NorthAmerica_cNN<variant>_<name>.
# Priority 1 = one central run per scenario; 2 = stretch (and the cross-check where the central reading is open); 3 = alternative / optional.
US = 'US side identical to the base (funnel unchanged).'
RUNS = [
    ('fel2026_base_49_2015_v6f', 'Base', '-', 'Frozen base, not rerun. Reference for every Canada run.', 'CER Current Measures corridor (-20 % / +60 % at 2035) for Canada.', '-', 'exists'),
    ('fel2026_c01a_gridmix_49_2015_v6', 'S1 Unleash generation', '1A', 'Base demand. Gas fleet kept at 34.2 / 33.4 / 36.6 GW (new CCGT minimum raised so the total does not shrink), SMR minimum 0.3 / 1.5 / 2.1 GW, battery minimum 4.5 / 6.5 / 10.5 GW.', 'Corridor minima raised for gas, SMR, batteries (SMR ceiling lifted); wind, solar, hydro unchanged. ' + US, 1, 'The "broad mix incl. natural gas" reading; the capacity target itself is already met by the base.'),
    ('fel2026_c01c_firmdoubling_49_2015_v6', 'S1 Unleash generation', '1C stretch', 'Firm non-emitting capacity (hydro + nuclear + SMR) 121 / 144 / 167 GW and gas 39 / 46 / 53 GW as minima.', 'Hydro, nuclear and gas ceilings lifted to the new minima. ' + US, 2, ''),
    ('fel2026_c01b_cerhigher_49_2015_v6', 'S1 Unleash generation', '1B', 'CER Higher mix: gas 34.6 / 36.2 / 41.3, wind 36.4 / 68.1 / 87.1, batteries 4.5 / 7.5 / 14.0 GW as minima.', 'Minima raised; ceilings unchanged. ' + US, 3, ''),
    ('fel2026_c01p_cerpath_49_2015_v6', 'S1 Unleash generation', '1P optional', 'Literal path reading: Canada demand cut to the CER Current Measures path (581 / 635 / 695 TWh).', 'Corridor unchanged (it is centred on this world). ' + US, 3, 'Lower than the base; only if the literal "150 to 310 GW by 2050" path is wanted.'),
    ('fel2026_c02a_localcontent_49_2015_v6', 'S2 Local content', '2A', 'Capital cost from 2028: wind x1.08, utility PV and batteries x1.06, CCGT x1.05.', 'Corridor unchanged. ' + US, 1, ''),
    ('fel2026_c02c_fortress_49_2015_v6', 'S2 Local content', '2C stretch', 'Capital cost +25 % plus financing premium from 2027; wind capped at 1.5 / 2.5 / 4.0 GW/yr, PV 1.0 GW/yr to 2030; wind, PV, batteries, CCGT paths 3 years later.', 'Wind and PV corridor minima scaled down to fit under the build-rate caps (inside the scenario definition). ' + US, 2, 'Needs the wind / PV subset tag for the group cap.'),
    ('fel2026_c02b_mandate_49_2015_v6', 'S2 Local content', '2B', 'Wind x1.16 fading to x1.08, others x1.10; wind capped at 2.0 / 3.5 GW/yr; transformer-bound capacity 1 year later.', 'Wind corridor minimum scaled down to the cap. ' + US, 3, ''),
    ('fel2026_c03b_nuclear_se_49_2015_v6', 'S3 Nuclear growth', '3B', 'Siemens Energy nuclear outlook (the "22 GW announced" list): large 11.5 / 15.6 / 17.9 / 23.4 GW (2030 / 2035 / 2038 / 2040), SMR 0.6 / 1.8 / 3.0 / 4.2 GW as minima.', 'Nuclear minimum = path, SMR ceiling lifted; reuses the Canada rows of the existing nuclear_announced overlay. ' + US, 1, 'Central because it carries the numbers of the request.'),
    ('fel2026_c03a_nuclear_public_49_2015_v6', 'S3 Nuclear growth', '3A', 'Public announced schedules: large 12.9 / 15.0 / 18.5 GW, SMR 0 / 1.2 / 1.8 GW.', 'As 3B. ' + US, 2, 'Cross-check: what public sources support by 2040.'),
    ('fel2026_c03c_nuclear_tripling_49_2015_v6', 'S3 Nuclear growth', '3C stretch', 'All announced capacity on line by 2040: large 12.9 / 17.6 / 33.6 GW, SMR 0.6 / 1.8 / 4.2 GW; fleet-learning capital cost (large 7,500 / 7,000 / 6,700 EUR/kW).', 'Nuclear ceiling (25 GW) lifted to the path. ' + US, 2, ''),
    ('fel2026_c04a_partnership_49_2015_v6', 'S4 Indigenous equity', '4A', 'Capital cost x0.98 (wind, PV) and x0.97 (hydro, nuclear); wind and PV ceiling 1 year earlier, hydro and nuclear paths 2 years earlier.', 'Corridor shifted in time for the partnered technologies. ' + US, 1, 'Small effect expected; read together with 4C.'),
    ('fel2026_c04c_consentfail_49_2015_v6', 'S4 Indigenous equity', '4C stretch', 'No new large hydro or new nuclear (beyond Darlington unit 1) before 2036; hydro and nuclear capital cost +20 % plus financing premium; wind and PV 3 years later.', 'Hydro, nuclear, wind and PV minima shifted later. ' + US, 2, ''),
    ('fel2026_c04b_gate_49_2015_v6', 'S4 Indigenous equity', '4B', 'Half of new projects delayed 3 years, capital cost x1.01-1.02, wind + PV capped at 1.5 GW/yr to 2030.', 'Wind and PV minima scaled down to the cap. ' + US, 3, ''),
    ('(side calculation, no run)', 'S5 Northern and remote power', '5A / 5B', 'Demand +0.9 / +2.5 TWh, diesel -0.8 / -1.2 TWh, microreactors 20 / 50 MW by 2040: reported as a table outside the model.', '-', 1, 'Below 0.6 % of the Canada node; a run would not differ visibly from the base.'),
    ('fel2026_c05c_north_49_2015_v6', 'S5 Northern and remote power', '5C stretch', 'Demand +0.5 / +2.5 / +5.0 TWh (flat), microreactors 0.005 / 0.10 / 0.30 GW at 16,000 / 13,000 / 10,000 EUR/kW as an SMR minimum.', 'SMR ceiling lifted by the microreactor capacity. ' + US, 3, 'Optional, only if a model result is wanted.'),
    ('fel2026_c06b_dcpipeline_49_2015_v6', 'S6 Data centres', '6B', 'Data-centre demand 47 / 121 / 177 TWh (base 71 / 178 / 269). Dedicated gas 2.8 / 9.9 / 13.5 GW is inside the new CCGT the base already forces.', 'Corridor unchanged. ' + US, 1, 'BELOW the base. Existing run fel2026_s08_canada_49_2015_v6_v3 (41 / 130 / 220 TWh) is a further waypoint.'),
    ('fel2026_c06c_dcqueue_49_2015_v6', 'S6 Data centres', '6C stretch', 'Data-centre demand 88 / 236 / 306 TWh; minimum new CCGT 6.9 / 22.7 / 28.2 GW (dedicated gas).', 'New CCGT minimum raised (stays under the base ceiling). ' + US, 2, 'The only variant above the base.'),
    ('fel2026_c06a_dcannounced_49_2015_v6', 'S6 Data centres', '6A', 'Data-centre demand 32 / 51 / 68 TWh.', 'Corridor unchanged. ' + US, 3, 'Floor case: only firm projects and operator reference forecasts.'),
    ('fel2026_c07a_windpaced_49_2015_v6', 'S7 Wind re-acceleration', '7A', 'Onshore wind ceiling 28.0 / 43.5 / 55.7 GW (announced procurement); wind capital cost x1.13 (cold-climate package, tower surtax).', 'Wind corridor minimum lowered to the ceiling in 2030-2035. ' + US, 1, 'BELOW the base (31 / 62 / 87 GW): the "Mixed" reading.'),
    ('fel2026_c07b_windaccel_49_2015_v6', 'S7 Wind re-acceleration', '7B', 'Onshore wind floor 45 / 70 / 87 GW (CanREA Accelerated); wind capital cost x0.95 / 0.93 / 0.91.', 'Wind ceiling 2026-2030 lifted to the floor. ' + US, 1, 'The "Tailwind" reading; pair with 7A.'),
    ('fel2026_c07c_windnetzero_49_2015_v6', 'S7 Wind re-acceleration', '7C stretch', 'Onshore wind floor 39.7 / 77.5 / 113.3 GW (CER Net-zero), offshore wind 0 / 5 / 15 GW fixed at the Nova Scotia cost (8,220 EUR/kW incl. transmission); onshore cost x0.85 / 0.83 / 0.81.', 'Offshore minimum added; onshore inside the ceiling. ' + US, 2, 'Far what-if: offshore 40 GW by 2040.'),
]
RUNS += getattr(P5, 'RUNS_S8', [])
RUNS += [
    ('fel2026_c09a_euprojects_49_2015_v6', 'S9 EU associate member', '9A', 'Added to the base: export hydrogen +4 / +26 / +36 TWh, industry +8 / +19 / +29 TWh (flat).', 'Corridor unchanged. ' + US, 1, ''),
    ('fel2026_c09c_eupartner_49_2015_v6', 'S9 EU associate member', '9C stretch', 'Hydrogen +4 / +30 / +60, general load +17 / +37 / +58, BEV 29 / 72 / 125 TWh; 37 TWh fixed export to Europe in 2040 (6 GW cable); offshore wind 0 / 5 / 10 GW, hydro +4 GW.', 'Offshore and hydro minima added, hydro ceiling lifted. ' + US, 2, 'Export cable enters as a flat demand (no European node).'),
    ('fel2026_c09b_euelectrification_49_2015_v6', 'S9 EU associate member', '9B', 'BEV 29 / 72 / 125 TWh, general load +0 / +15 / +29 TWh, hydrogen as 9A, offshore wind 5 GW in 2040, onshore wind floor 39.6 / 77.5 / 113.3 GW.', 'Wind minima raised. ' + US, 3, ''),
]

# =====================================================================================================================
# Open questions: (#, question, options / recommendation, affects)
OPEN_QUESTIONS = [
    (1, 'Scenario 1: which reading of "double the grid"? The base already reaches 297 GW in 2040, above the path to 310 GW in 2050.',
     'Recommended: 1A (mix reading: gas kept at 34-37 GW, SMR and storage minima on base demand) plus the stretch 1C. Optional 1P follows the literal path and is a lower-than-base case.', 'S1'),
    (2, 'Scenario 3: is the central case the Siemens Energy nuclear outlook (the "22 GW" list, 27.7 GW fleet in 2040) or the public schedules (20.3 GW in 2040)? "28 new CANDU reactors by 2050" was not found in public sources (public: fleet of 20-25 units, or up to 10 new).',
     'Recommended: 3B (SE outlook) as the scenario because it carries the numbers of the request, 3A (public schedules) as cross-check, 3C as stretch. Please confirm the source of "28 reactors".', 'S3'),
    (3, 'Scenario 6: every sourced data-centre path is below the frozen base (base 269 TWh in 2040; named pipeline 177; firm projects 68). Which variant is "the scenario"?',
     'Recommended: 6B (named pipeline) as central and 6C (full queue, +37 TWh above base, 28 GW dedicated gas) as the tailwind stretch. Alternative: only 6C, or the base plus a Crossfield block (+1.4 GW gas, +10 TWh). Needed from Siemens Energy: in-service year and customer of the TC Energy Crossfield concept (not public).', 'S6'),
    (4, 'Scenario 7: the base builds more wind (31 / 62 / 87 GW) than the announced procurement adds up to (28 / 43.5 / 56 GW). Run the pair 7A (announced path as a ceiling, with headwind cost) and 7B (accelerated floor)?',
     'Recommended: yes, both as priority 1, so the "Mixed" and the "Tailwind" reading are both on the table; 7C (net-zero pace plus 5-15 GW offshore) as stretch.', 'S7'),
    (5, 'Scenario 5: the territories are 0.3 % of the Canada node (1.7 TWh) and cannot be isolated in a one-node model. Side calculation instead of a run?',
     'Recommended: side calculation table (demand, diesel displaced, microreactor MW, cost) from the research note; optional stretch run 5C only if a model number is wanted.', 'S5'),
    (6, 'Scenarios 2 and 4 are procurement conditions, represented by proxies (cost premium, build-rate cap, delay). Is that acceptable, and can Siemens Energy supply its own figures?',
     'Needed from Siemens Energy if available: gas-turbine and transformer lead times and price escalation for Canada (not found in public sources), wind cold-climate product premium, any measured schedule gain with Indigenous partnership.', 'S2, S4, S7'),
    (7, 'Canada corridor (the Canadian counterpart of the US funnel): the base holds Canadian capacities inside CER Current Measures -20 % / +60 %. How to treat it in the scenarios?',
     'Recommended (same rule as for the US set): no separate "released" twin runs; each scenario edits the corridor inside its definition only where the storyline contradicts it (listed per run in the run plan).', 'all'),
    (8, 'Overlap between scenario 8 (critical minerals), scenario 9 (EU partnership: minerals, hydrogen, industry) and scenario 5 (northern mines).',
     'Recommended: run 8 and 9 separately on the base and state the shared load explicitly; do not add them up.', 'S5, S8, S9'),
    (9, 'Items found that concern the frozen base, not the scenarios: (a) nuclear refurbishment dip 2027-2033 (about 3.7 GW of 12.9 GW offline in 2030) is not in the base; (b) base-year data-centre demand 17 TWh against 9-11 TWh bottom-up; (c) the data-centre path of the base needs roughly the whole Alberta queue; (d) CER corridor carries 11 GW of Newfoundland wind-hydrogen capacity that was largely cancelled in 2026.',
     'Recommended: no change now (base is frozen); list them for the next baseline. (a) could also be added to scenario 3 as scenario content if wanted.', 'base, S3, S6, S7'),
    (10, 'Scope and order of runs.', 'Recommended: priority-1 set first (one central run per scenario, 7A and 7B as a pair; about 25 minutes per run, serial), review, then the stretch set. Results reported for the Canada node plus the Canada-US interconnectors and the US spill-over.', 'all'),
    (11, 'The colleague file "Canada Scenarios_MEP27.docx" is rights-protected and could not be opened. Does canada.txt carry its full content?',
     'If the docx has numbers or tables beyond the text file, an unprotected export is needed.', 'all'),
]
