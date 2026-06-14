from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

html = html.replace(
    "grid-template-columns:minmax(240px,1fr) 220px 210px;",
    "grid-template-columns:minmax(240px,1fr) minmax(340px,560px);",
    1,
)
html = html.replace(
    "input,select { width:100%; min-height:40px;",
    "input,select { width:100%; min-height:40px;",
    1,
)
html = html.replace(
    "input,select { width:100%; min-height:40px; border:1px solid var(--line); border-radius:6px; padding:8px 10px; background:#fff; color:var(--ink); font:inherit; }",
    "input,select { width:100%; min-height:40px; border:1px solid var(--line); border-radius:6px; padding:8px 10px; background:#fff; color:var(--ink); font:inherit; }\n.controls select { min-height:48px; padding:10px 14px; font-size:16px; }",
    1,
)

old_controls = '<section class="controls" aria-label="filters"><input id="q" type="search" placeholder="Search anomaly, target, note..." autocomplete="off"><select id="type"><option value="">All target groups</option></select><select id="status"><option value="">All statuses</option></select></section>'
new_controls = '<section class="controls" aria-label="filters"><input id="q" type="search" placeholder="Search anomaly, target, note..." autocomplete="off"><select id="anomalyFilter"><option value="">Anomaly</option></select></section>'
if old_controls not in html:
    raise RuntimeError("Controls markup was not found")
html = html.replace(old_controls, new_controls, 1)

html = html.replace(
    "const type = document.getElementById('type');\nconst status = document.getElementById('status');",
    "const anomalyFilter = document.getElementById('anomalyFilter');",
    1,
)

old_fill = """function fillSelects(){
  GROUPS.forEach(g => { const o=document.createElement('option'); o.value=g.key; o.textContent=`${g.label} (${g.hint})`; type.appendChild(o); });
  [...new Set(rows.map(r=>r.status).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'ja')).forEach(v => { const o=document.createElement('option'); o.value=v; o.textContent=v; status.appendChild(o); });
}"""
new_fill = """function fillSelects(){
  [...new Set(rows.map(r=>r.anomaly).filter(Boolean))]
    .sort((a,b)=>a.localeCompare(b,'ja'))
    .forEach(value => {
      const option=document.createElement('option');
      option.value=value;
      option.textContent=value;
      anomalyFilter.appendChild(option);
    });
}"""
if old_fill not in html:
    raise RuntimeError("fillSelects function was not found")
html = html.replace(old_fill, new_fill, 1)

old_filter = "return (!needle || hay.includes(needle)) && (!type.value || r.group===type.value) && (!status.value || r.status===status.value);"
new_filter = "return (!needle || hay.includes(needle)) && (!anomalyFilter.value || r.anomaly===anomalyFilter.value);"
if old_filter not in html:
    raise RuntimeError("Render filter expression was not found")
html = html.replace(old_filter, new_filter, 1)

html = html.replace(
    "fillSelects(); [q,type,status].forEach(el=>el.addEventListener('input',render)); render();",
    "fillSelects(); [q,anomalyFilter].forEach(el=>el.addEventListener('input',render)); render();",
    1,
)

path.write_text(html, encoding="utf-8")
