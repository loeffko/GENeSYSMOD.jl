# -*- coding: utf-8 -*-
"""Canada plan, part 4: scenario 6 (data sovereignty / acceleration of data centres). Research note C.
Demand figures are busbar TWh; MW-based figures use a load factor of 0.85 (assumption of the note)."""
from ca_plan_sources import U

BASE_DC = (71, 178, 269)          # frozen base, TWh 2030 / 2035 / 2040
DC_A = (32, 51, 68)
DC_B = (47, 121, 177)
DC_C = (88, 236, 306)
GAS_A = (1.0, 1.0, 1.0)           # dedicated (behind-the-meter / tethered) new gas, GW
GAS_B = (2.8, 9.9, 13.5)
GAS_C = (6.9, 22.7, 28.2)


def _d(path):
    return ' / '.join(f'{p - b:+d}' for p, b in zip(path, BASE_DC))


SOURCES = [
    ('C1', 'Alberta Electric System Operator', 'Connection Project List, September 2026 (own aggregation of the data-load and gas rows)', '2026-09-01', U('September-2026-Project-List'), 'S6 Alberta queue'),
    ('C2', 'Alberta Electric System Operator', 'Data Centre Update (Phase I: 4,800 MW qualified, 1,200 MW assigned)', '2025-09-26', U('AESO-Data-Centre-Update-September-2025'), 'S6 Alberta grid allocation'),
    ('C3', 'Alberta Electric System Operator', 'Phase II large-load integration (bring-your-own-generation rules; update of 8 Sep 2026)', '2026-09-08', U('aesoengage.aeso.ca'), 'S6 Alberta rules'),
    ('C4', 'Pembina Pipeline (via EnergyNow)', 'Positive Final Investment Decision on the Greenlight Electricity Centre', '2026-07-02', U('pembina-pipeline-announces'), 'S6 signal, gas ratio, specific cost'),
    ('C5', 'Capital Power', "Powering What's Next: Capital Power signs long-term 250 MW agreement with Meta", '2026-07-08', U('capitalpower.com'), 'S6 signal'),
    ('C6', 'TransAlta', 'Proposed Data Centre development (Keephills MOU with CPP Investments and Brookfield)', '2026-02-27', U('transalta.com'), 'S6 signal'),
    ('C7', 'BCE', 'Bell AI Fabric to expand nation-building project in Saskatchewan with up to 900 MW of additional power', '2026-09-14', U('bce.ca'), 'S6 signal'),
    ('C8', 'Daily Commercial News / Canadian Press', 'TC Energy sets growth sights on U.S. data centre boom', '2026-02-18', U('tc-energy-sets-growth'), 'S6 signal (TC Energy strategy)'),
    ('C9', 'TC Energy', 'Second quarter 2026 results (NGTL capacity marketed for new intra-Alberta demand)', '2026-07-30', U('tcenergy.com/announcements/2026'), 'S6 signal, gas supply'),
    ('C10', 'Daily Commercial News (ISED document)', 'Data centre capacity could soar to 20 GW in planned projects: government document', '2026-07', U('data-centre-capacity-could-soar'), 'S6 federal need estimate 5.5 GW'),
    ('C11', 'Gowling WLG', 'Canada launches "AI for All" national artificial intelligence strategy', '2026-06', U('gowlingwlg.com'), 'S6 sovereign compute target'),
    ('C12', 'Innovation, Science and Economic Development Canada', 'Enabling large-scale sovereign AI data centres (call for projects above 100 MW)', '2026', U('ised-isde.canada.ca'), 'S6 data sovereignty'),
    ('C13', 'Canada Energy Regulator', "Canada's Energy Future 2026 - Scenarios and Assumptions (data-centre load added by scenario)", '2026-03-17', U('scenarios-and-assumptions'), 'S6 forecast'),
    ('C14', 'IESO', '2026 Annual Planning Outlook - demand forecast module data (data-centre sub-sector)', '2026-03', U('2026-APO-Demand-Forecast-Module-Data'), 'S6 Ontario'),
    ('C15', 'Radio-Canada', 'Tarifs Hydro-Quebec pour les centres de donnees (hearing R-4333-2026)', '2026-10-01', U('radio-canada.ca/nouvelle/2289163'), 'S6 Quebec'),
    ('C16', 'BC Hydro', 'Emerging industries connections (competitive allocation for data centres)', '2026-10', U('emerging-industries-connections'), 'S6 British Columbia'),
    ('C17', 'McCord Investments (secondary tracker)', 'Provincial data-centre pages (cites regulations and government releases)', '2026-09', U('mccordinvestments.com/provinces/sk'), 'S6 SK, MB, Atlantic, BC detail'),
    ('C18', 'Alberta Data Centre Watch (secondary tracker)', 'Project tracker: demand and on-site generation of active projects', '2026-09', U('albertadatacentrewatch.ca'), 'S6 Alberta projects'),
    ('C19', 'BLG', 'Data centre regulation in Alberta: key considerations (levy, Bill 12 and Bill 17)', '2026-07', U('blg.com/en/insights/2026/07'), 'S6 Alberta levy'),
    ('C20', 'Osler', "Alberta's data centre regulations: guidance on power generation for large-load facilities", '2026', U('osler.com'), 'S6 Alberta rules'),
    ('C21', 'Global News', 'Olds data centre: Alberta Utilities Commission rejects the power plant (Synapse)', '2026-08', U('globalnews.ca/news/12024680'), 'S6 refusal risk'),
    ('C22', 'RTO Insider', 'Alberta Market Surveillance Administrator briefs (Q2 2026 pool price)', '2026-08-17', U('rtoinsider.com/139460'), 'S6 signal'),
    ('C23', 'DeSmog', 'Canadian gas CEOs are hyping AI data centres to investors', '2026-07-02', U('desmog.com'), 'S6 gas demand'),
    ('C24', 'Global News', 'TC Energy Alberta natural gas network demand (NGTL fully subscribed until 2029)', '2026-09-14', U('globalnews.ca/news/12058615'), 'S6 gas constraint'),
    ('C25', 'Government of Alberta, Major Projects', 'Malachite One Datacenter', '2026', U('Malachite-One'), 'S6 project, specific cost'),
    ('C26', 'Prime Minister of Canada', 'Canada-Alberta Memorandum of Understanding', '2025-11-27', U('canada-alberta-memorandum'), 'S6 sovereign compute, carbon price'),
    ('C27', 'The Logic', "Canada's Responsible Data Centre Development Principles (signatories; only one federal MOU)", '2026-09', U('thelogic.co/news/canada-responsible'), 'S6 data sovereignty'),
]

