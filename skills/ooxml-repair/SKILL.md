---
name: ooxml-repair
version: 1.0
argument-hint: "[path to DOCX file with corruption or unreadable-content error]"
description: >-
  Trigger on: /ooxml-repair, "Word unreadable content", "docx corrupt", "fix docx error", "Word recovery dialog", "OOXML schema violation", "repair Word document", "Word cannot open this file".
  Diagnose and repair "Word found unreadable content" errors in DOCX. Covers ZIP integrity, XML well-formedness, w14:paraId, orphaned bookmarkEnd / comment refs, duplicate style IDs, numbering chain, rels, RSIDs, footnotes, mc:Requires. Safe ZIP rebuild included.
dependencies: []
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.


# OOXML DOCX Repair Skill

A complete, ordered checklist for diagnosing and fixing DOCX files that trigger
Word's "Word found unreadable content" recovery dialog, built from the MAE-1R1
Well Completion Report repair sessions (June 2026).

---

## Working Environment

All work on DOCX files happens in a **scratch directory** — never edit the
source file in place. The safe rebuild recipe is mandatory for every deployment.

```
scratch/
├── unpacked_<name>/word/document.xml   ← edited XML
└── <name>_base_fixed.docx             ← ZIP template (never edited directly)
```

---

## Safe Rebuild Recipe

Use this for every output DOCX. It preserves the original ZIP's `flag_bits`
and `create_version` per entry, which Word checks during open.

```python
import zipfile, io

def rebuild_docx(base_path, new_doc_xml_path, out_path):
    with open(base_path, 'rb') as f:
        orig_data = f.read()
    with open(new_doc_xml_path, 'rb') as f:
        new_doc_xml = f.read()
    buf = io.BytesIO(orig_data)
    with zipfile.ZipFile(buf, 'r') as zf_in:
        with zipfile.ZipFile(out_path, 'w') as zf_out:
            for info in zf_in.infolist():
                data = new_doc_xml if info.filename == 'word/document.xml' \
                       else zf_in.read(info.filename)
                new_info = zipfile.ZipInfo(filename=info.filename)
                new_info.flag_bits    = info.flag_bits
                new_info.create_version = info.create_version
                new_info.compress_type  = info.compress_type
                zf_out.writestr(new_info, data)
```

**Important ZIP notes:**
- Some large DOCX files have zero-padding after the EOCD (End Of Central
  Directory). Read only the bytes before the EOCD if `zipfile` raises
  `BadZipFile`. Use `orig_data[:real_eocd_end]` after finding the EOCD offset.
- Never use Python's default `zipfile.ZipFile(path, 'w')` on the original
  file — it discards `flag_bits` and `create_version`.

---

## Diagnosis Checklist

Run **every check** before deploying. Each check is independent.

### 1. ZIP Integrity

```python
import zipfile
with zipfile.ZipFile('output.docx', 'r') as zf:
    bad = zf.testzip()
    print('CRC OK' if bad is None else f'FAIL: {bad}')
```

### 2. XML Well-Formedness (All XML Files)

```python
from lxml import etree
import zipfile, io
with zipfile.ZipFile('output.docx', 'r') as zf:
    for name in [n for n in zf.namelist() if n.endswith('.xml') or n.endswith('.rels')]:
        try:
            etree.fromstring(zf.read(name))
        except etree.XMLSyntaxError as e:
            print(f'PARSE ERROR: {name}: {e}')
```

### 3. w14:paraId Validity (document.xml + all headers/footers)

Every `w14:paraId` must be exactly 8 uppercase hex digits, unique across **all**
XML files in the ZIP (document.xml, header*.xml, footer*.xml, footnotes.xml,
endnotes.xml, comments.xml).

```python
import re

def check_para_ids(text, label):
    all_ids = re.findall(r'w14:paraId="([^"]+)"', text)
    invalid = [p for p in all_ids if not re.match(r'^[0-9A-Fa-f]{8}$', p)]
    dupes   = {v for v in all_ids if all_ids.count(v) > 1}
    print(f'{label}: total={len(all_ids)}, invalid={len(invalid)}, dupes={len(dupes)}')
    return all_ids
```

