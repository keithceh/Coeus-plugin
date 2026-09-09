"""Build index.html from README + EP-Council + LLM-Council docs.

Single-page navigation with 3 visible top-level tabs (Overview, EP-Council,
LLM-Council). The 5 companion panels (EP Members / Traps / Walkthrough,
LLM Members / Walkthrough) remain in the DOM and are reached only via
in-content links from their parent tab — each shows a "← Back to <origin>"
banner that returns the reader to the tab they came from.
"""
import markdown
from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent

# (sid, label, md_path, parent_main_tab_or_None)
SECTIONS = [
    ("readme",         "Overview",            ROOT / "README.md",                            None),
    ("installation",   "Installation",        ROOT / "docs/Installation.md",                 None),
    ("skills",         "Skills",              ROOT / "docs/SKILLS.md",                       None),
    ("keymaker",           "Keymaker",             ROOT / "docs/Keymaker.md",                 "skills"),
    ("atlas-doc",          "Atlas",                ROOT / "docs/Atlas.md",                    "skills"),
    ("seer-doc",           "Seer",                 ROOT / "docs/Seer.md",                     "skills"),
    ("minto-doc",          "Minto",                ROOT / "docs/Minto.md",                    "skills"),
    ("morpheus-pipeline",  "Morpheus Pipeline",    ROOT / "docs/Morpheus-Pipeline.md",        "skills"),
    ("architect-doc",      "The Architect",        ROOT / "docs/The-Architect.md",            "skills"),
    ("plugin-creator-doc", "Plugin-Creator",       ROOT / "docs/Plugin-Creator.md",            "skills"),
    ("evergreen-doc",      "Evergreen Artefacts",  ROOT / "docs/Evergreen-Artefacts.md",       "skills"),
    ("obsidian-doc",       "Obsidian Vault",       ROOT / "docs/Obsidian-Vault.md",            "skills"),
    ("ep-council",     "EP-Council",          ROOT / "docs/EP-Council.md",                   None),
    ("ep-members",     "EP Council Members",  ROOT / "docs/EP-Council-Council-Members.md",   "ep-council"),
    ("ep-traps",       "EP Trap Screen",      ROOT / "docs/EP-Council-Trap-Screen.md",       "ep-council"),
    ("ep-walkthrough", "EP Walkthrough",      ROOT / "docs/EP-Council-Walkthrough.md",       "ep-council"),
    ("llm-council",    "LLM-Council",         ROOT / "docs/LLM-Council.md",                  None),
    ("llm-members",    "LLM Council Members", ROOT / "docs/LLM-Council-Members.md",          "llm-council"),
    ("llm-walkthrough","LLM Walkthrough",     ROOT / "docs/LLM-Council-Walkthrough.md",      "llm-council"),
    ("tools",            "Office Tools",         ROOT / "docs/Tools.md",                          None),
    ("tools-ooxml-repair","OOXML Repair",        ROOT / "skills/ooxml-repair/SKILL.md",          "tools"),
    ("tools-ooxml-fields","OOXML Fields",        ROOT / "skills/ooxml-fields/SKILL.md",          "tools"),
    ("tools-docx-inventory","DOCX Inventory",    ROOT / "skills/docx-inventory/SKILL.md",        "tools"),
    ("project-lifecycle","Project Lifecycle",   ROOT / "docs/Project-Lifecycle.md",              None),
    ("pl-skill",         "Project-Lifecycle SKILL.md", ROOT / "skills/project-lifecycle/SKILL.md", "project-lifecycle"),
    ("seismic-tools",    "Seismic Tools",        ROOT / "docs/Seismic-Tools.md",                  None),
    ("seismic-dug-binary","DUG Binary",          ROOT / "skills/dug_binary/SKILL.md",            "seismic-tools"),
]

md = markdown.Markdown(extensions=[
    "fenced_code", "tables", "toc", "codehilite", "sane_lists", "attr_list"
])

def render(p: Path) -> str:
    md.reset()
    return md.convert(p.read_text(encoding="utf-8"))

# Only main tabs (parent is None) appear in the nav.
nav = "\n".join(
    f'      <a href="#{sid}" data-tab="{sid}" class="tab">{html.escape(label)}</a>'
    for sid, label, _, parent in SECTIONS if parent is None
)
sections = "\n".join(
    f'    <section id="{sid}" class="panel">\n{render(p)}\n    </section>'
    for sid, _, p, _ in SECTIONS
)

