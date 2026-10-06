# -*- coding: utf-8 -*-
"""Build the Canada scenario quantification plan workbook from ca_plan_content.py (model side)
and ca_plan_research.py (scenario rows, signal checks, assumptions, sources, runs, open questions).
Usage: python build_ca_plan_xlsx.py [out.xlsx]"""
import sys, os, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ca_plan_content as C
import ca_plan_research as R

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CA_scenario_plan_2026-10-04.xlsx')
HDR = PatternFill('solid', fgColor='1F3864'); HFONT = Font(bold=True, color='FFFFFF')
SUB = PatternFill('solid', fgColor='D9E1F2')
FLAG = {'GREEN': 'C6EFCE', 'YELLOW': 'FFEB9C', 'RED': 'FFC7CE'}
WRAP = Alignment(wrap_text=True, vertical='top')
thin = Side(style='thin', color='BFBFBF'); BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def sheet(wb, name, header, rows, widths, flag_col=None, freeze='A2', autofilter=True):
    ws = wb.create_sheet(name)
    ws.append(header)
    for c in range(1, len(header) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = HDR; cell.font = HFONT; cell.alignment = WRAP; cell.border = BORDER
    for r in rows:
        ws.append(list(r) + [''] * (len(header) - len(r)))
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(header)):
        for cell in row:
            cell.alignment = WRAP; cell.border = BORDER
        if flag_col is not None:
            v = str(row[flag_col].value or '').upper()
            for k, col in FLAG.items():
                if v.startswith(k):
                    row[flag_col].fill = PatternFill('solid', fgColor=col)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = freeze
    if autofilter:
        ws.auto_filter.ref = ws.dimensions
    return ws


def mark_sections(ws, ncols):
    """Bold + shade rows whose first cell starts with '##'."""
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=ncols):
        v = str(row[0].value or '')
        if v.startswith('## '):
            row[0].value = v[3:]
            for cell in row:
                cell.fill = SUB; cell.font = Font(bold=True)


wb = Workbook(); wb.remove(wb.active)

# --- README
ws = wb.create_sheet('README')
lines = [
    ('Canada scenario quantification plan', True),
    (f'Prepared {datetime.date.today().isoformat()} for the nine Canada scenarios requested by Siemens Energy Canada (docs/proposals/canada.txt). '
     'Status: PLAN - nothing is implemented or run. Numbers come from web-sourced reports (2025-2026 vintage, research notes A-E in this folder) plus the model baseline; '
     'every number in "Assumptions" carries a source id or is explicitly marked as an assumption.', False),
    ('Rules carried over from the North America set: runs are always based on the frozen v6 base (fel2026_base_49_2015_v6f, not changed); where the base is already higher than the '
     'scenario input this is flagged but the scenario numbers are used; judgement calls and far-fetched what-ifs are legitimate scenario content and are not down-rated - the flag only '
     'says whether the model can represent the scenario; every scenario has a stretch variant; as few data points as possible are invented.', False),
    ('', False),
    ('Sheets', True),
    ('Overview - one row per scenario: what it means for the model, levers, implementation route, REPRESENTABILITY flag, evidence strength (informational), base-vs-scenario comparison, proposed variants incl. a stretch, effort, anchors.', False),
    ('Signal check - each claim in the request text against the sources (confirmed / corrected / not found).', False),
    ('Assumptions - the quantified inputs per scenario and variant (parameter, years, value, unit, derivation, source ids, confidence, invented flag). This is what gets implemented.', False),
    ('Feasibility - concerns per scenario. Type "model" = representation limit (drives the flag); type "data" = evidence note (does not drive the flag). GREEN = existing levers; YELLOW = needs an approximation or a new lever; RED = cannot be represented.', False),
    ('Run plan - proposed runs with labels, data folders and funnel treatment.', False),
    ('Sources - reference list (id, organisation, title, date, URL, used for).', False),
    ('Model baseline - the Canada node of the frozen base: demand, capacity result and corridor, generation, interconnectors, model facts and levers.', False),
    ('CER comparison - Canada Energy Regulator "Canada\'s Energy Future 2026" paths by scenario and province, the benchmark for the base and for scenario 1.', False),
    ('Open questions - decisions needed before implementation.', False),
    ('Implemented_p1 - implementation record of the priority-1 runs (2026-10-05/06): data folder, definition as implemented, deviation from the plan, status, headline result. Results: scenario_plan_canada_2026-10-04/RESULTS_canada_p1_2026-10-06.md', False),
    ('', False),
    ('Conventions', True),
    ('Canada is one model node (no provinces, no territories, no off-grid systems). Years 2025-2040 annual; 2050 targets enter through their 2040 waypoint. Demand in busbar TWh. '
     'Costs in EUR2023 (1 USD = 0.925 EUR; 1 CAD = ' + str(R.CAD_EUR) + ' EUR). Capacity in GW.', False),
    ('Effort: S = data rows via the existing scenario generator (< 1 day incl. run); M = new lever or new technology rows (1-3 days); L = model change or external dependency.', False),
    ('Tags from the request: [Tailwind] upside to load / SE market, [Headwind] downside, [Mixed].', False),
]
for t, b in lines:
    ws.append([t])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=b, size=12 if b else 11)
    ws.cell(row=ws.max_row, column=1).alignment = WRAP
