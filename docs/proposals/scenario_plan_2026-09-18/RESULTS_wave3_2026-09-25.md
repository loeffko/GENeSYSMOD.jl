# SE scenario set - wave 3 results (2026-09-25)

Wave 3 = the wave-2 review's two base-data fixes (rooftop PV build-rate cap, gas-steam floor clamp) and the s10 derate
ramp, with the base and all 14 scenarios rerun on the fixed data, plus a **funnel-released twin** of every scenario except
s05 (gas guardrail minimum = residual capacity from 2031). Review and response:
`../scenario_results/REVIEW_wave2_2026-09-24.md`, `../scenario_results/REVIEW_RESPONSE_wave2_2026-09-24.md`;
definition record: `Wave3_changes` sheet of `../NA_scenario_plan_2026-09-18_v4.xlsx`.
Reference: `fel2026_base_49_2015_v6f`. Labels `fel2026_sNN_<name>_49_2015_v6_v3` (s03/s06 `_v4`, s14 `_v5`); twins
`fel2026_sNN_<name>_open_49_2015_v6`. All runs at 49-hour resolution, all `OPTIMAL`; infeasibility slack 2.4-5.0 TWh
(base 4.4). Tables: `Scripts/analyze_s14.py fel2026_base_49_2015_v6f 3|open` -> `s14_summary_wave3.csv` /
`s14_summary_wave3_open.csv`; markdown via `Scripts/s14_results_md.py`. Deltas are 2040 vs base.

## Base v6f vs v6e (the effect of the two fixes)

| | v6e | v6f |
|---|---|---|
| objective (bEUR, discounted 2025-40) | 2,675.3 | 2,677.2 (+0.07 %) |
| rooftop PV additions 2026-31 (US) | 15.6 / 28.4 / 38.4 / 33.2 / 35.7 / 34.9 GW | 7.0 GW/yr (on the cap), 7.3-9.7 GW/yr 2031-39 |
| rooftop fleet 2031 / 2040 (GW) | 188 / 188 | 46 / 115 |
| new gas steam 2026-40 | 12 GW (forced) | 0.1 GW; New York 0.7-1.5 GW/yr 2038-40 on its own (its gas pipeline maxima = residual fleet; v7 item) |
| generation 2030: solar / gas (TWh) | 885 / 1,821 | 700 / 2,003 |
| generation 2035: solar / gas / wind | 1,423 / 2,385 / 1,006 | 1,281 / 2,495 / 1,032 |
| generation 2040: solar / gas / wind | 1,853 / 2,770 / 1,349 | 1,788 / 2,798 / 1,384 |
| CO2 2030 / 2035 / 2040 (Mt) | 1,317 / 1,238 / 1,161 | 1,398 / 1,277 / 1,171 |
| 2025 | identical | identical |

The cap removes ~140 GW of rooftop that the model had used as an uncapped bypass of the utility-PV pipeline funnel; in
the funnel years the gap is filled by gas (2030 +182 TWh) and later by wind, so the base leans more on gas in the 2030s.
INF slack 4.4 TWh (v6e 4.5). `Scripts/compare_base_regression.py fel2026_base_49_2015_v6f fel2026_base_49_2015_v6e`.