**Fix for invalid paraIds** (must be 8 hex chars): generate new random hex IDs
using `uuid.uuid4().hex[:8].upper()` and ensure uniqueness across the pool.

**Fix for duplicate paraIds in VML textbox fallbacks**: OOXML DrawingML
textboxes (`<wps:txbx>`) have a legacy VML mirror (`<v:textbox>`). The
paragraphs inside both representations share the same `w14:paraId`, causing
cross-document duplicates. Rename the second (VML) occurrence by searching for
the pattern:

```python
# VML fallback paragraphs appear AFTER the DrawingML block.
# Find paragraphs in <v:textbox> context and assign new unique IDs.
```

### 4. Orphaned bookmarkEnd Tags

Every `<w:bookmarkEnd w:id="N"/>` must have a matching
`<w:bookmarkStart w:id="N"/>` earlier in the document.

```python
starts = set(re.findall(r'<w:bookmarkStart\b[^>]+w:id="(\d+)"', doc))
ends   = set(re.findall(r'<w:bookmarkEnd\b[^>]+w:id="(\d+)"', doc))
orphaned_ends = ends - starts
# Fix: delete each <w:bookmarkEnd w:id="N"/> where N in orphaned_ends
```

> Note: Two `<w:sectPr>` in a document is **not** a violation when one is
> inside `<w:pPr>` (mid-doc section break marker). Only the final direct child
> of `<w:body>` is the "real" sectPr.

### 5. Orphaned Comment References — PRIMARY FIX for MAE-1R1

This was the root cause of the persistent "unreadable content" error.

Every `<w:commentReference w:id="N"/>`, `<w:commentRangeStart w:id="N"/>`, and
`<w:commentRangeEnd w:id="N"/>` in document.xml **must** have a corresponding
`<w:comment w:id="N">` in `word/comments.xml`. When comments are deleted in
Word but their range markers remain in the document body, this violation occurs.

```python
# Detect
comment_ids_defined = set(re.findall(r'<w:comment\b[^>]+w:id="(\d+)"', comments_xml))
comment_ids_in_doc  = set(re.findall(r'<w:commentReference[^>]+w:id="(\d+)"', doc))
orphaned = comment_ids_in_doc - comment_ids_defined

# Fix via lxml (removes commentRangeStart, commentRangeEnd, and containing run)
from lxml import etree
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
tree = etree.fromstring(doc_bytes)
# For each elem in tree.iter():
#   if elem.get('{W}id') in orphaned:
#     tag = elem.tag.split('}')[-1]
#     if tag == 'commentRangeStart': parent.remove(elem)
#     if tag == 'commentRangeEnd':   parent.remove(elem)
#     if tag == 'commentReference':
#       r = parent_of_elem  # the containing <w:r>
#       non_rpr = [c for c in r if c.tag not in (rPr_tag, commentReference_tag)]
#       if not non_rpr: grandparent.remove(r)  # run is comment-only
#       else: r.remove(elem)                   # run has real content
```

### 6. Duplicate Style IDs (styles.xml)

```python
style_ids = re.findall(r'w:styleId="([^"]+)"', styles_xml)
dupes = {v for v in style_ids if style_ids.count(v) > 1}
```

### 7. Numbering Chain Integrity (numbering.xml)

```python
defined_abstract = set(re.findall(r'<w:abstractNum\b[^>]+w:abstractNumId="(\d+)"', num_xml))
num_refs         = set(re.findall(r'<w:abstractNumId w:val="(\d+)"', num_xml))
broken = num_refs - defined_abstract
# Also check: numIds referenced in document exist in numbering.xml
```

### 8. Relationship Target Existence (all .rels files)

```python
with zipfile.ZipFile('output.docx', 'r') as zf:
    all_files = set(zf.namelist())
    for rels_name in [n for n in all_files if n.endswith('.rels')]:
        rels = zf.read(rels_name).decode('utf-8')
        for target in re.findall(r'Target="([^"]+)"', rels):
            if target.startswith(('http', 'mailto', '#')): continue
            full = target[3:] if target.startswith('../') else 'word/' + target
            if full not in all_files:
                print(f'MISSING: {rels_name} -> {target}')
```

