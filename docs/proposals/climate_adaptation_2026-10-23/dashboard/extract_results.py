# -*- coding: utf-8 -*-
"""Extract the climate-adaptation dashboard data from the results DBs and the data repo into climate_dash.json."""
import duckdb, pandas as pd, numpy as np, json, os
SP = os.path.dirname(os.path.abspath(__file__))
CODE = 'C:/Users/testbed/Documents/GENeSYSMOD.jl_SE'; DATA = 'C:/Users/testbed/Documents/GENeSYS-MOD.data_francesca'
con = duckdb.connect(f'{CODE}/Results/genesysmod_db.duckdb', read_only=True)
dcon = duckdb.connect(f'{CODE}/Results/genesysmod_dispatch_results.duckdb', read_only=True)
INV = {'v6f': 'fel2026_base_49_2015_v6f', 'base': 'fel2026_climate_base_49_2015_v1', 'central': 'fel2026_climate_central_49_2015_v1',
       'extreme': 'fel2026_climate_extreme_49_2015_v1', 'severe': 'fel2026_climate_severe_49_2015_v1',
       'base_nf': 'fel2026_climate_base_nofossil_49_2015_v1', 'extreme_nf': 'fel2026_climate_extreme_nofossil_49_2015_v1', 'severe_nf': 'fel2026_climate_severe_nofossil_49_2015_v1'}
DISP = {'v6f_base': 'fel2026_v6f_climate_base_dispatch_v1', 'v6f_central': 'fel2026_v6f_climate_central_dispatch_v1', 'v6f_extreme': 'fel2026_v6f_climate_extreme_dispatch_v1', 'v6f_severe': 'fel2026_v6f_climate_severe_dispatch_v1',
        'cb_base': 'fel2026_climate_base_dispatch_v1', 'cb_central': 'fel2026_climate_central_dispatch_v1', 'cb_extreme': 'fel2026_climate_extreme_dispatch_v1', 'cb_severe': 'fel2026_climate_severe_dispatch_v1'}
POOLS = ['California', 'WECC', 'SPP', 'MISO', 'ERCOT', 'SERC', 'PJM', 'NewYork', 'NewEngland', 'Canada']
US = ['California', 'ERCOT', 'MISO', 'NewEngland', 'NewYork', 'PJM', 'SERC', 'SPP', 'WECC']
YEARS = [2030, 2035, 2040]
GROUPS = ['Nuclear', 'Coal', 'Gas CCGT', 'Gas OCGT', 'Hydro', 'Biomass', 'Geothermal', 'Wind', 'Solar', 'Li-ion', 'LDES']
def grp(t):
    t = str(t)
    for k, v in [('Gas_CCGT', 'Gas CCGT'), ('Gas_OCGT', 'Gas OCGT'), ('Gas_Engines', 'Gas OCGT'), ('Gas_Steam', 'Gas CCGT'), ('Gas_CCS', 'Gas CCGT'), ('Coal', 'Coal'), ('Lignite', 'Coal'), ('Nuclear', 'Nuclear'), ('PV', 'Solar'), ('Wind', 'Wind'), ('Hydro', 'Hydro'),
                 ('Biomass', 'Biomass'), ('WasteToEnergy', 'Biomass'), ('Battery_Li', 'Li-ion'), ('Redox', 'LDES'), ('CAES', 'LDES'), ('PHS', 'LDES'), ('Geothermal', 'Geothermal'), ('EGS', 'Geothermal'), ('Infeasibility', 'INF'), ('Oil', 'Coal')]:
        if k in t: return v
    return None
out = {}
# ---------- investment: capacity + generation by group, objective, slack
inv = {}
for k, s in INV.items():
    cap = con.execute("select Technology, Year, sum(Value) v from output_capacity where Scenario=? and Type='TotalCapacity' group by 1,2", [s]).df(); cap['g'] = cap.Technology.map(grp)
    gen = con.execute("select Technology, Year, sum(Value) v from output_annual_production where Scenario=? and Fuel='Power' group by 1,2", [s]).df(); gen['g'] = gen.Technology.map(grp)
    obj = con.execute("select Value from output_model where Scenario=? and lower(Type) like '%objective%' limit 1", [s]).fetchone()[0]
    slack = con.execute("select Region, Year, round(sum(Value),2) from output_annual_production where Scenario=? and Technology like 'Infeasibility%' group by 1,2", [s]).fetchall()
    tr = con.execute("select Year, round(sum(Value),1) from output_trade where Scenario=? and Type='Transmissions Capacity' and Fuel='Power' group by 1", [s]).fetchall()
    inv[k] = {'objective_bEUR': round(obj / 1000, 1), 'slack_PJ_total': round(sum(v for _, _, v in slack), 1),
              'slack': [{'region': r, 'year': int(y), 'PJ': v} for r, y, v in slack if v > 0.05],
              'cap': {str(y): {g: round(float(cap[(cap.Year == y) & (cap.g == g)].v.sum()), 1) for g in GROUPS} for y in YEARS},
              'gen': {str(y): {g: round(float(gen[(gen.Year == y) & (gen.g == g)].v.sum() / 3.6), 1) for g in GROUPS + ['INF']} for y in YEARS},
              'trade_GW': {str(y): v for y, v in tr}}