SIGNALS = [
    (6, 'TC Energy is developing a concept for up to three gas-fired power plants at its Crossfield, Alberta site, about 465 MW each, about 1.4 GW in total',
     'No public source: nothing on the TC Energy site or in its Q2 2026 results, no entry in the AESO connection lists June 2025 - September 2026 (the only "Crossfield" gas plant, Kalina 178 MW, is cancelled). TC Energy owns the Crossfield gas storage; its CEO said in February 2026 that the company focuses on in-front-of-the-meter supply for utilities and is not developing behind-the-meter power. 465 MW is exactly one 1x1 H-class combined-cycle block (same size as the Greenlight units).',
     'Not found in public sources (treated as non-public market intelligence; unit size is plausible)', 'C1, C8, C9'),
    (6, 'Reaching data sovereignty (scenario title)',
     'Federal policy exists but is small in MW: "AI for All" strategy (June 2026) targets 850 MW of sovereign compute by 2030 and estimates a national need of 5.5 GW by 2030; call for sovereign data centres above 100 MW has produced one non-binding MOU (TELUS, 150 MW by 2032); voluntary principles with 23-42 signatories; data residency is a funding criterion, not a law. Saskatchewan and British Columbia score Canadian ownership or sovereignty.',
     'Partly: policy direction confirmed, no binding rule and under 1 GW of committed sovereign capacity', 'C10, C11, C12, C26, C27'),
    (6, 'Acceleration of data centres',
     'Operating load is small (337-449 MW tracked). Alberta queue: 42 projects, 20,660 MW, flat for a year, only 1,754 MW with an in-service date. First firm steps in 2026: Greenlight 932 MW gas plant (final investment decision 2 July, Siemens Energy SGT6-8000H, in service second half of 2030), Capital Power - Meta 250 MW supply from 2028, TransAlta Keephills MOU 230 MW, Bell Saskatchewan MOU 1.2 GW. Counter-signals: first refusal of a data-centre gas plant (Synapse 1.4 GW), Kalina projects cancelled, British Columbia, Quebec, Manitoba and Ontario ration or re-price connections.',
     'Partly: first firm projects, 92 % of the Alberta queue undated', 'C1, C4, C5, C6, C7, C21'),
    (6, '(hub note) Greenlight Electricity Centre: 932 MW, about CAD 4.6 bn, in service 2030',
     'Confirmed: CAD 4.0 bn before financing, 4.6 bn with; two 466 MW blocks, expandable to 1,864 MW; gas about 150 MMcf/d.', 'Confirmed', 'C4, M4'),
    (6, '(hub note) Alberta spot power about 29 $/MWh in Q2 2026',
     'Average pool price CAD 29.47/MWh (EUR 20/MWh) in Q2 2026, 27 % below the year before; the price hit the cap on 28 May and sat at zero for 34 hours from 31 May.', 'Confirmed', 'C22, M4'),
    (6, '(hub note) Alberta levy of 2 % on grid-connected data centres (Bill 17)',
     'The levy was created by Bill 12 (2025): 2 % of hardware value for grid-connected sites of 75 MW or more; Bill 17 (2026) ties the rate to grid electricity actually used, only on-site generation qualifies for 0 %. Effect: pushes projects towards dedicated gas.',
     'Corrected: threshold 75 MW, created by Bill 12, amended by Bill 17', 'C19'),
    (6, '(hub note) Alberta bring-your-own-generation rules, 4.8 GW deemed viable',
     'Rules confirmed (generation must cover the maximum demand, gas only in phase 2A, bridging pool 1,600 MW for three years), but the first intake has not opened. 4.8 GW is the Phase I qualified volume, of which 1.2 GW was assigned.',
     'Corrected: rules in place, no Phase II result yet', 'C2, C3, C20'),
]