## Main set (funnel kept)

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CF solar/wind 2040 | curtailed 2040 | cost per MWh of extra demand | CO2 payments (bEUR) | resource cost net of transfers (bEUR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | v6f | 8,242 TWh | 2,798 | 1,788 | 1,384 | 1,150 | 844 | 305 | 1,171 Mt | 2,677 | 0.20/0.36 | 175 TWh | - | 0 | - |
| 1 | EV comeback (s01_ev, v3) | +245 | +58 | +39 | +150 | 0 | +5 | +1 | +22 | +67 | 0.20/0.35 | +18 | 28.7 EUR | 0 | +67 |
| 2 | H2 comeback (s02_h2, v3) | +399 | +161 | +84 | +155 | 0 | +12 | 0 | +58 | +56 | 0.20/0.35 | +8 | 23.6 EUR | 0 | +56 |
| 3 | Age of compute (s03_compute, v4) | +694 | +363 | +124 | +205 | 0 | +21 | +1 | +141 | +81 | 0.20/0.35 | +6 | 23.8 EUR | 0 | +81 |
| 4 | Space race, terrestrial (s04_space, v3) | +155 | +79 | +41 | +35 | 0 | +9 | 0 | +29 | +15 | 0.20/0.36 | +1 | 22.4 EUR | 0 | +15 |
| 5 | Political brakes (s05_brakes, v3) | -518 | -461 | -72 | +2 | 0 | -210 | -1 | -154 | -201 | 0.20/0.35 | +27 | 46.1 EUR | 0 | -201 |
| 6 | Hormuz 6C (s06_hormuz, v4) | 0 | +3 | +1 | -3 | 0 | 0 | -2 | +1 | -16 | 0.20/0.36 | 0 | 9.6 EUR | 0 | -16 |
| 7 | Tech breakthrough (s07_tech, v3) | 0 | -80 | +42 | -14 | 0 (+73 fusion) | -28 | +35 (+39 iron-air) | -31 | -1 | 0.20/0.36 | -16 | - | 0 | +12 |
| 8 | Canada DC, pipeline-consistent (s08_canada, v3) | -49 | +10 | +1 | -60 | 0 | +3 | 0 | +4 | -11 | 0.20/0.36 | 0 | 20.4 EUR | 0 | -11 |
| 9 | Water boom (s09_water, v3) | +36 | +10 | +10 | +16 | 0 | +1 | 0 | +4 | +4 | 0.20/0.36 | +2 | 21.2 EUR | 0 | +4 |
| 10 | Climate reshuffle (s10_climate, v3) | +216 | +38 | +66 | +134 | -27 | -7 | +1 | +27 | +49 | 0.20/0.35 | +27 | 34.0 EUR | 0 | +49 |
| 11 | FEOC (s11_feoc, v3) | 0 | +4 | -1 | -3 | 0 | 0 | 0 | +1 | +7 | 0.20/0.36 | 0 | - | 0 | +7 |
| 12 | AI overbuild (s12_overbuild, v3) | -1,294 | -719 | -320 | -254 | 0 | -26 | -4 | -262 | -205 | 0.20/0.36 | -13 | 23.2 EUR | 0 | -205 |
| 13 | Reindustrialization (s13_reindustrial, v3) | +163 | +84 | +45 | +34 | 0 | +12 | 0 | +30 | +51 | 0.20/0.36 | +3 | 35.0 EUR | 0 | +51 |
| 14 | Decarbonization (s14_decarb, v5) | 0 | -606 | +193 | +284 | +254 | +25 (+40 CCS) | +1 | -501 | +304 | 0.19/0.31 | +319 | - | 361 | +149 |

Units: TWh unless stated; storage = D_ power capacity; cost = total discounted system cost delta 2025-40; cost per MWh
of extra demand = delta cost / delta demand 2025-40 (undiscounted TWh). Resource cost = delta cost - CO2 payments +
capex reduction vs base x new capacity + variable-cost credits (both discounted); it matters for s14 (ITC 180, 45Q 26,
CO2 payments 361 bEUR -> resource cost +149 bEUR, +5.6 % of base) and is not a transfer correction for s07/s11 (their
capex changes are the scenario itself).

### What the rooftop cap changed against wave 2 (2040 deltas, wave 2 / wave 3)

| scenario | gas | solar | wind | CO2 | cost |
|---|---|---|---|---|---|
| s01 EV | +73 / +58 | +49 / +39 | +124 / +150 | +31 / +22 | +64 / +67 |
| s02 H2 | +189 / +161 | +86 / +84 | +123 / +155 | +67 / +58 | +55 / +56 |
| s03 compute | +327 / +363 | +174 / +124 | +193 / +205 | +122 / +141 | +77 / +81 |
| s04 space | +83 / +79 | +34 / +41 | +37 / +35 | +30 / +29 | +15 / +15 |
| s05 brakes | -491 / -461 | -67 / -72 | +28 / +2 | -163 / -154 | -210 / -201 |
| s06 Hormuz | +20 / +3 | -21 / +1 | 0 / -3 | +7 / +1 | -18 / -16 |
| s07 tech | -101 / -80 | +35 / +42 | +10 / -14 | -40 / -31 | -1 / -1 |
| s08 Canada DC | -2 / +10 | -4 / +1 | -43 / -60 | -2 / +4 | -10 / -11 |
| s09 water | +8 / +10 | +9 / +10 | +19 / +16 | +3 / +4 | +4 / +4 |
| s10 climate | -35 / +38 | +128 / +66 | +143 / +134 | -6 / +27 | +44 / +49 |
| s11 FEOC | +4 / +4 | -4 / -1 | -2 / -3 | +2 / +1 | +8 / +7 |
| s12 overbuild | -741 / -719 | -332 / -320 | -222 / -254 | -267 / -262 | -202 / -205 |
| s13 reindustrial | +85 / +84 | +41 / +45 | +36 / +34 | +30 / +30 | +50 / +51 |
| s14 decarb | -690 / -606 | +269 / +193 | +304 / +284 | -524 / -501 | +271 / +304 |

Reading: with rooftop capped, the flexible PV response of wave 2 turns into wind and gas. The demand scenarios (s01-s04,
s13) keep their cost per MWh (22-35 EUR/MWh); s10's solar-led north-shift becomes wind-led and no longer lowers CO2
(+27 Mt instead of -6); s14 keeps less solar (+193 instead of +269 TWh) and more gas (-606 instead of -690), so its
2040 CO2 is 670 Mt (v4: 637) at +304 bEUR objective delta / +149 bEUR resource cost. s06 is now almost invisible in 2040
(the pre-build is gone, net -16 bEUR = recession savings minus the 2026-27 fuel shock). s05 and s12 are unchanged in
substance.

## Funnel-released twins

Every scenario except s05 rerun with the gas guardrail minimum (`TotalAnnualMinCapacity` of CCGT, OCGT, steam, engines)
set to the residual capacity from 2031 on; announced projects through 2030, the build-rate caps and everything else
unchanged. **The base is not released** (user decision), so the deltas vs base below contain the release effect
itself; the second table isolates it by comparing each twin with its own funnel run. s05 already releases from 2027
and is shown with its main run. Labels `fel2026_sNN_<name>_open_49_2015_v6`, all `OPTIMAL`, INF slack 2.5-5.0 TWh.

### Twins vs base v6f (2040)

| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CF solar/wind 2040 | curtailed 2040 | cost per MWh of extra demand | CO2 payments (bEUR) | resource cost net of transfers (bEUR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | v6f | 8,242 TWh | 2,798 | 1,788 | 1,384 | 1,150 | 844 | 305 | 1,171 Mt | 2,677 | 0.20/0.36 | 175 TWh | - | 0 | - |
| 1 | EV comeback (s01_ev, open) | +245 | -28 | +68 | +190 | 0 | -108 | +1 | +2 | +46 | 0.20/0.35 | +41 | 19.7 EUR | 0 | +46 |
| 2 | H2 comeback (s02_h2, open) | +399 | +74 | +105 | +206 | 0 | -102 | +1 | +36 | +35 | 0.20/0.35 | +28 | 14.8 EUR | 0 | +35 |
| 3 | Age of compute (s03_compute, open) | +694 | +323 | +141 | +219 | 0 | -67 | 0 | +127 | +62 | 0.20/0.35 | +21 | 18.1 EUR | 0 | +62 |
| 4 | Space race, terrestrial (s04_space, open) | +155 | -65 | +70 | +140 | 0 | -120 | 0 | -13 | -9 | 0.20/0.35 | +31 | -14.2 EUR | 0 | -9 |
| 5 | Political brakes (s05_brakes, v3) | -518 | -461 | -72 | +2 | 0 | -210 | -1 | -154 | -201 | 0.20/0.35 | +27 | 46.1 EUR | 0 | -201 |
| 6 | Hormuz 6C (s06_hormuz, open) | 0 | -170 | +35 | +129 | 0 | -137 | -2 | -49 | -42 | 0.20/0.35 | +32 | 25.7 EUR | 0 | -42 |
| 7 | Tech breakthrough (s07_tech, open) | 0 | -287 | +80 | +160 | 0 (+73 fusion) | -179 | +47 (+52 iron-air) | -93 | -27 | 0.20/0.35 | +10 | - | 0 | -15 |
| 8 | Canada DC, pipeline-consistent (s08_canada, open) | -49 | -164 | +32 | +79 | 0 | -135 | 0 | -47 | -36 | 0.20/0.35 | +30 | 68.6 EUR | 0 | -36 |
| 9 | Water boom (s09_water, open) | +36 | -151 | +44 | +138 | 0 | -133 | 0 | -43 | -20 | 0.20/0.35 | +32 | -95.9 EUR | 0 | -20 |
| 10 | Climate reshuffle (s10_climate, open) | +216 | +5 | +75 | +145 | -27 | -97 | +1 | +23 | +31 | 0.20/0.35 | +40 | 21.3 EUR | 0 | +31 |
| 11 | FEOC (s11_feoc, open) | 0 | -171 | +33 | +133 | 0 | -137 | 0 | -50 | -18 | 0.20/0.35 | +31 | - | 0 | -18 |
| 12 | AI overbuild (s12_overbuild, open) | -1,294 | -946 | -263 | -83 | 0 | -242 | -2 | -325 | -255 | 0.20/0.35 | +25 | 28.8 EUR | 0 | -255 |
| 13 | Reindustrialization (s13_reindustrial, open) | +163 | -60 | +74 | +144 | 0 | -118 | 0 | -11 | +28 | 0.20/0.35 | +33 | 19.0 EUR | 0 | +28 |
| 14 | Decarbonization (s14_decarb, open) | 0 | -643 | +206 | +278 | +254 | -180 (+40 CCS) | +1 | -488 | +264 | 0.18/0.31 | +365 | - | 367 | +106 |

### Release effect = twin minus its own funnel run (2040)

| scenario | gas TWh | gas GW | new gas 2026-40 (GW) | solar TWh | wind TWh | CO2 Mt | cost bEUR |
|---|---|---|---|---|---|---|---|
| s01 EV | -86 | -113 | 446 -> 333 | +29 | +40 | -20 | -21 |
| s02 H2 | -88 | -114 | 453 -> 339 | +21 | +51 | -22 | -21 |
| s03 compute | -40 | -88 | 461 -> 373 | +17 | +14 | -14 | -20 |
| s04 space | -144 | -129 | 449 -> 320 | +29 | +105 | -42 | -24 |
| s06 Hormuz | -173 | -137 | 441 -> 304 | +34 | +133 | -50 | -26 |
| s07 tech | -207 | -151 | 412 -> 262 | +38 | +175 | -62 | -27 |
| s08 Canada DC | -175 | -137 | 443 -> 306 | +32 | +140 | -50 | -25 |
| s09 water | -161 | -134 | 441 -> 308 | +35 | +122 | -47 | -25 |
| s10 climate | -33 | -90 | 434 -> 344 | +9 | +10 | -4 | -18 |
| s11 FEOC | -174 | -137 | 441 -> 304 | +34 | +136 | -51 | -25 |
| s12 overbuild | -227 | -216 | 415 -> 199 | +56 | +171 | -63 | -50 |
| s13 reindustrial | -144 | -130 | 452 -> 322 | +28 | +110 | -41 | -23 |
| s14 decarb | -37 | -204 | 465 -> 261 | +13 | -6 | +12 | -40 |

Base new gas 2026-40: 440 GW (funnel). New CCGT+OCGT in 2031-40: base 318 GW, s14 funnel 306, s14 twin 108, s07
twin 149, s12 twin 87.

Reading:
- The release is worth **-18 to -27 bEUR** in every ordinary scenario, **-40** in s14 and **-50** in s12; it removes
  90-140 GW of gas capacity (s12 216, s14 204) and shifts 30-230 TWh of gas generation to wind (+10 to +175 TWh)
  and some solar. CO2 falls by 40-60 Mt in 2040 where gas generation drops; in the demand booms (s03, s10) the
  release changes little because the extra gas is wanted anyway (new CCGT still runs at 60-66 %).
- **s14 twin:** new CCGT 137 GW instead of 278, new-CCGT capacity factor 0.54 instead of 0.39, objective +264 bEUR
  (funnel run +304), **resource cost +106 bEUR** (funnel run +149; CO2 payments 367, ITC 180, 45Q 26). CO2 2040 is
  682 Mt against 670 in the funnel run: with fewer new CCGTs the residual fleet runs harder (1,023 vs 888 TWh) and a
  little coal survives (22 vs 1 TWh) - the policy case gets cheaper, not cleaner, when it stops paying for gas
  plants it does not need.
- **s07 twin:** the tech breakthrough now displaces gas instead of idling it: gas -287 TWh / -179 GW vs base,
  iron-air 52 GW, CO2 -93 Mt, cost -27 bEUR (funnel run: -80 TWh, -1 bEUR).
- **s12 twin:** the overbuild story with project cancellations: new gas 199 GW instead of 415, gas -946 TWh,
  CO2 -325 Mt, cost -255 bEUR (funnel run -205); firm capacity 1,319 GW vs 1,561 in the base.
- **Peaking caveat:** the twins keep the model's peaking constraint (firm capacity 2040: base 1,561 GW, s14 twin
  1,437, s12 twin 1,319 incl. storage credit). The v6 `economic` dispatch showed that funnel-freed fleets can carry
  winter-drought scarcity that this constraint accepts; the twins have not been dispatch-checked (v7 item
  `project-peaking-capacity-review`).

## Run notes

- All 28 runs terminated `OPTIMAL` (Gurobi barrier, crossover off); INF slack 2.4-5.0 TWh (main set and twins).
- s10 v3: the 2030 peaker step is gone (OCGT +18 TWh in 2030 instead of +97, rising with the ramp to +125 in 2034).
- s06 v4: 2026/27 new capacity equals the base (rooftop 7.8 / 7.3 GW on the cap, utility identical); the wave-2
  foresight pre-build (43 / 51 GW rooftop) is gone without pinning.
- Input dumps: base v6f differs from v6e only in `input_GroupTotalAnnualMaxNewCapacity` (+RooftopPV rows),
  `input_TagTechnologyToSubsets` (+1) and `input_TotalAnnualMinCapacity` (31 steam rows).

## Reproduction

- Data: data repo `NA_inputs/build_14_scenarios.py --apply --repo C:/v6wt` (base fixes in `base_additions()` /
  `base_fixes()`, twins via `open_variant()`; commit 5aa542d), overlays regenerated from empty folders; conversion
  `C:/v6wt/Conversion Script/script_northamerica.py` (base) and `_s14_convert.py` (14 + 13 twins); workbooks
  `InputData/RegularParameters_NorthAmerica_v6f.xlsx`, `..._sNN_<name>.xlsx`, `..._sNN_<name>_open.xlsx`.
- Runs: `_s14/run_base_v6f.jl`, `_s14/run_sNN_v3.jl` (s03/s06 `_v4`, s14 `_v5`), `_s14/run_sNN_open.jl`; chain
  `_s14/run_all_v3.sh` (log `Results/_s14_runs_w3.log`); 1924-hour probe `_s14/probe_base_v6f.jl`.
- Storage tables for the export: `Scripts/export_storage_tables.py <labels>`.