### 9. Revision ID Uniqueness (document.xml)

```python
for rtype in ['w:ins', 'w:del', 'w:moveFrom', 'w:moveTo',
              'w:rPrChange', 'w:pPrChange', 'w:sectPrChange',
              'w:tblPrChange', 'w:trPrChange', 'w:tcPrChange']:
    ids = re.findall(rf'<{rtype}\b[^>]+w:id="(\d+)"', doc)
    dupes = {v for v in ids if ids.count(v) > 1}
    if dupes: print(f'{rtype} DUPES: {dupes}')
```

### 10. Cross-File paraId Uniqueness

```python
all_ids = {}
for fname in ['word/document.xml', 'word/header1.xml', 'word/header2.xml',
              'word/header3.xml', 'word/footer1.xml', 'word/footer2.xml',
              'word/footer3.xml', 'word/footnotes.xml', 'word/endnotes.xml',
              'word/comments.xml']:
    data = zf.read(fname).decode('utf-8')
    for pid in re.findall(r'w14:paraId="([^"]+)"', data):
        all_ids.setdefault(pid, []).append(fname)
cross_dupes = {k: v for k, v in all_ids.items() if len(v) > 1}
```

### 11. Footnote / Endnote Reference Integrity

```python
fn_refs     = set(re.findall(r'<w:footnoteReference[^>]+w:id="(\d+)"', doc))
fn_defined  = set(re.findall(r'<w:footnote\b[^>]+w:id="(\d+)"', footnotes_xml))
missing_fn  = fn_refs - fn_defined
```

### 12. Header/Footer r:id Without Rels File

If `word/header2.xml` has a rels file but `header1.xml` does not, any `r:id`
references in `header1.xml` are broken. Check:

```python
for hf in ['word/header1.xml', 'word/header2.xml', 'word/header3.xml',
           'word/footer1.xml', 'word/footer2.xml', 'word/footer3.xml']:
    rels_name = hf.replace('word/', 'word/_rels/') + '.rels'
    has_rels = rels_name in all_files
    r_refs = re.findall(r'\br:(?:id|embed)="([^"]+)"', zf.read(hf).decode())
    if r_refs and not has_rels:
        print(f'ORPHANED refs in {hf}: {r_refs}')
```

### 13. mc:Requires Namespace Declarations

```python
required = re.findall(r'mc:Requires="([^"]+)"', doc)
ns_decls = re.findall(r'xmlns:(\w+)=', doc[:5000])
for req in required:
    for prefix in req.split():
        if prefix not in ns_decls:
            print(f'UNDECLARED required ns: {prefix}')
```

---

## Document.xml lxml Round-Trip

When using lxml to edit document.xml, serialize with:

```python
new_bytes = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
```

lxml is safe for this document (confirmed). It preserves namespace declarations
and attribute order. The round-trip does not introduce any paraId or structural
changes.

---

## MAE-1R1 v11 Reference Data (Known-Good State + Repair History)

Project-specific reference data lives in [`../../docs/Ooxml-Repair-MAE1R1-Reference.md`](../../docs/Ooxml-Repair-MAE1R1-Reference.md). Load it when comparing a current diagnostic against the v11 baseline or when reviewing the session-by-session repair history (Sessions 4, 5, 6 — including the orphaned-commentReference root-cause find).

## Notes

- **Narrow no-break space (U+202F)**: Used throughout document between numerals
  and units (e.g., `88.5 MMscfd`). Preserve when editing text content.
- **Two sectPr in document**: Valid — first is inside `<w:pPr>` (mid-document
  section break), second is the final body element. Not a violation.
- **Comments defined greater than referenced**: 81 defined / 38 referenced in
  v11. The 43 extra comment definitions in comments.xml (defined but not
  anchored to any document text) are not an OOXML violation per spec. Only
  orphaned *references* (in doc body pointing to non-existent comments) are
  violations.
- **commentsExtended.xml / commentsIds.xml**: Reference `w15:paraId` of
  paragraphs within `comments.xml`, not the document body. Safe to leave
  untouched when only cleaning document.xml.