ASSUMPTIONS = [
    (6, 'Data centres', '6A announced-consistent', 'Data-centre demand (Power_DataCenter)', 'Canada', '2030 / 2035 / 2040', f'{DC_A[0]} / {DC_A[1]} / {DC_A[2]}  (base 71 / 178 / 269; difference {_d(DC_A)})', 'TWh',
     'Projects with a final investment decision, a grid allocation or under construction, plus the system operators\' reference forecasts (Ontario 6.4 / 10.3 / 19.9 TWh; Quebec 1.1 GW in 2035) and the allocation ceilings fully used (British Columbia 400 MW + 200 MW/yr; Alberta 1.2 GW Phase I, dated loads, Meta about 1 GW). Alberta share 43 % / 34 % / 26 %.',
     'C1, C2, C13, C14, C15, C16, C17', 'Medium', 'Partly (load factor 0.85, phasing)'),
    (6, 'Data centres', '6B named pipeline builds out', 'Data-centre demand (Power_DataCenter)', 'Canada', '2030 / 2035 / 2040', f'{DC_B[0]} / {DC_B[1]} / {DC_B[2]}  (difference to base {_d(DC_B)})', 'TWh',
     '6A plus every named project with an identified power solution (regulatory decision pending, MOU or proposal), one to two years late: Alberta 9.4 GW in 2035 and 13.0 GW in 2040, Bell Saskatchewan 1.2 GW from 2035, Ontario high forecast, Quebec 2.0 / 2.5 GW. Cross-check: 6.3 GW connected in 2030 against the federal need estimate of 5.5 GW.',
     'C1, C7, C10, C14, C18', 'Low', 'Partly (timing of undated projects)'),
    (6, 'Data centres', '6C stretch: full queue and sovereignty push', 'Data-centre demand (Power_DataCenter)', 'Canada', '2030 / 2035 / 2040', f'{DC_C[0]} / {DC_C[1]} / {DC_C[2]}  (difference to base {_d(DC_C)})', 'TWh',
     'Whole Alberta queue (20.7 GW) energised within the 3-6 year connection window, off-grid mega-projects on the proponents\' dates (Wonder Valley to 7.5 GW by 2040), all Quebec requests granted (3.5 GW), Bell 1.2 GW. The only variant above the base. Alberta share 68-72 %.',
     'C1, C15, C18', 'Low', 'Partly (assumes every queue entry is built)'),
    (6, 'Data centres', 'all variants', 'Load factor for figures given in MW', 'Canada', '2026-2040', '0.85', '-', 'Assumption of the research note (the base states its GW at 100 %); Ontario enters with the IESO TWh directly.', '-', 'Low', 'Yes'),
    (6, 'Data centres', 'all variants', 'Years between the waypoints; start value', 'Canada', '2025-2040', 'linear between 2025 (base value 17.1 TWh, unchanged), 2030, 2035 and 2040', 'TWh', 'The frozen base year is kept. A bottom-up estimate of operating load gives 9-11 TWh for 2025, so the start value looks high (note for the next baseline).', 'C10, C14, C15', 'Medium', 'Partly (interpolation)'),
    (6, 'Data centres', '6A / 6B', 'Dedicated new gas capacity that goes with the load', 'Canada', '2030 / 2035 / 2040', f'6A: {GAS_A[0]} / {GAS_A[1]} / {GAS_A[2]};  6B: {GAS_B[0]} / {GAS_B[1]} / {GAS_B[2]}  (base forced new CCGT 5.0 / 10.0 / 15.1)', 'GW',
     '6A: Greenlight 0.93 + Bitdeer 0.10. 6B adds Beacon, Malachite, Wonder Valley phase 1, Genesee new gas, Bell Saskatchewan, New Brunswick. Both are inside the new CCGT the base already forces, so the gas minimum is left unchanged and read as "dedicated".',
     'C1, C4, C18, C25', 'Medium', 'No'),
    (6, 'Data centres', '6C stretch', 'Minimum new CCGT capacity (dedicated gas under the Alberta bring-your-own-generation rule)', 'Canada', '2030 / 2035 / 2040', f'{GAS_C[0]} / {GAS_C[1]} / {GAS_C[2]}  (base minimum 5.0 / 10.0 / 15.1; base maximum 10.4 / 23.1 / 31.6)', 'GW',
     'Rule applied to the whole queue: 20.7 GW minus the 1.2 GW grid allocation minus about 1.0 GW served by existing units = 18.5 GW of new tethered gas, plus Wonder Valley, Malachite, Saskatchewan 0.9, New Brunswick. Fits under the base maximum in every year. Gas need 1.1 / 3.7 / 4.5 Bcf/d at the Greenlight ratio (0.161 Bcf/d per GW), against about 1.0 Bcf/d of new delivery capacity marketed on the Alberta system for 2030-2032 and an industry view of 1.5 Bcf/d by 2030.',
     'C1, C3, C4, C9, C18, C23, C24', 'Low', 'Partly'),
    (6, 'Data centres', 'optional add-on to any variant', 'TC Energy Crossfield block as named in the request', 'Canada', 'from the in-service year (not public)', '+1.4 GW new CCGT minimum; up to +10.4 TWh if it serves a new 1.4 GW load', 'GW, TWh',
     'Three 465 MW blocks; energy at load factor 0.85. Customer, date and status are not public: inside 6B by size, or added on top once Siemens Energy supplies the timing.', 'C8, C9', '-', 'User input (timing)'),
    (6, 'Data centres', 'information only', 'Specific cost of a dedicated H-class plant against the model value', 'Alberta', '2026', 'Greenlight 2,940 EUR/kW before financing (CAD 4.0 bn / 932 MW); Malachite 3,425 EUR/kW; model new CCGT 883 EUR/kW (2030)', 'EUR/kW',
     'Announced budgets are nominal investment totals (owner\'s cost, interconnection, contingency), not overnight cost; still a factor of three. Not changed in the scenario; candidate for a cost sensitivity.', 'C4, C25', 'Medium', 'No'),
]

