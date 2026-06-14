from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

old = '''  const groupsHtml=GROUPS.map(g=>renderGroup(g, anomalyRows.filter(r=>r.group===g.key))).join('');'''
new = '''  const anomalyGroups=GROUPS.map(group=>{
    const groupRows=anomalyRows.filter(row=>row.group===group.key);
    if(group.key==='special' && groupRows.some(row=>/異常効果による内容変更/.test(row.restriction))){
      return {...group,label:'バディの内容が変更されるヒーロー',hint:''};
    }
    return group;
  });
  const groupsHtml=anomalyGroups.map(group=>renderGroup(group, anomalyRows.filter(row=>row.group===group.key))).join('');'''

if old not in html:
    raise RuntimeError("renderAnomaly group block was not found")
html = html.replace(old, new, 1)
path.write_text(html, encoding="utf-8")
