from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

old_css = '''.hero-trinket-heading { padding:16px 18px 14px; border-bottom:1px solid var(--line); background:var(--paper); }
.hero-trinket-heading h2 { margin:0; font-size:20px; line-height:1.3; }
.hero-trinket-heading p { margin-top:6px; font-size:13px; }'''
new_css = '''.hero-trinket-heading { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:16px 18px; background:var(--paper); cursor:pointer; list-style:none; }
.hero-trinket-heading::-webkit-details-marker { display:none; }
.hero-trinket-heading::after { content:"＋"; flex:0 0 auto; color:var(--muted); font-size:20px; line-height:1; }
.hero-trinket-section[open] .hero-trinket-heading { border-bottom:1px solid var(--line); }
.hero-trinket-section[open] .hero-trinket-heading::after { content:"−"; }
.hero-trinket-title { font-size:20px; font-weight:700; line-height:1.3; }
.hero-trinket-description { padding:12px 18px; border-bottom:1px solid #eeeeea; color:var(--muted); font-size:13px; line-height:1.55; }'''
if old_css not in html:
    raise RuntimeError("Hero trinket heading CSS was not found")
html = html.replace(old_css, new_css, 1)

old_start = '''<section class="hero-trinket-section" aria-labelledby="heroTrinketTitle">
  <div class="hero-trinket-heading">
    <h2 id="heroTrinketTitle">ヒーロー固有の装飾品BAN</h2>
    <p>特定のヒーローに対する装飾品の利用制限と、ヒーローパワー専用プールからの除外情報です。</p>
  </div>
  <div class="hero-trinket-categories">'''
new_start = '''<details class="hero-trinket-section">
  <summary class="hero-trinket-heading">
    <span class="hero-trinket-title">ヒーロー固有の装飾品BAN</span>
  </summary>
  <div class="hero-trinket-description">特定のヒーローに対する装飾品の利用制限と、ヒーローパワー専用プールからの除外情報です。</div>
  <div class="hero-trinket-categories">'''
if old_start not in html:
    raise RuntimeError("Hero trinket section start was not found")
html = html.replace(old_start, new_start, 1)

old_end = '''  </div>
</section>
<div class="summary" id="summary"></div>'''
new_end = '''  </div>
</details>
<div class="summary" id="summary"></div>'''
if old_end not in html:
    raise RuntimeError("Hero trinket section end was not found")
html = html.replace(old_end, new_end, 1)

path.write_text(html, encoding="utf-8")
