# -*- coding: utf-8 -*-
"""Canada plan, part 5: scenarios 7 (wind re-acceleration) and 8 (critical minerals). Research note D.
Wind paths are national onshore totals in GW; the base corridor values were read from the input dump of the frozen base."""
from ca_plan_sources import U

BASE_WIND = (31.0, 62.2, 87.2)             # frozen base result, GW 2030 / 2035 / 2040
BASE_WIND_MIN = (31.0, 44.2, 50.6)         # corridor minimum (P_Wind_Onshore_Avg)
BASE_WIND_MAX = (40.6, 107.0, 150.9)       # corridor maximum, all onshore classes (Avg + Opt + Inf)
CAPEX = (1150, 1125, 1100)                 # model onshore capex EUR/kW 2030 / 2035 / 2040
W_A = (28.0, 43.5, 55.7)                   # announced procurement (bottom-up)
W_B = (45.0, 70.0, 87.0)                   # CanREA / Dunsky Accelerated
W_C = (39.7, 77.5, 113.3)                  # CER Canada Net-zero, onshore
OFF_C = (0, 5, 15)                         # offshore, stretch
F_A = (1.13, 1.13, 1.13)                   # cold-climate package x tower surtax
F_B = (0.948, 0.93, 0.91)                  # Accelerated / Reference cost ratio
F_C = (0.846, 0.83, 0.81)                  # CER Net-zero / Current Measures cost ratio


def _cx(f):
    return ' / '.join(f'{round(c * x / 10) * 10:,}' for c, x in zip(CAPEX, f))


def _p(t):
    return ' / '.join(f'{x:g}' for x in t)


SOURCES = [
    ('D1', 'Hydro-Quebec', 'Wind Power (more than 10,000 MW of new wind by 2035; partnership zones)', '2026-10', U('hydroquebec.com/a/wind-power'), 'S7 Quebec target'),
    ('D2', 'Hydro-Quebec', 'New procurement strategy to maximise economic benefits of major wind power projects (turbine request for proposals)', '2026-05-11', U('hydro-quebec-introduces-new-procurement'), 'S7 Quebec zones, suppliers'),
    ('D3', 'Canadian Renewable Energy Association', "News release: the stage is set for the future of Canada's wind, solar and energy storage industry (2025 data)", '2026-02-03', U('the-stage-is-set'), 'S7 additions 2025, pipeline'),
    ('D4', 'IEA Wind TCP', 'Annual Report 2025 - Canada', '2026', U('iea-wind.org'), 'S7 fleet, generation, procurement need'),
    ('D5', 'Canada Energy Regulator', 'Wind power to drive Canada renewable energy growth through 2030', '2025-11-26', U('wind-power-drive-canada'), 'S7 planned additions by province'),
    ('D6', 'Canadian Renewable Energy Association / Dunsky', "Canada's Renewable Energy Market Outlook 2025 - executive summary", '2025-09', U('CanadianREmarketoutlook2025'), 'S7 Reference and Accelerated paths, cost trend'),
    ('D7', 'Canada Energy Regulator', "Canada's Energy Future 2026 - Appendix 2 (technology cost assumptions)", '2026-03', U('appendix-2'), 'S7 wind capital cost by scenario'),
    ('D8', 'BC Hydro', '2024 Call for Power - electricity purchase agreements filing', '2025-02-12', U('2025-02-12-bch-2024-call'), 'S7 British Columbia'),
    ('D9', 'Today in BC', "Four wind projects selected from BC Hydro's 2025 Call for Power", '2026-05-13', U('todayinbc.com'), 'S7 British Columbia'),
    ('D10', 'Manitoba Hydro', 'First request for proposals under the Indigenous wind call for power', '2026-03', U('hydro.mb.ca/articles/2026/03'), 'S7 Manitoba'),
    ('D11', 'SaskPower', 'Rose Valley and Seven Stars wind projects', '2026', U('saskpower.com'), 'S7 Saskatchewan'),
    ('D12', 'Government of Nova Scotia', 'Offshore wind (licensing: first call up to 5 GW)', '2026', U('novascotia.ca/offshore-wind'), 'S7 offshore'),
    ('D13', 'Global News / Canadian Press', 'Nova Scotia Wind West: CAD 60 bn for the initial phase (government document)', '2025-09-12', U('globalnews.ca/news/11417164'), 'S7 offshore cost'),
    ('D14', 'Privy Council Office, Major Projects Office', 'Wind West Atlantic Energy (project referred to the office)', '2026', U('referred/wind-wes'), 'S7 offshore ambition'),
    ('D15', 'Canada Gazette', 'Remission order SOR/2026-34 (surtax on steel derivative goods incl. wind towers)', '2026-03-11', U('sor-dors34'), 'S7 tower surtax'),
    ('D16', 'Canadian Renewable Energy Association', "Statement: Canada's tariff announcement will increase the cost of electricity", '2025-11-27', U('statement-canadas-tariff'), 'S7 tower surtax'),
    ('D17', 'NYSERDA (citing NREL)', 'Great Lakes Wind Energy Feasibility Study - cost analysis (cold-weather package)', '2022', U('22-12g-GLWFS'), 'S7 cold-climate premium'),
    ('D18', 'Winterwind', 'Icing challenge for Canadian wind energy', '2019', U('winterwind.se'), 'S7 icing losses'),
    ('D19', 'Pembina Institute', 'Renewable energy project cancellations in Alberta hit alarming milestone', '2025-08', U('pembina.org/media-release'), 'S7 Alberta counter-signal'),
    ('D20', 'The Independent (Newfoundland and Labrador)', 'Hydrogen hype (wind-hydrogen projects losing land reserves)', '2026-06-16', U('theindependent.ca'), 'S7, S9 Newfoundland'),
    ('D21', 'Hydro-Quebec Distribution', "Etat d'avancement 2025 du Plan d'approvisionnement 2023-2032", '2025-10-31', U('etat-davancement'), 'S7 Quebec supply gap'),
    ('D22', 'National Observer', 'Steel tariffs and Canadian wind energy (tower share of capital cost)', '2025-12-12', U('steel-tariffs-canada-wind-energy'), 'S7 tower share'),
]

