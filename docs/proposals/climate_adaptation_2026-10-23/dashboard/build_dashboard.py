# -*- coding: utf-8 -*-
"""Compose climate_adaptation_dashboard.html from the three tab templates and the data extracts.
Run from this folder:  python build_dashboard.py
Data: cooling_viz.json (tab 1, profile analysis), climate_dash.json (tab 2, extract_results.py),
deep_dive.json (tab 3, extract_deep_dive.py). The page is published as a claude.ai artifact; the
composed file here is the archive copy."""
import re, json


def part(x, tag):
    return re.search(r'<!--%s-->(.*?)<!--/%s-->' % (tag, tag), x, re.S).group(1)


ts = open('tab1_timeseries.html', encoding='utf-8').read()
rt = open('tab2_results.html', encoding='utf-8').read()
dt = open('tab3_deep_dive.html', encoding='utf-8').read()
style1 = re.search(r'<style>(.*?)</style>', ts, re.S).group(1)
main1 = re.search(r'<main>(.*?)</main>', ts, re.S).group(1)
script1 = re.search(r'<script>(.*?)</script>', ts, re.S).group(1).replace('const D = DATA_JSON;', 'const D = DATA1;')
head = ts.split('<style>')[0].replace('<title>Cooling Shape Check</title>', '<title>Climate Adaptation Findings</title>')
tabs = ('<div class="tabs" role="tablist"><button role="tab" id="tabA" aria-selected="true" aria-controls="tab-ts">Timeseries analysis</button>'
        '<button role="tab" id="tabB" aria-selected="false" aria-controls="tab-results">Model results</button>'
        '<button role="tab" id="tabC" aria-selected="false" aria-controls="tab-deep">Regional deep dive</button>'
        '<span class="seg" id="ySel" role="group" aria-label="Model year" hidden><button data-y="2030" aria-pressed="false">2030</button>'
        '<button data-y="2035" aria-pressed="true">2035</button><button data-y="2040" aria-pressed="false">2040</button></span></div>')
tabjs = """
(function(){ const T=[['tabA','tab-ts',false],['tabB','tab-results',true],['tabC','tab-deep',true]]; const ys=document.getElementById('ySel');
function show(k){ T.forEach(([b,s,y],i)=>{ document.getElementById(b).setAttribute('aria-selected', String(i===k)); document.getElementById(s).hidden = i!==k; }); ys.hidden = !T[k][2]; window.scrollTo({top:0}); }
T.forEach(([b],i)=>document.getElementById(b).addEventListener('click',()=>show(i)));
if(location.hash==='#results') show(1); if(location.hash==='#regions') show(2); })();
"""
html = (head + '<style>' + style1 + part(rt, 'STYLE') + part(dt, 'STYLE') + '</style>\n<main>' + tabs
        + '<section id="tab-ts">' + main1 + '</section><section id="tab-results" hidden>' + part(rt, 'BODY')
        + '</section><section id="tab-deep" hidden>' + part(dt, 'BODY') + '</section></main>\n<div class="tip" id="tip"></div>\n<script>\n(function(){'
        + script1 + '})();\n' + part(rt, 'SCRIPT') + part(dt, 'SCRIPT') + tabjs + '</script>\n')
d = [json.dumps(json.load(open(f)), separators=(',', ':')) for f in ('cooling_viz.json', 'climate_dash.json', 'deep_dive.json')]
out = html.replace('DATA1', d[0], 1).replace('DATA2', d[1], 1).replace('DATA3', d[2], 1)
open('climate_adaptation_dashboard.html', 'w', encoding='utf-8').write(out)
print('written', len(out) // 1024, 'KB')
