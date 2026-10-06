# -*- coding: utf-8 -*-
"""Canada scenario set (plan docs/proposals/CA_scenario_plan_2026-10-04.xlsx): gate and summary for the Canada node
against the frozen base fel2026_base_49_2015_v6f.

Usage: python Scripts/analyze_canada.py            table of all Canada runs present + Results/ca_summary.csv
       python Scripts/analyze_canada.py gate c07b  one run: solver status, infeasibility-slack generation, key deltas
"""
import sys, os, re, csv, glob, duckdb
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BASE = 'fel2026_base_49_2015_v6f'
CA = 'Canada'
YRS = (2030, 2035, 2040)
con = duckdb.connect(os.path.join(ROOT, 'Results', 'genesysmod_db.duckdb'), read_only=True)
q = lambda s, p=(): con.execute(s, list(p)).fetchall()
one = lambda s, p=(): (q(s, p)[0][0] or 0.0)

# run key -> label, read from the drivers so that the labels are never retyped
LABELS = {}
for f in sorted(glob.glob(os.path.join(ROOT, '_s14', 'run_c[0-9][0-9]*.jl'))):
    m = re.search(r'^label = "([^"]+)"', open(f, encoding='utf-8').read(), re.M)
    if m:
        LABELS[os.path.basename(f)[4:-3]] = m.group(1)

GRP = """CASE WHEN Technology LIKE 'P_Gas%' THEN 'Gas' WHEN Technology LIKE 'P_Coal%' THEN 'Coal'
 WHEN Technology LIKE 'P_Nuclear%' THEN 'Nuclear' WHEN Technology LIKE 'P_PV%' THEN 'Solar'
 WHEN Technology LIKE 'P_Wind_Off%' THEN 'WindOff' WHEN Technology LIKE 'P_Wind%' THEN 'Wind' WHEN Technology LIKE 'P_Hydro%' THEN 'Hydro'
 WHEN Technology LIKE 'P_Bio%' THEN 'Biomass' ELSE 'Other' END"""


def status(key):
    lg = os.path.join(ROOT, 'Results', f'_ca_run_{key}.log')
    if not os.path.exists(lg):
        return '?'
    m = re.findall(r'post-optimize: status=([A-Z_]+)', open(lg, encoding='utf-8', errors='ignore').read())
    return m[-1] if m else 'NO STATUS'


