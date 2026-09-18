# -*- coding: utf-8 -*-
"""Regression check of a base rerun against reference scenarios in the results DB.
Usage: python Scripts/compare_base_regression.py <new> <ref_same_code> [<ref_original>]
- input_* tables: exact comparison new vs ref_same_code (both must carry an input dump)
- outputs: generation / capacity / trade / emissions / cost per year vs both references"""
import sys, duckdb, math
sys.stdout.reconfigure(encoding='utf-8')
N = sys.argv[1]; R = sys.argv[2]; O = sys.argv[3] if len(sys.argv) > 3 else None
con = duckdb.connect(r'C:\Users\testbed\Documents\GENeSYSMOD.jl_SE\Results\genesysmod_db.duckdb', read_only=True)
q = lambda s, p=(): con.execute(s, list(p)).fetchall()

# ---------------- 1. input parameters: exact match
tabs = [r[0] for r in q("SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'input_%' ORDER BY 1")]
print(f'=== INPUT DUMP {N} vs {R}: {len(tabs)} tables')
bad = []
for t in tabs:
    cols = [r[0] for r in q(f"SELECT column_name FROM information_schema.columns WHERE table_name='{t}' ORDER BY ordinal_position")]
    if 'Scenario' not in cols: continue
    key = [c for c in cols if c not in ('Scenario', 'Value')]
    hasv = 'Value' in cols
    kq = ', '.join(f'"{c}"' for c in key)
    if hasv:
        r = q(f'''WITH a AS (SELECT {kq}, "Value" v FROM {t} WHERE Scenario=?), b AS (SELECT {kq}, "Value" v FROM {t} WHERE Scenario=?)
            SELECT (SELECT COUNT(*) FROM a), (SELECT COUNT(*) FROM b),
                   (SELECT COUNT(*) FROM a FULL JOIN b USING ({kq}) WHERE a.v IS NULL OR b.v IS NULL OR abs(a.v-b.v) > 1e-9*greatest(abs(a.v),1)),
                   (SELECT COALESCE(MAX(abs(a.v-b.v)),0) FROM a JOIN b USING ({kq}))''', [N, R])[0]
        na, nb, nd, mx = r
    else:
        r = q(f'''WITH a AS (SELECT DISTINCT {kq} FROM {t} WHERE Scenario=?), b AS (SELECT DISTINCT {kq} FROM {t} WHERE Scenario=?)
            SELECT (SELECT COUNT(*) FROM a), (SELECT COUNT(*) FROM b), (SELECT COUNT(*) FROM ((SELECT * FROM a EXCEPT SELECT * FROM b) UNION ALL (SELECT * FROM b EXCEPT SELECT * FROM a)))''', [N, R])[0]
        na, nb, nd = r; mx = 0
    if na == 0 and nb == 0: continue
    if nd or na != nb: bad.append((t, na, nb, nd, mx))
if bad:
    print('DIFFERING INPUT TABLES:')
    for b in bad: print(f'  {b[0]:45s} rows {b[1]}|{b[2]}  differing {b[3]}  max|d| {b[4]:.3g}')
else:
    print('all input tables identical (rows and values).')

# ---------------- 2. outputs
grp = """CASE WHEN Technology LIKE 'P_Gas%' THEN 'Gas' WHEN Technology LIKE 'P_Coal%' OR Technology LIKE 'P_Lignite%' THEN 'Coal'
 WHEN Technology LIKE 'P_Nuclear%' THEN 'Nuclear' WHEN Technology LIKE 'P_PV%' THEN 'Solar' WHEN Technology LIKE 'P_Wind%' THEN 'Wind'
 WHEN Technology LIKE 'P_Hydro%' THEN 'Hydro' WHEN Technology LIKE 'P_Bio%' THEN 'Biomass' WHEN Technology LIKE 'Infeasibility%' THEN 'INF' ELSE 'Other' END"""
def gen(lab):
    return {(y, g): v for y, g, v in q(f"SELECT Year, {grp}, SUM(Value)/3.6 FROM output_production WHERE Scenario=? AND Fuel='Power' AND Type='Production' AND (Technology LIKE 'P_%' OR Technology LIKE 'Infeasibility%') GROUP BY 1,2", [lab])}