SIGNALS = [
    (7, 'Hydro-Quebec targeting up to 10 GW of wind by 2035',
     'The Action Plan 2035 targets "over 10,000 MW" of NEW wind by 2035 on top of about 4,000 MW installed: an addition and a floor, not a total. Quebec would reach about 14 GW. The current tender (5-10 TWh) has a commissioning window of 2031-2038, so part of the volume arrives after 2035.',
     'Corrected: more than 10 GW added (total about 14 GW); part lands 2036-2038', 'D1, E3, E9'),
    (7, 'Quebec is the anchor market',
     'Planned renewable additions to 2030: Quebec 3,545 MW of 8,745 MW nationally. Five Hydro-Quebec partnership zones of 12-12.5 GW together are under study without in-service dates; a consolidated turbine request for proposals was launched on 11 May 2026 (qualified European and North American manufacturers only).',
     'Confirmed', 'D2, D5'),
    (7, 'Ontario, British Columbia, Manitoba, Saskatchewan and Atlantic Canada add smaller but material procurement waves',
     'British Columbia: 2.7 GW contracted in two calls (1,531 + 1,158 MW), on line 2030-2033. Ontario: only 0.2-0.4 GW of wind in the first LT2 window. Manitoba: up to 600 MW, first 200 MW tendered. Saskatchewan: 400 MW. Nova Scotia 625 MW by 2028, New Brunswick 450 MW. Newfoundland wind-hydrogen pipeline largely cancelled in 2026.',
     'Confirmed (British Columbia is larger than "smaller"; Ontario is small)', 'D8, D9, D10, D11, D20, E4'),
    (7, 'Re-acceleration',
     '2025 was a trough: 347 MW of new wind, fleet about 19 GW. About 8 GW of wind, solar and storage expected to connect by 2029; "nearly 24 GW" announced for the next ten years.',
     'Confirmed (from a low base)', 'D3, D4'),
    (7, 'Opportunity strongest where wind is paired with transmission, storage and Indigenous equity partnerships',
     'Indigenous equity is in every recent award (Ontario 50-51 %, British Columbia 51 %, Manitoba majority ownership, Hydro-Quebec zones 50/50). Pairing with transmission and storage is not quantified in the sources.',
     'Confirmed for equity; pairing not quantified', 'D9, D10, E4'),
    (7, 'Headwind: product adaptation for cold climate and de-icing',
     'Icing losses 1.3-2.7 % of Quebec wind production (up to 20 % at single farms); generic cold-weather package +10 % turbine capital cost and +15 % operating cost (NREL). No Canada-specific premium found.',
     'Confirmed (generic figures)', 'D17, D18'),
    (7, 'Headwind: tower and tariff exposure',
     '25 % surtax on imported wind towers since 26 December 2025 (remission for offshore projects and earlier purchase orders); one domestic tower maker. Industry claims towers are 20-30 % of capital cost.',
     'Confirmed', 'D15, D16, D22'),
    (7, 'Headwind: competitive pressure',
     'No market-share table by turbine maker found; winner of the Hydro-Quebec turbine request for proposals not announced.',
     'Not found', '-'),
    (7, '(not in the request) Alberta',
     'About 11 GW of wind, solar and storage withdrawn from the Alberta queue since October 2023; installations in 2025 down 93 % against 2022.',
     'Partly: counter-signal in the largest merchant market', 'D19'),
]