def kpis(lab):
    d = {}
    d['inf_twh'] = one("SELECT SUM(Value)/3.6 FROM output_production WHERE Scenario=? AND Technology LIKE 'Infeasibility%' AND Type='Production'", [lab])
    d['inf_twh_ca'] = one("SELECT SUM(Value)/3.6 FROM output_production WHERE Scenario=? AND Region=? AND Technology LIKE 'Infeasibility%' AND Type='Production'", [lab, CA])
    d['cost'] = one("SELECT SUM(Value)/1000 FROM raw_TotalDiscountedCost WHERE Scenario=?", [lab])
    d['cost_ca'] = one("SELECT SUM(Value)/1000 FROM raw_TotalDiscountedCost WHERE Scenario=? AND Region=?", [lab, CA])
    d['us_gas_new_2026_40'] = one("SELECT SUM(Value) FROM output_capacity WHERE Scenario=? AND Type='NewCapacity' AND Technology LIKE 'P_Gas%' AND Region<>? AND Year BETWEEN 2026 AND 2040", [lab, CA])
    for y in YRS:
        d[f'dem_{y}'] = one("SELECT SUM(\"Value\")/3.6 FROM input_SpecifiedAnnualDemand WHERE Scenario=? AND Region=? AND Year=? AND Fuel LIKE 'Power_%'", [lab, CA, y])
        c = dict(q(f"SELECT {GRP}, SUM(Value) FROM output_capacity WHERE Scenario=? AND Region=? AND Year=? AND Type='TotalCapacity' AND Technology LIKE 'P_%' GROUP BY 1", [lab, CA, y]))
        g = dict(q(f"SELECT {GRP}, SUM(Value)/3.6 FROM output_production WHERE Scenario=? AND Region=? AND Year=? AND Fuel='Power' AND Type='Production' AND Technology LIKE 'P_%' GROUP BY 1", [lab, CA, y]))
        for k in ('Wind', 'WindOff', 'Solar', 'Hydro', 'Nuclear', 'Gas'):
            d[f'cap_{k}_{y}'] = c.get(k, 0.0)
            d[f'gen_{k}_{y}'] = g.get(k, 0.0)
        d[f'cap_total_{y}'] = sum(c.values())
        d[f'cap_ccgt_new_{y}'] = one("SELECT SUM(Value) FROM output_capacity WHERE Scenario=? AND Region=? AND Year=? AND Type='TotalCapacity' AND Technology='P_Gas_CCGT'", [lab, CA, y])
        gen_cc = one("SELECT SUM(Value)/3.6 FROM output_production WHERE Scenario=? AND Region=? AND Year=? AND Fuel='Power' AND Type='Production' AND Technology='P_Gas_CCGT'", [lab, CA, y])
        d[f'cf_ccgt_new_{y}'] = gen_cc / (d[f'cap_ccgt_new_{y}'] * 8.76) if d[f'cap_ccgt_new_{y}'] else 0.0
        d[f'cf_wind_{y}'] = d[f'gen_Wind_{y}'] / (d[f'cap_Wind_{y}'] * 8.76) if d[f'cap_Wind_{y}'] else 0.0
        d[f'cap_smr_{y}'] = one("SELECT SUM(Value) FROM output_capacity WHERE Scenario=? AND Region=? AND Year=? AND Type='TotalCapacity' AND Technology='P_Nuclear_SMR'", [lab, CA, y])
        d[f'cap_battery_{y}'] = one("SELECT SUM(Value) FROM output_capacity WHERE Scenario=? AND Region=? AND Year=? AND Type='TotalCapacity' AND Technology='D_Battery_Li-Ion'", [lab, CA, y])
        ex = one("SELECT SUM(Value)/3.6 FROM output_trade WHERE Scenario=? AND Fuel='Power' AND Type='Export' AND Region=? AND Year=?", [lab, CA, y])
        im = one("SELECT SUM(Value)/3.6 FROM output_trade WHERE Scenario=? AND Fuel='Power' AND Type='Import' AND Region=? AND Year=?", [lab, CA, y])
        d[f'net_export_{y}'] = ex - im
        d[f'co2_{y}'] = one("SELECT SUM(Value)*1000 FROM output_emission WHERE Scenario=? AND Region=? AND Year=? AND Emission='CO2' AND Type='Emissions'", [lab, CA, y])
        d[f'curtail_{y}'] = one("SELECT SUM(Value)/3.6 FROM raw_CurtailedEnergyAnnual WHERE Scenario=? AND Region=? AND Fuel='Power' AND Year=?", [lab, CA, y])
        d[f'us_gas_gen_{y}'] = one("SELECT SUM(Value)/3.6 FROM output_production WHERE Scenario=? AND Region<>? AND Year=? AND Fuel='Power' AND Type='Production' AND Technology LIKE 'P_Gas%'", [lab, CA, y])
    return d


def line(name, d, b=None, y=2040):
    f = (lambda k: d[k]) if b is None else (lambda k: d[k] - b[k])
    s = '' if b is None else '+'
    return (f'{name:38s} INF {d["inf_twh"]:5.1f}  dem{y%100} {d[f"dem_{y}"]:6.0f}  cap: wind {f(f"cap_Wind_{y}"):{s}6.1f} sol {f(f"cap_Solar_{y}"):{s}6.1f} hyd {f(f"cap_Hydro_{y}"):{s}5.1f} '
            f'nuc {f(f"cap_Nuclear_{y}"):{s}5.1f} gas {f(f"cap_Gas_{y}"):{s}5.1f} bat {f(f"cap_battery_{y}"):{s}5.1f} | gen: wind {f(f"gen_Wind_{y}"):{s}6.0f} gas {f(f"gen_Gas_{y}"):{s}5.0f} nuc {f(f"gen_Nuclear_{y}"):{s}5.0f} '
            f'| netexp {f(f"net_export_{y}"):{s}5.0f} CO2 {f(f"co2_{y}"):{s}5.1f} | cost CA {f("cost_ca"):{s}6.1f} all {f("cost"):{s}6.1f} | CF ccgt {d[f"cf_ccgt_new_{y}"]:.2f} wind {d[f"cf_wind_{y}"]:.2f}')