ws.column_dimensions['A'].width = 150

# --- Overview
sheet(wb, 'Overview',
      ['ID', 'Scenario', 'Tag', 'What it means for the model', 'Model levers (parameters)', 'Implementation route', 'Representability',
       'Representability summary', 'Evidence strength (info)', 'Base vs scenario', 'Proposed variants (incl. stretch)', 'Effort', 'Key external anchors'],
      [(s['id'], s['name'], s['tag'], s['meaning'], s['levers'], s['route'], s['flag'], s['flag_summary'], s['evidence'], s['base_cmp'],
        s['variants'], s['effort'], s['anchors']) for s in R.SCENARIOS],
      [5, 26, 11, 46, 42, 38, 12, 44, 26, 40, 54, 7, 44], flag_col=6, freeze='C2')

# --- Signal check
ws = sheet(wb, 'Signal check', ['ID', 'Claim in the request', 'What the sources say', 'Verdict', 'Source id(s)'],
           [tuple(x) for x in R.SIGNALS], [5, 52, 80, 14, 16])
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    v = str(row[3].value or '').lower()
    row[3].fill = PatternFill('solid', fgColor=FLAG['GREEN'] if v.startswith('confirmed') else (FLAG['YELLOW'] if v.startswith(('corrected', 'partly')) else FLAG['RED']))

# --- Assumptions
ws = sheet(wb, 'Assumptions',
           ['ID', 'Scenario', 'Variant', 'Parameter / lever', 'Region(s)', 'Years', 'Value', 'Unit', 'Basis / derivation', 'Source id(s)', 'Confidence', 'Invented?'],
           [tuple(a) for a in R.ASSUMPTIONS], [5, 22, 14, 34, 14, 14, 26, 12, 62, 16, 11, 10], freeze='D2')
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    v = str(row[11].value or '').lower()
    if v.startswith('yes'):
        row[11].fill = PatternFill('solid', fgColor=FLAG['RED'])
    elif v.startswith('partly'):
        row[11].fill = PatternFill('solid', fgColor=FLAG['YELLOW'])
    c = str(row[10].value or '').lower()
    if c.startswith('high'):
        row[10].fill = PatternFill('solid', fgColor=FLAG['GREEN'])
    elif c.startswith('low'):
        row[10].fill = PatternFill('solid', fgColor=FLAG['RED'])
    elif c.startswith('med'):
        row[10].fill = PatternFill('solid', fgColor=FLAG['YELLOW'])

# --- Feasibility
feas = [(s['id'], s['name'], sev, typ, why, fix) for s in R.SCENARIOS for (sev, typ, why, fix) in s['concerns']]
sheet(wb, 'Feasibility', ['ID', 'Scenario', 'Severity', 'Type', 'Concern', 'Workaround / proposal'], feas, [5, 26, 10, 8, 72, 72], flag_col=2)

# --- Run plan
sheet(wb, 'Run plan', ['Run label', 'Scenario', 'Variant', 'Definition', 'Corridor / funnel treatment', 'Priority', 'Note'],
      [tuple(x) for x in R.RUNS], [44, 22, 10, 70, 44, 9, 44])

# --- Sources
sheet(wb, 'Sources', ['Source id', 'Organisation', 'Title', 'Date', 'URL', 'Used for'], [tuple(x) for x in R.SOURCES], [10, 26, 62, 13, 62, 26])