ASSUMPTIONS = [
    (7, 'Wind re-acceleration', '7A procurement-paced', 'Onshore wind capacity MAXIMUM (all classes together)', 'Canada', '2030 / 2035 / 2040', f'{_p(W_A)}  (base result {_p(BASE_WIND)})', 'GW',
     'Bottom-up sum of contracted volumes and stated utility targets: Quebec 8.3 / 14.3 / 19, Ontario 6.1 / 7.7 / 8.5, Alberta 7.2 / 10.2 / 13.4 (CER Current Measures), British Columbia 1.4 / 3.4 / 5.8, others 5.0 / 7.9 / 9.0; Newfoundland wind-hydrogen fleet removed. Imposed as a ceiling because as a floor it would not bind.',
     'D1, D5, D8, D9, D10, D11, E4, M2', 'Medium', 'Partly (2040 values, Ontario share)'),
    (7, 'Wind re-acceleration', '7A procurement-paced', 'Onshore wind corridor minimum', 'Canada', '2030 / 2035 / 2040', f'lowered to the 7A path where the base minimum is higher (base minimum {_p(BASE_WIND_MIN)})', 'GW',
     'The base minimum (CER Current Measures -20 %) is above the announced path in 2030 and 2035 because CER carries 11 GW of Newfoundland wind-hydrogen capacity.', 'M1, M2, D20', 'High', 'No'),
    (7, 'Wind re-acceleration', '7A procurement-paced', 'Onshore wind capital cost with headwinds', 'Canada', '2030 / 2035 / 2040', f'x1.13 = {_cx(F_A)}  (model {_p(CAPEX)})', 'EUR/kW',
     'Cold-climate package +10 % of turbine cost = +7 % of total at a 70 % turbine share; tower surtax 25 % on a tower share of 10-30 % = +2.5 to +7.5 %; product 1.10-1.15, 1.13 used. Optional: capacity factor -2 % for icing.',
     'D15, D17, D18, D22', 'Low', 'Partly (turbine and tower shares)'),
    (7, 'Wind re-acceleration', '7B accelerated', 'Onshore wind capacity MINIMUM', 'Canada', '2030 / 2035 / 2040', f'{_p(W_B)}  (base result {_p(BASE_WIND)}; base maximum 2030 {BASE_WIND_MAX[0]})', 'GW',
     'CanREA / Dunsky Accelerated scenario (45 GW in 2030, 70 GW in 2035); 2040 linear between 70 GW (2035) and 122 GW (2050). Front-loads the base build-out by about five years; the 2026-2030 corridor ceiling must be lifted to let 45 GW in. Same order of magnitude as CER Higher (36 / 68 / 87).',
     'D6, M2', 'Medium', 'Partly (2040 interpolation)'),
    (7, 'Wind re-acceleration', '7B accelerated', 'Onshore wind capital cost', 'Canada', '2030 / 2035 / 2040', f'x{_p(F_B)} = {_cx(F_B)}', 'EUR/kW',
     'Ratio of the Accelerated to the Reference cost trend in the same outlook (-9 % against -4 % in 2030; -15 % against -2 % in 2050), interpolated.', 'D6', 'Medium', 'Partly (interpolation)'),
    (7, 'Wind re-acceleration', '7C stretch: net-zero pace plus offshore', 'Onshore wind capacity MINIMUM', 'Canada', '2030 / 2035 / 2040', f'{_p(W_C)}', 'GW',
     'CER Canada Net-zero onshore path (Ontario 20, Alberta 25, British Columbia 17, Newfoundland 16, Nova Scotia 13, Quebec 12 GW in 2040). Inside the base corridor maximum.', 'M2', 'Medium', 'No'),
    (7, 'Wind re-acceleration', '7C stretch: net-zero pace plus offshore', 'Offshore wind capacity (fixed path, shallow class)', 'Canada', '2030 / 2035 / 2040', f'{_p(OFF_C)}  (far what-if: 40 in 2040)', 'GW',
     'Nova Scotia first licensing call up to 5 GW, later calls up to a further 10 GW; operation of the first 5 GW in 2035 is an assumption (construction possible from 2033). 40 GW is the Wind West ambition. Energy 24 TWh per 5 GW (capacity factor 54.8 %).',
     'D12, D14, A20', 'Low', 'Partly (timing)'),
    (7, 'Wind re-acceleration', '7C stretch: net-zero pace plus offshore', 'Offshore wind capital cost', 'Canada', '2030-2040', '5,480 generation + 2,740 transmission = 8,220  (model shallow class 2,393 in 2030 as the optimistic sub-case)', 'EUR/kW',
     'Nova Scotia government estimate for the first 5 GW: CAD 40 bn wind farms + CAD 20 bn transmission. The path is forced, so the cost only moves the system cost, not the build.', 'D13', 'Low', 'No'),
    (7, 'Wind re-acceleration', '7C stretch: net-zero pace plus offshore', 'Onshore wind capital cost', 'Canada', '2030 / 2035 / 2040', f'x{_p(F_C)} = {_cx(F_C)}', 'EUR/kW',
     'Ratio of the CER Net-zero to the Current Measures wind cost (1,495 / 1,767 C$/kW in 2030; 1,196 / 1,530 in 2050), interpolated.', 'D7', 'Medium', 'Partly (interpolation)'),
]

