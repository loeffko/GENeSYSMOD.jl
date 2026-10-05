# -*- coding: utf-8 -*-
"""Canada plan, part 3: scenarios 2 (local content) and 4 (Indigenous equity). Research note E.
WACC effects are converted into capex multipliers with the annuity ratio CRF(new, life) / CRF(5 %, life),
because the model discounts overnight capex and has no financing-cost lever."""
from ca_plan_sources import U


def crf(r, n):
    return r * (1 + r) ** n / ((1 + r) ** n - 1)


def mult(wacc, life):
    return round(crf(wacc, life) / crf(0.05, life), 3)


LIFE = {'wind': 27, 'pv': 35, 'ccgt': 25, 'nuclear': 61, 'hydro': 60}
M483 = {k: mult(0.0483, v) for k, v in LIFE.items()}     # S4 variant A, blended 4.83 %
M513 = {k: mult(0.0513, v) for k, v in LIFE.items()}     # S4 variant B, blended 5.13 %
M563 = {k: mult(0.0563, v) for k, v in LIFE.items()}     # S4 variant C, blended 5.63 %
M550 = {k: mult(0.0550, v) for k, v in LIFE.items()}     # S2 variant C, +50 bp

SOURCES = [
    ('E1', 'Public Services and Procurement Canada', 'Buy Canadian - Backgrounder', '2025-12', U('buy-canadian'), 'S2 federal rule'),
    ('E2', 'Torys', 'Buy Ontario Procurement Directive: key requirements', '2026-04', U('buy-ontario'), 'S2 Ontario rule'),
    ('E3', 'Stikeman Elliott', "Understanding Hydro-Quebec's Call for Tenders 2026-01: Key New Features", '2026', U('stikeman.com'), 'S2 Quebec content 65 %'),
    ('E4', 'IESO', 'Results of the Long-Term 2 Window 1 Energy Stream', '2026-04', U('LT2-W1-results'), 'S2, S4 Ontario procurement results'),
    ('E5', 'OECD', 'Overcoming Barriers to International Investment in Clean Energy (ch. 3, local-content requirements)', '2015', U('oecd.org/content/dam'), 'S2 cost premium wind'),
    ('E6', 'Peterson Institute', "'Buy American' and similar domestic purchase policies impose high costs on taxpayers", '2020-08-06', U('piie.com/research/piie-charts'), 'S2 cost premium'),
    ('E7', 'Probst et al., Nature Energy', 'The short-term costs of local content requirements in the Indian solar auctions', '2020', U('nature.com/articles/s41560-020-0677-7'), 'S2 cost premium solar'),
    ('E8', 'Canadian Renewable Energy Association', 'By the Numbers (2025 data)', '2026', U('renewablesassociation.ca/by-the-numbers'), 'S2, S7 wind fleet and build rate'),
    ('E9', 'Hydro-Quebec', 'Wind Power Development Strategy', '2024', U('wind-power-development-strategy'), 'S2, S4, S7 Quebec wind'),
    ('E10', 'IEA', 'Building the Future Transmission Grid (executive summary)', '2025', U('building-the-future-transmission-grid'), 'S2 transformer lead times and prices'),
    ('E11', 'CleanTechnica', 'The New Geography Of Wind Power In Canada', '2026-04-16', U('cleantechnica.com/2026/04/16'), 'S2, S7 wind additions 2025'),
    ('E12', 'ANS Nuclear Newswire / ReNew Canada', 'OPG completes Darlington refurbishment (96 % Ontario spend); Darlington SMR 80 % Ontario spend', '2026-02-03', U('ans.org/news/2026-02-03'), 'S2 nuclear local content'),
    ('E13', 'World Nuclear News', 'First Nations group takes stake in Ontario nuclear plant', '2026-06', U('first-nations-group-takes-stake'), 'S4 signal'),
    ('E14', 'Department of Finance Canada', 'Government announces largest Indigenous loan guarantee in Canadian history to support Darlington New Nuclear Project', '2026-06-23', U('largest-indigenous-loan-guarantee'), 'S4 financing'),
    ('E15', 'RBC Thought Leadership', "Nations Building: Assessing Indigenous loan guarantee programs in Canada's new project wave", '2026-04-29', U('rbc.com/en/thought-leadership/indigenous'), 'S4 guarantee programmes, cost of capital'),
    ('E16', 'CIM Magazine', 'A fairer future (FNMPC on loan guarantees: 150-250 bp)', '2024-07-15', U('cim.org/en/news/2024/a-fairer-future'), 'S4 cost of capital'),
    ('E17', 'Hydro One', 'First Nation Partnership Powers Completion of the Niagara Reinforcement Line', '2019-09-05', U('First-Nation-Partnership'), 'S4 delay evidence'),
    ('E18', 'Government of Canada', 'Getting Major Projects Built in Canada - Discussion Paper', '2026-07', U('getting-major-projects-built'), 'S4 review timelines'),
    ('E19', 'Prime Minister of Canada', 'Major Projects Office launch (two-year maximum for national-interest projects)', '2025-08-29', U('pm.gc.ca/en/news/news-releases/2025/08/29'), 'S4 review timelines'),
    ('E20', 'The Narwhal', 'Wind energy in B.C. now exempt from environmental assessment', '2024-12-09', U('thenarwhal.ca'), 'S4 acceleration evidence'),
]

