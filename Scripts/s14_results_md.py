# -*- coding: utf-8 -*-
"""Turn Results/s14_summary.csv (written by analyze_s14.py) into the markdown results table used in
docs/proposals/scenario_plan_2026-09-18/RESULTS_wave*.md. Deltas are 2040 vs the reference row (first row).
Usage: python Scripts/s14_results_md.py [Results/s14_summary.csv]"""
import sys, csv
sys.stdout.reconfigure(encoding='utf-8')
path = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\testbed\Documents\GENeSYSMOD.jl_SE\Results\s14_summary.csv'
rows = list(csv.DictReader(open(path, encoding='utf-8')))
base, scen = rows[0], rows[1:]
NAME = {'s01_ev': 'EV comeback', 's02_h2': 'H2 comeback', 's03_compute': 'Age of compute', 's04_space': 'Space race, terrestrial',
        's05_brakes': 'Political brakes', 's06_hormuz': 'Hormuz 6C', 's07_tech': 'Tech breakthrough', 's08_canada': 'Canada DC, pipeline-consistent',
        's09_water': 'Water boom', 's10_climate': 'Climate reshuffle', 's11_feoc': 'FEOC', 's12_overbuild': 'AI overbuild',
        's13_reindustrial': 'Reindustrialization', 's14_decarb': 'Decarbonization'}
f = lambda r, k: float(r.get(k) or 0.0)   # older csvs lack the KPI columns
def d(r, k, fmt='{:+,.0f}'):
    x = f(r, k) - f(base, k)
    return '0' if abs(x) < 0.5 else fmt.format(x)
print('| # | scenario (run) | demand 2040 | gas gen | solar | wind | nuclear | gas GW | storage GW | CO2 | cost (bEUR, 2025-40 disc.) | CF solar/wind 2040 | curtailed 2040 | cost per MWh of extra demand | CO2 payments (bEUR) | resource cost net of transfers (bEUR) |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
print(f'| base | {base["scenario"].split("_")[-1]} | {f(base,"dem_2040"):,.0f} TWh | {f(base,"gen_Gas_2040"):,.0f} | {f(base,"gen_Solar_2040"):,.0f} | {f(base,"gen_Wind_2040"):,.0f} | '
      f'{f(base,"gen_Nuclear_2040"):,.0f} | {f(base,"cap_Gas_2040"):,.0f} | {f(base,"cap_storage_2040"):,.0f} | {f(base,"co2_2040"):,.0f} Mt | {f(base,"cost"):,.0f} | '
      f'{f(base,"cf_solar_2040"):.2f}/{f(base,"cf_wind_2040"):.2f} | {f(base,"curtail_2040"):,.0f} TWh | - | {f(base,"co2_payments"):.0f} | - |')
for r in scen:
    key = r['scenario'].replace('fel2026_', '').split('_49_')[0]
    is_open = key.endswith('_open'); key = key.replace('_open', '')
    n = int(key[1:3]); suffix = ('open' if is_open else '') or r['scenario'].split('_49_2015_v6')[-1].strip('_') or 'v1'
    ddem = f(r, 'dem_total_2025_40') - f(base, 'dem_total_2025_40')
    per_mwh = f'{(f(r,"cost") - f(base,"cost")) * 1e3 / ddem:,.1f} EUR' if abs(ddem) > 50 else '-'
    extra = []
    if f(r, 'gen_Fusion_2040') > 0: extra.append(f'+{f(r,"gen_Fusion_2040"):.0f} fusion')
    nuc = d(r, 'gen_Nuclear_2040') + (f' ({", ".join(extra)})' if extra else '')
    sto = d(r, 'cap_storage_2040') + (f' (+{f(r,"cap_ironair_2040"):.0f} iron-air)' if f(r, 'cap_ironair_2040') > 0 else '')
    gas = d(r, 'cap_Gas_2040') + (f' (+{f(r,"cap_ccs_2040"):.0f} CCS)' if f(r, 'cap_ccs_2040') > 0.5 else '')
    dem = d(r, 'dem_2040') if abs(f(r, 'dem_2040') - f(base, 'dem_2040')) > 0.5 else '0'
    print(f'| {n} | {NAME[key]} ({key}, {suffix}) | {dem} | {d(r,"gen_Gas_2040")} | {d(r,"gen_Solar_2040")} | {d(r,"gen_Wind_2040")} | {nuc} | {gas} | {sto} | '
          f'{d(r,"co2_2040")} | {d(r,"cost")} | {f(r,"cf_solar_2040"):.2f}/{f(r,"cf_wind_2040"):.2f} | {d(r,"curtail_2040")} | {per_mwh} | {f(r,"co2_payments"):.0f} | {f(r,"resource_cost"):+,.0f} |')