def cap(lab):
    return {(y, g): v for y, g, v in q(f"SELECT Year, {grp}, SUM(Value) FROM output_capacity WHERE Scenario=? AND Type='TotalCapacity' AND Technology LIKE 'P_%' GROUP BY 1,2", [lab])}
def stor(lab):
    return {y: v for y, v in q("SELECT Year, SUM(Value) FROM output_capacity WHERE Scenario=? AND Type='TotalCapacity' AND Technology LIKE 'D_%' GROUP BY 1", [lab])}
def trade(lab):
    return {y: v for y, v in q("SELECT Year, SUM(Value)/3.6 FROM output_trade WHERE Scenario=? AND Fuel='Power' AND Type='Export' GROUP BY 1", [lab])}
def em(lab):
    return {y: v * 1000 for y, v in q("SELECT Year, SUM(Value) FROM output_emission WHERE Scenario=? GROUP BY 1", [lab])}
def cost(lab):
    return q("SELECT SUM(Value)/1000 FROM raw_TotalDiscountedCost WHERE Scenario=?", [lab])[0][0]
def report(ref):
    gn, gr = gen(N), gen(ref); cn, cr = cap(N), cap(ref); sn, sr = stor(N), stor(ref); tn, tr = trade(N), trade(ref); en, er = em(N), em(ref)
    print(f'\n=== OUTPUTS {N} vs {ref}')
    print(f'  objective bEUR: {cost(N):.3f} vs {cost(ref):.3f}  ({(cost(N)/cost(ref)-1)*100:+.3f} %)')
    groups = ['Gas', 'Coal', 'Nuclear', 'Solar', 'Wind', 'Hydro', 'Biomass', 'Other', 'INF']
    worst = []
    for y in (2025, 2030, 2035, 2040):
        line = []
        for g in groups:
            a, b = gn.get((y, g), 0), gr.get((y, g), 0)
            d = a - b; line.append(f'{g} {a:.0f}|{b:.0f}')
            if max(abs(a), abs(b)) > 5: worst.append((abs(d) / max(abs(b), 1), y, g, a, b))
        print(f'  gen TWh {y}: ' + '  '.join(line))
    for y in (2025, 2040):
        print(f'  cap GW {y}:  ' + '  '.join(f'{g} {cn.get((y,g),0):.0f}|{cr.get((y,g),0):.0f}' for g in groups[:-1]) + f'  storage {sn.get(y,0):.0f}|{sr.get(y,0):.0f}')
    print('  power trade TWh 2025/2040: ' + ' '.join(f'{tn.get(y,0):.0f}|{tr.get(y,0):.0f}' for y in (2025, 2040)) + f'   CO2 Mt 2025/2040: ' + ' '.join(f'{en.get(y,0):.0f}|{er.get(y,0):.0f}' for y in (2025, 2040)))
    worst.sort(reverse=True)
    print('  largest relative generation deviations (share, year, group, new, ref):')
    for w in worst[:6]: print(f'    {w[0]*100:6.2f} %  {w[1]} {w[2]:8s} {w[3]:8.1f} {w[4]:8.1f}')
    flag = [w for w in worst if w[0] > 0.15]
    print(f'  >15 % deviations: {len(flag)}')
    # per-region-per-year gas/solar/wind check
    rows = q(f"""WITH a AS (SELECT Region, Year, {grp} g, SUM(Value)/3.6 v FROM output_production WHERE Scenario=? AND Fuel='Power' AND Type='Production' AND Technology LIKE 'P_%' GROUP BY 1,2,3),
                      b AS (SELECT Region, Year, {grp} g, SUM(Value)/3.6 v FROM output_production WHERE Scenario=? AND Fuel='Power' AND Type='Production' AND Technology LIKE 'P_%' GROUP BY 1,2,3)
                 SELECT a.Region, a.Year, a.g, a.v, b.v FROM a JOIN b USING (Region, Year, g) WHERE greatest(a.v,b.v) > 10 ORDER BY abs(a.v-b.v)/greatest(b.v,1) DESC LIMIT 5""", [N, ref])
    print('  largest regional deviations (region, year, group, new, ref):')
    for r in rows: print(f'    {r[0]:11s} {r[1]} {r[2]:8s} {r[3]:8.1f} {r[4]:8.1f}  ({(r[3]/max(r[4],1)-1)*100:+.1f} %)')
report(R)
if O: report(O)