SCENARIOS = [
    dict(id=7, name='Wind market re-acceleration', tag='Mixed/Tailwind',
         meaning='How much onshore wind Canada builds and at what cost. In the model: the national onshore wind path (as a ceiling or a floor), the wind capital cost with the named headwinds, and offshore wind in the stretch.',
         levers='Par_TotalAnnualMaxCapacity / Par_TotalAnnualMinCapacity Canada / P_Wind_Onshore_* ; Par_CapitalCost Canada wind; P_Wind_Offshore_Shallow minimum path and cost (stretch).',
         route='Scenario generator, data rows only. Offshore wind exists as a technology with potential for Canada and is simply not built in the base.',
         flag='GREEN', flag_summary='Existing levers. Provincial pattern (Quebec as anchor) and the pairing with transmission and storage are invisible in one node.',
         evidence='High for procurement volumes (utility plans, awards); medium for timing after 2030; low for the headwind cost figures (generic, not Canada-specific)',
         base_cmp=f'BASE IS ABOVE THE ANNOUNCED PROCUREMENT. Base {_p(BASE_WIND)} GW (2030 / 2035 / 2040) against announced procurement {_p(W_A)} and CER Current Measures 33.9 / 55.2 / 63.3; the base equals CER Higher in 2040 (87.2). The base adds 5.5 GW/yr on average against 0.35 GW built in 2025. The signal as worded is inside the base.',
         variants=f'7A procurement-paced: announced path as a CEILING ({_p(W_A)} GW) with headwind cost x1.13 - the "Mixed" reading. 7B accelerated: CanREA Accelerated as a FLOOR ({_p(W_B)} GW), cost x0.95-0.91 - the "Tailwind" reading. 7C stretch: CER Net-zero onshore ({_p(W_C)} GW) plus Nova Scotia offshore 0 / 5 / 15 GW (far what-if 40 GW).',
         effort='S', anchors='Hydro-Quebec Action Plan 2035 and wind strategy; BC Hydro calls 2024 and 2025; IESO LT2; CanREA / Dunsky outlook 2025; CER EF2026 scenario paths and cost appendix; Nova Scotia Wind West; Canada Gazette tower surtax',
         concerns=[('GREEN', 'data', 'The base already builds more wind than the announced procurement adds up to; a variant that follows the signal literally is a restriction against the base.', 'Run 7A as a ceiling (Mixed) and 7B as a floor (Tailwind) so both directions are visible; decide the pair in the open questions.'),
                   ('YELLOW', 'model', f'7A needs the wind corridor minimum lowered in 2030-2035 (base minimum {_p(BASE_WIND_MIN)} GW), 7B needs the 2026-2030 ceiling lifted (base maximum 24.2 GW in 2028, {BASE_WIND_MAX[0]} GW in 2030).', 'Both are corridor edits inside the scenario definition (no separate "released" run); state them in the run definition.'),
                   ('YELLOW', 'model', 'Offshore wind sits in one Canada node: Nova Scotia location, the Atlantic transmission and the export route to New England cannot be represented; the model cost (2,393 EUR/kW) is 44 % of the Nova Scotia estimate.', 'Force the offshore path, use the Nova Scotia cost including transmission, and report where the energy goes (curtailment, exports).'),
                   ('GREEN', 'data', 'Cold-climate and tower-surtax premia rest on generic or industry figures; turbine-maker shares were not found.', 'Siemens Energy / Siemens Gamesa product cost data could replace the x1.13 factor.')]),
]

