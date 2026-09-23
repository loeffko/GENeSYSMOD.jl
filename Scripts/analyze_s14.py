# -*- coding: utf-8 -*-
"""Summary of the 14 SE scenario runs against the v6c base: INF gate, demand, generation mix,
capacity, CO2, objective, plus scenario-specific KPIs. Writes Results/s14_summary.csv and prints a table.
Usage: python Scripts/analyze_s14.py [ref_scenario] [wave: 1|2]"""
import sys, duckdb, csv
sys.stdout.reconfigure(encoding='utf-8')
B = sys.argv[1] if len(sys.argv) > 1 else 'fel2026_base_49_2015_v6c'
con = duckdb.connect(r'C:\Users\testbed\Documents\GENeSYSMOD.jl_SE\Results\genesysmod_db.duckdb', read_only=True)
q = lambda s, p=(): con.execute(s, list(p)).fetchall()
SCEN = ['s01_ev', 's02_h2', 's03_compute', 's04_space', 's05_brakes', 's06_hormuz', 's07_tech', 's08_canada',
        's09_water', 's10_climate', 's11_feoc', 's12_overbuild', 's13_reindustrial', 's14_decarb']
have = {r[0] for r in q("SELECT DISTINCT Scenario FROM output_production")}
# prefer the latest _vN rerun of a scenario when present
WAVE = sys.argv[2] if len(sys.argv) > 2 else None   # '1' = first labels, '2' = _v2 (s14 _v4), default = latest
def latest(s):
    base = f'fel2026_{s}_49_2015_v6'
    if WAVE == '1':
        return base if s != 's14_decarb' else base + '_v3'
    if WAVE == '2':
        return base + ('_v4' if s == 's14_decarb' else '_v2')
    cands = sorted([h for h in have if h.startswith(base)], key=lambda h: (len(h), h))
    return cands[-1] if cands else base
labels = [latest(s) for s in SCEN]
GRP = """CASE WHEN Technology LIKE 'P_Gas%' THEN 'Gas' WHEN Technology LIKE 'P_Coal%' OR Technology LIKE 'P_Lignite%' THEN 'Coal'
 WHEN Technology LIKE 'P_Nuclear%' THEN 'Nuclear' WHEN Technology='P_Fusion' THEN 'Fusion' WHEN Technology LIKE 'P_PV%' THEN 'Solar'
 WHEN Technology LIKE 'P_Wind%' THEN 'Wind' WHEN Technology LIKE 'P_Hydro%' THEN 'Hydro' WHEN Technology LIKE 'P_Bio%' THEN 'Biomass'
 WHEN Technology LIKE 'P_EGS%' OR Technology='P_Geothermal' THEN 'Geothermal' ELSE 'Other' END"""

def kpis(lab):
    d = {}
    import re, os, glob
    d['status'] = '?'
    key = lab.replace('fel2026_', '').split('_49_')[0]
    suffix = lab.split('_49_2015_v6')[-1]
    logs = [f'Results/_s14_run_{key.split("_")[0]}{suffix}.log', f'Results/_s14_run_{key.split("_")[0]}.log'] if 'base' not in lab else [f'Results/_s14_run_base_{lab.rsplit("_", 1)[-1]}.log', 'Results/_na_base_v6c.log']
    for lg in logs:
        if os.path.exists(lg):
            m = re.findall(r'post-optimize: status=([A-Z_]+)', open(lg, encoding='utf-8', errors='ignore').read())
            if m:
                d['status'] = m[-1]; break
    d['inf_twh'] = (q("SELECT COALESCE(SUM(Value),0)/3.6 FROM output_production WHERE Scenario=? AND Technology LIKE 'Infeasibility%' AND Type='Production'", [lab])[0][0])
    d['cost'] = q("SELECT SUM(Value)/1000 FROM raw_TotalDiscountedCost WHERE Scenario=?", [lab])[0][0]
    for y in (2030, 2040):
        d[f'dem_{y}'] = q("SELECT SUM(\"Value\")/3.6 FROM input_SpecifiedAnnualDemand WHERE Scenario=? AND Year=? AND Fuel LIKE 'Power_%'", [lab, y])[0][0]
        g = dict(q(f"SELECT {GRP}, SUM(Value)/3.6 FROM output_production WHERE Scenario=? AND Year=? AND Fuel='Power' AND Type='Production' AND Technology LIKE 'P_%' GROUP BY 1", [lab, y]))
        for k in ('Gas', 'Coal', 'Nuclear', 'Fusion', 'Solar', 'Wind', 'Geothermal'):
            d[f'gen_{k}_{y}'] = g.get(k, 0.0)
        c = dict(q(f"SELECT {GRP}, SUM(Value) FROM output_capacity WHERE Scenario=? AND Year=? AND Type='TotalCapacity' AND Technology LIKE 'P_%' GROUP BY 1", [lab, y]))
        for k in ('Gas', 'Nuclear', 'Fusion', 'Solar', 'Wind'):
            d[f'cap_{k}_{y}'] = c.get(k, 0.0)
        d[f'cap_storage_{y}'] = q("SELECT COALESCE(SUM(Value),0) FROM output_capacity WHERE Scenario=? AND Year=? AND Type='TotalCapacity' AND Technology LIKE 'D_%'", [lab, y])[0][0]
        d[f'cap_ironair_{y}'] = q("SELECT COALESCE(SUM(Value),0) FROM output_capacity WHERE Scenario=? AND Year=? AND Type='TotalCapacity' AND Technology='D_IronAir'", [lab, y])[0][0]
        d[f'cap_ccs_{y}'] = q("SELECT COALESCE(SUM(Value),0) FROM output_capacity WHERE Scenario=? AND Year=? AND Type='TotalCapacity' AND Technology='P_Gas_CCS'", [lab, y])[0][0]
        d[f'co2_{y}'] = q("SELECT COALESCE(SUM(Value),0)*1000 FROM output_emission WHERE Scenario=? AND Year=? AND Emission='CO2' AND Type IN ('Emissions','ExogenousEmissions')", [lab, y])[0][0]
    d['gas_new_2026_40'] = q("SELECT COALESCE(SUM(Value),0) FROM output_capacity WHERE Scenario=? AND Type='NewCapacity' AND Technology LIKE 'P_Gas%' AND Year BETWEEN 2026 AND 2040", [lab])[0][0]
    # reviewer KPIs: implied fleet CF of solar / wind in 2040 (curtailment proxy), demand served 2025-40, CO2 payments (discounted, bEUR)
    for k, pat in (('solar', 'P_PV%'), ('wind', 'P_Wind%')):
        g = q(f"SELECT COALESCE(SUM(Value),0)/3.6 FROM output_production WHERE Scenario=? AND Year=2040 AND Fuel='Power' AND Type='Production' AND Technology LIKE '{pat}'", [lab])[0][0]
        c = q(f"SELECT COALESCE(SUM(Value),0) FROM output_capacity WHERE Scenario=? AND Year=2040 AND Type='TotalCapacity' AND Technology LIKE '{pat}'", [lab])[0][0]
        d[f'cf_{k}_2040'] = g / (c * 8.76) if c else 0.0
    d['dem_total_2025_40'] = q("SELECT SUM(\"Value\")/3.6 FROM input_SpecifiedAnnualDemand WHERE Scenario=? AND Fuel LIKE 'Power_%'", [lab])[0][0]
    d['co2_payments'] = q("""SELECT COALESCE(SUM(e.v * p."Value" / POWER(1.05, e.Year - 2025 + 0.5)), 0) / 1000 FROM
        (SELECT Region, Year, SUM(Value) v FROM output_emission WHERE Scenario=? AND Emission='CO2' AND Type='Emissions' GROUP BY 1,2) e
        JOIN (SELECT Region, Year, "Value" FROM input_EmissionsPenalty WHERE Scenario=? AND Emission='CO2') p USING (Region, Year)""", [lab, lab])[0][0]
    d['trade_2040'] = q("SELECT COALESCE(SUM(Value),0)/3.6 FROM output_trade WHERE Scenario=? AND Fuel='Power' AND Type='Export' AND Year=2040", [lab])[0][0]
    return d

