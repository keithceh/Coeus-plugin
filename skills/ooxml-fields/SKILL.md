---
name: ooxml-fields
version: 1.0
argument-hint: "[path to DOCX file with SEQ field, REF field, or caption numbering issue]"
description: >-
  Trigger on: /ooxml-fields, "fix figure numbers", "SEQ field", "caption numbering wrong", "table numbers out of order", "cross-reference broken", "REF field", "renumber figures", "SEQ counter reset", "caption style", "hardcoded figure number".
  Manage SEQ fields, REF fields, and caption numbering in DOCX. Fix figure/table numbers that are wrong, out of sequence, duplicated, or missing; fix broken REF fields; identify hardcoded caption numbers; verify Caption-style usage.
dependencies: []
---

# OOXML Fields — SEQ Field and Caption Management

## Overview

DOCX figure and table numbering is controlled by `SEQ` fields inside
`<w:fldChar>` / `<w:instrText>` elements in document.xml. When these are
wrong, the F9 recalculation in Word fixes displayed values — but the
underlying XML may still have cached wrong values or be missing fields
entirely.

All work on DOCX files must happen in a scratch copy. Never edit the
source file in place.

---

## 1. Locate All SEQ Fields

Parse document.xml (unzip the DOCX first):

```python
import zipfile, re

def get_seq_fields(docx_path):
    with zipfile.ZipFile(docx_path, 'r') as zf:
        doc = zf.read('word/document.xml').decode('utf-8')
    # SEQ instructions appear in <w:instrText> elements
    # They may be split across multiple instrText elements (complex fields)
    # Simple pattern covers most cases:
    seq_figure = re.findall(r'SEQ\s+Figure\b[^<]*', doc, re.IGNORECASE)
    seq_table  = re.findall(r'SEQ\s+Table\b[^<]*',  doc, re.IGNORECASE)
    return seq_figure, seq_table
```

For paragraph-level analysis, extract paragraphs with their indices:

```python
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def get_caption_paragraphs(doc_bytes):
    tree = etree.fromstring(doc_bytes)
    body = tree.find(f'{{{W}}}body')
    results = []
    for i, para in enumerate(body):
        tag = para.tag.split('}')[-1]
        if tag != 'p':
            continue
        # Get paragraph style
        pPr = para.find(f'{{{W}}}pPr')
        style = None
        if pPr is not None:
            pStyle = pPr.find(f'{{{W}}}pStyle')
            if pStyle is not None:
                style = pStyle.get(f'{{{W}}}val')
        # Get all text
        texts = ''.join(t.text or '' for t in para.iter(f'{{{W}}}t'))
        # Get SEQ field instruction text
        instrs = [e.text or '' for e in para.iter(f'{{{W}}}instrText')]
        seq_instr = [i for i in instrs if 'SEQ' in i.upper()]
        if seq_instr or (style and 'caption' in style.lower()):
            results.append({
                'para_index': i,
                'style': style,
                'text': texts,
                'seq_instrs': seq_instr,
            })
    return results
```

---

## 2. Read Cached SEQ Values

The displayed number (cached result) is in `<w:fldChar w:fldCharType="separate">` ... `<w:t>` ... `<w:fldChar w:fldCharType="end">`. Extract it:

```python
def get_cached_seq_value(para_element):
    """Returns the cached display value of the first SEQ field in a paragraph."""
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    in_field = False
    after_sep = False
    for run in para_element.iter(f'{{{W}}}r'):
        for child in run:
            tag = child.tag.split('}')[-1]
            if tag == 'fldChar':
                ftype = child.get(f'{{{W}}}fldCharType')
                if ftype == 'begin':
                    in_field = True
                    after_sep = False
                elif ftype == 'separate':
                    after_sep = True
                elif ftype == 'end':
                    in_field = False
                    after_sep = False
            elif tag == 't' and after_sep and in_field:
                return child.text
    return None
```

---

## 3. Correct Cached Values

When a cached value is wrong (e.g., shows "3" but should show "4"), update it:

