# -*- coding: utf-8 -*-
"""Gas-infrastructure run diagnostics: balance, corridors, storage, prices, INF gate,
and comparison against a reference (power-only) scenario.
Usage: python Scripts/analyze_gas_run.py <gas_scenario> [ref_scenario]"""
import sys, duckdb
sys.stdout.reconfigure(encoding='utf-8')
S = sys.argv[1] if len(sys.argv) > 1 else 'fel2026_gas_49_2015_v6'
B = sys.argv[2] if len(sys.argv) > 2 else 'fel2026_base_49_2015_v6c'
con = duckdb.connect(r'C:\Users\testbed\Documents\GENeSYSMOD.jl_SE\Results\genesysmod_db.duckdb', read_only=True)
q = lambda sql, p=(): con.execute(sql, list(p)).fetchall()

print(f'=== {S} vs {B} ===')
inf = q("SELECT Technology, ROUND(SUM(Value)/3.6,2) FROM output_production WHERE Scenario=? AND Technology LIKE 'Infeasibility%' GROUP BY 1", [S])
print('INF gate (TWh-eq, all years):', inf)

# --- gas balance per region 2025 / 2040 (PJ)
for y in (2025, 2040):
    print(f'\n--- Gas_Natural balance {y} (PJ): production | import | use(power) | use(export) | demand(non-power) | export')
    rows = q("""SELECT Region,
      ROUND(SUM(CASE WHEN Type='Production' AND Technology='R_Gas' THEN Value END),0) rgas,
      ROUND(SUM(CASE WHEN Type='Production' AND Technology='Z_Import_Gas' THEN Value END),0) zimp,
      ROUND(SUM(CASE WHEN Type='Use' AND Technology LIKE 'P_Gas%' THEN Value END),0) upow,
      ROUND(SUM(CASE WHEN Type='Use' AND Technology='X_Gas_Export' THEN Value END),0) uexp,
      ROUND(SUM(CASE WHEN Type='Import' THEN Value END),0) imp,
      ROUND(SUM(CASE WHEN Type='Export' THEN Value END),0) exp
      FROM output_production WHERE Scenario=? AND Year=? AND Fuel='Gas_Natural' GROUP BY 1 ORDER BY 1""", [S, y])
    for r in rows:
        print(f'  {r[0]:12s} R_Gas {r[1] or 0:6.0f}  Zimp {r[2] or 0:5.0f}  use_power {r[3] or 0:6.0f}  use_export {r[4] or 0:6.0f}  trade_in {r[5] or 0:6.0f}  trade_out {r[6] or 0:6.0f}')
    tot = q("SELECT ROUND(SUM(CASE WHEN Type='Production' AND Technology='R_Gas' THEN Value END)), ROUND(SUM(CASE WHEN Type='Use' AND Technology LIKE 'P_Gas%' THEN Value END)) FROM output_production WHERE Scenario=? AND Year=? AND Fuel='Gas_Natural'", [S, y])[0]
    print(f'  TOTAL R_Gas {tot[0]:.0f} PJ ({tot[0]/399.4:.1f} Bcf/d) | power burn {tot[1]:.0f} PJ ({tot[1]/399.4:.1f} Bcf/d)  [EIA 2024: production 105, power burn 36.9 Bcf/d]')

# --- corridor flows 2040 (top) and capacity expansion
print('\n--- top gas corridor flows 2040 (PJ) and capacity 2025->2040 (PJ/yr)')
fl = q("""SELECT t.Region, t.Region2, ROUND(SUM(t.Value),0) FROM output_trade t WHERE t.Scenario=? AND t.Fuel='Gas_Natural' AND t.Year=2040 AND t.Type='Export' GROUP BY 1,2 ORDER BY 3 DESC LIMIT 12""", [S])
cap = {(r[0], r[1], r[2]): r[3] for r in q("SELECT Region, Region2, Year, ROUND(SUM(Value),0) FROM output_trade WHERE Scenario=? AND Fuel='Gas_Natural' AND Type LIKE '%Capacity%' AND Year IN (2025,2040) GROUP BY 1,2,3", [S])}
for a, b, v in fl:
    print(f'  {a:>11s} -> {b:<11s} flow {v:6.0f}   cap {cap.get((a,b,2025),0):6.0f} -> {cap.get((a,b,2040),0):6.0f}')