# =====================================================================================================================
# Scenario 8: critical minerals. Load added to the Canada node as a flat adder (busbar TWh, relative to 2025).
M_A = (3.0, 4.4, 4.4)                      # decided projects
M_B = (7.5, 19.7, 21.7)                    # advanced projects + utility planning view for Quebec
M_C = (13.8, 37.3, 58.3)                   # stretch: whole named pipeline + processing build-out
CELLS = ((1.3, 3.3, 4.2), (1.0, 3.3, 4.2), (1.3, 5.3, 6.2))     # optional battery cell plants, variants A / B / C
_US = 'US side identical to the base (funnel unchanged).'


def _plus(t):
    return ' / '.join(f'+{x:g}' for x in t)


SOURCES += [
    ('D23', 'Government of Canada', 'Budget 2025, chapter 1 (Critical Minerals Sovereign Fund; First and Last Mile Fund)', '2025-11-04', U('budget.canada.ca'), 'S8 signal'),
    ('D24', 'Natural Resources Canada', 'Canada announces first agreement under new Canada Critical Minerals Accelerator (Teck Trail)', '2026-07-07', U('canada-announces-first-agreement-under-new-canada-critical-minerals-accelerator'), 'S8 signal'),
    ('D25', 'Natural Resources Canada', 'Backgrounder: new investments and partnerships with 9 allied countries (Critical Minerals Production Alliance, first round)', '2025-10-31', U('backgrounder-canada-unlocks-25'), 'S8 signal'),
    ('D26', 'Natural Resources Canada', 'Canada secures 30 new critical minerals partnerships and unlocks CAD 12.1 billion in mining project capital', '2026-03-02', U('canada-secures-30-new-critical-minerals'), 'S8 signal'),
    ('D27', 'Natural Resources Canada', "Backgrounder: Government of Canada invests to unlock Canada's critical minerals advantage (First and Last Mile Fund awards)", '2026-03-03', U('backgrounder-government-of-canada-invests-to-unlock'), 'S8 project loads, grid upgrades for mines'),
    ('D28', 'Natural Resources Canada', 'Comprehensive Energy Use Database, industrial sector (smelting and refining, iron and steel, mining)', '2023 data', U('oee.nrcan.gc.ca'), "S8 today's electricity use"),
    ('D29', 'Statistics Canada', 'Table 16-10-0029-02: mining industries, energy consumption in quantities by industry', '2026-06-03', U('pid=1610002902'), "S8 today's electricity use"),
    ('D30', 'The Narwhal', "B.C.'s North Coast transmission line: big claims, few details (government briefing note: mining 900 MW)", '2026', U('north-coast-transmission-line-power-demand'), 'S8 British Columbia'),
    ('D31', 'BHP', 'Update - Jansen Stage 2 potash project', '2026-06', U('update---jansen-stage-2'), 'S8 Saskatchewan'),
    ('D32', 'Champion Iron', 'Pre-feasibility study for the Kami iron ore property (site power 172 MW)', '2024-03-14', U('championiron.com'), 'S8 Labrador'),
    ('D33', 'Generation Mining / Ausenco', 'Marathon copper-palladium project, feasibility study update (48.9 MW)', '2025-03-28', U('Marathon-FS'), 'S8 Ontario'),
    ('D34', 'Canada Nickel', 'Agreements with Hydro One to commence engineering for the Crawford nickel project power connection', '2026-03-09', U('canada-nickel-secures-agreements'), 'S8 Ontario'),
    ('D35', 'Newfoundland and Labrador Hydro', 'Labrador West Transmission Expansion Study (735 kV line, about 1,500 MW)', '2026', U('labrador-west-transmission-expansion'), 'S8 Labrador'),
    ('D36', 'Department of Finance Canada', 'Canada Growth Fund investment in Ontario copper and palladium mine (Marathon)', '2026-09-15', U('minister-champagne-welcomes'), 'S8 signal, decided projects'),
    ('D37', 'Natural Resources Canada', "Canada's Critical Minerals Strategy - progress update (pipeline CAD 72.4 bn)", '2026-02-27', U('canadas-critical-minerals-strategy-progress-update'), 'S8 pipeline size'),
    ('D38', 'Privy Council Office, Major Projects Office', 'North Coast Transmission Line (project page)', '2026', U('projects/national/nctl'), 'S8 British Columbia'),
    ('D39', 'Newcrest Red Chris Mining', 'Block Cave Project - project description (site demand 48 to about 120 MW)', '2023', U('projects.eao.gov.bc.ca'), 'S8 British Columbia'),
    ('D40', 'International Aluminium Institute', 'Primary aluminium smelting power consumption', '2024', U('international-aluminium.org'), 'S8 intensity'),
    ('D41', 'Fraunhofer FFB (Degen et al., Nature Energy 2023)', 'Energy consumption of current and future production of lithium-ion battery cells', '2023', U('ffb.fraunhofer.de'), 'S8 intensity (cell plants)'),
    ('D42', 'Kelly et al. (Argonne National Laboratory)', 'Energy, greenhouse gas and water life cycle analysis of lithium carbonate and lithium hydroxide monohydrate', '2021', U('osti.gov'), 'S8 intensity (lithium)'),
]

