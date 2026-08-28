# ooxml-repair — MAE-1R1 v11 Reference Data

> Project-specific reference data for the MAE-1R1 Well Completion Report v11 repair sessions. Used as a known-good benchmark and historical repair log. The `ooxml-repair` skill links here when a user needs to compare a current diagnostic against the v11 baseline.

---

## Known-Good State (MAE-1R1 v11, June 2026)

After all fixes applied:

| Check | Result |
|---|---|
| ZIP CRC | PASS |
| XML parse (all files) | OK |
| w14:paraId total | 3,060 |
| w14:paraId invalid | 0 |
| w14:paraId duplicates (doc) | 0 |
| Cross-file paraId duplicates | 0 |
| Orphaned bookmarkEnd | 0 |
| Orphaned commentReference | 0 |
| Revision ID duplicates | 0 |
| styleId duplicates | 0 |
| Numbering chain broken | 0 |
| Missing rels targets | 0 |

---

## Repair History — MAE-1R1 WCR v11

| Session | Fix Applied |
|---|---|
| 4 | 6 QC content fixes (text replacements): heading text, reserves text, Table 35, Figure 21 caption |
| 5 | 432 invalid w14:paraId values (non-8-hex-char) corrected; 4 duplicate paraIds deduplicated; ZIP stale artefacts (.bak, wrong image extensions) removed; zero-padding EOCD handled; base template v11_base_fixed3.docx created |
| 6 | 3 VML textbox fallback duplicate paraIds renamed (second/VML occurrence); 1 orphaned bookmarkEnd removed; **43 orphaned commentReference/Range markup removed from document.xml** (root cause of persistent error) |
