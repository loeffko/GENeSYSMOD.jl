# Review of the wave-2 results (2026-09-24)

Reviewed material: `FEL_HubNA_AI-Scenarios_Results_Wave2.xlsx` (base `fel2026_base_49_2015_v6e`, 14 scenarios, s14 = v4, 19 technologies) and `REVIEW_RESPONSE_2026-09-23.md`.
Compared against: wave-1 workbook `FEL_HubNA_AI-Scenarios_Results.xlsx`.
Basis of verification: generation, installed capacity and gross additions in the workbook. CO2, cost, curtailment and input dumps are not in the workbook; figures on those are taken from the response as given.

## Summary

- The fixes hold. Wave 2 matches wave 1 within a few TWh in every run except s03, s06, s07 and s14, which are the ones that changed on purpose. The base differs from v6d only in 2030 (gas now 1,822 TWh, all fossil modes).
- Status of the 16 wave-1 items: 8 closed, 3 accepted by design (keep the caveat), 4 partly resolved, 1 open.
- The 19-technology split exposes one new serious issue (rooftop PV) and one side effect of the s06 fix (a foresight pre-build). Both should be addressed before wave 3 / v7.
- For messaging: the gas split shows that CCGT capacity is set by the funnel, not by the scenarios. Use CCGT CF and gas TWh, not gas GW.

## Status of the wave-1 items

| # | Wave 1 | Item | Response | Verdict | Comment on wave 2 |
|---|---|---|---|---|---|
| 1 | Critical | Biogas mode understates 2030 CO2 | Fixed in base data, base v6e | Closed | Base 2030 gas 1,822 TWh, all in CCGT/OCGT/engines/steam rows; all other base years within 3 TWh of wave 1. CO2 not verifiable from the workbook. |
| 2 | Critical | Gas GW is an input, not a result | By design, not changed | By design, keep caveat | The split sharpens it: CCGT sits at the base 531 GW (+-0.5) in 7 of 14 runs, incl. s12 (-1.3 PWh) and s14 (90 USD/t). OCGT lands on the same floor (~234.5 GW, -22.3 to -22.9) in s07, s12 and s14. s14 builds the same ~278 GW of new unabated CCGT as the base. |
| 3 | Critical | s03 adders on in 2025-27 | Crypto adder now growth above today | Closed | 2025-27 deltas are zero; 2040 generation +697 TWh, gas +327 TWh (47 %). |
| 4 | Serious | Fusion and storage missing from export | Export mapping issue | Partly | Fusion row present (9.5 GW, 73 TWh, CF 88 %). Storage is still not in the wave-2 workbook, so s07 iron-air and s11 Li-ion remain invisible. |
| 5 | Serious | Coal and nuclear output pinned | By design | By design, keep caveat | Agreed. State it next to any s06 gas-price statement: coal-gas switching is switched off. |
| 6 | Serious | s06 cancels projects under construction | Uplift on 2028-31 vintages only | Partly | The 2026-28 cut is gone, but the model now pre-builds ahead of the shock. See N2. |
| 7 | Serious | s14 build spike, Canada scope | ITC phased in 2029-31; NA policy case | Partly | Phase-in verified: new solar 102 / 115 / 121 GW in 2029-31. Label accepted. But 49-77 GW/yr of that is rooftop PV (+240 GW by 2036) while utility PV ends at -58 TWh in 2040. See N1. |
| 8 | Check | 9 GW hydro in 2026 | Pre-existing, v7 item | By design, keep caveat | Still there (reservoir +6.0, run-of-river +3.0 GW in 2026). |
| 9 | Check | s14 curtailment, idle coal | Curtailment reported (189 / 562 TWh) | Closed | Accepted; figures are in the results note only. s14 keeps +2.2 GW coal and lignite idle. |
| 10 | Check | EGS numbers | Note figure was total EGS | Closed | EGS row now 11.9 to 23.7 GW. The row also carries the existing conventional geothermal fleet. See N5. |
| 11 | Check | s10 relocation one-sided | Demand dump confirms | Closed | Accepted. |
| 12 | Check | s05 gas cap exceeded 2028 | Separate engine window cap | Closed | Verified: US 2028 = 9.9 GW plants + 1.0 GW engines; 2029-31 plants 9.8 / 4.4 / 10.0 GW. |
| 13 | Check | 2025 calibration low on gas | Known (27.9 vs 36.9 Bcf/d), v7 | Open | The team figure (-24 %) is larger than the reviewer's estimate. The 2025 gas starting point is materially low; keep the caveat on every absolute gas TWh until v7. |
| 14 | Note | SMR stays at 2.8 GW | Capex rows verified | Closed | Accepted. |
| 15 | Note | s08 headwind by construction | Label "announcement-consistent" | Closed | Accepted. |
| 16 | Note | Cost column is not cost of scenario | Cost per MWh added; s14 CO2 payments 322 bEUR | Partly | Cost per MWh (20-35 EUR/MWh) is plausible as a lower bound. For s14 see N3. |

## New findings

### N1 (Serious) Rooftop PV behaves like a cheap, unconstrained PV class

