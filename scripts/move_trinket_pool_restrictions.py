from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

section = '''<details class="hero-trinket-section" id="trinketPoolRestrictionsSection">
  <summary class="hero-trinket-heading">
    <span class="hero-trinket-title">【装飾品プール禁止事項/Trinket Pool Restrictions】</span>
  </summary>
  <div class="hero-trinket-description">特定の条件下で装飾品プールから除外される項目です。</div>
  <div id="trinketPoolRestrictions" class="groups"></div>
</details>
'''

if 'id="trinketPoolRestrictionsSection"' not in html:
    anchor = '<details class="hero-trinket-section">'
    if anchor not in html:
        raise RuntimeError("Hero trinket details anchor was not found")
    html = html.replace(anchor, section + anchor, 1)

esc_anchor = "function esc(s){ return String(s ?? '').replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',\"'\":'&#39;'}[c])); }"
if "function isTrinketPoolRestrictionName" not in html:
    if esc_anchor not in html:
        raise RuntimeError("esc function anchor was not found")
    html = html.replace(
        esc_anchor,
        esc_anchor + "\nfunction isTrinketPoolRestrictionName(value){ return /Trinket Pool Restrictions|装飾品プール禁止事項/i.test(String(value??'')); }",
        1,
    )

old_select = "[...new Set([...rows.map(r=>r.anomaly),...Object.keys(ANOMALY_DESCRIPTIONS)].filter(Boolean))]\n    .sort((a,b)=>a.localeCompare(b,'ja'))"
new_select = "[...new Set([...rows.map(r=>r.anomaly),...Object.keys(ANOMALY_DESCRIPTIONS)].filter(Boolean))]\n    .filter(value=>!isTrinketPoolRestrictionName(value))\n    .sort((a,b)=>a.localeCompare(b,'ja'))"
if old_select in html:
    html = html.replace(old_select, new_select, 1)
elif new_select not in html:
    raise RuntimeError("Anomaly select source was not found")

old_desc_loop = "Object.keys(ANOMALY_DESCRIPTIONS).forEach(name=>{\n    if(anomalyFilter.value && name!==anomalyFilter.value) return;"
new_desc_loop = "Object.keys(ANOMALY_DESCRIPTIONS).forEach(name=>{\n    if(isTrinketPoolRestrictionName(name)) return;\n    if(anomalyFilter.value && name!==anomalyFilter.value) return;"
if old_desc_loop in html:
    html = html.replace(old_desc_loop, new_desc_loop, 1)
elif new_desc_loop not in html:
    raise RuntimeError("Description anomaly loop was not found")

render_group_anchor = "function renderGroup(group, rowsForGroup){ if(!rowsForGroup.length) return ''; const items=rowsForGroup.slice().sort((a,b)=>a.target.localeCompare(b.target,'ja')).map(renderItem).join(''); return `<section class=\"group\"><div class=\"group-label\"><strong>${esc(group.label)}</strong><span>${esc(group.hint)} / ${rowsForGroup.length}</span></div><div class=\"items\">${items}</div></section>`; }"
render_pool = '''function renderTrinketPoolRestrictions(){
  const container=document.getElementById('trinketPoolRestrictions');
  if(!container) return;
  const poolRows=enrichedRows().filter(row=>isTrinketPoolRestrictionName(row.anomaly));
  const groupsHtml=GROUPS.map(group=>renderGroup(group,poolRows.filter(row=>row.group===group.key))).join('');
  container.innerHTML=groupsHtml||'<div class="empty">掲載項目はありません。</div>';
}'''
if "function renderTrinketPoolRestrictions" not in html:
    if render_group_anchor not in html:
        raise RuntimeError("renderGroup function anchor was not found")
    html = html.replace(render_group_anchor, render_group_anchor + "\n" + render_pool, 1)

old_all = "const all=enrichedRows();"
new_all = "const all=enrichedRows().filter(row=>!isTrinketPoolRestrictionName(row.anomaly));"
if old_all in html:
    html = html.replace(old_all, new_all, 1)
elif new_all not in html:
    raise RuntimeError("Main row source was not found")

html = html.replace("${filtered.length} / ${rows.length} entries", "${filtered.length} / ${all.length} entries", 1)

old_boot = "fillSelects(); [q,anomalyFilter].forEach(el=>el.addEventListener('input',render)); render();"
new_boot = "renderTrinketPoolRestrictions(); fillSelects(); [q,anomalyFilter].forEach(el=>el.addEventListener('input',render)); render();"
if old_boot in html:
    html = html.replace(old_boot, new_boot, 1)
elif new_boot not in html:
    raise RuntimeError("Page boot sequence was not found")

path.write_text(html, encoding="utf-8")
