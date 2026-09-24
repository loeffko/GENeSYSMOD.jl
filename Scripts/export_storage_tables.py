# -*- coding: utf-8 -*-
"""Storage capacity tables for the reviewer's export (wave-2 review item 4): D_* power capacity (GW) and
S_* energy capacity (GWh) per scenario, region and year.
Usage: python Scripts/export_storage_tables.py <scenario> [<scenario> ...]
Writes Results/storage_capacity_<tag>.csv (tag = 'wave' if several scenarios, else the scenario label)."""
import sys, csv, duckdb
sys.stdout.reconfigure(encoding='utf-8')
scen = sys.argv[1:]
if not scen:
    sys.exit('give at least one scenario label')
con = duckdb.connect(r'C:\Users\testbed\Documents\GENeSYSMOD.jl_SE\Results\genesysmod_db.duckdb', read_only=True)
q = lambda s, p=(): con.execute(s, list(p)).fetchall()
rows = []
for lab in scen:
    for r, t, y, v in q("SELECT Region, Technology, Year, SUM(Value) FROM output_capacity WHERE Scenario=? AND Type='TotalCapacity' AND Technology LIKE 'D_%' GROUP BY 1,2,3 ORDER BY 1,2,3", [lab]):
        rows.append({'Scenario': lab, 'Region': r, 'Technology': t, 'Year': y, 'Quantity': 'power capacity', 'Value': round(v, 4), 'Unit': 'GW'})
    for r, t, y, v in q("SELECT Region, Storage, Year, SUM(Value) FROM raw_TotalStorageCapacityAnnual WHERE Scenario=? GROUP BY 1,2,3 ORDER BY 1,2,3", [lab]):
        rows.append({'Scenario': lab, 'Region': r, 'Technology': t, 'Year': y, 'Quantity': 'energy capacity', 'Value': round(v / 3.6 * 1000, 2), 'Unit': 'GWh'})
tag = 'wave' if len(scen) > 1 else scen[0]
out = rf'C:\Users\testbed\Documents\GENeSYSMOD.jl_SE\Results\storage_capacity_{tag}.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['Scenario', 'Region', 'Technology', 'Year', 'Quantity', 'Value', 'Unit']); w.writeheader(); w.writerows(rows)
print(f'{len(rows)} rows -> {out}')
