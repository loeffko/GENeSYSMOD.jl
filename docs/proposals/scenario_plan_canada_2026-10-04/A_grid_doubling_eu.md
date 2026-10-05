# Research A: grid doubling and Canada-EU partnership (Canada scenarios 1, 9)

Research date: 2026-10-04. Web research only; nothing in the model or data repo was touched.

Conventions
- "snippet - verify" = figure seen only in a search-result snippet; the page itself was not fetchable from here (403 / certificate error) or was not opened.
- "OWN ASSUMPTION" = number proposed by the research agent, not a sourced figure. "own calc" = arithmetic on sourced figures.
- CER EF2026 numbers were computed directly from the CER open-data CSV files (downloaded 2026-10-04), not from a summary. Capacity in the files is MW, generation GWh, end-use demand PJ (TWh = PJ / 3.6).
- Currency: 1 CAD = 0.685 EUR (Bank of Canada annual average 2023: 1 EUR = 1.4597 CAD, 1 USD = 1.3497 CAD; consistent with the model's 1 USD = 0.925 EUR in EUR2023; https://www.bankofcanada.ca/rates/exchange/annual-average-exchange-rates/). Nominal conversion, no deflation.
- "Base" = the frozen model base run for Canada given in the task brief.
- The web-search budget of the session ran out before all checks were done; the open items are listed in the Gaps sections.

HEADLINE FLAGS FOR THE MODELLER
1. The "150 GW -> ~310 GW" number is NOT in the federal strategy. It is the CER "Canada's Energy Future 2026" Current Measures result (159 GW in 2023 -> 308 GW in 2050). The base run was built from exactly that scenario and already holds 297 GW in 2040, so the S1 capacity target is INSIDE the base; S1 only differs through the technology mix (gas kept, firm capacity) and interties.
2. Base demand (624 / 768 / 899 TWh in 2030 / 2035 / 2040) is already ABOVE every "doubling by 2050" path and above CER Higher and CER Canada Net-zero end-use demand (627/710/806 and 619/719/832 TWh). "Demand outpaces planning" (S9) therefore has to be built as export-oriented load stacked on top of the base, not by switching to a published high case.
3. "EU associate member" is a proposal of 16 Sept 2026 with no legal definition and no quantified energy content yet; the EU-Canada summit in Montreal on 29-30 Oct 2026 is the next datable event.

---

## S1 - Signal check

| Claim | What the sources say | Verdict | Source (org, title, date) | URL |
|---|---|---|---|---|
| A federal signal exists to "double electricity grid capacity by 2050" | Yes. PM Carney announced the National Electricity Strategy on 14 May 2026; the document is "Powering Canada Strong: A National Strategy for an Electrified Canadian Economy" (NRCan). The wording varies by text: PM release "electricity demand in Canada is expected to double by 2050"; NRCan page "building new infrastructure to double Canada's electricity supply by 2050"; pillar 1 "building infrastructure to double generation"; press and law firms "double grid capacity". | confirmed (but what is doubled - demand, supply/generation or capacity - is not defined consistently) | PMO, "Prime Minister Carney announces forthcoming National Electricity Strategy", 2026-05-14; NRCan, "Powering Canada Strong", 2026-05 | https://www.pm.gc.ca/en/news/news-releases/2026/05/14/prime-minister-carney-announces-forthcoming-national-electricity ; https://natural-resources.canada.ca/energy-sources/electricity-infrastructure/powering-canada-strong-national-strategy-electrified-canadian-economy |
| "from 150 GW to ~310 GW" | No GW baseline or GW target appears in the PM release, the NRCan strategy page or the four law-firm / consultant summaries that could be read (Torys, BLG, Blakes, Power Advisory; Dentons, McCarthy and McMillan were not fetchable). The 310 GW figure matches CER EF2026 Current Measures: "capacity increases from around 160 GW in 2023 to 310 GW in 2050" (CSV: 159.4 GW 2023, 168.7 GW 2025, 308.3 GW 2050). The only "150 GW" in the strategy context is a Canadian Nuclear Association study cited by the strategy: Canada could need 150 GW of ADDITIONAL FIRM generation by mid-century, of which 115 GW new non-emitting baseload. | corrected: 159 GW (2023) / 169 GW (2025) -> 308 GW (2050), factor 1.93 on 2023; source is the CER baseline scenario, not a strategy target | CER, "Canada's Energy Future 2026", results page + open data, 2026; Global News, 2026-05-14 | https://www.cer-rec.gc.ca/en/data-analysis/canada-energy-future/2026/results/ ; https://www.cer-rec.gc.ca/open/energy/energyfutures2026/electricity-capacity-technology-2026.csv ; https://globalnews.ca/news/11849175/carney-clean-electricity-strategy/ |
| Intermediate milestones 2030/2035/2040 | None for capacity or generation. Only transmission: interprovincial transmission capacity "could increase 27 %" by 2035 and 70 % by 2050 (same figure as CER EF2026: "roughly 70 % in all scenarios"). | not found (capacity); confirmed (transmission +27 % 2035, +70 % 2050) | NRCan, "Powering Canada Strong", 2026-05; CER EF2026 | https://natural-resources.canada.ca/energy-sources/electricity-infrastructure/powering-canada-strong-national-strategy-electrified-canadian-economy |
| Investment figure | "over $1 trillion" from now to 2050 (CAD; = ~EUR 685 bn; ~CAD 40 bn/yr over 25 years, own calc). Electricity Canada: utilities "will need to invest $2 trillion to double the electricity system" by 2050. Canada Electricity Advisory Council: ~CAD 35 bn/yr, CAD 1.2 trillion by 2050 (snippet - verify). | confirmed (CAD 1 trillion federal; range CAD 1-2 trillion) | NRCan strategy 2026-05; Electricity Canada, "Forging Canada's Electricity Future: 2026 State of the Canadian Electricity Industry", 2026-01 | https://electriccanadian.com/img/SOTI-2026-Digital-Jan26.pdf ; https://www.electricity.ca/advocacy/forging-canadas-electricity-future-2026-state-of-the-electricity-industry/ |
| "broad energy mix, including natural gas" | Confirmed. PM release: "wide range of energy - including natural gas". Strategy: gas provides "baseload and operational flexibility", strategic role "particularly in Western Canada"; Clean Electricity Regulations to be adjusted: "greater use of credible carbon offsets", "greater flexibility for existing units to maintain reliability", "more room to add new units in the near-term", net-zero 2050 kept. No draft amendment text found. | confirmed | PMO 2026-05-14; NRCan strategy; BLG 2026-05-22; Blakes 2026-05 | https://www.blg.com/en/insights/2026/05/canadas-new-electricity-strategy-powering-an-electrified-future-by-2050 ; https://www.blakes.com/insights/canada-issues-national-strategy-for-electrifying-the-canadian-economy-powering-canada-strong%E2%80%9D/ |
| Drivers: growth, energy security, electrification, AI/data centres, decarbonisation | Confirmed qualitatively (industrial growth, electrification, home-building, data centres). Workforce: 130,000 workers by 2050, 28,000-30,000 by 2028. Savings: up to CAD 15 bn by 2050, 7 in 10 households pay less (CEAC analysis). | confirmed | PMO 2026-05-14; Torys 2026-05 | https://www.torys.com/our-latest-thinking/publications/2026/05/powering-canada-strong |
| Status of the strategy | Released 14 May 2026 as a strategy for consultation ("over the next few months"; Power Advisory: finalise "over the next four months"). Electricity Canada filed a submission dated 1 Sept 2026 (snippet). A FINAL strategy with numeric targets: NOT FOUND as of 2026-10-04. | confirmed as consultation document; final version not found | Power Advisory, "Canada's New Electricity Strategy: Powering Canada Strong", 2026-05; Electricity Canada, "The National Electricity Strategy", 2026 | https://www.poweradvisoryllc.com/reports/canadas-new-electricity-strategy-powering-canada-strong ; https://www.electricity.ca/publications/the-national-electricity-strategy/ |
| Grid/intertie element | Confirmed. A "Transmission InterConnect Investment Strategy" was referred to the Major Projects Office on 14 May 2026; five priority items named 26 June 2026 (see anchors); Clean Electricity ITC (15 %) to be extended to major intra-provincial transmission. | confirmed | Privy Council Office / MPO page; NRCan release 2026-06-26 | https://www.canada.ca/en/privy-council/major-projects-office/projects/other/referred/interconnect.html ; https://www.canada.ca/en/natural-resources-canada/news/2026/06/canada-takes-action-to-advance-a-stronger-grid-and-increase-reliable-affordable-energy.html |

Position of the signal relative to the base (own calc)

| Path | 2025 | 2030 | 2035 | 2040 | 2050 |
|---|---|---|---|---|---|
| Base model total capacity, GW | 167 | 190 | 241 | 297 | n/a |
| CER EF2026 Current Measures total capacity, GW | 168.7 | 193.7 | 225.8 | 243.7 | 308.3 |
| Linear path 169 GW (2025) -> 310 GW (2050), GW (own calc) | 169 | 197 | 225 | 254 | 310 |
| Base model demand, busbar TWh | 545 | 624 | 768 | 899 | n/a |
| "Demand doubles by 2050" from 545 TWh, constant growth 2.81 %/yr, TWh (own calc) | 545 | 626 | 719 | 826 | 1,090 |
| Same, linear, TWh (own calc) | 545 | 654 | 763 | 872 | 1,090 |

Reading: from 2035 the base is above the doubling path in both capacity and demand. Only in 2030 is the base (190 GW) slightly below CER Current Measures (194 GW).

## S1 - Quantification anchors

### National (CER "Canada's Energy Future 2026", open data, published 2026)

Sources for all rows of the three tables below: CER, "Canada's Energy Future 2026: Energy Supply and Demand Projections to 2050", data tables electricity-capacity-technology-2026.csv, electricity-generation-technology-2026.csv, end-use-demand-2026.csv, electricity-interchange-2026.csv - https://open.canada.ca/data/en/dataset/07c42deb-9435-43b9-a416-7ce316f3893d (files under https://www.cer-rec.gc.ca/open/energy/energyfutures2026/). Scope Canada. Scenario names: Current Measures (CM), Higher, Lower, Canada Net-zero (NZ).

Total installed capacity, GW

| Scenario | 2023 | 2025 | 2030 | 2035 | 2040 | 2045 | 2050 |
|---|---|---|---|---|---|---|---|
| Lower | 159.4 | 168.7 | 192.6 | 217.4 | 226.9 | 237.5 | 269.6 |
| Current Measures | 159.4 | 168.7 | 193.7 | 225.8 | 243.7 | 266.7 | 308.3 |
| Higher | 159.4 | 168.7 | 196.8 | 244.8 | 278.6 | 316.1 | 359.5 |
| Canada Net-zero | 159.4 | 168.9 | 200.4 | 252.4 | 302.1 | 350.0 | 402.4 |

Capacity by technology, GW (2030 / 2035 / 2040 / 2050)

| Technology | Current Measures | Higher | Canada Net-zero | Base model 2030/2035/2040 |
|---|---|---|---|---|
| Hydro | 85.3 / 91.1 / 91.5 / 91.5 | 85.3 / 91.1 / 91.5 / 91.5 | 85.3 / 91.1 / 91.5 / 91.5 | 91 / 97 / 98 |
| Onshore wind | 33.9 / 55.2 / 63.3 / 90.4 | 36.4 / 68.1 / 87.1 / 114.1 | 39.6 / 77.5 / 113.3 / 165.6 | 31 / 62 / 87 |
| Offshore wind | 0 / 0 / 0 / 1.1 | 0 / 0.1 / 0.1 / 1.1 | 0 / 0.1 / 0.2 / 1.3 | 0 |
| Solar (utility + distributed) | 14.5 / 18.0 / 18.9 / 30.5 | 14.6 / 20.1 / 21.6 / 37.8 | 14.9 / 17.5 / 19.0 / 32.0 | 14 / 30 / 62 |
| Nuclear (large) | 10.7 / 13.5 / 13.5 / 13.5 | 10.7 / 13.5 / 13.5 / 13.5 | 10.7 / 13.5 / 13.5 / 13.5 | 12.9 / 15.0 / 15.6 |
| SMR | 0.3 / 1.5 / 2.1 / 6.1 | 0.3 / 1.5 / 2.1 / 17.3 | 0.3 / 1.5 / 2.1 / 11.3 | 0 / 0.32 / 0.32 |
| Natural gas unabated | 34.2 / 32.9 / 35.7 / 34.6 | 34.6 / 35.8 / 38.2 / 37.5 | 34.4 / 36.2 / 35.4 / 33.3 | 31 / 29 / 27 (gas total) |
| Natural gas with CCUS | 0 / 0.45 / 0.9 / 7.4 | 0 / 0.45 / 3.1 / 8.4 | 0 / 1.3 / 3.3 / 8.9 | n/a |
| Coal (unabated; + 0.11 with CCUS) | 2.7 / 0 / 0 / 0 | 2.7 / 0 / 0 / 0 | 2.7 / 0 / 0 / 0 | 2.9 / 1.5 / 1.5 |
| Battery storage | 4.5 / 6.5 / 10.5 / 23.6 | 4.5 / 7.5 / 14.0 / 25.7 | 4.8 / 7.0 / 15.3 / 29.0 | 4.1 / 5.2 / 8.4 |
| Hydrogen turbines | 0 / 0 / 0.6 / 4.0 | 0 / 0 / 0.6 / 6.5 | 0 / 0 / 0.3 / 4.6 | n/a |
| Bioenergy (+ BECCS in NZ: 0 / 0 / 1.4 / 5.5) | 3.4 / 3.4 / 3.4 / 3.0 | 3.4 / 3.4 / 3.4 / 3.4 | 3.4 / 3.4 / 3.4 / 3.0 | n/a |
| Oil | 4.2 / 3.2 / 3.3 / 2.6 | 4.2 / 3.2 / 3.3 / 2.7 | 4.2 / 3.2 / 3.3 / 2.6 | n/a |

Generation, end-use electricity demand and trade, TWh

| Item | Scenario | 2023 | 2025 | 2030 | 2035 | 2040 | 2050 |
|---|---|---|---|---|---|---|---|
| Total generation | Lower | 621.5 | 650.9 | 686.9 | 756.1 | 810.4 | 864.7 |
| Total generation | Current Measures | 621.5 | 651.5 | 704.2 | 800.2 | 881.1 | 975.0 |
| Total generation | Higher | 621.5 | 650.9 | 725.0 | 860.4 | 970.6 | 1,156.4 |
| Total generation | Canada Net-zero | 621.5 | 651.3 | 726.0 | 871.7 | 1,030.6 | 1,323.0 |
| Wind generation (on+offshore) | CM / Higher / NZ | 40.1 | 44.8 | 86.7 / 98.6 / 102.3 | 150.7 / 193.3 / 221.2 | 189.2 / 263.6 / 356.4 | 277.0 / 362.1 / 534.6 |
| Gas generation (unabated + CCUS) | CM / Higher / NZ | 98.8 | 112.2 | 105.5 / 108.5 / 105.6 | 79.5 / 88.3 / 70.5 | 100.0 / 110.9 / 76.7 | 68.8 / 72.1 / 72.1 |
| Hydro generation | CM | 357.2 | 385.7 | 393.9 | 425.5 | 429.9 | 434.1 |
| Nuclear incl. SMR generation | CM | 84.0 | 75.7 | 78.5 | 107.5 | 120.8 | 128.1 |
| End-use electricity demand (excl. electricity for hydrogen production) | Lower | 566.6 | 566.8 | 587.5 | 624.4 | 656.6 | 713.1 |
| End-use electricity demand | Current Measures | 566.6 | 566.8 | 604.0 | 660.8 | 723.2 | 813.9 |
| End-use electricity demand | Higher | 566.6 | 567.1 | 627.4 | 710.3 | 806.0 | 981.7 |
| End-use electricity demand | Canada Net-zero | 566.6 | 566.8 | 619.3 | 718.8 | 832.4 | 1,042.0 |
| of which industrial | CM / Higher / NZ | 232.9 | 229 | 253 / 262 / 247 | 283 / 302 / 280 | 309 / 338 / 307 | 337 / 398 / 388 |
| of which commercial (incl. data centres) | CM / Higher / NZ | 156.3 | 156 | 164 / 177 / 169 | 172 / 198 / 182 | 187 / 233 / 204 | 212 / 303 / 243 |
| of which residential | CM / Higher / NZ | 174.7 | 177 | 173 / 175 / 174 | 176 / 180 / 184 | 182 / 188 / 196 | 197 / 207 / 208 |
| of which transportation | CM / Higher / NZ | 2.7 | 5 | 13 / 14 / 29 | 29 / 30 / 72 | 45 / 47 / 125 | 68 / 72 / 203 |
| Hydrogen end-use (energy content, not electricity) | CM / Higher / NZ | 0 | 0 | 9 / 9 / 11 | 20 / 20 / 43 | 20 / 20 / 97 | 20 / 21 / 161 |
| Net exports to the US | CM (Higher/Lower identical) | 27.0 | 49.1 | 45.9 | 47.5 | 47.2 | 45.4 |
| Gross exports / imports | CM | 47.8 / 20.8 | 59.4 / 10.3 | 57.1 / 11.2 | 57.4 / 9.9 | 57.1 / 9.9 | 56.4 / 11.0 |
| Interprovincial flows | CM / NZ | 55.6 | 66.6 | 79.9 / 81.5 | 111.2 / 110.6 | 125.9 / 125.9 | 136.8 / 140.5 |

Notes on the CER tables
- CER text: total electricity demand including hydrogen production rises by ~30 % (Lower), ~50 % (CM), 80 % (Higher), ~120 % (NZ) from 2023 to 2050; end-use only: +26 % to +85 %. Data centres are "about a quarter, or 100 TWh" of end-use demand growth in Higher. Source: https://www.cer-rec.gc.ca/en/data-analysis/canada-energy-future/2026/results/ and https://www.cer-rec.gc.ca/en/data-analysis/canada-energy-future/2026/executive-summary/
- A data-centre demand series is not in the open-data CSVs (NOT FOUND as a separate column).
- Base net exports (~93 TWh in 2025, ~66 TWh in 2040) are about twice the CER figures (49 / 47 TWh). Not an S1 issue, but worth knowing when comparing generation totals.

Provincial split, CER EF2026 (total capacity GW; end-use electricity TWh), 2023 / 2030 / 2035 / 2040 / 2050

| Province | Capacity, Current Measures | Capacity, Canada Net-zero | End-use demand, Current Measures | End-use demand, Higher |
|---|---|---|---|---|
| Quebec | 46.9 / 51.9 / 54.3 / 58.2 / 68.4 | 46.9 / 52.4 / 54.8 / 59.7 / 74.8 | 209.5 / 211.7 / 223.1 / 233.0 / 254.1 | 209.5 / 217.4 / 235.3 / 252.0 / 287.4 |
| Ontario | 43.4 / 46.9 / 48.4 / 50.1 / 73.2 | 43.4 / 48.1 / 55.0 / 70.6 / 102.3 | 138.5 / 149.3 / 167.3 / 188.2 / 218.1 | 138.5 / 155.3 / 182.9 / 219.1 / 275.7 |
| Alberta | 21.0 / 31.1 / 35.5 / 41.8 / 60.5 | 21.0 / 32.0 / 45.2 / 55.7 / 74.4 | 76.3 / 86.6 / 95.8 / 107.9 / 128.3 | 76.3 / 90.3 / 104.1 / 122.2 / 161.4 |
| British Columbia | 19.0 / 24.0 / 35.0 / 36.5 / 41.0 | 19.0 / 24.1 / 37.6 / 40.6 / 47.6 | 61.4 / 72.4 / 85.5 / 99.2 / 107.8 | 61.4 / 78.5 / 94.1 / 110.2 / 135.6 |
| Newfoundland and Labrador | 8.8 / 12.5 / 23.6 / 25.8 / 26.3 | 8.8 / 14.4 / 22.8 / 28.5 / 35.9 | 10.0 / 10.5 / 11.1 / 11.6 / 12.3 | 10.0 / 10.6 / 11.4 / 12.1 / 13.5 |
| Manitoba | 6.6 / 6.9 / 7.2 / 7.3 / 7.5 | 6.6 / 7.3 / 8.5 / 9.5 / 11.3 | 22.0 / 22.4 / 23.4 / 24.3 / 26.6 | 22.0 / 23.0 / 24.8 / 26.3 / 30.2 |
| Saskatchewan | 5.3 / 7.2 / 8.0 / 9.4 / 14.6 | 5.3 / 7.2 / 10.0 / 13.9 / 23.2 | 21.4 / 23.8 / 25.6 / 27.9 / 31.6 | 21.4 / 24.5 / 27.5 / 31.2 / 38.9 |
| Nova Scotia | 3.1 / 6.7 / 7.8 / 7.8 / 9.3 | 3.1 / 8.0 / 11.9 / 16.7 / 24.2 | 10.1 / 10.0 / 10.7 / 11.5 / 13.0 | 10.1 / 10.1 / 11.1 / 12.2 / 14.3 |
| New Brunswick | 4.5 / 5.3 / 4.7 / 5.2 / 5.3 | 4.5 / 5.7 / 5.3 / 5.3 / 6.6 | 13.7 / 13.5 / 14.1 / 15.0 / 16.7 | 13.7 / 13.8 / 14.8 / 15.9 / 18.6 |

Gas capacity by province, CER Current Measures, GW incl. CCUS (2023 / 2030 / 2035 / 2040 / 2050): Alberta 12.2 / 14.2 / 14.7 / 16.3 / 21.6; Ontario 11.7 / 14.0 / 11.6 / 12.7 / 12.1; Saskatchewan 2.2 / 3.2 / 3.7 / 3.9 / 4.2; Nova Scotia 0.5 / 0.8 / 1.3 / 1.3 / 1.6; New Brunswick 0.4 / 0.3 / 0.3 / 0.7 / 1.2; Manitoba 0.3 / 0.3 / 0.4 / 0.5 / 0.6; Canada 29.0 / 34.2 / 33.4 / 36.6 / 42.0.

### Federal strategy, regulation, interties, investment

| Data point | Value | Unit | Scope | Year(s) | Source (org, title, date) | URL | Note |
|---|---|---|---|---|---|---|---|
| Investment need, federal estimate | > 1 trillion (= ~685 bn EUR) | CAD | Canada | now-2050 | NRCan, "Powering Canada Strong", 2026-05 | https://natural-resources.canada.ca/energy-sources/electricity-infrastructure/powering-canada-strong-national-strategy-electrified-canadian-economy | ~CAD 40 bn/yr (own calc) |
| Investment need, utilities' estimate | 2 trillion (= ~1.37 trillion EUR) | CAD | Canada | to 2050 | Electricity Canada, 2026 State of the Canadian Electricity Industry, 2026-01 | https://electriccanadian.com/img/SOTI-2026-Digital-Jan26.pdf | sector currently spends ~CAD 30 bn/yr (same report) |
| Investment need, CEAC | ~35 bn/yr; 1.2 trillion by 2050 | CAD | Canada | to 2050 | Canada Electricity Advisory Council, quoted in a 2026 grid roadmap | https://www.electrofed.com/wp-content/uploads/2026/04/EFC_Grid-Technology-Roadmap_Final-Report_2026-04-07-v2.pdf | snippet - verify |
| Additional firm capacity needed | 150 (115 non-emitting baseload + 35 flexible) | GW | Canada | by 2050 | Canadian Nuclear Association study, 2025-09-15, cited in the strategy | https://cna.ca/2025/09/15/canada-faces-unprecedented-electricity-demand-growth-nuclear-energy-critical-to-meeting-2050-needs/ ; https://globalnews.ca/news/11849175/carney-clean-electricity-strategy/ | 150 and 115 GW confirmed via Global News; the 35 GW flexible split and the 17 GW "low build" nuclear case are snippet - verify |
| Interprovincial transmission capacity growth | +27 % by 2035; +70 % by 2050 | % | Canada | 2035, 2050 | NRCan strategy; CER EF2026 | (as above) | not visible in a one-node model |
| Existing transfer capability | 24 north-south (Canada-US) vs 16 east-west | GW | Canada | 2025/26 | Electricity Canada SOTI 2026 | https://electriccanadian.com/img/SOTI-2026-Digital-Jan26.pdf | the 24 GW is the relevant cap for the model's Canada-US link |
| Priority intertie: BC-Yukon Grid Connect | ~800 km, +200 kV HVDC; CAD 40 m NRCan funding for development | km / kV | BC-YT | announced 2026-06-26 | NRCan news release 2026-06-26 | https://www.canada.ca/en/natural-resources-canada/news/2026/06/canada-takes-action-to-advance-a-stronger-grid-and-increase-reliable-affordable-energy.html | MW, cost, in-service date NOT FOUND |
| Priority intertie: Alberta-BC restoration | ~+150 | MW | AB-BC | announced 2026-06-26 | same | same | date/cost NOT FOUND |
| Priority intertie: Alberta-Saskatchewan (McNeill converter) | ~+250 | MW | AB-SK | announced 2026-06-26 | same | same | date/cost NOT FOUND |
| Priority intertie: Saskatchewan-Manitoba (Regina-Winnipeg) | up to +2,000 | MW | SK-MB | announced 2026-06-26 | same | same | "scalable"; date/cost NOT FOUND |
| Priority intertie: PEI-New Brunswick expansion (subsea) | n/a | - | PEI-NB | announced 2026-06-26 | same | same | MW NOT FOUND |
| NS-NB Wasoqonatl Reliability Intertie | 160 km, 345 kV; doubles NS-NB transfer capability; CAD 285 m federal equity + CAD 24.7 m predevelopment | km / kV / CAD | NS-NB | under development | Electricity Canada SOTI 2026; NRCan strategy | https://electriccanadian.com/img/SOTI-2026-Digital-Jan26.pdf | first phase of a "modified Atlantic Loop" |
| Federal financing envelopes named with the strategy | Canada Strong Fund 25 bn; CIB capital 35 -> 45 bn (clean-energy target 20 bn); Smart Renewables 4.5 bn; SMR 2 bn via Canada Growth Fund; Indigenous Loan Guarantee 5 -> 10 bn; Clean Electricity ITC 15 % | CAD | Canada | 2026 | Blakes 2026-05; BLG 2026-05-22; NRCan 2026-06-26 | https://www.blakes.com/insights/canada-issues-national-strategy-for-electrifying-the-canadian-economy-powering-canada-strong%E2%80%9D/ | |
| Clean Electricity Regulations (final) | published 2024-12-18 (SOR/2024-263); limits from 2035; units >= 25 MW; existing units exempt until 25 years after commissioning; pooling; offsets allowed; emergency flexibility; net-zero 2050; ~181 Mt cumulative reduction 2024-2050 | - | Canada | 2035-2050 | ECCC, "Canada's clean electricity future" | https://www.canada.ca/en/services/environment/weather/climatechange/climate-plan/clean-electricity.html ; https://gazette.gc.ca/rp-pr/p2/2024/2024-12-18/html/sor-dors263-eng.html | |
| CER (regulation) numeric limits | annual emission limit based on 65 t CO2/GWh (0 from 2050); offsets up to 35 t/GWh-equivalent 2035-2049 and 42 t/GWh from 2050 | t/GWh | Canada | 2035+ | Canada Gazette II, 2024-12-18 | https://gazette.gc.ca/rp-pr/p2/2024/2024-12-18/html/sor-dors263-eng.html | snippet - verify |
| Planned loosening of the regulation | more offsets, more room for existing units and for new units "in the near-term" | - | Canada | announced 2026-05-14 | NRCan strategy; National Observer 2026-05-14 | https://www.nationalobserver.com/2026/05/14/news/feds-clean-electricity-regulations | no draft text / dates found |
| IESO on the regulation | APO 2026 does not model the federal regulation; gas fleet limited to an emissions path instead | - | Ontario | 2026 | IESO, "Annual Planning Outlook 2026", 2026-03 | https://www.ieso.ca/-/media/Files/IESO/Document-Library/planning-forecasts/apo/2026/2026-Annual-Planning-Outlook.pdf | |

### Provincial plans and projects

| Data point | Value | Unit | Scope | Year(s) | Source (org, title, date) | URL | Note |
|---|---|---|---|---|---|---|---|
| Net annual energy demand, reference | 152 -> 250 (+65 %, 2.1 %/yr) | TWh | Ontario | 2026 -> 2050 | IESO, Annual Planning Outlook 2026, 2026-03 | https://www.ieso.ca/-/media/Files/IESO/Document-Library/planning-forecasts/apo/2026/2026-Annual-Planning-Outlook.pdf | 2030/2035/2040 only as a chart; at 2.1 %/yr: ~165 / ~183 / ~203 TWh (own calc) |
| Net annual energy demand, high / low | 154 -> 297 (+92 %) / 150 -> 207 (+38 %) | TWh | Ontario | 2026 -> 2050 | same | same | 2025 APO reference was +75 % (263 TWh) |
| System needs, reference | the report gives two sets: executive summary "incremental" needs: energy 8.5 TWh (2032) and 37 TWh (2040), capacity 950 MW (2035) and 3,800 MW (2040); needs chapter: summer capacity > 7,000 MW (2035) and > 11,000 MW (2040), energy 21 TWh (2035) to 65 TWh (2040) | TWh / MW | Ontario | 2032-2040 | same | same | the difference between the two sets (which planned actions are netted off) was not resolved here; unserved energy without new procurement: ~19 TWh by 2035 (ref), ~42 TWh (high), ~6 TWh (low) |
| Installed capacity end 2026 | 39 total: gas/oil 11.4, hydro 9.3, nuclear 8.5, wind 5.5, solar 2.6, storage 1.2, bio 0.4 | GW | Ontario | 2026 | same | same | 10.6 GW of nuclear refurbished by end 2034 |
| Data centres | 8.6 % of demand in 2050 (reference) | % | Ontario | 2050 | IESO, 2026 APO summary | https://ieso.ca/Sector-Participants/Planning-and-Forecasting/Annual-Planning-Outlook/2026-APO-Summary | |
| New nuclear ambitions | up to 17,800 new by 2050: Bruce C up to 4,800; Wesleyville/Port Hope up to 10,000; Darlington SMR 4 units 1,200-1,600 (first before end 2030, others 2033-2035) | MW | Ontario | 2030-2050 | Government of Ontario, "Energy for Generations", 2025-06-12 | https://www.ontario.ca/page/energy-generations | IESO: large new nuclear "in the 2040s" -> outside the model horizon except the SMRs |
| Procurements | LT2: up to 14 TWh/yr and 1,600 MW by 2034; Long Lead-Time RFP 800 MW / 1 TWh by 2035; earlier E-LT1/LT1 > 3,300 MW; storage ~3,000 MW; pumped storage up to 1,000 MW; hydro potential 3,000-4,000 MW | MW / TWh | Ontario | 2030-2035 | Ontario, "Energy for Generations"; IESO APO 2026 | https://www.ontario.ca/page/energy-generations | |
| Action Plan 2035 additions | +60 TWh, +8,000-9,000 MW by 2035: hydro 3,800-4,200 MW; wind 1,500-1,700 MW accredited (> 10,000 MW installed); efficiency 1,600-1,800 MW (21 TWh savings) | TWh / MW | Quebec | by 2035 | Hydro-Quebec, "Action Plan 2035 - Towards a Decarbonized and Prosperous Quebec", 2023-11 | https://www.hydroquebec.com/data/a-propos/pdf/action-plan-2035.pdf | 2026 update NOT FOUND |
| Long-run need | +150-200 TWh | TWh | Quebec | by 2050 | same | same | vs CER CM Quebec end-use: only +45 TWh 2023-2050 |
| Investment | 155-185 bn total by 2035 (= 106-127 bn EUR): growth 90-110, reliability 45-50, other 20-25; hydro additions 35-45 bn; transmission 45-50 bn | CAD | Quebec | 2023-2035 | same | same | |
| Churchill Falls upgrades | +1,275 (the federal release also says "increase capacity by up to 2,500 MW" for the expansion) | MW | NL / QC | DCIA signed 2026-08-17 | NRCan/PMO release 2026-08; BLG, "New Churchill Falls agreement", 2026-09 | https://www.canada.ca/en/natural-resources-canada/news/2026/08/prime-minister-carney-announces-the-largest-clean-energy-investment-in-north-american-history.html ; https://www.blg.com/en/insights/2026/09/new-churchill-falls-agreement-key-terms | definitive agreements due by 2027-03-31 (BLG; a snippet says 2026-12-31); Quebec election 2026-10-05 is a risk |
| Gull Island | 2,250 or 2,700; ~12 TWh/yr; online 2036-2037 | MW / TWh | NL | 2036-2037 | same | same | 60 % NLH / 40 % HQ; 735 kV lines to Churchill Falls and Romaine-4 |
| Labrador wind | 2,000 | MW | NL | n/a | same | same | |
| Package value / federal support | ~70 bn (= ~48 bn EUR); federal support up to 10 bn | CAD | NL / QC | 2026 | same | same | "approximately 14,000 MW" delivered in total |
| BC Hydro 2025 IRP | demand +15 % by 2030; 2025 Call for Power up to 5,000 GWh/yr by 2034; Revelstoke unit 6 +500 MW; GMS units 1-5 +100 MW | % / GWh / MW | BC | 2030-2034 | BC Hydro, news release on the 2025 IRP, 2025 | https://www.bchydro.com/news/press_centre/news_releases/2025/ltep.html | |
| BC 2025 Call for Power result | ~3,500 GWh/yr awarded 2026-05-13 (incl. 1,158 MW wind in four projects) | GWh / MW | BC | awarded 2026 | BC Hydro 2025 Call for Power page; trade press | https://www.bchydro.com/work-with-us/selling-clean-energy/2025-call-for-power.html | snippet - verify |
| North Coast Transmission Line | ~6 bn (= ~4.1 bn EUR); construction 2026, completion by 2034 | CAD | BC | 2026-2034 | The Tyee, 2025-10-21 | https://thetyee.ca/News/2025/10/21/BC-Fast-Tracks-North-Coast-Transmission-Line/ | snippet - verify; estimate doubled from CAD 3 bn (2023) |
| Site C | budget 16 bn (= ~11 bn EUR); 14.9 bn spent to date | CAD | BC | 2026 | CBC, 2026 | https://www.cbc.ca/news/canada/british-columbia/bc-hydro-site-c-cost-14-9-billion-progress-report-9.7273159 | snippet - verify; MW not re-checked |
| Alberta gas for data centres | > 20,000 MW of data-centre load on the AESO project list (July 2026); grid allocation capped at 1,200 MW to 2028; proposals: Beacon Indus ~1,494 MW gas plant, Heartland 800-920 MW gas engines, Wonder Valley 7.5-9 GW off-grid gas | MW | Alberta | 2026-2028 | EnergyNow, 2026-08; AESO | https://energynow.ca/2026/08/how-alberta-became-ground-zero-for-data-centre-development-in-canada/ | snippet - verify; mostly behind-the-fence / off-grid -> outside the model |
| Alberta gas fleet | 14,201 MW (~60 % of operating capacity) | MW | Alberta | 2026 | DNE Resources on the AESO long-term adequacy report, 2026-05 | https://www.dneresources.com/unpacking-the-aesos-may-2026-long-term-adequacy-report/ | snippet - verify; AESO 2026 Long-Term Outlook is due Q4 2026 (not yet published) |
| Saskatchewan | Aspen gas plant 370 MW (2027); coal life extension up to 1,530 MW beyond 2030 (as far as 2050); nuclear >= 2,600 MW by 2050, first large reactor ~2042 | MW | Saskatchewan | 2027-2050 | Gov. of Saskatchewan, energy security strategy / news 2026-09-29; World Nuclear News | https://www.saskatchewan.ca/government/news-and-media/2026/september/29/saskatchewan-advances-nuclear-power-to-support-long-term-energy-security | snippet - verify; coal extension conflicts with CER tables (coal 0 by 2035) but matches the base (1.5 GW) |
| Manitoba Hydro 2025 IRP | +1,760 MW accredited by 2035, incl. 750 MW gas combustion turbines by 2030 (Brandon) and 600 MW wind | MW | Manitoba | 2030-2035 | Osler, 2025; Manitoba Hydro 2025 IRP | https://www.hydro.mb.ca/docs/corporate/irp/2025-irp-report-final.pdf | snippet - verify |
| Nova Scotia Wind West (offshore) | phase 1 ~5 GW, ~60 bn (40 turbines + 20 transmission; = ~41 bn EUR); earliest 2033-2035; ambition 40-60 GW; first licence auction "by end of 2026" | GW / CAD | Nova Scotia | 2033+ | CMS; National Observer 2026-07-01; Globe and Mail | https://cms.law/en/int/legal-updates/nova-scotia-s-offshore-wind-strategy-gathers-pace | snippet - verify; detail belongs to the wind research file |
| Taltson hydro expansion / Iqaluit hydro | 60 / 15-30 | MW | NWT / Nunavut | n/a | NRCan strategy 2026-05 | (NRCan page above) | off-grid, outside the model |

### Other "how much must the grid grow" estimates

| Data point | Value | Unit | Scope | Year(s) | Source (org, title, date) | URL | Note |
|---|---|---|---|---|---|---|---|
| Aggregated provincial system outlooks | 604 -> 982 (+62 %, 2.0 %/yr) | TWh | Canada | 2025 -> 2050 | Transition Accelerator / Dunsky, "Forecasting Canada's Electricity Future", 2025-11 | https://transitionaccelerator.ca/wp-content/uploads/2025/11/Forecasting-Canadas-Electricity-Future-Report-Final-November-2025.pdf | at 2.0 %/yr: ~667 (2030), ~736 (2035), ~813 (2040) (own calc) |
| CER EF2023 Global Net-zero | 587 -> 1,187 (+102 %, 2.6 %/yr); peak ~100 -> 212 GW | TWh / GW | Canada | 2023 -> 2050 | same (Table 4) | same | at 2.6 %/yr: ~703 / ~799 / ~908 TWh in 2030 / 2035 / 2040 (own calc) = the base demand level in 2040 |
| IET (Institut de l'energie Trottier) NZ50 | 519 -> 1,031 (+99 %, 2.4 %/yr) | TWh | Canada | 2021 -> 2050 | same | same | |
| Canadian Climate Institute, "The Big Switch" | demand x1.6-2.1; capacity x2.2-3.4 | factor | Canada | 2050 vs ~2020 | Canadian Climate Institute, 2022-05 | https://climateinstitute.ca/reports/big-switch/ | snippet - verify |
| Public Policy Forum, "Project of the Century" | "more than doubling of grid capacity by 2050"; build pace 3-6x previous decades | factor | Canada | 2050 | PPF, 2023 | https://ppforum.ca/publications/net-zero-electricity-canada-capacity/ | snippet - verify |
| RBC Climate Action Institute | "at least doubling" capacity by 2050; > CAD 1 trillion; 337 GW wind + solar by 2050 (CER-based) | GW / CAD | Canada | 2050 | RBC, Climate Action 2026 (electricity) | https://www.rbc.com/climate-action-institute/climate-action-26/electricity.html | snippet - verify |

## S1 - Proposed variants

General remark: demand is left at base in all three variants, because the base (624 / 768 / 899 TWh) already lies above the published doubling paths (see Signal check). If S1 should also move demand, combine it with an S9 demand variant.

### S1-A (central, announced-consistent): "Strategy = CER Current Measures, gas kept"
Minimum capacity paths in GW. Source rows: CER EF2026 Current Measures capacity table; Clean Electricity Regulations loosening (strategy); provincial gas builds (Manitoba 750 MW, Aspen 370 MW).

| Lever | 2030 | 2035 | 2040 | Base | Binding? |
|---|---|---|---|---|---|
| Total capacity, minimum | 193.7 | 225.8 | 243.7 | 190 / 241 / 297 | only 2030 (+3.7) |
| Gas incl. CCUS, minimum | 34.2 | 33.4 | 36.6 | 31 / 29 / 27 | yes: +3.2 / +4.4 / +9.6 |
| Onshore wind, minimum | 33.9 | 55.2 | 63.3 | 31 / 62 / 87 | only 2030 (+2.9) |
| Solar, minimum | 14.5 | 18.0 | 18.9 | 14 / 30 / 62 | only 2030 (+0.5) |
| SMR, minimum | 0.3 | 1.5 | 2.1 | 0 / 0.32 / 0.32 | yes: +0.3 / +1.1 / +1.7 |
| Battery storage, minimum | 4.5 | 6.5 | 10.5 | 4.1 / 5.2 / 8.4 | yes: +0.4 / +1.3 / +2.1 |
| Hydro, minimum | 85.3 | 91.1 | 91.5 | 91 / 97 / 98 | no |
| Coal, maximum | 2.8 | 1.5 | 1.5 | 2.9 / 1.5 / 1.5 | keep base (SaskPower coal extension; CER has 0.1 from 2035) |
| Demand by category | base | base | base | - | - |
| Canada-US interconnector | base | base | base | - | Canada-internal interties are not visible in a one-node model |
| No CO2 constraint on gas before 2040 | - | - | - | - | OWN ASSUMPTION: reflects the announced loosening of the Clean Electricity Regulations |

### S1-B (alternative): "Growth case with a gas-heavier mix = CER Higher"
Source rows: CER EF2026 Higher capacity table. CER Higher is the scenario with higher GDP, LNG and data-centre load; it carries the most gas (41 GW in 2040).

| Lever | 2030 | 2035 | 2040 | Base | Binding? |
|---|---|---|---|---|---|
| Total capacity, minimum | 196.8 | 244.8 | 278.6 | 190 / 241 / 297 | 2030 (+6.8), 2035 (+3.8) |
| Gas incl. CCUS, minimum | 34.6 | 36.2 | 41.3 | 31 / 29 / 27 | yes: +3.6 / +7.2 / +14.3 |
| Onshore wind, minimum | 36.4 | 68.1 | 87.1 | 31 / 62 / 87 | yes: +5.4 / +6.1 / +0.1 |
| Solar, minimum | 14.6 | 20.1 | 21.6 | 14 / 30 / 62 | 2030 only |
| SMR, minimum | 0.3 | 1.5 | 2.1 | 0 / 0.32 / 0.32 | yes |
| Battery storage, minimum | 4.5 | 7.5 | 14.0 | 4.1 / 5.2 / 8.4 | yes: +0.4 / +2.3 / +5.6 |
| Demand by category | base | base | base | - | CER Higher end-use (627 / 710 / 806 TWh) is below base |

Alternative B2 with a renewables-heavier mix: use the CER Canada Net-zero column instead (total 200.4 / 252.4 / 302.1; onshore wind 39.6 / 77.5 / 113.3; gas incl. CCUS 34.4 / 37.4 / 38.7; batteries 4.8 / 7.0 / 15.3 GW). That is the only CER scenario in which generation truly doubles (651 TWh in 2025 -> 1,323 TWh in 2050; 1,031 TWh in 2040).

### S1-C (stretch what-if): "Firm doubling" - the 150 GW of new firm capacity is forced
Source rows: Canadian Nuclear Association study cited by the strategy (150 GW additional firm capacity by 2050 = 115 GW non-emitting baseload + 35 GW flexible). OWN ASSUMPTION: linear phasing 2025-2050 (30 / 60 / 90 GW by 2030 / 2035 / 2040), baseload = hydro + nuclear incl. SMR, flexible = gas.

| Lever | 2030 | 2035 | 2040 | Base | Note |
|---|---|---|---|---|---|
| Hydro + nuclear + SMR, minimum, GW | 121 | 144 | 167 | 104 / 112 / 114 | 2025 level 97.9 + 23 / 46 / 69 (OWN ASSUMPTION phasing) |
| Gas, minimum, GW | 39 | 46 | 53 | 31 / 29 / 27 | 2025 level 32 + 7 / 14 / 21 (OWN ASSUMPTION phasing) |
| Total capacity, minimum, GW | none | none | none (optional 320) | 190 / 241 / 297 | no separate total floor needed, the firm floors drive the build; optional extra: doubling pulled forward to 2040 = ~320 GW (2 x 159 GW; OWN ASSUMPTION) |
| Demand by category | base | base | base | - | - |

Real projects that could fill the baseload wedge by 2040: Gull Island 2.25-2.7 GW (2036-37), Churchill Falls +1.3 to 2.5 GW, Hydro-Quebec +3.8-4.2 GW hydro by 2035, Darlington SMR 1.2-1.6 GW (2030-2035); together roughly 9-11 GW, i.e. far short of 69 GW - the variant is deliberately a what-if.

## S1 - Gaps

- NOT FOUND: any federal document that states "150 GW" as the baseline or "310 GW" as a target; the pairing appears to be the requester's paraphrase of CER EF2026 Current Measures.
- NOT FOUND: a final National Electricity Strategy (after the consultation) and any 2030 / 2035 / 2040 milestones for capacity or generation.
- NOT FOUND: draft text or dates of the announced Clean Electricity Regulations amendments.
- NOT FOUND: MW, cost and in-service dates for the BC-Yukon link and the PEI-NB expansion; cost and dates for the other three priority interties; a project list of the Transmission InterConnect Investment Strategy.
- NOT FOUND: Canada-US interconnector additions with dates (the 24 GW north-south figure is the only sourced number; new lines to New England / New York were not re-verified).
- NOT FOUND: IESO APO 2026 demand values for 2030 / 2035 / 2040 as numbers (chart only; the data tables were not downloaded).
- NOT FOUND: AESO 2026 Long-Term Outlook (due Q4 2026); NB Power and Nova Scotia gas build plans; a 2026 update of the Hydro-Quebec plan; BC Hydro IRP numbers for 2035 / 2040.
- NOT FOUND: IEA estimate specific to Canada.
- Several provincial rows are "snippet - verify" (Saskatchewan, Manitoba, Alberta, Nova Scotia, BC call results, Site C, North Coast line).

---

## S9 - Signal check

| Claim | What the sources say | Verdict | Source (org, title, date) | URL |
|---|---|---|---|---|
| "Canada, an EU associate member" | Not a fact, a proposal. Commission President von der Leyen, State of the Union, Strasbourg, 16 Sept 2026: "I would like to work with you on opening the door for Canada to be the first associate member of the EU." PM Carney had said days earlier that Canada seeks a "unique alliance", not membership; on 17 Sept 2026 he told the European Parliament "Canada welcomes this ambition". No such status exists in EU law (possible basis: Art. 217 TFEU association agreement; full membership barred by Art. 49 TEU). Process would be: European Council mandate -> Commission negotiation -> unanimous Council + EP consent (+ possibly national ratifications). | corrected: proposal stage, content undefined, no negotiation mandate yet | Al Jazeera, 2026-09-16; PMO, address to the European Parliament, 2026-09-17; Squire Patton Boggs, "EU invites Canada to become its first associate member", 2026-09 | https://www.aljazeera.com/news/2026/9/16/eu-chief-von-der-leyen-proposes-associate-member-status-for-canada ; https://www.pm.gc.ca/en/news/speeches/2026/09/17/prime-minister-carney-delivers-address-european-parliament ; https://www.squirepattonboggs.com/insights/publications/eu-invites-canada-to-become-its-first-associate-member/ |
| Next formal step | EU-Canada summit, Montreal, 29-30 Oct 2026. Draft joint statement (press reports): digital trade agreement, critical-minerals projects with EIB funding, joint purchase of 50 De Havilland water bombers (by 2030), competition pact, an LNG-export-to-Europe feasibility study, Erasmus talks, Horizon Europe / Galileo steps, and a pledge to "jointly assess opportunities to expand energy connectivity and strengthen long-term energy co-operation". | confirmed (as reported from a draft) | Canadian Affairs, 2026-09-30; Squire Patton Boggs 2026-09 | https://www.canadianaffairs.news/2026/09/30/canada-eu-readying-deals-on-minerals-water-bombers-in-efforts-to-draw-closer/ |
| Existing building blocks | CETA provisionally applied since 2017; 17 of 27 member states have ratified (not: Belgium, Bulgaria, Cyprus, France, Greece, Hungary, Ireland, Italy, Poland, Slovenia). Bilateral trade 2025: EUR 130 bn goods + services, +80 % vs 2016 (EUR 72.1 bn). Security and Defence Partnership signed 23 June 2025 (20th summit). SAFE: Canada first non-European participant; agreement signed 14 Feb 2026, concluded by the Council 15 June 2026 (snippet - verify). Horizon Europe Pillar II. | confirmed | Euronews, "What is CETA...", 2026-09-21; Global News, 2026-09; Council of the EU, 2026-06-15 | https://www.euronews.com/2026/09/21/what-is-ceta-and-why-is-the-eu-canada-trade-deal-still-in-limbo ; https://globalnews.ca/news/12062954/eu-leaders-canada-associate-membership/ ; https://www.consilium.europa.eu/en/press/press-releases/2026/06/15/safe-council-concludes-agreement-with-canada/ |
| "Discussions include energy, critical minerals, advanced manufacturing, technology, economic security" | Confirmed. Von der Leyen named manufacturing, AI, critical minerals and energy. Carney: "critical minerals, defence industrial capacity, AI and compute, energy security, space, and payments"; "Canada can contribute LNG and hydrogen at large scale to support Europe's energy security including by developing and leveraging new port infrastructure in the High North and on our East Coast"; Canada supplies minerals, Europe "advanced processing capabilities". | confirmed | PMO speech 2026-09-17; Al Jazeera 2026-09-16 | (as above) |
| Critical raw materials cooperation | EU-Canada Strategic Partnership on Raw Materials reaffirmed 2 March 2026 (Hodgson - Sejourne, PDAC Toronto); Letter of Intent EIB - Government of Canada on critical raw materials; EU-Canada Industrial Policy Dialogue (announced at the June 2025 summit). No project names, amounts or timelines in the statement. | confirmed (no quantities) | NRCan, "Joint Statement by Minister Hodgson and Executive Vice President Sejourne", 2026-03-02 | https://www.canada.ca/en/natural-resources-canada/news/2026/03/joint-statement-by-minister-hodgson-and-executive-vice-president-sejourne.html |
| "accelerate electricity infrastructure investment, grid expansion, clean generation" | No official EU-Canada text quantifies electricity infrastructure, generation or grid. The only electricity-specific item is the draft wording on "energy connectivity". | not found (qualitative only) | Canadian Affairs 2026-09-30 | (as above) |
| "Major growth in ... hydrogen" | The political offer exists (Carney: hydrogen "at large scale"; Canada-Germany Hydrogen Alliance of Aug 2022; H2Global Canada-Germany window: EUR 400 m, EC state-aid approval 15 Jan 2026, ~300 MW electrolysis, auction to conclude 2027). The project reality is the opposite: Newfoundland's wind-hydrogen pipeline shrank to two projects by April 2026 (World Energy GH2, EverWind NL and Toqlukuti'k lost their Crown land reserves; Pattern/Argentia went wind-only). | corrected: announced pipeline > 6 Mt NH3/yr, but most of it is cancelled or paused; firm support covers ~300 MW | King & Spalding, 2026-01; EnergyNow, 2026-04; CER market snapshot on low-carbon ammonia, 2026 | https://www.kslaw.com/news-and-insights/canada-germany-joint-400-million-h2global-green-hydrogen-auction-receives-european-commission-state-aid-approval ; https://energynow.ca/2026/04/newfoundland-and-labradors-big-plans-for-hydrogen-dwindle-to-two-projects/ ; https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/market-snapshots/2026/market-snapshot-low-carbon-ammonia-and-its-role-in-canadas-hydrogen-economy.html |
| "National electricity demand growth outpaces current planning assumptions" | No source quantifies an EU-partnership demand effect. Published high cases exist (CER Higher / Net-zero, IESO high, Hydro-Quebec), see anchors - but the model base is already at or above them. | not found | - | - |
| Public and political backing | Leger (19-21 Sept 2026): 70 % support associate membership, 13 % oppose, 18 % unsure (snippet - verify). Abacus (4-9 Sept 2026): 81 % support closer integration, 49 % full membership. Ireland (Council presidency) endorsed; France "will examine"; Germany open but questions the label. US: President Trump called it "laughable" and threatened tariffs on the EU; US-Canada trade talks collapsed in late Aug 2026, duties up to 50 % on cars and trucks. | confirmed | National Observer, 2026-09-24; Squire Patton Boggs 2026-09 | https://www.nationalobserver.com/2026/09/24/news/more-two-three-canadians-back-eu-associate-membership-says-poll |

## S9 - Quantification anchors

Conversion rule used for ammonia / hydrogen exports (OWN ASSUMPTION, engineering rule of thumb, no source fetched): 52 kWh per kg H2 for electrolysis; 0.178 t H2 per t NH3; plus ~0.7 MWh per t NH3 for air separation and synthesis -> ~10 TWh of electricity per Mt NH3; 1 GW of electrolysis at 60 % utilisation = 5.3 TWh/yr.

### Partnership status and trade

| Data point | Value | Unit | Scope | Year(s) | Source (org, title, date) | URL | Note |
|---|---|---|---|---|---|---|---|
| Associate-membership proposal | 2026-09-16 | date | Canada-EU | 2026 | Al Jazeera | https://www.aljazeera.com/news/2026/9/16/eu-chief-von-der-leyen-proposes-associate-member-status-for-canada | |
| EU-Canada summit | 2026-10-29/30, Montreal | date | Canada-EU | 2026 | Squire Patton Boggs | https://www.squirepattonboggs.com/insights/publications/eu-invites-canada-to-become-its-first-associate-member/ | |
| Bilateral trade | 130 (2025) vs 72.1 (2016), +80 % | bn EUR | Canada-EU | 2016-2025 | Euronews 2026-09-21 | https://www.euronews.com/2026/09/21/what-is-ceta-and-why-is-the-eu-canada-trade-deal-still-in-limbo | goods + services |
| CETA ratifications | 17 of 27 | member states | EU | 2026-09 | same | same | |
| SAFE instrument | 150 bn loan facility; Canada participates | EUR | EU | 2026 | Council of the EU, 2026-06-15 | https://www.consilium.europa.eu/en/press/press-releases/2026/06/15/safe-council-concludes-agreement-with-canada/ | snippet - verify |
| CBAM | definitive phase since 2026-01-01; covers iron and steel, aluminium, cement, fertiliser, electricity, hydrogen; proposal of 2025-12-16 to add 180 downstream steel / aluminium products from 2028 | - | EU | 2026-2028 | BLG, "What the EU's Carbon Border Adjustment Measure means for Canada", 2026-01 | https://www.blg.com/en/insights/2026/01/the-worlds-first-carbon-border-adjusted-tax-enters-its-definitive-phase-what-it-means-for-canada | no Canadian export volumes in the article |

### Hydrogen / ammonia export projects (Atlantic Canada)

| Data point | Value | Unit | Scope | Year(s) | Source (org, title, date) | URL | Note |
|---|---|---|---|---|---|---|---|
| Total proposed Atlantic low-carbon ammonia | > 6 (= > ~60 TWh/yr, own calc with the rule above) | Mt NH3/yr | NL + NS | no date | CER, market snapshot "Low-carbon ammonia and its role in Canada's hydrogen economy", 2026 | https://www.cer-rec.gc.ca/en/data-analysis/energy-markets/market-snapshots/2026/market-snapshot-low-carbon-ammonia-and-its-role-in-canadas-hydrogen-economy.html | Canada produced ~5 Mt NH3 in 2023 |
| EverWind Point Tupper | 1 Mt NH3/yr at full build; first 240,000 t "late 2020s" (= ~2.4 / ~10 TWh) | t NH3 | Nova Scotia | late 2020s | same | same | phase 1 supply: 650 MW wind + 150 MW solar + 50 MW / 100 MWh battery; CAD 240 m financing March 2026, operations targeted 2028 (snippet - verify, https://www.bnnbloomberg.ca/investing/investor-outlook/2026/03/03/investor-outlook-everwind-lands-240m-for-point-tupper-wind-phase/) |
| Bear Head Energy, Point Tupper | > 1 Mt NH3/yr (= ~10 TWh) | t NH3 | Nova Scotia | n/a | CER snapshot | same | environmental approval received; no date |
| EVREC (Abraxas), Botwood | 3.5 GW wind + 150 MW solar; 2.6 GW hydrogen/ammonia facility; ~180,000 t H2 -> ~1 Mt NH3/yr (= ~10 TWh) | GW / t | Newfoundland | sales to Europe "by 2030" | EnergyNow, 2026-04; CER snapshot | https://energynow.ca/2026/04/newfoundland-and-labradors-big-plans-for-hydrogen-dwindle-to-two-projects/ | alive; land reserve extended to 2027-02-28 |
| North Atlantic, Placentia Bay | 324 MW wind; 90,000 t H2/yr (two plants; = ~4.7 TWh at full volume, more than 324 MW of wind can supply); FID Q1 2027; start 2030 | MW / t | Newfoundland | 2030 | same | same | alive; LOHC first, ammonia later; markets Germany / Netherlands |
| Pattern Energy, Argentia | up to 146,000 t NH3/yr (= ~1.5 TWh) | t NH3 | Newfoundland | - | CER snapshot; EnergyNow | same | hydrogen part withdrawn Nov 2025, wind-only resubmission |
| World Energy GH2, Nujio'qonik | 1.2 GW electrolysis (> 600 MW first phase); CAD 12 bn | GW | Newfoundland | - | EnergyNow 2026-04; FuelCellsWorks 2026-01-08 | https://fuelcellsworks.com/2026/01/08/h2/giant-canadian-green-hydrogen-project-shelved-as-developer-shifts-focus-to-domestic-power-exports | shelved; pivot to "Clean Grid Atlantic" power exports (snippet - verify) |
| EverWind Burin Peninsula | > 3 Mt NH3/yr (= ~30 TWh) | t NH3 | Newfoundland | - | CER snapshot; EnergyNow | same | Crown land reserve cancelled |
| Toqlukuti'k (ABO / CIP), Come by Chance | > 1 Mt NH3/yr (= ~10 TWh) | t NH3 | Newfoundland | - | same | same | Crown land reserve cancelled |
| H2Global Canada-Germany bilateral window | 400 m (200 + 200); ~300 MW electrolysis in Canada (= ~1.6 TWh/yr at 60 %); 10-year contracts; auction concludes 2027 | EUR / MW | Canada-Germany | 2026-2027 | King & Spalding, 2026-01 | https://www.kslaw.com/news-and-insights/canada-germany-joint-400-million-h2global-green-hydrogen-auction-receives-european-commission-state-aid-approval | the only firm public funding found |
| CER hydrogen end-use, all scenarios | CM 9 / 20 / 20; NZ 11 / 43 / 97 (energy content) | TWh H2 | Canada | 2030 / 2035 / 2040 | CER EF2026 end-use-demand CSV | https://www.cer-rec.gc.ca/open/energy/energyfutures2026/end-use-demand-2026.csv | electrolytic share NOT FOUND; base model: 2.5 / 5 / 8.5 TWh electricity |

### Export-oriented industry, links

| Data point | Value | Unit | Scope | Year(s) | Source (org, title, date) | URL | Note |
|---|---|---|---|---|---|---|---|
| Primary aluminium production | ~3.3 Mt; 10 smelters (9 in Quebec, 1 Kitimat BC) | Mt | Canada | 2024 | NRCan, "Aluminum facts" | https://natural-resources.canada.ca/minerals-mining/mining-data-statistics-analysis/minerals-metals-facts/aluminum-facts | electricity use NOT FOUND; at ~14 MWh/t (OWN ASSUMPTION) = ~46 TWh/yr |
| Aluminium export destinations | US 91 % of export value, Mexico 2 %, Netherlands 1 % | % | Canada | 2024 | same | same | |
| Shift of aluminium exports to the EU | EU share of monthly exports 6-40 % between Apr 2025 and Mar 2026 (near zero before); May 2026 exports CAD 1.2 bn | % / CAD | Canada | 2025-2026 | Discovery Alert, 2026; BNN Bloomberg 2026-05-27 | https://www.bnnbloomberg.ca/business/international/2026/05/27/canada-turns-from-us-to-europe-as-iran-war-propels-aluminum-higher/ | snippet - verify; diversion of existing output, not new load |
| Canada-Europe subsea power link (NATL) | 6 GW HVDC, ~4,000 km, > 30 bn (currency not confirmed); power "as early as 2040" | GW / km | Atlantic Canada - UK / EU | 2040 | National Observer, 2025-04-07 and 2025-11-19; Irish Times 2026-01-27 | https://www.nationalobserver.com/2025/11/19/news/transatlantic-power-line-europe-canada | snippet - verify; private proposal, no government commitment found; 6 GW at 70 % = ~37 TWh/yr (OWN ASSUMPTION utilisation) |
| LNG to Europe | feasibility study to be announced at the Oct 2026 summit | - | Canada-EU | 2026 | Canadian Affairs 2026-09-30 | https://www.canadianaffairs.news/2026/09/30/canada-eu-readying-deals-on-minerals-water-bombers-in-efforts-to-draw-closer/ | no volumes; no electricity figure |
| Nova Scotia Wind West (export-oriented offshore wind) | phase 1 ~5 GW, ~CAD 60 bn, 2033-2035 earliest; ambition 40-60 GW | GW | Nova Scotia | 2033+ | CMS; National Observer 2026-07-01 | https://cms.law/en/int/legal-updates/nova-scotia-s-offshore-wind-strategy-gathers-pace | snippet - verify |

### High-demand cases that could serve as "demand outpaces planning"

| Data point | Value | Unit | Scope | Year(s) | Source (org, title, date) | URL | Note |
|---|---|---|---|---|---|---|---|
| Base model demand (for reference) | 624 / 768 / 899 | TWh busbar | Canada | 2030 / 2035 / 2040 | task brief | - | of which data centres 71 / 178 / 269 |
| CER EF2026 Current Measures, end-use | 604 / 661 / 723 (814 in 2050) | TWh | Canada | 2030 / 2035 / 2040 | CER EF2026 CSV | https://www.cer-rec.gc.ca/open/energy/energyfutures2026/end-use-demand-2026.csv | below base |
| CER EF2026 Higher, end-use | 627 / 710 / 806 (982 in 2050) | TWh | Canada | same | same | same | below base; +24 / +49 / +83 vs Current Measures |
| CER EF2026 Canada Net-zero, end-use | 619 / 719 / 832 (1,042 in 2050) | TWh | Canada | same | same | same | below base; +15 / +58 / +109 vs Current Measures |
| CER Higher minus Current Measures, industry only | +8 / +19 / +29 | TWh | Canada | same | same (own calc from PJ) | same | proxy for "more manufacturing / minerals" |
| CER Net-zero transport electricity | 29 / 72 / 125 (CM: 13 / 29 / 45) | TWh | Canada | same | same | same | base BEV: 14 / 37 / 62 |
| CER generation, Higher / Net-zero | 725 / 860 / 971 and 726 / 872 / 1,031 | TWh | Canada | same | CER EF2026 generation CSV | https://www.cer-rec.gc.ca/open/energy/energyfutures2026/electricity-generation-technology-2026.csv | base generation ~ demand + net exports = ~965 TWh in 2040 |
| CER EF2023 Global Net-zero | 587 -> 1,187 (2.6 %/yr); ~703 / ~799 / ~908 (own calc) | TWh | Canada | 2023 -> 2050 | Transition Accelerator / Dunsky, 2025-11 | https://transitionaccelerator.ca/wp-content/uploads/2025/11/Forecasting-Canadas-Electricity-Future-Report-Final-November-2025.pdf | highest published national pathway; equals the base in 2040 |
| Aggregated provincial system outlooks | 604 -> 982 (2.0 %/yr) | TWh | Canada | 2025 -> 2050 | same | same | "current planning assumptions" in the sense of the scenario text |
| IESO high-demand scenario | 154 -> 297 (+92 %, 2.8 %/yr) vs reference 250 | TWh | Ontario | 2026 -> 2050 | IESO APO 2026 | https://www.ieso.ca/-/media/Files/IESO/Document-Library/planning-forecasts/apo/2026/2026-Annual-Planning-Outlook.pdf | unserved energy by 2035: 42 TWh (high) vs 19 TWh (reference) -> high case is ~+20 TWh in 2035 (own reading) |
| Ontario Pathways to Decarbonization | 325 | TWh | Ontario | 2050 | Ontario, "Energy for Generations", 2025-06 | https://www.ontario.ca/page/energy-generations | industrial demand +23 TWh (+58 %) and EVs 20 TWh by 2035 |
| Hydro-Quebec planning | +60 by 2035; +150-200 by 2050 | TWh | Quebec | 2035 / 2050 | Hydro-Quebec Action Plan 2035, 2023-11 | https://www.hydroquebec.com/data/a-propos/pdf/action-plan-2035.pdf | CER Current Measures has Quebec end-use at only +18 TWh 2025 -> 2035: the utility plans ~40 TWh more than CER (own calc) |

## S9 - Proposed variants

All variants are increments ON TOP of the base, because every published high case is at or below the base total (see table above). Categories as in the model. Numbers in TWh busbar.

### S9-A (central, announced-consistent): "Partnership delivers the surviving projects"
Source rows: H2Global window (300 MW), EverWind Point Tupper, EVREC, North Atlantic, Bear Head (project sizes sourced; all in-service timing is OWN ASSUMPTION); CER Higher minus Current Measures industrial electricity.

| Lever | 2030 | 2035 | 2040 | Derivation |
|---|---|---|---|---|
| Hydrogen (export electrolysis), added to base 2.5 / 5 / 8.5 | +4 | +26 | +36 | 2030: H2Global 1.6 + EverWind phase 1 2.4; 2035: + EverWind to 1 Mt (7.6) + EVREC 1 Mt (10) + North Atlantic 90 kt H2 (4.7); 2040: + Bear Head 1 Mt (10). Conversion rule and timing OWN ASSUMPTION |
| General (industry + buildings), added to base 518 / 522 / 525 | +8 | +19 | +29 | CER Higher minus CM industrial |
| Data centres, BEV, building heat | base | base | base | - |
| Total demand | 636 | 813 | 964 | base 624 / 768 / 899 |
| Capacity: onshore wind minimum (optional, project-linked) | base + 0.65 | base + 4.5 | base + 6.5 | EverWind 0.65 GW; EVREC 3.5 GW + North Atlantic 0.32 GW; Labrador wind 2 GW (Churchill agreement) - timing OWN ASSUMPTION |
| Interconnector | base | base | base | - |

### S9-B (alternative): "Regulatory alignment with the EU = net-zero electrification plus the surviving export projects"
Logic: an association brings alignment with EU climate rules (CBAM since 2026); CER Canada Net-zero is the published proxy. Source rows: CER Net-zero transport electricity; CER Net-zero minus CM non-transport end-use (0 / +15 / +29); hydrogen as in S9-A.

| Lever | 2030 | 2035 | 2040 | Derivation |
|---|---|---|---|---|
| BEV | 29 | 72 | 125 | CER Net-zero transport electricity (base 14 / 37 / 62) |
| General (industry + buildings) | +0 | +15 | +29 | CER Net-zero minus CM, end-use excluding transport |
| Hydrogen | +4 | +26 | +36 | as S9-A |
| Data centres, building heat | base | base | base | - |
| Total demand | 643 | 844 | 1,027 | own calc |
| Capacity: offshore wind minimum | 0 | 0 | 5 | Wind West phase 1 (5 GW, 2033-2035 earliest); placing it in 2040 is OWN ASSUMPTION |
| Capacity: onshore wind minimum | 39.6 | 77.5 | 113.3 | CER Net-zero (base 31 / 62 / 87) |
| Interconnector | base | base | base | - |

### S9-C (stretch what-if): "Preferred partner - the whole export pipeline is revived, plus a transatlantic cable"
Source rows: CER snapshot (> 6 Mt NH3/yr Atlantic pipeline incl. the cancelled projects); CER Higher industrial delta; CER Net-zero transport; NATL 6 GW cable; Wind West.

| Lever | 2030 | 2035 | 2040 | Derivation |
|---|---|---|---|---|
| Hydrogen | +4 | +30 | +60 | full > 6 Mt NH3/yr pipeline by 2040 at ~10 TWh/Mt; phasing OWN ASSUMPTION |
| General (industry + buildings) | +17 | +37 | +58 | twice the CER Higher industrial delta (factor 2 is OWN ASSUMPTION; stands for minerals processing, aluminium, steel, for which no sourced TWh were found) |
| BEV | 29 | 72 | 125 | CER Net-zero |
| Data centres, building heat | base | base | base | - |
| Total domestic demand | 660 | 870 | 1,080 | own calc |
| Export to Europe via NATL cable (fixed export load in a one-node model) | 0 | 0 | 37 (6 GW) | 6 GW from 2040 at 70 % utilisation (OWN ASSUMPTION) |
| Capacity: offshore wind minimum | 0 | 5 | 10 | Wind West phase 1 in 2035; second 5 GW by 2040 is OWN ASSUMPTION |
| Capacity: hydro minimum | base | base + 1.3 | base + 4.0 | Churchill Falls +1.275 GW; Gull Island 2.7 GW in 2036-37 - check whether the base hydro path (97 / 98 GW) already contains them |

## S9 - Gaps

- NOT FOUND: any official quantification of what "associate membership" means for energy, electricity demand, grid or generation; no negotiating mandate, no timetable beyond the 29-30 Oct 2026 summit.
- NOT FOUND: electricity demand (TWh or MW) of Canadian critical-minerals processing, battery supply chain, green steel (Algoma, ArcelorMittal Dofasco) or aluminium expansion projects; the industrial uplift in the variants is a CER-scenario proxy.
- NOT FOUND: electricity intensity and expansion plans of Canadian aluminium smelters; volumes of Canadian steel, aluminium, fertiliser exports to the EU and a quantified CBAM effect.
- NOT FOUND: Canada-EU nuclear fuel cooperation figures (uranium supply, Euratom) and LNG export volumes or dates.
- NOT FOUND: electrolyser MW and in-service dates for EverWind phases 2-3 and Bear Head; H2Global window volumes in tonnes.
- NOT FOUND: the electrolytic share of hydrogen in CER EF2026 (needed to turn the CER hydrogen energy rows into electricity).
- NOT FOUND: Hydro-Quebec industrial connection requests (MW) and an HQ high case for 2040; IESO high-case TWh for 2030 / 2035 / 2040 (chart only).
- "snippet - verify" rows: SAFE dates, Leger poll, NATL cable, aluminium export shift, World Energy GH2 pivot, EverWind financing.
- The search budget ended before these could be closed; the Carney speech, CER snapshot, EnergyNow, King & Spalding, Euronews, BLG and NRCan pages were read in full.