SIGNALS = [
    (2, 'Buyers increasingly require Canadian content (federal, ON, QC)', 'Federal Buy Canadian policy in force since Dec 2025 (10 % price preference, threshold lowered to CAD 5 m in June 2026); Buy Ontario directive in force April 2026 (10 % advantage, up to 35 % of the score; OPG and IESO capital projects exempt from the supply-chain-plan part); Hydro-Quebec wind tender 2026-01 targets 65 % Quebec content, worth up to CAD 20/MWh.', 'Confirmed', 'E1, E2, E3'),
    (2, 'Alberta requires local content', 'No formal Alberta rule found (merchant market without a central buyer).', 'Not found', '-'),
    (2, 'Local content becomes a differentiator in procurements', 'True as a scored preference (1-3 % IESO, 10 % federal and Ontario, up to CAD 20/MWh Hydro-Quebec); hard mandates only for steel, aluminium and wood (federal) and the exclusion of some US suppliers (Ontario). 13 of 14 winners in Ontario LT2 window 1 were Canadian-status proponents.', 'Confirmed as scoring; corrected: mostly not a mandate', 'E2, E3, E4'),
    (2, 'Calls from AIEQ, OPG, Invest Alberta, CANDU for SE to invest locally', 'No public statement naming Siemens Energy and no SE manufacturing investment in Canada found; competitors invest (Hitachi Energy, Northern Transformer, BWXT). Private conversations cannot be verified.', 'Not found (not verifiable)', '-'),
    (4, 'Seven Williams Treaties First Nations secured a $700-million equity partnership in the Darlington New Nuclear Project', 'Announced 23 June 2026: CAD 700 m, structured as a loan to the project partnership that converts to equity once all four units are built; backed by about CAD 715 m of federal and Ontario loan guarantees (largest ever). Share undisclosed (about 3-5 % by arithmetic).', 'Confirmed (loan-to-equity, share undisclosed)', 'E13, E14'),
    (4, 'Projects with Indigenous ownership move faster; projects without may face delay', 'No source shows a schedule effect for Darlington. General evidence is case-based: British Columbia exempted partnered wind from environmental assessment (1-2 years saved); delays without consent range from 10 months (Trans Mountain) to 13 years (Niagara line). No statistical estimate found.', 'Partly: mechanism documented by cases, not quantified', 'E17, E18, E20'),
    (4, 'Indigenous equity as a gating factor in procurement', 'Ontario LT2 window 1: 14 of 14 winners with 50 % or more Indigenous equity; British Columbia calls for power: minimum 25 %, awarded about 51 %; Hydro One: 50 % First Nations equity on new lines; Manitoba 600 MW Indigenous-majority wind. Alberta has no rule.', 'Confirmed for utility procurements', 'E4, E15'),
]