SCENARIOS = [
    dict(id=6, name='Reaching data sovereignty: acceleration of data centres', tag='Tailwind',
         meaning='More data-centre load, mostly in Alberta and mostly supplied by dedicated gas plants built for it. In the model: the Canadian data-centre demand path plus a minimum for new combined-cycle capacity equal to the dedicated gas that comes with the load.',
         levers='Par_SpecifiedAnnualDemand Canada / Power_DataCenter (flat profile); Par_TotalAnnualMinCapacity Canada / P_Gas_CCGT (dedicated gas, stretch variant only).',
         route='Scenario generator: demand rows and minimum-capacity rows, both existing helpers. The existing run fel2026_s08_canada_49_2015_v6_v3 (41 / 130 / 220 TWh) already sits between 6B and the base and can be reused as a waypoint.',
         flag='GREEN', flag_summary='Existing levers. Limits of the single node: behind-the-meter and grid supply cannot be told apart, and Alberta (gas) cannot be told apart from the hydro provinces that ration data centres.',
         evidence='High for the named projects and rules (operator lists, company releases); low for timing (92 % of the Alberta queue has no date); the Crossfield signal itself is not public',
         base_cmp=f'BASE IS ABOVE EVERY SOURCED FORECAST. Base 71 / 178 / 269 TWh (2030 / 2035 / 2040) against 6A {DC_A[0]} / {DC_A[1]} / {DC_A[2]}, 6B {DC_B[0]} / {DC_B[1]} / {DC_B[2]}, federal need estimate 41-48 TWh in 2030, CER Higher about 100 TWh in 2050. Only the stretch 6C ({DC_C[0]} / {DC_C[1]} / {DC_C[2]}) is a tailwind against the base. The base needs roughly the whole Alberta queue to be built.',
         variants=f'6A announced-consistent ({DC_A[0]} / {DC_A[1]} / {DC_A[2]} TWh; dedicated gas 1.0 GW, inside the base). 6B named pipeline builds out ({DC_B[0]} / {DC_B[1]} / {DC_B[2]} TWh; dedicated gas 2.8 / 9.9 / 13.5 GW = about the new CCGT the base already forces). 6C stretch: full queue and sovereignty push ({DC_C[0]} / {DC_C[1]} / {DC_C[2]} TWh; minimum new CCGT 6.9 / 22.7 / 28.2 GW). Optional: Crossfield block +1.4 GW.',
         effort='S', anchors='AESO connection list (Sep 2026) and Phase I / II rules; Greenlight final investment decision; Capital Power - Meta; TransAlta Keephills; Bell Saskatchewan; IESO 2026 outlook; Hydro-Quebec and BC Hydro allocations; CER EF2026 data-centre assumptions; federal "AI for All" strategy',
         concerns=[('GREEN', 'data', 'The frozen base is above every sourced forecast, so the central and the pipeline variant lower Canadian demand (by 92-201 TWh in 2040). Against the base the "tailwind" only appears in the stretch.', 'Use the sourced numbers as agreed and flag it; decide which variant is the scenario (open question).'),
                   ('YELLOW', 'model', 'One node: the model cannot keep the load in Alberta or tie it to dedicated gas; hydro and wind from other provinces serve it on a copper plate.', 'Force the dedicated gas as a minimum for new CCGT (stretch) and report gas burn and capacity factor of new CCGT against the dedicated volume.'),
                   ('YELLOW', 'model', 'In the lower-demand variants the Canadian fleet sits on the corridor minima (new CCGT 15 GW, wind 51 GW in 2040); the surplus goes to the US or into low capacity factors.', 'Keep the corridor (it is centred on a CER world with similar demand) and report exports and capacity factors; alternatively release the gas minimum, see open questions.'),
                   ('GREEN', 'data', 'Gas supply: the Alberta pipeline system is fully subscribed until 2029 and markets about 1.0 Bcf/d of new capacity for 2030-2032 (about 6 GW of combined cycle); the stretch needs 3.7 Bcf/d by 2035. The model has no gas-network limit for Canada.', 'State it as a condition of the stretch; no model change.'),
                   ('GREEN', 'data', 'The Crossfield concept (customer, date, status) is not public.', 'Siemens Energy to supply timing; until then it is inside 6B by size.'),
                   ('GREEN', 'data', 'Announced specific cost of dedicated H-class plants (2,900-3,400 EUR/kW nominal) is about three times the model CCGT cost.', 'Not changed in the scenario; candidate for a cost sensitivity or the next baseline.')]),
]