SIGNALS += [
    (8, '$2B funding for Critical Mineral Accelerator, provides equity, loan guarantees, offtake',
     'Budget 2025 created the Critical Minerals Sovereign Fund: CAD 2 bn over five years from 2026-27 for equity investments, loan guarantees and offtake agreements. It was launched on 7 July 2026 as the Canada Critical Minerals Accelerator, delivered by Export Development Canada.',
     'Confirmed (name, amount and instruments)', 'D23, D24'),
    (8, '... to push projects to FID faster',
     'One agreement so far (Teck Trail smelter: germanium, antimony, gallium; Canada Growth Fund up to CAD 400 m), still subject to final documentation. Investment decisions taken in 2025-2026 came through other channels (Highland Valley Copper, Matawinie graphite, Marathon copper-palladium, Thompson nickel).',
     'Partly: instrument exists with one conditional deal; no investment decision attributable to it yet', 'D24, D36'),
    (8, '26 new investments / partnerships with allied countries',
     'First round of the G7 Critical Minerals Production Alliance (31 October 2025): 26 items with 9 countries, CAD 6.4 bn of projects. March 2026: 30 more items with 12 partners, CAD 12.1 bn; June 2026: 13 more. The amounts are total project values, not public money, and include projects outside Canada.',
     'Confirmed (first round; 69 items after three rounds)', 'D25, D26'),
    (8, '221 active exploration licenses, including $1.1B committed investment',
     'No source found for this pair of numbers in two search sessions; jurisdiction unknown.', 'Not found', '-'),
    (8, '(not in the request) processing and battery chain',
     'Counter-signals since 2024: Northvolt Six dead (352 MW block freed), Ford left the Becancour cathode plant, Vale cancelled its nickel sulphate plant, Ultium CAM phase 2 paused, Honda Alliston and Umicore Loyalist suspended, PowerCo delayed to 2029, Glencore suspended about CAD 1 bn at the Horne copper smelter; Hydro-Quebec cut its battery-chain forecast by 314 MW.',
     'Partly: the tailwind is in mining and strategic by-product metals, not in battery materials', 'D21'),
]

