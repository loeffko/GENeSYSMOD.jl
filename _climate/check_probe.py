# -*- coding: utf-8 -*-
"""Mechanism check of the climate probes (1924-hour runs with write_reduced_timeserie=1).
Usage: python _climate/check_probe.py [base central extreme severe]
Reads Results/scen_probe/reduced_ts_climate_<k>_1924.xlsx (+ the probe log) and reports
  - solve status, timeseries scaling status, year-banded variants announced by the build,
  - Power_Buildings_Heat / _Cooling demand profiles per year (should switch at 2030 and 2035 in the US regions, stay in Canada),
  - thermal capacity factors per year (1 before 2030, derated in the summer timeslices from 2030) for a CCGT, a steam and an OCGT tech,
  - infeasibility-slack generation from the processed results."""
import os, re, sys, glob
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'Results', 'scen_probe')
cases = sys.argv[1:] or ['base', 'central', 'extreme', 'severe']
for k in cases:
    print(f'\n================ {k}')
    log = os.path.join(P, f'_climate_probe_{k}.log')
    if os.path.exists(log):
        txt = open(log, encoding='utf-8', errors='ignore').read()
        for pat in (r'post-optimize: status=\S+', r'Timeseries scaling (NLP|bisection)[^\n]*', r'year-banded timeseries variants:[^\n]*', r'Objective[^\n]*', r'ERROR[^\n]*'):
            m = re.findall(pat, txt)
            if m:
                print('  log:', m[0] if isinstance(m[0], str) else m[0])
    f = os.path.join(P, f'reduced_ts_climate_{k}_1924.xlsx')
    if not os.path.exists(f):
        print('  no reduced-timeseries export found'); continue
    x = pd.ExcelFile(f)
    sdp = x.parse('SpecifiedDemandProfile'); sdp.columns = ['Region', 'Fuel', 'Timeslice', 'Year', 'Value']
    cf = x.parse('CapacityFactor'); cf.columns = ['Region', 'Technology', 'Timeslice', 'Year', 'Value']
    for fuel in ('Power_Buildings_Heat', 'Power_Buildings_Cooling'):
        for r in ('ERCOT', 'Canada'):
            d = sdp[(sdp.Fuel == fuel) & (sdp.Region == r)].pivot_table(index='Timeslice', columns='Year', values='Value')
            if d.empty:
                print(f'  {fuel} {r}: no rows'); continue
            yrs = sorted(d.columns)
            changes = [y for a, y in zip(yrs, yrs[1:]) if (d[y] - d[a]).abs().max() > 1e-9]
            print(f'  {fuel:24s} {r:8s} profile changes in years {changes or "none"}; 2029/2030/2035 peak share {d[2029].max():.3f}/{d[2030].max():.3f}/{d[2035].max():.3f}' if 2029 in d.columns else f'  {fuel} {r}: years {yrs}')
    for t in ('P_Gas_CCGT', 'P_Coal_Hardcoal', 'P_Nuclear', 'P_Gas_OCGT'):
        d = cf[(cf.Technology == t)]
        if d.empty:
            print(f'  CF {t}: not exported (untagged)'); continue
        g = d.groupby(['Year']).Value.agg(['min', 'mean']).round(4)
        mins = {y: g.loc[y, 'min'] for y in (2029, 2030, 2035, 2040) if y in g.index}
        us = d[(d.Region == 'SERC') & (d.Year == 2035)].sort_values('Timeslice')
        print(f'  CF {t:16s} min by year {mins}; SERC 2035 by timeslice {dict(zip(us.Timeslice, us.Value.round(3)))}')
    gen = glob.glob(os.path.join(P, f'output_annual_production*climate_{k}_1924probe*.csv'))
    for fn in gen[:1]:
        df = pd.read_csv(fn)
        tcol = next((c for c in df.columns if 'Tech' in c), None)
        if tcol is not None:
            inf = df[df[tcol].astype(str).str.startswith('Infeasibility')]
            vcol = df.columns[-1]
            print(f'  infeasibility slack rows {len(inf)}, sum {inf[vcol].astype(float).sum():.3f} ({os.path.basename(fn)})')