ASSUMPTIONS = [
    # ---- S2
    (2, 'Local content', '2A scored preference', 'Capital cost multiplier from 2028', 'Canada', '2028-2040', 'onshore wind 1.08; utility PV 1.06; batteries 1.06; CCGT 1.05; hydro 1.00; nuclear 1.00', 'factor', 'Mid evidence band: US Buy American +5.6 %, Indian solar LCR +6 %; wind adds a 25 % tower surtax on 10-15 % of capex (+2 %). Nuclear and hydro already have 80-96 % Canadian content (OPG).', 'E6, E7, E12', 'Medium', 'Partly (technology split, start year)'),
    (2, 'Local content', '2B hard mandate', 'Capital cost multiplier', 'Canada', '2028-2032 / 2033-2040', 'wind 1.16 then 1.08; PV 1.10; batteries 1.10; CCGT 1.10; hydro 1.05; nuclear 1.00', 'factor', 'Quebec and Ontario wind local-content rules added about USD 193/kW (+16 %) around 2010-2013; federal and Ontario 10 % price preference; fade after 2032 motivated by the Hydro-Quebec "more than 20 % economies of scale" statement.', 'E5, E1, E2, E9', 'Medium', 'Partly (fade)'),
    (2, 'Local content', '2B hard mandate', 'Build-rate cap onshore wind (group cap on new capacity)', 'Canada', '2026-2030 / 2031-2035', '2.0 / 3.5', 'GW/yr', 'Anchors: 1 GW/yr actually built 2021-2025 (347 MW in 2025), Quebec plan 1.0-1.5 GW/yr, one tower and one blade plant in Canada. Base builds 2-10 GW/yr (5.5 GW/yr on average). The corridor minimum for wind must be scaled down with the cap.', 'E8, E9, E11', 'Low', 'Yes (cap level)'),
    (2, 'Local content', '2B hard mandate', 'Delay of new capacity needing large power transformers', 'Canada', 'to 2032', '+1 year', 'years', 'Transformer lead times up to 4 years and prices +75 % since 2019 (IEA); Canadian transformer capacity expansions reach full output 2028-2032.', 'E10', 'Low', 'Partly'),
    (2, 'Local content', '2C stretch: fortress Canada', 'Capital cost multiplier incl. financing premium', 'Canada', '2027-2040', f"wind 1.25 x {M550['wind']}; PV 1.25 x {M550['pv']}; batteries 1.25; CCGT 1.25 x {M550['ccgt']}; hydro 1.10; nuclear 1.05", 'factor', 'Policy ceiling: federal exception at a 25 % cost increase, Hydro-Quebec CAD 20/MWh. Plus a +50 bp financing premium (direction from the OECD finding that such rules reduce foreign investment; magnitude assumed), converted with the annuity ratio.', 'E1, E3, E5', 'Low', 'Partly (ceiling as premium; +50 bp)'),
    (2, 'Local content', '2C stretch: fortress Canada', 'Build-rate caps and delay', 'Canada', '2026-2040', 'wind 1.5 / 2.5 / 4.0 GW/yr (to 2030 / 2035 / 2040); PV 1.0 GW/yr to 2030; +3 years for wind, PV, batteries, CCGT', 'GW/yr, years', 'Same anchors as 2B; 2-3 years to open a new factory (Northern Transformer, BWXT).', 'E8, E10', 'Low', 'Yes'),
    (2, 'Local content', 'all variants', 'Gas-turbine lead times and price escalation', 'Canada', '2026-2032', 'NOT FOUND - to be supplied by Siemens Energy', '-', 'No public source could be retrieved; this is the most relevant input for an SE scenario and SE holds it.', '-', '-', 'User input'),
    # ---- S4
    (4, 'Indigenous equity', '4A partnership is the norm', 'Financing effect as capital cost multiplier (blended WACC 4.83 %)', 'Canada', '2026-2040', f"wind {M483['wind']}; PV {M483['pv']}; hydro {M483['hydro']}; nuclear {M483['nuclear']}", 'factor', 'Loan guarantees cut the Indigenous partner borrowing cost by 50-150 bp (RBC) to 150-250 bp (FNMPC); on a 15-20 % slice of project capital this is about 25 bp at project level; 70 % of new capacity assumed partnered (all utility procurements outside Alberta).', 'E15, E16', 'Medium', 'Partly (capital slice, 70 % share)'),
    (4, 'Indigenous equity', '4A partnership is the norm', 'Earlier availability of partnered capacity', 'Canada', '2026-2040', 'wind and PV corridor ceiling shifted 1 year earlier; hydro and nuclear paths 2 years earlier', 'years', 'British Columbia environmental-assessment exemption saves 1-2 years; federal reviews from more than 5 years to a 2-year maximum for national-interest projects.', 'E18, E19, E20', 'Medium', 'Partly'),
    (4, 'Indigenous equity', '4B partnership as a gate', 'Capital cost multiplier (blended WACC 5.13 %) and delay for un-partnered projects', 'Canada', '2026-2040', f"wind {M513['wind']}; PV {M513['pv']}; hydro {M513['hydro']}; nuclear {M513['nuclear']}; un-partnered share (50 %) delayed 3 years", 'factor, years', 'Partnered share 50 % (guarantee deal flow limits closings: 26 deals to date); +50 bp risk premium for un-partnered projects (assumed); delay from the 3.5-year average federal assessment and the "more than five years" statement.', 'E15, E18', 'Low', 'Partly (+50 bp, shares)'),
    (4, 'Indigenous equity', '4B partnership as a gate', 'Build-rate cap wind + PV', 'Canada', '2026-2030', '1.5', 'GW/yr', 'Only the partnered pipeline (about 6 GW under construction) can proceed to 2030. Needs the corridor minimum scaled down.', 'E15', 'Low', 'Yes'),
    (4, 'Indigenous equity', '4C stretch: consent failure', 'Availability of new large hydro, new nuclear beyond Darlington unit 1', 'Canada', '2026-2040', 'not before 2036 (+10 years); wind and PV +3 years', 'years', 'Legal delays without consent: Niagara line 13 years, OPG deep geologic repository 15 years and cancellation.', 'E17', 'Low', 'Partly'),
    (4, 'Indigenous equity', '4C stretch: consent failure', 'Capital cost multiplier', 'Canada', '2026-2040', f"hydro 1.20 x {M563['hydro']}; nuclear 1.20 x {M563['nuclear']}; wind {M563['wind']}; PV {M563['pv']}", 'factor', 'Conflict delay costs about 20-35 % of capex per year (Davis and Franks, extractive sector); blended WACC 5.63 % (30 % partnered at -25 bp, 70 % un-partnered at +100 bp, assumed).', 'E15', 'Low', 'Partly'),
]