CSS = """
:root{
  --bg:#0e1015;--bg2:#12151d;--fg:#e8eaee;--mut:#98a0ab;--acc:#f2b63c;--acc2:#7cb1ff;
  --card:#171b24;--bd:#252a37;--bd2:#2e3444;--code:#0a0c11;
  --r:10px;--maxw:1080px;
}
*{box-sizing:border-box}
::selection{background:rgba(242,182,60,.28)}
html{scroll-behavior:smooth}
html,body{margin:0;padding:0;background:var(--bg);color:var(--fg);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}

header{position:sticky;top:0;z-index:50;background:rgba(14,16,21,.88);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--bd)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.brand{display:flex;align-items:baseline;gap:12px;padding:16px 0 10px}
.brand h1{margin:0;font-size:19px;font-weight:700;letter-spacing:.04em}
.brand h1::after{content:"";display:inline-block;width:7px;height:7px;margin-left:9px;
  border-radius:50%;background:var(--acc);vertical-align:baseline}
.brand .v{color:var(--mut);font-size:13px;letter-spacing:.01em}

nav{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}
nav::-webkit-scrollbar{display:none}
.tab{position:relative;padding:9px 13px 12px;color:var(--mut);text-decoration:none;
  font-size:14px;font-weight:500;white-space:nowrap;border-radius:7px 7px 0 0;
  transition:color .15s}
.tab:hover{color:var(--fg)}
.tab:focus-visible{outline:2px solid var(--acc2);outline-offset:-2px}
.tab.active{color:var(--fg)}
.tab.active::after{content:"";position:absolute;left:11px;right:11px;bottom:0;height:2px;
  background:var(--acc);border-radius:2px 2px 0 0}

main{padding:36px 0 72px}
.panel{display:none;max-width:var(--maxw);margin:0 auto;padding:0 24px}
.panel.active{display:block;animation:fadein .18s ease-out}
@keyframes fadein{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.panel.active{animation:none}}

.panel h1,.panel h2,.panel h3,.panel h4{line-height:1.25;letter-spacing:-.01em}
.panel h1{font-size:30px;font-weight:750;margin:1.2em 0 .55em;
  border-bottom:1px solid var(--bd);padding-bottom:.35em}
.panel>h1:first-child{margin-top:.2em}
.panel h2{font-size:22px;font-weight:700;color:#fff;margin:2em 0 .6em}
.panel h3{font-size:17.5px;font-weight:650;color:var(--acc);margin:1.7em 0 .5em}
.panel h4{font-size:15.5px;color:var(--fg);margin:1.5em 0 .4em}
.panel p,.panel li{max-width:76ch}
.panel [id]{scroll-margin-top:110px}

.panel a{color:var(--acc2);text-decoration:none}
.panel a:hover{text-decoration:underline;text-underline-offset:3px}

.panel code{background:var(--code);border:1px solid var(--bd);padding:2px 6px;border-radius:5px;
  font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.panel pre{background:var(--code);padding:15px 17px;border-radius:var(--r);
  border:1px solid var(--bd);overflow-x:auto;line-height:1.55}
.panel pre code{background:transparent;border:0;padding:0}

.panel table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:14px;
  border:1px solid var(--bd);border-radius:var(--r);overflow:hidden;display:block;overflow-x:auto}
.panel thead{position:sticky;top:0}
.panel th{background:var(--card);color:var(--fg);font-weight:650;text-align:left;
  padding:10px 12px;border-bottom:2px solid var(--bd2)}
.panel td{padding:9px 12px;border-bottom:1px solid var(--bd);text-align:left;vertical-align:top}
.panel tbody tr:nth-child(even){background:var(--bg2)}
.panel tbody tr:last-child td{border-bottom:0}

.panel blockquote{border-left:3px solid var(--acc);margin:1.2em 0;
  padding:.7em 1.1em;color:var(--mut);background:var(--card);
  border-radius:0 var(--r) var(--r) 0}
.panel blockquote p{margin:.3em 0}
.panel hr{border:0;border-top:1px solid var(--bd);margin:2.4em 0}
.panel img{max-width:100%;height:auto;border-radius:var(--r)}
.panel ul,.panel ol{padding-left:1.4em}
.panel li{margin:.25em 0}

footer{color:var(--mut);font-size:13px;text-align:center;padding:28px 24px;
  border-top:1px solid var(--bd)}
footer a{color:var(--mut)}
footer a:hover{color:var(--fg)}

.backbar{display:none;max-width:var(--maxw);margin:0 auto 18px;padding:10px 24px;
  background:var(--card);border:1px solid var(--bd);border-radius:var(--r);font-size:14px}
.backbar.show{display:block}
.backbar a{color:var(--acc);text-decoration:none;cursor:pointer;font-weight:550}
.backbar a:hover{text-decoration:underline}
"""