out['inv'] = inv
# ceiling utilisation extreme_nf and extreme (tech x pool, per year)
util = {}
for k in ['extreme', 'extreme_nf']:
    s = INV[k]
    cap = con.execute("select Region, Technology, Type, Year, Value from output_capacity where Scenario=? and Type in ('TotalCapacity','TotalAnnualMaxCapacity') and Year in (2030,2035,2040)", [s]).df()
    p = cap.pivot_table(index=['Region', 'Technology', 'Year'], columns='Type', values='Value').fillna(0).reset_index()
    p = p[p.TotalAnnualMaxCapacity.between(0.0011, 9e5)]
    techs = {'P_PV_Utility_Opt': 'PV best class', 'P_PV_Utility_Avg': 'PV average class', 'P_Wind_Onshore_Opt': 'Wind best class', 'P_Wind_Onshore_Avg': 'Wind average class', 'D_Battery_Li-Ion': 'Li-ion battery', 'D_Battery_Redox': 'Redox flow (8 h)', 'D_CAES': 'CAES', 'D_PHS': 'Pumped hydro', 'P_Nuclear': 'Nuclear', 'P_Gas_CCGT': 'Gas CCGT', 'P_Gas_OCGT': 'Gas OCGT', 'P_Geothermal': 'Geothermal'}
    util[k] = {str(y): {techs[t]: {r: round(float(min(1.0, row.TotalCapacity / row.TotalAnnualMaxCapacity)), 3) for r in US for row in [p[(p.Region == r) & (p.Technology == t) & (p.Year == y)]] if len(row) for row in [row.iloc[0]]} for t in techs} for y in YEARS}
out['util'] = util
# ---------- dispatch: unserved by pool x year, scarcity hours, hourly heatmaps
disp = {}
for k, s in DISP.items():
    u = dcon.execute("select Region, Year, round(sum(Unserved),1), sum(case when Unserved>0.5 then 1 else 0 end) from dispatch_balance where Scenario=? group by 1,2", [s]).fetchall()
    summ = dcon.execute("select Year, round(Unserved_GWh,0), round(Curtailment_GWh,0), MaxPrice_EURMWh from dispatch_summary where Scenario=? order by Year", [s]).fetchall()
    disp[k] = {'unserved': [{'region': r, 'year': int(y), 'GWh': v, 'hours': int(h)} for r, y, v, h in u if v > 0],
               'summary': {str(y): {'unserved_GWh': uu, 'curtail_GWh': c, 'max_price': mp} for y, uu, c, mp in summ}}
out['disp'] = disp
# hourly heatmaps (day x hour, unserved MW) for PJM and NewYork, v6f fleet extreme/severe + cb extreme, years 2030/35/40
hm = {}
for k in ['v6f_extreme', 'v6f_severe', 'cb_extreme']:
    for reg in ['PJM', 'NewYork']:
        for y in YEARS:
            rows = dcon.execute("select Hour, Unserved from dispatch_balance where Scenario=? and Region=? and Year=? order by Hour", [DISP[k], reg, y]).fetchall()
            if not rows or sum(v for _, v in rows) < 0.5: continue
            arr = np.zeros(8760)
            for h, v in rows:
                if 1 <= h <= 8760: arr[int(h) - 1] = v
            m = arr.reshape(365, 24)  # GWh per hour = GW
            hm[f'{k}|{reg}|{y}'] = {'daymax': [round(float(x), 2) for x in m.max(axis=1)], 'grid': [[round(float(v), 2) for v in row] for row in m if row.max() > 0], 'days': [int(i) for i, row in enumerate(m) if row.max() > 0], 'total_GWh': round(float(arr.sum()), 0), 'peak_GW': round(float(arr.max()), 2)}
out['hourly'] = hm
# dispatch generation shift by group (v6f fleet) per year
dg = dcon.execute("select Scenario, Year, Technology, Generation_GWh from dispatch_gen_annual where Scenario like 'fel2026_%'").df(); dg['g'] = dg.Technology.map(grp)
inv_d = {v: k for k, v in DISP.items()}
out['disp_gen'] = {inv_d[s]: {str(y): {g: round(float(dg[(dg.Scenario == s) & (dg.Year == y) & (dg.g == g)].Generation_GWh.sum() / 1000), 1) for g in GROUPS} for y in YEARS} for s in dg.Scenario.unique() if s in inv_d}
# ---------- thermal derate heatmap: region x week mean CF per class and sensitivity (weeks 20-40)
der = {}
for sens in ['central', 'extreme', 'severe']:
    der[sens] = {}
    for g in ['STEAM', 'CCGT', 'OCGT']:
        df = pd.read_csv(f'{DATA}/Data/Timeseries/TS_CF_THERMAL_{g}_2030/NorthAmerica_climate_{sens}/TS_CF_THERMAL_{g}_2030.csv', header=1)
        der[sens][g] = {r: [round(float(df[r].values[w * 168:(w + 1) * 168].mean()), 3) for w in range(52)] for r in US}
        der[sens][g + '_min'] = {r: round(float(df[r].min()), 3) for r in US}
out['derate'] = der
# ---------- demand / profile material from the previous page
prev = json.load(open(f'{SP}/cooling_viz.json'))
out['weekly'] = prev['weekly']; out['pools'] = prev['pools']; out['peak'] = prev['peak']
json.dump(out, open(f'{SP}/climate_dash.json', 'w'), separators=(',', ':'))
print('written', os.path.getsize(f'{SP}/climate_dash.json') // 1024, 'KB; hourly heatmaps:', list(hm))
print({k: (v['objective_bEUR'], v['slack_PJ_total'], v['trade_GW']) for k, v in inv.items()})
print({k: v['summary'] for k, v in disp.items() if 'v6f' in k})