def md(base, runs):
    """Markdown tables for the results write-up: one table per year (deltas vs base, Canada node), one cost / spill-over table."""
    out = []
    cols = [('demand TWh', 'dem_{y}', 0), ('wind GW', 'cap_Wind_{y}', 1), ('solar GW', 'cap_Solar_{y}', 1), ('hydro GW', 'cap_Hydro_{y}', 1), ('nuclear GW', 'cap_Nuclear_{y}', 1),
            ('gas GW', 'cap_Gas_{y}', 1), ('battery GW', 'cap_battery_{y}', 1), ('wind TWh', 'gen_Wind_{y}', 0), ('solar TWh', 'gen_Solar_{y}', 0), ('nuclear TWh', 'gen_Nuclear_{y}', 0),
            ('gas TWh', 'gen_Gas_{y}', 0), ('net export TWh', 'net_export_{y}', 0), ('CO2 Mt', 'co2_{y}', 1)]
    for y in YRS:
        out.append(f'\n**{y}** (Canada node; base absolute, scenarios as change against the base)\n')
        out.append('| run | ' + ' | '.join(c[0] for c in cols) + ' | new-CCGT CF | wind CF |')
        out.append('|---|' + '---:|' * (len(cols) + 2))
        out.append('| base v6f | ' + ' | '.join(f'{base[k.format(y=y)]:.{nd}f}' for _, k, nd in cols) + f' | {base[f"cf_ccgt_new_{y}"]:.2f} | {base[f"cf_wind_{y}"]:.2f} |')
        for key, d in runs:
            out.append(f'| {key} | ' + ' | '.join(f'{d[k.format(y=y)] - base[k.format(y=y)]:+.{nd}f}' for _, k, nd in cols) + f' | {d[f"cf_ccgt_new_{y}"]:.2f} | {d[f"cf_wind_{y}"]:.2f} |')
    out.append('\n**System cost and US spill-over** (discounted 2025-2040, bEUR; generation in TWh, capacity in GW)\n')
    out.append('| run | status | slack TWh | cost Canada | cost US pools | cost total | US gas generation 2040 | US new gas capacity 2026-40 | Canada curtailment 2040 TWh |')
    out.append('|---|---|---:|---:|---:|---:|---:|---:|---:|')
    out.append(f'| base v6f | OPTIMAL | {base["inf_twh"]:.1f} | {base["cost_ca"]:.1f} | {base["cost"] - base["cost_ca"]:.1f} | {base["cost"]:.1f} | {base["us_gas_gen_2040"]:.0f} | {base["us_gas_new_2026_40"]:.1f} | {base["curtail_2040"]:.1f} |')
    for key, d in runs:
        out.append(f'| {key} | {status(key)} | {d["inf_twh"]:.1f} | {d["cost_ca"] - base["cost_ca"]:+.1f} | {(d["cost"] - d["cost_ca"]) - (base["cost"] - base["cost_ca"]):+.1f} | {d["cost"] - base["cost"]:+.1f} | '
                   f'{d["us_gas_gen_2040"] - base["us_gas_gen_2040"]:+.0f} | {d["us_gas_new_2026_40"] - base["us_gas_new_2026_40"]:+.1f} | {d["curtail_2040"] - base["curtail_2040"]:+.1f} |')
    return '\n'.join(out)


if __name__ == '__main__':
    have = {r[0] for r in q("SELECT DISTINCT Scenario FROM output_capacity WHERE Scenario LIKE 'fel2026_c%' OR Scenario=?", [BASE])}
    base = kpis(BASE)
    if len(sys.argv) > 1 and sys.argv[1] == 'md':
        print(md(base, [(key, kpis(lab)) for key, lab in LABELS.items() if lab in have])); sys.exit(0)
    if len(sys.argv) > 2 and sys.argv[1] == 'gate':
        key = sys.argv[2]; lab = LABELS[key]
        if lab not in have:
            print(f'GATE {key} {lab}: NOT IN DATABASE (status {status(key)})'); sys.exit(1)
        d = kpis(lab)
        ok = status(key) == 'OPTIMAL' and d['inf_twh'] < base['inf_twh'] + 6.0
        print(f'GATE {key} {"PASS" if ok else "CHECK"}: status {status(key)} | INF {d["inf_twh"]:.2f} TWh (Canada {d["inf_twh_ca"]:.2f}; base {base["inf_twh"]:.2f})')
        for y in YRS:
            print('   ' + line(f'{y} delta vs base', d, base, y))
        sys.exit(0)
    print('units: TWh, GW, Mt CO2, bEUR (discounted system cost); deltas vs base for the scenario rows; Canada node unless stated')
    for y in YRS:
        print(f'\n--- {y}')
        print(line(BASE + ' (absolute)', base, None, y))
        for key, lab in LABELS.items():
            if lab in have:
                print(line(f'{key} [{status(key)}]', kpis(lab), base, y))
            elif y == YRS[0]:
                print(f'{key:38s} (not run yet)')
    rows = [{'scenario': BASE, 'status': 'OPTIMAL', **base}] + [{'scenario': lab, 'status': status(key), **kpis(lab)} for key, lab in LABELS.items() if lab in have]
    out = os.path.join(ROOT, 'Results', 'ca_summary.csv')
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('\nwritten', out)