JS = """
const tabs=[...document.querySelectorAll('.tab')];
const panels=[...document.querySelectorAll('.panel')];
const MAIN_TABS=['readme','installation','skills','ep-council','llm-council','tools','project-lifecycle','seismic-tools'];
const SUB_PARENT={
  'ep-members':'ep-council',
  'ep-traps':'ep-council',
  'ep-walkthrough':'ep-council',
  'llm-members':'llm-council',
  'llm-walkthrough':'llm-council',
  'tools-ooxml-repair':'tools',
  'tools-ooxml-fields':'tools',
  'tools-docx-inventory':'tools',
  'pl-skill':'project-lifecycle',
  'seismic-dug-binary':'seismic-tools',
  'keymaker':'skills',
  'atlas-doc':'skills',
  'seer-doc':'skills',
  'minto-doc':'skills',
  'morpheus-pipeline':'skills',
  'architect-doc':'skills',
  'plugin-creator-doc':'skills',
  'evergreen-doc':'skills',
  'obsidian-doc':'skills'
};
const SUB_LABEL={'ep-council':'EP-Council','llm-council':'LLM-Council','tools':'Office Tools','project-lifecycle':'Project-Lifecycle','seismic-tools':'Seismic Tools','readme':'Overview','skills':'Skills'};
const MD2TAB={
  'docs/EP-Council-Council-Members.md':'ep-members',
  'docs/EP-Council-Trap-Screen.md':'ep-traps',
  'docs/EP-Council-Walkthrough.md':'ep-walkthrough',
  'docs/EP-Council.md':'ep-council',
  'docs/LLM-Council-Members.md':'llm-members',
  'docs/LLM-Council-Walkthrough.md':'llm-walkthrough',
  'docs/LLM-Council.md':'llm-council',
  'docs/Tools.md':'tools',
  'docs/Seismic-Tools.md':'seismic-tools',
  'docs/Installation.md':'installation',
  'docs/SKILLS.md':'skills',
  'SKILLS':'skills',
  'docs/Keymaker.md':'keymaker',
  'docs/Atlas.md':'atlas-doc',
  'docs/Seer.md':'seer-doc',
  'docs/Minto.md':'minto-doc',
  'docs/Morpheus-Pipeline.md':'morpheus-pipeline',
  'docs/The-Architect.md':'architect-doc',
  'docs/Plugin-Creator.md':'plugin-creator-doc',
  'docs/Evergreen-Artefacts.md':'evergreen-doc',
  'docs/Obsidian-Vault.md':'obsidian-doc',
  'Installation':'installation',
  'docs/Project-Lifecycle.md':'project-lifecycle',
  'Project-Lifecycle':'project-lifecycle',
  'skills/ooxml-repair/SKILL.md':'tools-ooxml-repair',
  'skills/ooxml-fields/SKILL.md':'tools-ooxml-fields',
  'skills/docx-inventory/SKILL.md':'tools-docx-inventory',
  'skills/project-lifecycle/SKILL.md':'tools-project-lifecycle',
  'skills/dug_binary/SKILL.md':'seismic-dug-binary',
  'Tools':'tools',
  'Tools-OOXML-Repair':'tools-ooxml-repair',
  'Tools-OOXML-Fields':'tools-ooxml-fields',
  'Tools-DOCX-Inventory':'tools-docx-inventory',
  'Tools-Project-Lifecycle':'tools-project-lifecycle',
  'Seismic-Tools':'seismic-tools',
  'Seismic-Tools-DUG-ProjDB':'seismic-dug-binary',
  'Seismic-Tools-DUG-Binary':'seismic-dug-binary',
  'README.md':'readme',
  // Wiki-style basenames (from links like [Council Members](EP-Council-Council-Members))
  // and Vercel rewrite pathnames (/EP-Council-Council-Members).
  'EP-Council':'ep-council',
  'EP-Council-Council-Members':'ep-members',
  'EP-Council-Trap-Screen':'ep-traps',
  'EP-Council-Walkthrough':'ep-walkthrough',
  'LLM-Council':'llm-council',
  'LLM-Council-Members':'llm-members',
  'LLM-Council-Walkthrough':'llm-walkthrough'
};
const backbar=document.getElementById('backbar');
const backlink=document.getElementById('backlink');
let originStack=[];
function isMain(id){return MAIN_TABS.includes(id);}
function updateBack(id){
  if(isMain(id)||!SUB_PARENT[id]){backbar.classList.remove('show');return;}
  const origin=originStack[originStack.length-1]||SUB_PARENT[id];
  backlink.textContent='\\u2190 Back to '+(SUB_LABEL[origin]||origin);
  backlink.dataset.target=origin;
  backbar.classList.add('show');
}
function show(id,anchor,opts){
  opts=opts||{};
  if(!panels.some(p=>p.id===id))id='readme';
  const currentActive=(document.querySelector('.panel.active')||{}).id;
  if(SUB_PARENT[id]&&currentActive&&currentActive!==id&&!opts.back){
    const origin=isMain(currentActive)?currentActive:(originStack[originStack.length-1]||SUB_PARENT[id]);
    originStack.push(origin);
  }
  if(isMain(id))originStack=[];
  tabs.forEach(t=>t.classList.toggle('active',t.dataset.tab===id));
  panels.forEach(p=>p.classList.toggle('active',p.id===id));
  updateBack(id);
  if(anchor){
    const el=document.getElementById(anchor);
    if(el){el.scrollIntoView({behavior:'instant',block:'start'});if(history.replaceState)history.replaceState(null,'','#'+id);return;}
  }
  if(history.replaceState)history.replaceState(null,'','#'+id);
  window.scrollTo({top:0,behavior:'instant'});
}
tabs.forEach(t=>t.addEventListener('click',e=>{e.preventDefault();show(t.dataset.tab)}));
backlink.addEventListener('click',e=>{
  e.preventDefault();
  const target=backlink.dataset.target||'readme';
  originStack.pop();
  show(target,null,{back:true});
});
document.addEventListener('click',e=>{
  const a=e.target.closest('a[href]');if(!a)return;
  if(a.id==='backlink')return;
  let href=a.getAttribute('href');if(!href||href.startsWith('http')||href.startsWith('mailto:'))return;
  if(href.startsWith('#')){e.preventDefault();show(document.querySelector('.tab.active')?.dataset.tab||(document.querySelector('.panel.active')||{}).id||'readme',href.slice(1));return;}
  const clean=href.replace(/^\\.\\//,'').replace(/^\\//,'');
  const [pathPart,frag]=clean.split('#');
  let tabId=MD2TAB[pathPart];
  if(!tabId){for(const k of Object.keys(MD2TAB)){if(k.endsWith('/'+pathPart)){tabId=MD2TAB[k];break;}}}
  if(tabId){e.preventDefault();show(tabId,frag);}
});
// Initial tab: hash wins, else pathname (Vercel rewrites /foo -> /index.html),
// else default to readme.
let initial=null;
if(location.hash){initial=location.hash.slice(1).split('#')[0];}
else{
  const path=location.pathname.replace(/^\\//,'').replace(/\\/$/,'');
  if(path&&path!=='index.html'){
    initial=MD2TAB[path]||MD2TAB[path+'.md']||MD2TAB['docs/'+path+'.md']||null;
  }
}
show(panels.some(p=>p.id===initial)?initial:'readme');
"""

html_out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Coeus — Titan of Intelligence and Foresight</title>
<meta name="description" content="EP-industry skill suite for high-stakes decisions: LLM-Council, Morpheus, The Architect, EP-Council, Caveman, Prompt-Master, Plugin-Creator.">
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="brand">
      <h1>Coeus</h1>
      <span class="v">Titan of Intelligence and Foresight</span>
    </div>
    <nav>
{nav}
    </nav>
  </div>
</header>
<main>
<div id="backbar" class="backbar"><a id="backlink" href="#">← Back</a></div>
{sections}
</main>
<footer>
  <a href="https://github.com/keithceh/Coeus">github.com/keithceh/Coeus</a> · ENERGEIA SERVICES PTE. LTD. · BSL 1.1 → Apache 2.0 (2028-05-28)
</footer>
<script>{JS}</script>
</body>
</html>
"""

OUT = ROOT / "index.html"
OUT.write_text(html_out, encoding="utf-8")
print(f"wrote {OUT}  ({len(html_out):,} bytes)")