ASSUMPTIONS += [
    (8, 'Critical minerals', '8A decided projects', 'Flat load added to the Canada node (relative to 2025)', 'Canada', '2030 / 2035 / 2040', _plus(M_A), 'TWh',
     'Projects with an investment decision, closed financing or under construction: Jansen potash stages 1 and 2 (150 + 150 MW, 54 % of the total), Highland Valley Copper +34 MW, Marathon 48.9 MW, McIlvenna Bay 16 MW, Phoenix uranium 8.8 MW, Nemaska lithium, Matawinie graphite, Alouette +50 MW.',
     'D27, D31, D33, D36', 'Medium', 'Partly (Jansen stage split, MW of Nemaska and Matawinie)'),
    (8, 'Critical minerals', '8B advanced projects, utility planning view', 'Flat load added to the Canada node', 'Canada', '2030 / 2035 / 2040', _plus(M_B), 'TWh',
     '8A plus permitted and advanced projects one to two years late (Red Chris block cave +72 MW, Crawford nickel 150 MW rising to 270 MW, Thunder Bay lithium, Kami iron ore 171 MW, Sisson 40 MW); Quebec taken from the Hydro-Quebec supply-plan filing read one year late (battery chain, mines, smelting and refining, aluminium: 5.5 / 13.1 / 14.2 TWh). Two thirds of the total is Quebec. Same size as the CER Higher wedge over Current Measures (+9 / +19 / +29).',
     'D21, D32, D34, D39, M2', 'Low', 'Partly (timing; Crawford phase 2 and Sisson MW)'),
    (8, 'Critical minerals', '8C stretch: whole pipeline plus processing build-out', 'Flat load added to the Canada node', 'Canada', '2030 / 2035 / 2040', _plus(M_C), 'TWh',
     'Whole named pipeline: North Coast mining block 900 MW (6.7 TWh), Labrador West 1,000 MW (7.4 TWh), Ontario high-demand industrial wedge (+8.7 TWh), Hydro-Quebec filing without delay plus the freed Northvolt block, one new 500,000 t/yr aluminium line (6.75 TWh), two more potash stages, and a domestic lithium / graphite / nickel sulphate / copper / rare-earth processing chain (under 2 TWh in total).',
     'D21, D30, D35, D37, D38, D40, D42, C14', 'Low', 'Partly (assumed tonnages and shares of line capacity)'),
    (8, 'Critical minerals', 'all variants', 'Load factor; path between waypoints; profile', 'Canada', '2025-2040', '0.85 mines and concentrators; 0.90 potash, smelters, chemical plants; linear from zero in 2025; flat profile', '-',
     'Assumptions of the research note. Off-grid projects (Rook I, Eagle\'s Nest, Strange Lake, the territories) count zero unless a variant connects them; gold-only mines and steel electric-arc furnaces are left out.', '-', 'Low', 'Yes (load factors)'),
    (8, 'Critical minerals', 'optional add-on', 'Battery cell plants (manufacturing, not minerals)', 'Canada', '2030 / 2035 / 2040', f'8A {_plus(CELLS[0])};  8B {_plus(CELLS[1])};  8C {_plus(CELLS[2])}', 'TWh',
     'NextStar 49.5 GWh/yr and PowerCo 90 GWh/yr (start 2029) at 30 kWh per kWh of cells, all as electricity (upper bound); stretch adds Honda 36 GWh/yr and one further plant.', 'D41', 'Low', 'Partly (ramp, intensity)'),
    (8, 'Critical minerals', 'information only', "Today's electricity use of the sector", 'Canada', '2023-2024', 'mining 16.5 (purchased); non-ferrous smelting and refining 68.2 (of which aluminium 60.2); iron and steel 7.9; together about 93 = 18 % of the general load of the base', 'TWh',
     'Statistics Canada and NRCan energy-use tables. Outside aluminium, the part a minerals boom scales is about 32 TWh.', 'D28, D29', 'High', 'No'),
    (8, 'Critical minerals', 'information only', 'Industrial electricity growth in the CER outlook (all industry, from 2025)', 'Canada', '2030 / 2035 / 2040', 'Current Measures +24 / +54 / +80; Higher +32 / +72 / +108; base general load +5 / +9 / +12', 'TWh',
     'The base general load is flat, so none of the minerals load is in the base; all three variants stay inside the CER Current Measures industrial growth.', 'M1, M2', 'High', 'No'),
]