Evidence:
- US rooftop PV is 0 GW in every pool in 2025 (Canada 1.7 GW). The US has roughly 50 GW of distributed PV today, California alone more than 15 GW.
- Base build: +186 GW in 2026-2031 (15.6 / 28.4 / 38.4 / 33.2 / 35.7 / 34.9 GW), i.e. ~31 GW/yr, roughly four times the US record for distributed PV. Flat at ~188 GW from 2031 on, which looks like a potential cap.
- Location: PJM 78 GW, SERC 76 GW, New England 11 GW, SPP 11 GW, New York 8 GW by 2031. California, WECC and ERCOT get none in any scenario.
- It is the first-responder PV technology across the set (2040 vs base): s05 +88 GW while utility PV -109 GW (the RES funnel cap in s05 is bypassed through rooftop), s10 +89 GW, s12 -72 GW, s14 +240 GW vs utility +22 GW. s14 2040 solar TWh: rooftop +327, utility -58.
- Rooftop is 294 of 1,853 TWh of base solar in 2040 (16 %).

Asks:
1. Check rooftop capex/FOM against utility PV (rooftop should be well above utility per kW).
2. Check whether rooftop sits outside the RES funnel (TotalAnnualMin/MaxCapacity) and the s05 "RES max = pipeline" rule.
3. Check rooftop potentials and build-rate limits by pool, and why CA/WECC/ERCOT have none.
4. Clarify how today's behind-the-meter PV is treated: if it is netted from busbar demand, new rooftop should not sell at busbar either.

### N2 (Serious) s06 fix creates a foresight pre-build

Evidence: with the capex/WACC uplift on 2028-31 vintages only, s06 builds 43 and 51 GW of rooftop PV in 2026 and 2027 (base 16 and 28), then almost none in 2028-2030. Solar capacity vs base: +27 GW (2026), +50 GW (2027), -54 GW (2030), -64 GW (2031). The model anticipates a shock that, in the scenario story, nobody saw coming.

Ask: fix 2026-27 new builds to the base values (min = max = base) in s06, or run the shock years with limited foresight.

### N3 (Check) s14 cost: CO2 payments are not the only transfer

Evidence: the +271 bEUR objective delta contains 322 bEUR of CO2 payments, so it is -51 bEUR net of those. The restored ITC (capex x0.7 from 2029-31) and 45Q (negative variable cost, -7.95 MEUR/PJ) are also transfers between taxpayers and the power sector; they lower the objective without lowering real resource cost.

Ask: report s14 resource cost with the CO2 payments, the ITC and the 45Q credit all backed out, before any statement that decarbonization is cheaper than the base.

### N4 (Check) New gas steam units are being built

Evidence: gross additions of "Gas Steam" are 12 GW in the base 2026-2040 (17 GW in s10), at 1-3 GW/yr from 2036. New gas-fired steam/boiler units are not built in practice.

Ask: check which model technologies map to "Gas Steam" additions (repowering, CHP, a retirement-replacement rule?) and relabel or fix.

### N5 (Note) The geothermal row is not only EGS

Evidence: "Enhanced Geothermal" starts at 4.1 GW / 32 TWh in 2025, which is the existing conventional US geothermal fleet.

Ask: rename to "Geothermal (incl. EGS)" in the export.

### N6 (Note) s10 shifts 2030 energy onto peakers

Evidence: in 2030, s10 OCGT generation is +97 TWh (fleet CF 11 %) while CCGT is -88 TWh. By 2040 the effect is +37 TWh OCGT. The coastal availability cut appears to hit CCGTs broadly, and the relocated load arrives in 2030 before new capacity.

Ask: check which units carry the coastal derate; consider ramping the relocation in over 2030-2032.

## Observations for messaging (no action needed)

- Base new gas 2026-2040 by type: 279 GW CCGT, 139 GW OCGT, 18 GW engines, 12 GW steam (448 GW). CCGT CF rises from 50 % (2025) to 57 % (2040); OCGT ends at 4 % CF, i.e. reserve capacity.
- Added flat load is served ~47-54 % by gas (s02, s03, s04, s13), ~30 % in s01. CCGT capacity moves only +1 to +17 GW, OCGT +2 to +3 GW; the existing CCGTs run harder (CF 57 % to 60 % in s03).
- s12: gas output -741 TWh, CCGT fleet unchanged (CF 57 % to 43 %), OCGT -22 GW to its floor.
- s05: new gas 233 instead of 448 GW (2040: CCGT -114, OCGT -85, engines -12 GW).
- s14 v4: CCGT fleet stays at 531 GW, CF 57 % to 38 %; +40 GW CCS at 84 % CF; nuclear +254 TWh (19 GW SMR, 14 GW large).

## Requested before wave 3 / v7

1. N1 rooftop PV: cost, funnel membership, potentials, BTM treatment. Highest priority, because it drives the solar response in s05, s10, s12 and s14.
2. N2 s06: pin 2026-27 builds to base.
3. Item 4: add a storage capacity sheet (D_* power and energy) to the export.
4. N3: s14 resource cost net of all transfers.
5. N4 and N5: export mapping and labels.
