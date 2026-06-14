from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

# Styles
style_anchor = 'header { background:var(--paper); border-bottom:1px solid var(--line); padding:28px 32px 20px; } h1 { margin:0 0 8px; font-size:30px; line-height:1.15; letter-spacing:0; } p { margin:0; color:var(--muted); line-height:1.55; }'
style_replacement = '''header { background:var(--paper); border-bottom:1px solid var(--line); padding:28px 32px 20px; } h1 { margin:0 0 8px; font-size:30px; line-height:1.15; letter-spacing:0; } p { margin:0; color:var(--muted); line-height:1.55; }
.header-actions { margin-top:14px; }
.source-button { min-height:38px; border:1px solid var(--line-strong); border-radius:6px; padding:8px 14px; background:#fff; color:var(--ink); font:inherit; cursor:pointer; }
.source-button:hover { background:#f8f7f2; }
.source-button[aria-expanded="true"] { background:var(--accent-soft); border-color:#bfd5cf; }
.source-panel { max-width:1180px; margin:16px auto 0; padding:0 32px; }
.source-panel[hidden] { display:none; }
.source-panel-inner { border:1px solid var(--line); border-radius:8px; background:var(--panel); padding:18px; box-shadow:var(--shadow); }
.source-panel h2 { margin:0 0 10px; font-size:18px; }
.source-list { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:0 22px; }
.source-entry { padding:10px 0; border-bottom:1px solid #ecebe5; }
.source-entry strong { display:block; margin-bottom:3px; font-size:14px; }
.source-entry a { color:#245f8f; font-size:13px; line-height:1.45; overflow-wrap:anywhere; }
.source-message { color:var(--muted); font-size:14px; }'''
if style_anchor not in html:
    raise RuntimeError("Header style anchor not found")
html = html.replace(style_anchor, style_replacement, 1)

# Mobile spacing
mobile_anchor = '@media (max-width:760px) { header { padding:24px 16px 18px; }'
mobile_replacement = '@media (max-width:760px) { header { padding:24px 16px 18px; } .source-panel { padding:0 16px; }'
if mobile_anchor not in html:
    raise RuntimeError("Mobile style anchor not found")
html = html.replace(mobile_anchor, mobile_replacement, 1)

# Header button and collapsible panel
header_anchor = '<header><h1>Anomaly Ban Ledger v1</h1><p>Grouped by anomaly, then by target type. This keeps the original source rows intact while making the ledger easier to scan.</p></header>'
header_replacement = '''<header><h1>Anomaly Ban Ledger v1</h1><p>Grouped by anomaly, then by target type. This keeps the original source rows intact while making the ledger easier to scan.</p><div class="header-actions"><button type="button" id="sourceToggle" class="source-button" aria-expanded="false" aria-controls="sourcePanel">ソース1欄</button></div></header>
<section id="sourcePanel" class="source-panel" hidden><div class="source-panel-inner"><h2>ソース1欄</h2><div id="sourceList" class="source-list"><p class="source-message">読み込み中です。</p></div></div></section>'''
if header_anchor not in html:
    raise RuntimeError("Header markup anchor not found")
html = html.replace(header_anchor, header_replacement, 1)

# Element references
js_anchor = "const anomalyFilter = document.getElementById('anomalyFilter');"
js_replacement = """const anomalyFilter = document.getElementById('anomalyFilter');
const sourceToggle = document.getElementById('sourceToggle');
const sourcePanel = document.getElementById('sourcePanel');
const sourceList = document.getElementById('sourceList');
let sourceLoaded = false;"""
if js_anchor not in html:
    raise RuntimeError("JavaScript element anchor not found")
html = html.replace(js_anchor, js_replacement, 1)

# Loader and toggle functions
function_anchor = "function byAnomaly(filtered){"
functions = '''async function loadSourceList(){
  if(sourceLoaded) return;
  try {
    const response=await fetch('./source.txt',{cache:'no-store'});
    if(!response.ok) throw new Error(`HTTP ${response.status}`);
    const text=await response.text();
    const lines=text.split(/\\r?\\n/).map(line=>line.trim()).filter(Boolean);
    sourceList.innerHTML='';
    for(let i=0;i<lines.length;i+=2){
      const title=lines[i];
      const url=lines[i+1]||'';
      const item=document.createElement('div');
      item.className='source-entry';
      const heading=document.createElement('strong');
      heading.textContent=title;
      item.appendChild(heading);
      if(url){
        const link=document.createElement('a');
        link.href=url;
        link.target='_blank';
        link.rel='noopener noreferrer';
        link.textContent=url;
        item.appendChild(link);
      }
      sourceList.appendChild(item);
    }
    sourceLoaded=true;
  } catch(error) {
    sourceList.innerHTML='<p class="source-message">ソース一覧を読み込めませんでした。</p>';
  }
}
sourceToggle.addEventListener('click',async()=>{
  const willOpen=sourcePanel.hidden;
  sourcePanel.hidden=!willOpen;
  sourceToggle.setAttribute('aria-expanded',String(willOpen));
  if(willOpen) await loadSourceList();
});

'''
if function_anchor not in html:
    raise RuntimeError("JavaScript function anchor not found")
html = html.replace(function_anchor, functions + function_anchor, 1)

path.write_text(html, encoding="utf-8")