# --- Model baseline
rows = [('## Demand of the Canada node, busbar TWh (frozen base ' + C.BASE_LABEL + ')', '2025', '2030', '2035', '2040', '', '')]
rows += [(n, a, b, c, d, '', '') for n, a, b, c, d in C.DEMAND]
rows.append(('## Capacity, GW: model result and corridor', '2025', '2030', '2035', '2040', 'corridor minimum 2040', 'corridor maximum 2040'))
rows += [tuple(x) for x in C.CAPACITY]
rows.append(('## Generation TWh, exports, CO2', '2025', '2030', '2035', '2040', '', ''))
rows += [(n, a, b, c, d, '', '') for n, a, b, c, d in C.GENERATION]
rows.append(('## Interconnectors Canada - US', 'GW 2025', 'GW 2040 (max)', 'net export TWh 2025', 'net export TWh 2040', '', ''))
rows += [(n, a, b, c, d, '', '') for n, a, b, c, d in C.INTERTIES]
rows.append(('## Model facts', '', '', '', '', '', ''))
rows += [(k, v, '', '', '', '', '') for k, v in C.MODEL_FACTS]
rows.append(('## Levers available for Canada', 'parameter', '', '', '', '', 'used by'))
rows += [(k, v, '', '', '', '', u) for k, v, u in C.LEVERS]
ws = sheet(wb, 'Model baseline', ['Item', 'a', 'b', 'c', 'd', 'e', 'f'], rows, [46, 16, 16, 18, 18, 22, 30], autofilter=False)
mark_sections(ws, 7)
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):   # long text rows: merge b..g
    if isinstance(row[1].value, str) and len(row[1].value) > 60:
        ws.merge_cells(start_row=row[0].row, start_column=2, end_row=row[0].row, end_column=6)
        ws.row_dimensions[row[0].row].height = max(30, 15 * (len(row[1].value) // 85 + 1))

# --- CER comparison
rows = []
for sc, lst in C.CER_CAPACITY.items():
    rows.append((f'## CER EF2026 capacity, GW - {sc}', '2025', '2030', '2035', '2040', '2050'))
    rows += [tuple(x) for x in lst]
rows.append(('## CER EF2026 electricity end-use demand, TWh (gross end use, not busbar)', '2025', '2030', '2035', '2040', '2050'))
rows += [tuple(x) for x in C.CER_DEMAND]
rows.append(('## CER EF2026 generation, TWh', '2025', '2030', '2035', '2040', '2050'))
rows += [tuple(x) for x in C.CER_GENERATION]
rows.append(('## Model base for comparison (generation capacity GW / demand busbar TWh)', '2025', '2030', '2035', '2040', '2050'))
rows.append(('Base: generation capacity (excl. batteries)', 167.2, 190.1, 241.4, 296.8, 'not modelled'))
rows.append(('Base: demand', 545.2, 623.7, 767.6, 899.4, 'not modelled'))
rows.append(('## CER Current Measures by province, GW (2025 / 2040 / 2050)', 'total', 'wind', 'nuclear', 'gas', ''))
rows += [tuple(x) + ('',) for x in C.CER_PROVINCES]
ws = sheet(wb, 'CER comparison', ['Item', 'a', 'b', 'c', 'd', 'e'], rows, [62, 20, 20, 20, 20, 16], autofilter=False)
mark_sections(ws, 6)

# --- Open questions
sheet(wb, 'Open questions', ['#', 'Question', 'Options / recommendation', 'Affects'], [tuple(x) for x in R.OPEN_QUESTIONS], [4, 70, 80, 22])

# --- Implemented (priority 1)
sheet(wb, 'Implemented_p1', ['Run label', 'Scenario', 'Variant', 'Data folder', 'As implemented', 'Deviation from the plan', 'Status', 'Canada 2040 headline (vs base)'],
      [tuple(x) for x in R.IMPLEMENTED], [38, 9, 9, 30, 90, 40, 18, 50])

wb.save(OUT)
print('written', os.path.normpath(OUT), '| scenarios', len(R.SCENARIOS), '| assumptions', len(R.ASSUMPTIONS), '| sources', len(R.SOURCES), '| signals', len(R.SIGNALS), '| runs', len(R.RUNS))