```python
def set_cached_seq_value(para_element, new_value: str):
    """Replace the cached display value of the first SEQ field in a paragraph."""
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    in_field = False
    after_sep = False
    for run in para_element.iter(f'{{{W}}}r'):
        for child in list(run):
            tag = child.tag.split('}')[-1]
            if tag == 'fldChar':
                ftype = child.get(f'{{{W}}}fldCharType')
                if ftype == 'begin':   in_field = True;  after_sep = False
                elif ftype == 'separate': after_sep = True
                elif ftype == 'end':   in_field = False; after_sep = False
            elif tag == 't' and after_sep and in_field:
                child.text = new_value
                return True
    return False
```

**Note:** Correcting the cached value fixes what is displayed when the DOCX
is opened WITHOUT recalculation. The user should still press Ctrl+A then F9 in
Word after opening to recalculate all fields from scratch.

---

## 4. Check for Hardcoded Caption Numbers

A "hardcoded" caption has plain text like "Figure 3:" with no SEQ field:

```python
def find_hardcoded_captions(results):
    """Flag caption-style paragraphs that have no SEQ field instruction."""
    return [r for r in results
            if not r['seq_instrs']
            and re.search(r'(Figure|Table)\s+\d+', r['text'], re.IGNORECASE)]
```

Hardcoded captions will NOT update when fields are recalculated. They must
either be left as-is (with a note) or converted to proper SEQ fields manually
in Word. Do not attempt to add SEQ fields programmatically — the field
structure is complex and safer to insert via Word's Insert then Field dialog.

---

## 5. Audit SEQ Sequence Integrity

```python
def audit_seq_sequence(caption_paragraphs, seq_type='Figure'):
    """Check for gaps and duplicates in the SEQ sequence."""
    seq_items = [r for r in caption_paragraphs
                 if any(seq_type.upper() in i.upper() for i in r['seq_instrs'])]
    numbers = []
    for item in seq_items:
        val = item.get('cached_value')
        if val and val.isdigit():
            numbers.append((item['para_index'], int(val)))
    numbers.sort(key=lambda x: x[1])
    issues = []
    for i, (pidx, n) in enumerate(numbers):
        expected = i + 1
        if n != expected:
            issues.append(f'Para #{pidx}: expected SEQ {seq_type} #{expected}, cached = {n}')
    return issues
```

---

## 6. REF Field Checking

Cross-references to captions use REF fields pointing to bookmarks created
by the SEQ field. Check that every REF target bookmark exists:

```python
def check_ref_fields(doc_bytes):
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    doc = doc_bytes.decode('utf-8')
    ref_targets = re.findall(r'REF\s+(_Ref\w+)', doc)
    bookmark_names = re.findall(r'w:name="(_Ref\w+)"', doc)
    defined = set(bookmark_names)
    missing = [t for t in ref_targets if t not in defined]
    return missing  # Empty list = all REFs have targets
```

---

## 7. MAE-1R1 WCR v11 — Protected Elements

When working on `ZZ-99-TN-xxxxxx-MAE-1R1 Well Completion Report_draft_v11.docx`,
the following elements MUST NOT be modified under any circumstances:

### Protected drawing paragraphs (Section 8.3 images)
Para indices in body element list: `{2377, 2387, 2390, 2402}`
These contain drawings for Figures 67–70 (rIds rId92–rId95, image73–image76.png).
Do not alter, remove, or reparent these paragraphs.

### Protected caption paragraph indices (SEQ cached values only — safe to edit)
`2380` (Figure 68 caption), `2391` (Figure 69 caption), `2403` (Figure 70 caption)
These captions may have their cached SEQ values corrected. The paragraph
element itself and its drawing sibling must not be touched.

### Protected rIds
`rId92, rId93, rId94, rId95` map to `image73.png, image74.png, image75.png, image76.png`.
Do not reassign, delete, or renumber these relationship IDs.

### Hardcoded caption — do not convert
Para #2454: contains plain text "Table 36:" with no SEQ field.
This is intentional. Do not add a SEQ field here — it would conflict
with any Table SEQ field inserted before it.

---

## 8. Known Good State — MAE-1R1 v11 (after Session 13)

| Metric | Value |
|---|---|
| Total Figure captions with SEQ field | 69 (Figures 1–69) |
| Total Table captions with SEQ field | 35 (Tables 1–35) |
| Hardcoded captions (no SEQ field) | 1 (Table 36, para #2454) |
| Broken REF fields | 0 |
| SEQ sequence gaps or duplicates | 0 |