base = kpis(B)
rows = []
print(f'{"scenario":34s} {"status":14s} {"INF":>6s} {"dem40":>7s} {"dGas40":>7s} {"dSol40":>7s} {"dWind40":>8s} {"dNuc40":>7s} {"Fus40":>6s} {"dGasGW":>7s} {"dStoGW":>7s} {"IronAir":>7s} {"CCS":>5s} {"dCO2_40":>8s} {"dCost":>7s}')
print(f'{B:34s} {base["status"]:14s} {base["inf_twh"]:6.1f} {base["dem_2040"]:7.0f} {base["gen_Gas_2040"]:7.0f} {base["gen_Solar_2040"]:7.0f} {base["gen_Wind_2040"]:8.0f} {base["gen_Nuclear_2040"]:7.0f} {base["gen_Fusion_2040"]:6.0f} {base["cap_Gas_2040"]:7.0f} {base["cap_storage_2040"]:7.0f} {base["cap_ironair_2040"]:7.0f} {base["cap_ccs_2040"]:5.0f} {base["co2_2040"]:8.0f} {base["cost"]:7.0f}   (absolute: TWh, GW, Mt, bEUR) | CF sol/wind {base["cf_solar_2040"]:.2f}/{base["cf_wind_2040"]:.2f}')
for s, lab in zip(SCEN, labels):
    if lab not in have:
        print(f'{lab:34s} (not run yet)'); continue
    d = kpis(lab)
    row = {'scenario': lab, **d}; rows.append(row)
    ddem = d['dem_total_2025_40'] - base['dem_total_2025_40']
    per_mwh = (d['cost'] - base['cost']) * 1e3 / ddem if abs(ddem) > 50 else float('nan')   # EUR/MWh of demand change (undiscounted TWh)
    print(f'{lab:34s} {d["status"]:14s} {d["inf_twh"]:6.1f} {d["dem_2040"]:7.0f} {d["gen_Gas_2040"]-base["gen_Gas_2040"]:+7.0f} {d["gen_Solar_2040"]-base["gen_Solar_2040"]:+7.0f} {d["gen_Wind_2040"]-base["gen_Wind_2040"]:+8.0f} {d["gen_Nuclear_2040"]-base["gen_Nuclear_2040"]:+7.0f} {d["gen_Fusion_2040"]:6.0f} {d["cap_Gas_2040"]-base["cap_Gas_2040"]:+7.0f} {d["cap_storage_2040"]-base["cap_storage_2040"]:+7.0f} {d["cap_ironair_2040"]:7.0f} {d["cap_ccs_2040"]:5.0f} {d["co2_2040"]-base["co2_2040"]:+8.0f} {d["cost"]-base["cost"]:+7.0f}  | CF sol/wind {d["cf_solar_2040"]:.2f}/{d["cf_wind_2040"]:.2f}  cost/MWh dDem {per_mwh:6.1f}  CO2 pay {d["co2_payments"]:5.0f}')
if rows:
    with open(r'C:\Users\testbed\Documents\GENeSYSMOD.jl_SE\Results\s14_summary.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['scenario'] + [k for k in base]); w.writeheader(); w.writerow({'scenario': B, **base}); w.writerows(rows)
    print('\nwritten Results/s14_summary.csv')
