# -*- coding: utf-8 -*-
"""Tab 3 data: stress-week dispatch (PJM, New York; FEL26 Base fleet under Air temp increase and Extreme),
pool-level steam-cycle fleet and derate statistics, and the ISO pool polygons (GENeSYSMOD.tools geodata).
Writes deep_dive.json next to this script."""
import duckdb, pandas as pd, json, os

SP = os.path.dirname(os.path.abspath(__file__))
CODE = 'C:/Users/testbed/Documents/GENeSYSMOD.jl_SE'
DATA = 'C:/Users/testbed/Documents/GENeSYS-MOD.data_francesca'
G = 'C:/Users/testbed/Documents/GENeSYSMOD.tools_SE/GIS_&_Timeseries_Tool/geodata/'
dcon = duckdb.connect(f'{CODE}/Results/genesysmod_dispatch_results.duckdb', read_only=True)
con = duckdb.connect(f'{CODE}/Results/genesysmod_db.duckdb', read_only=True)


def grp(t):
    for k, v in [('Gas_CCGT', 'Gas CCGT'), ('Gas_Steam', 'Gas steam'), ('Gas_OCGT', 'Gas OCGT'), ('Gas_Engines', 'Gas OCGT'), ('Coal', 'Coal'),
                 ('Nuclear', 'Nuclear'), ('PV', 'Solar'), ('Wind', 'Wind'), ('Hydro', 'Hydro'), ('Biomass', 'Biomass'), ('Battery', 'Storage'),
                 ('Redox', 'Storage'), ('CAES', 'Storage'), ('PHS', 'Storage'), ('Geo', 'Geothermal'), ('EGS', 'Geothermal')]:
        if k in str(t):
            return v
    return 'Other'


STEAM = ['P_Nuclear', 'P_Nuclear_SMR', 'P_Coal_Hardcoal', 'P_Coal_Lignite', 'P_Biomass', 'P_Gas_Steam', 'P_Oil',
         'CHP_Biomass_Solid', 'CHP_Coal_Hardcoal', 'CHP_Oil', 'CHP_WasteToEnergy']
US = ['California', 'ERCOT', 'MISO', 'NewEngland', 'NewYork', 'PJM', 'SERC', 'SPP', 'WECC']
cfS = {s: pd.read_csv(f'{DATA}/Data/Timeseries/TS_CF_THERMAL_STEAM_2030/NorthAmerica_climate_{s}/TS_CF_THERMAL_STEAM_2030.csv', header=1)
       for s in ('severe', 'extreme')}
cfC = pd.read_csv(f'{DATA}/Data/Timeseries/TS_CF_THERMAL_CCGT_2030/NorthAmerica_climate_extreme/TS_CF_THERMAL_CCGT_2030.csv', header=1)
out = {'week': {}, 'pools': {}}
for Y in [2030, 2035, 2040]:
    for reg in ['PJM', 'NewYork']:
        b = dcon.execute("select Hour, Unserved from dispatch_balance where Scenario='fel2026_v6f_climate_extreme_dispatch_v1' and Region=? and Year=? order by Hour", [reg, Y]).df()
        if b.Unserved.max() <= 0:
            continue
        h0 = int(b.loc[b.Unserved.idxmax(), 'Hour'])
        start = max(1, min(8760 - 167, h0 - 84))
        hrs = list(range(start, start + 168))
        rec = {'start_hour': start, 'peak_hour': h0}
        for sc, lab in (('fel2026_v6f_climate_extreme_dispatch_v1', 'extreme'), ('fel2026_v6f_climate_base_dispatch_v1', 'airtemp')):
            g = dcon.execute("select Hour, Technology, Value from dispatch_generation where Scenario=? and Region=? and Year=? and Hour between ? and ?", [sc, reg, Y, start, start + 167]).df()
            g['g'] = g.Technology.map(grp)
            p = g.pivot_table(index='Hour', columns='g', values='Value', aggfunc='sum').reindex(hrs).fillna(0)
            s = dcon.execute("select Hour, sum(Discharge)-sum(Charge) as net from dispatch_storage where Scenario=? and Region=? and Year=? and Hour between ? and ? group by 1", [sc, reg, Y, start, start + 167]).df().set_index('Hour').reindex(hrs).fillna(0)
            bb = dcon.execute("select Hour, Unserved, Demand, NetImport from dispatch_balance where Scenario=? and Region=? and Year=? and Hour between ? and ? order by Hour", [sc, reg, Y, start, start + 167]).df().set_index('Hour').reindex(hrs).fillna(0)
            rec[lab] = {'gen': {c: [round(float(v), 2) for v in p[c]] for c in p.columns}, 'storage_net': [round(float(v), 2) for v in s['net']],
                        'import': [round(float(v), 2) for v in bb.NetImport], 'demand': [round(float(v), 2) for v in bb.Demand], 'unserved': [round(float(v), 2) for v in bb.Unserved]}
        rec['cf_steam'] = [round(float(v), 3) for v in cfS['extreme'][reg].values[start - 1:start + 167]]
        rec['cf_ccgt'] = [round(float(v), 3) for v in cfC[reg].values[start - 1:start + 167]]
        out['week'][f'{reg}|{Y}'] = rec
cap = con.execute("select Region, Technology, Year, Value from output_capacity where Scenario='fel2026_base_49_2015_v6f' and Type='TotalCapacity' and Year in (2030,2035,2040)").df()
for Y in [2030, 2035, 2040]:
    out['pools'][str(Y)] = {}
    for r in US + ['Canada']:
        c = cap[(cap.Region == r) & (cap.Year == Y)]
        d = {'steam_GW': round(float(c[c.Technology.isin(STEAM)].Value.sum()), 1), 'nuclear_GW': round(float(c[c.Technology.str.startswith('P_Nuclear')].Value.sum()), 1),
             'coal_GW': round(float(c[c.Technology.str.contains('Coal')].Value.sum()), 1), 'gas_GW': round(float(c[c.Technology.str.contains('Gas')].Value.sum()), 1)}
        for sens in ['severe', 'extreme']:
            cf = cfS[sens]
            d[f'{sens}_min'] = round(float(cf[r].min()), 3) if r in cf.columns else 1.0
            d[f'{sens}_summer_mean'] = round(float(cf[r].values[3621:6478].mean()), 3) if r in cf.columns else 1.0
            u = dcon.execute("select sum(Unserved), sum(case when Unserved>0.5 then 1 else 0 end) from dispatch_balance where Scenario=? and Region=? and Year=?", [f'fel2026_v6f_climate_{sens}_dispatch_v1', r, Y]).fetchone()
            d[f'{sens}_unserved_GWh'] = round(float(u[0] or 0), 1)
            d[f'{sens}_hours'] = int(u[1] or 0)
        out['pools'][str(Y)][r] = d


def rnd(c):
    return [round(c[0], 2), round(c[1], 2)] if isinstance(c[0], (int, float)) else [rnd(x) for x in c]


feats = []
for f in json.load(open(G + 'iso_regions.geojson'))['features'] + json.load(open(G + 'iso_regions_canada_south55.geojson'))['features']:
    feats.append({'region': f['properties'].get('region') or f['properties'].get('name') or 'Canada', 'type': f['geometry']['type'], 'coords': rnd(f['geometry']['coordinates'])})
out['geo'] = feats
json.dump(out, open(f'{SP}/deep_dive.json', 'w'), separators=(',', ':'))
print('deep_dive.json written')