SCENARIOS += [
    dict(id=8, name='Critical minerals essential for trade', tag='Tailwind',
         meaning='New mines, concentrators, smelters and processing plants as additional industrial load on the Canadian grid. The policy money decides when projects go ahead; in the model only the load arrives.',
         levers='Par_SpecifiedAnnualDemand Canada / Power_LargeLoads (flat demand adder).',
         route='Scenario generator: demand rows with the existing helper.',
         flag='GREEN', flag_summary='Existing lever. Limits: off-grid mines and the territories are outside the node, and the location of the load (north-west British Columbia, Labrador West, northern Ontario) with the transmission it needs is invisible.',
         evidence='High for the policy instruments and for today\'s electricity use; medium for decided projects; low for the stretch (assumed tonnages). "221 licences / $1.1B" was not found',
         base_cmp=f'The base general load is FLAT (513 to 525 TWh), so every variant is additional: {_plus(M_A)} / {_plus(M_B)} / {_plus(M_C)} TWh in 2030 / 2035 / 2040 for 8A / 8B / 8C = 0.5 % / 2.4 % / 6.5 % of Canadian demand in 2040. All variants stay inside the industrial growth of CER Current Measures (+80 TWh by 2040). Small against data centres (+252 TWh from 2025 in the base).',
         variants=f'8A decided projects ({_plus(M_A)} TWh). 8B advanced projects and the utility planning view ({_plus(M_B)} TWh). 8C stretch: whole named pipeline plus a domestic processing chain ({_plus(M_C)} TWh; one new aluminium line, the 900 MW North Coast mining block, 1,000 MW in Labrador West). Optional add-on: battery cell plants ({_plus(CELLS[1])} TWh).',
         effort='S', anchors='Budget 2025 and the Canada Critical Minerals Accelerator; Critical Minerals Production Alliance rounds; First and Last Mile Fund awards; Hydro-Quebec supply-plan filing 2025; IESO 2026 outlook; Statistics Canada and NRCan energy-use tables; technical reports (Kami, Marathon, Red Chris, Crawford); North Coast Transmission Line',
         concerns=[('GREEN', 'data', 'The signal is policy money (CAD 2 bn fund, CAD 1.5 bn infrastructure fund) against a CAD 72 bn project pipeline; the electricity effect is modest: about 4 TWh from decided projects, about 20 TWh in the utility planning view.', 'Run 8B as the scenario and 8C as the stretch; 8A is below 1 % of Canadian demand and will not differ visibly from the base.'),
                   ('YELLOW', 'model', 'One node: remote mining loads need dedicated lines (North Coast line about CAD 6 bn, Labrador West 735 kV) that the model neither sees nor costs.', 'Report the load nationally and list the enabling lines as cost outside the model.'),
                   ('GREEN', 'model', 'Overlap with scenario 9 (its industry adder of +8 / +19 / +29 TWh has the size of 8B) and with scenario 5 (northern mines).', 'Run separately; do not add the scenarios up.'),
                   ('GREEN', 'data', 'Several project loads are not published (Nemaska, Ultium CAM, Crawford phase 2; Jansen split assumed); two thirds of 8B rest on one Hydro-Quebec filing; the source of "221 licences / $1.1B" is unknown.', 'Ask the requester for the source of the licence figure; Siemens Energy customer data could replace the assumed MW.')]),
]

RUNS_S8 = [
    ('fel2026_c08b_minerals_49_2015_v6', 'S8 Critical minerals', '8B', f'Flat load added to the base: {_plus(M_B)} TWh (2030 / 2035 / 2040), linear from zero in 2025.', 'Corridor unchanged. ' + _US, 1, 'Same size as the CER Higher industrial wedge.'),
    ('fel2026_c08c_minerals_pipeline_49_2015_v6', 'S8 Critical minerals', '8C stretch', f'Flat load added: {_plus(M_C)} TWh.', 'Corridor unchanged. ' + _US, 2, 'Optional add-on: battery cell plants +1.3 / +5.3 / +6.2 TWh.'),
    ('fel2026_c08a_minerals_decided_49_2015_v6', 'S8 Critical minerals', '8A', f'Flat load added: {_plus(M_A)} TWh.', 'Corridor unchanged. ' + _US, 3, 'Below 1 % of Canadian demand; expect results close to the base.'),
]
