from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

old_render_group = '''function renderGroup(group, rowsForGroup){ if(!rowsForGroup.length) return ''; const items=rowsForGroup.slice().sort((a,b)=>a.target.localeCompare(b.target,'ja')).map(renderItem).join(''); return `<section class="group"><div class="group-label"><strong>${esc(group.label)}</strong><span>${esc(group.hint)} / ${rowsForGroup.length}</span></div><div class="items">${items}</div></section>`; }'''
new_render_group = '''function renderGroup(group, rowsForGroup){
  if(!rowsForGroup.length) return '';
  const items=rowsForGroup.slice().sort((a,b)=>a.target.localeCompare(b.target,'ja')).map(renderItem).join('');
  const subLabel=group.hint?`${esc(group.hint)} / ${rowsForGroup.length}`:`${rowsForGroup.length}件`;
  return `<section class="group"><div class="group-label"><strong>${esc(group.label)}</strong><span>${subLabel}</span></div><div class="items">${items}</div></section>`;
}'''
if old_render_group not in html:
    raise RuntimeError("renderGroup function was not found")
html = html.replace(old_render_group, new_render_group, 1)

old_pool = '''  const poolRows=enrichedRows().filter(row=>isTrinketPoolRestrictionName(row.anomaly));
  const groupsHtml=GROUPS.map(group=>renderGroup(group,poolRows.filter(row=>row.group===group.key))).join('');'''
new_pool = '''  const poolRows=enrichedRows().filter(row=>isTrinketPoolRestrictionName(row.anomaly));
  const poolGroups=GROUPS.map(group=>group.key==='special'?{...group,label:'登場しないバディ',hint:''}:group);
  const groupsHtml=poolGroups.map(group=>renderGroup(group,poolRows.filter(row=>row.group===group.key))).join('');'''
if old_pool not in html:
    raise RuntimeError("Trinket pool render block was not found")
html = html.replace(old_pool, new_pool, 1)

path.write_text(html, encoding="utf-8")