SCENARIOS = [
    dict(id=2, name='Local content no longer an option', tag='Mixed',
         meaning='A procurement condition, not an energy quantity. In the model it can only act as a cost premium on import-dependent technologies, a cap on how fast they can be built, and a delay while supply chains localise.',
         levers='Par_CapitalCost Canada by technology and year (multiplier); Par_GroupTotalAnnualMaxNewCap with region subset Canada (build-rate cap); corridor paths shifted in time (delay).',
         route='Scenario generator: cost multiplier helper exists; build-rate caps need a wind / PV technology subset tag and a scaled-down corridor minimum (as done for the US Li-ion cap).',
         flag='YELLOW', flag_summary='Representable only through proxies (capex premium, build-rate cap, delay). The SE-relevant content (who wins the order) is outside the model; the model shows what dearer or slower equipment does to the mix.',
         evidence='Medium for the rules; cost evidence is from older or foreign cases (Quebec and Ontario wind +16 %, India solar +6 %, US Buy American +5.6 %); build-rate caps are assumptions',
         base_cmp='No quantity to compare. Context: the base builds Canadian wind at 5.5 GW/yr on average (2-10 GW/yr), against 1 GW/yr actually built in 2021-2025, so any build-rate cap bites hard.',
         variants='2A scored preference (wind +8 %, PV and batteries +6 %, CCGT +5 % from 2028). 2B hard mandate (wind +16 % fading to +8 %, others +10 %, wind capped at 2.0 / 3.5 GW/yr, +1 year for transformer-bound capacity). 2C stretch "fortress Canada" (+25 % plus financing premium, wind 1.5 / 2.5 / 4.0 GW/yr, +3 years).',
         effort='M', anchors='Buy Canadian policy; Buy Ontario directive; Hydro-Quebec tender 2026-01 (65 % content); OECD 2015 / Peterson Institute; Nature Energy 2020; IEA transformer lead times; CanREA build rates',
         concerns=[('YELLOW', 'model', 'No direct representation; the scenario is a bundle of proxies and the split by technology is a judgement.', 'Keep the three levers separate in the write-up (cost, rate, delay) so each effect is visible.'),
                   ('YELLOW', 'model', 'A wind build-rate cap of 1.5-2.0 GW/yr is below the forced corridor minimum of the base (the minimum path alone needs up to 5.6 GW/yr around 2030).', 'Scale the wind minimum path to fit under the cap, as done for the US Li-ion cap; state that the base minimum is released.'),
                   ('GREEN', 'model', 'Financing premium has no native lever (the technology discount rate only discounts).', 'Converted into a capex multiplier with the annuity ratio.'),
                   ('GREEN', 'data', 'Gas-turbine lead times and prices, the core SE item, were not found in public sources.', 'Ask SE for its own lead-time and price data; until then CCGT carries only the generic premium.')]),
    dict(id=4, name='Indigenous equity and partnership as a project-gating factor', tag='Mixed/Tailwind',
         meaning='Partnered projects get cheaper capital (loan guarantees) and faster permits; un-partnered projects are delayed. In the model: a small capex-equivalent financing effect, a time shift of capacity paths, and in the downside variants a build-rate cap.',
         levers='Par_CapitalCost Canada (annuity-ratio multiplier for the blended WACC); corridor minimum / maximum paths shifted in time; Par_GroupTotalAnnualMaxNewCap (downside variants).',
         route='Scenario generator; blended effects only, because the model cannot tell a partnered project from an un-partnered one.',
         flag='YELLOW', flag_summary='Proxy representation with blended national factors; the province pattern (rule in BC, ON, QC, MB; none in Alberta) is invisible in one node.',
         evidence='Medium for programmes and procurement rules (CAD 17 bn guarantee authority, 14 of 14 Ontario winners at 50 % or more); low for timing effects (single cases, no statistics)',
         base_cmp='No quantity to compare. Guarantee envelope check: remaining authority about CAD 14.5 bn supports EUR 66-99 bn of project capex; the base wind build alone costs about EUR 78 bn, so the envelope would bind.',
         variants=f"4A partnership is the norm (capex x{M483['wind']} for wind, x{M483['nuclear']} for nuclear and hydro; partnered capacity 1-2 years earlier). 4B partnership as a gate (blended +13 bp, half of new projects delayed 3 years, wind + PV capped at 1.5 GW/yr to 2030). 4C stretch: consent failure on flagship projects (no new large hydro or nuclear before 2036, +20 % capex, wind and PV +3 years).",
         effort='M', anchors='Darlington Williams Treaties deal (CAD 700 m, June 2026); federal Indigenous Loan Guarantee Program (CAD 10 bn); RBC "Nations Building"; Ontario LT2 results; BC calls for power; Hydro One equity model; Niagara line and Trans Mountain delay cases',
         concerns=[('YELLOW', 'model', 'Project-level distinction (partnered vs not) does not exist in the model; all effects are national blends.', 'Blended multipliers and time shifts; report the assumed partnered share with each variant.'),
                   ('YELLOW', 'model', 'The tailwind variant (4A) is small: about -2 % capex-equivalent and 1-2 years; results will be close to the base.', 'Run 4A and 4C as a pair so the range is visible; 4B optional.'),
                   ('GREEN', 'data', 'No statistical estimate of faster approval with partnership; delay figures come from single cases.', 'Flag the timing numbers as case-based; SE project experience could replace them.')]),
]