# --- corridor flows 2025 vs EIA 2024 inter-regional movements (state-level ISO mapping; Bcf/d)
import os, csv
GR = 'C:/Users/testbed/Documents/GENeSYS-MOD.data_francesca/NA_inputs/gas_research'
try:
    eia = {(r['RF'], r['RT']): float(r['bcfd']) for r in csv.DictReader(open(os.path.join(GR, 'eia_interregional_flows_2024.csv')))}
    mod = {(r[0], r[1]): r[2] / 399.4 for r in q("SELECT Region, Region2, SUM(Value) FROM output_trade WHERE Scenario=? AND Fuel='Gas_Natural' AND Year=2025 AND Type='Export' GROUP BY 1,2", [S])}
    print('\n--- corridor flows 2025 model vs EIA 2024 (Bcf/d, gross per direction; EIA state->ISO mapping is coarse for TX/NM/AR/IL/KY/MS/MO)')
    print(f'  {"corridor":24s} {"model":>7s} {"EIA":>7s}')
    for k in sorted(set(eia) | {k for k, v in mod.items() if v > 0.05}, key=lambda k: -eia.get(k, 0)):
        print(f'  {k[0]:>11s} -> {k[1]:<10s} {mod.get(k, 0):7.2f} {eia.get(k, 0):7.2f}')
    for grp, pairs in {'ERCOT+SPP -> MISO': [('ERCOT','MISO'),('SPP','MISO')], 'MISO+PJM -> SERC': [('MISO','SERC'),('PJM','SERC')], 'WECC -> California': [('WECC','California')], 'PJM -> NewYork': [('PJM','NewYork')]}.items():
        print(f'  {grp:24s} {sum(mod.get(k,0) for k in pairs):7.2f} {sum(eia.get(k,0) for k in pairs):7.2f}')
    bor = {(r['region'], r['type']): float(r['bcfd']) for r in csv.DictReader(open(os.path.join(GR, 'eia_border_flows_2024.csv')))}
    print('  Canada border 2025 model (import from / export to Canada) vs EIA 2024:')
    for reg in ('WECC', 'MISO', 'SPP', 'NewYork', 'NewEngland'):
        print(f'    {reg:11s} imp {mod.get(("Canada", reg), 0):5.2f} / {bor.get((reg, "import_Canada"), 0):5.2f}   exp {mod.get((reg, "Canada"), 0):5.2f} / {bor.get((reg, "export_Canada"), 0):5.2f}')
except Exception as e:
    print('EIA corridor benchmark skipped:', str(e)[:200])

# --- storage
st = q("SELECT Region, Year, ROUND(SUM(Value),1) FROM output_capacity WHERE Scenario=? AND Technology='D_Gas_Methane' AND Type='TotalCapacity' AND Year IN (2025,2040) GROUP BY 1,2 ORDER BY 1,2", [S])
print('\n--- D_Gas_Methane capacity (GW-th) 2025/2040:', {(r[0], r[1]): r[2] for r in st})
cyc = q("SELECT Region, ROUND(SUM(Value),0) FROM output_production WHERE Scenario=? AND Technology='D_Gas_Methane' AND Type='Production' AND Year=2040 GROUP BY 1", [S])
print('storage discharge 2040 (PJ):', dict(cyc))

# --- regional gas prices (EB2 duals): the dual of the timeslice balance is the marginal
# value of 1 PJ in that slice in discounted money; undiscount with the run's social
# discount rate (output_switches) to get EUR/GJ (= M EUR/PJ) comparable to Henry Hub.
try:
    import statistics, collections
    sdr = float(q('SELECT "Value" FROM output_switches WHERE Scenario=? AND "Switch"=?', [S, 'socialdiscountrate'])[0][0])
    y0 = int(q("SELECT MIN(Year) FROM output_production WHERE Scenario=?", [S])[0][0])
    rows = q('SELECT "Constraint", "Dual" FROM duals_EB2_EnergyBalanceEachTS WHERE Scenario=? AND "Constraint" LIKE ?', [S, '%|Gas_Natural|%'])
    acc = collections.defaultdict(list)
    for c, d in rows:
        pth = c.split('|')  # EB2_EnergyBalanceEachTS|year|timeslice|fuel|region
        acc[(pth[4], int(pth[1]))].append(d)
    yrs = [y for y in (2025, 2030, 2035, 2040) if any(k[1] == y for k in acc)]
    print(f'\n--- Gas_Natural shadow price, mean over timeslices, undiscounted at {sdr:.3f} (EUR/GJ; HH 2025 ~3.1, base folded path 3.7/4.8/4.8/4.4)')
    print('  ' + ' '.join(f'{y:>7d}' for y in yrs))
    for r in sorted({k[0] for k in acc}):
        print(f'  {r:11s}' + ' '.join(f'{statistics.mean(acc[(r, y)]) * (1 + sdr) ** (y - y0):7.2f}' for y in yrs))
except Exception as e:
    print('duals query failed:', str(e)[:200])

# --- comparison vs reference: gas generation, RES, CO2, cost
def sc(lab):
    g = q("""SELECT ROUND(SUM(CASE WHEN Technology LIKE 'P_Gas%' THEN Value END)/3.6),
             ROUND(SUM(CASE WHEN Technology LIKE 'P_PV%' OR Technology LIKE 'P_Wind%' THEN Value END)/3.6),
             ROUND(SUM(CASE WHEN Technology LIKE 'P_Nuclear%' THEN Value END)/3.6)
             FROM output_production WHERE Scenario=? AND Year=2040 AND Fuel='Power' AND Type='Production'""", [lab])[0]
    em = q("SELECT ROUND(SUM(Value)*1000) FROM output_emission WHERE Scenario=? AND Year=2040", [lab])[0][0]
    c = q("SELECT ROUND(SUM(Value)/1000) FROM raw_TotalDiscountedCost WHERE Scenario=?", [lab])[0][0]
    return g, em, c
for lab in (B, S):
    g, em, c = sc(lab)
    print(f'\n{lab:32s} 2040: gas {g[0]} TWh | RES {g[1]} | nuclear {g[2]} | CO2 {em} Mt | cost {c} bEUR')
