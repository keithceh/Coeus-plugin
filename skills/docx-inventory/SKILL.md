---
name: docx-inventory
version: 1.0
argument-hint: "[path to DOCX file to inventory] [optional output xlsx path]"
description: >-
  Trigger on: /docx-inventory, "figure inventory", "table inventory", "list all figures", "list all tables", "extract captions", "caption list", "audit captions", "what figures are in the document".
  Extract a complete figure and table inventory from a DOCX to an xlsx (two sheets: figures, tables). Each row: paragraph index, SEQ number, caption text, paragraph style, issues detected. Use to audit caption numbering or build a cross-reference index.
dependencies: []
---

# DOCX Inventory — Figure and Table Extraction

Produces a structured xlsx inventory of all figures and tables in a DOCX file
by parsing the OOXML directly. Does not require Word to be installed.

---

## 1. Dependencies

```bash
pip install openpyxl lxml --break-system-packages
```

---

## 2. Extraction Script

Save as `extract_inventory.py` and run it, or execute inline via bash:

```python
import zipfile, re, sys
from lxml import etree
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

def extract_inventory(docx_path, out_xlsx_path):
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    with zipfile.ZipFile(docx_path, 'r') as zf:
        doc_bytes = zf.read('word/document.xml')

    tree = etree.fromstring(doc_bytes)
    body = tree.find(f'{{{W}}}body')

    figures = []
    tables  = []

    def get_text(para):
        return ''.join(t.text or '' for t in para.iter(f'{{{W}}}t'))

    def get_seq_instr(para):
        return [e.text or '' for e in para.iter(f'{{{W}}}instrText')
                if e.text and 'SEQ' in e.text.upper()]

    def get_cached_value(para):
        in_field = after_sep = False
        for run in para.iter(f'{{{W}}}r'):
            for child in run:
                tag = child.tag.split('}')[-1]
                if tag == 'fldChar':
                    ft = child.get(f'{{{W}}}fldCharType', '')
                    if ft == 'begin':    in_field = True;  after_sep = False
                    elif ft == 'separate': after_sep = True
                    elif ft == 'end':    in_field = False; after_sep = False
                elif tag == 't' and after_sep and in_field:
                    return child.text
        return None

    for i, elem in enumerate(body):
        tag = elem.tag.split('}')[-1]
        if tag != 'p':
            continue
        pPr = elem.find(f'{{{W}}}pPr')
        style = None
        if pPr is not None:
            pStyle = pPr.find(f'{{{W}}}pStyle')
            if pStyle is not None:
                style = pStyle.get(f'{{{W}}}val', '')

        text    = get_text(elem)
        instrs  = get_seq_instr(elem)
        cached  = get_cached_value(elem)

        is_fig_seq = any('SEQ' in s.upper() and 'FIGURE' in s.upper() for s in instrs)
        is_tbl_seq = any('SEQ' in s.upper() and 'TABLE'  in s.upper() for s in instrs)

        # Also catch caption-style paragraphs starting with Figure/Table
        is_fig_text = bool(re.match(r'Figure\s+\d+', text, re.IGNORECASE))
        is_tbl_text = bool(re.match(r'Table\s+\d+',  text, re.IGNORECASE))

        issues = []
        if (is_fig_text or is_fig_seq) and not is_fig_seq:
            issues.append('No SEQ Figure field — hardcoded')
        if (is_tbl_text or is_tbl_seq) and not is_tbl_seq:
            issues.append('No SEQ Table field — hardcoded')

        if is_fig_seq or is_fig_text:
            figures.append({
                'para_index': i,
                'seq_num': cached or '',
                'text': text[:200],
                'style': style or '',
                'issues': '; '.join(issues),
            })
        elif is_tbl_seq or is_tbl_text:
            tables.append({
                'para_index': i,
                'seq_num': cached or '',
                'text': text[:200],
                'style': style or '',
                'issues': '; '.join(issues),
            })

    # Check for duplicate and gap SEQ numbers
    def add_seq_issues(rows, label):
        nums = [(r['seq_num'], r['para_index']) for r in rows if r['seq_num'].isdigit()]
        nums.sort(key=lambda x: int(x[0]))
        seen = {}
        for n, pidx in nums:
            if n in seen:
                for r in rows:
                    if r['para_index'] == pidx:
                        r['issues'] = (r['issues'] + f'; DUPLICATE SEQ {label} #{n}').strip('; ')
            seen[n] = pidx
        # Gap check
        int_nums = sorted(int(n) for n, _ in nums)
        for j, n in enumerate(int_nums):
            if n != j + 1:
                print(f'  GAP: expected {label} #{j+1}, found #{n}')

    add_seq_issues(figures, 'Figure')
    add_seq_issues(tables, 'Table')

    # Write xlsx
    wb = openpyxl.Workbook()
    header_font = Font(bold=True, color='FFFFFF')
    header_fill = PatternFill('solid', fgColor='2F4F8F')

    def write_sheet(ws, rows, label):
        ws.title = label
        headers = ['Para Index', f'SEQ # (cached)', 'Caption Text', 'Style', 'Issues']
        ws.append(headers)
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
        for r in rows:
            ws.append([r['para_index'], r['seq_num'], r['text'], r['style'], r['issues']])
            if r['issues']:
                ws.cell(ws.max_row, 5).font = Font(color='CC0000')
        ws.column_dimensions['C'].width = 80
        ws.column_dimensions['E'].width = 40

    ws_fig = wb.active
    write_sheet(ws_fig, figures, 'Figures')
    ws_tbl = wb.create_sheet('Tables')
    write_sheet(ws_tbl, tables, 'Tables')

    wb.save(out_xlsx_path)
    print(f'Inventory written: {out_xlsx_path}')
    print(f'  Figures: {len(figures)} ({sum(1 for r in figures if r["issues"])} with issues)')
    print(f'  Tables:  {len(tables)} ({sum(1 for r in tables if r["issues"])} with issues)')
```

---

## 3. Usage

```bash
python extract_inventory.py \
  "C:/Claude/Claude-Work/Projects/Technical_Reports/Inputs/ZZ-99-TN-xxxxxx-MAE-1R1 Well Completion Report_draft_v11.docx" \
  "C:/Claude/Claude-Work/Projects/Technical_Reports/Outputs/MAE-1R1_WCR_Figure_Table_Inventory_v11.xlsx"
```

Or run inline via the bash tool using the script content above.

---

## 4. Output Format

**Sheet: Figures**

| Para Index | SEQ # (cached) | Caption Text | Style | Issues |
|---|---|---|---|---|
| 142 | 1 | Figure 1: Location map of ... | Caption | |
| 201 | 2 | Figure 2: Stratigraphic ... | Caption | |
| ... | | | | |

**Sheet: Tables**

Same structure for tables.

Issues column flags: `No SEQ field — hardcoded`, `DUPLICATE SEQ Figure #N`, gaps printed to stdout.

---

## 5. Known Output — MAE-1R1 v11 (reference values)

After Session 13 corrections:

| Metric | Expected value |
|---|---|
| Total Figure rows | 69 |
| Total Table rows | 36 (35 with SEQ + 1 hardcoded) |
| Figure issues | 0 |
| Table issues | 1 (para #2454, Table 36, hardcoded — expected) |
