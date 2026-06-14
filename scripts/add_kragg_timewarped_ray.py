from pathlib import Path

# One-time updater for the hero-specific restriction section.
path = Path("index.html")
html = path.read_text(encoding="utf-8")

entry = '''      <div class="hero-trinket-entry">
        <span class="hero-trinket-hero">空賊船長クラッグのヒーローパワー所持時</span>
        <span class="hero-trinket-name">時渡のレイ</span>
        <span class="hero-trinket-note">タイムワープの候補から除外</span>
      </div>
'''

if "空賊船長クラッグのヒーローパワー所持時" in html:
    print("Kragg entry already exists")
else:
    anchor = '''        <span class="hero-trinket-note">31.2時点。通常の装飾品提示ではなく、ヒーローパワー専用プール。</span>
      </div>
    </section>'''
    replacement = '''        <span class="hero-trinket-note">31.2時点。通常の装飾品提示ではなく、ヒーローパワー専用プール。</span>
      </div>
''' + entry + '''    </section>'''
    if anchor not in html:
        raise RuntimeError("Target hero-specific restriction section was not found")
    html = html.replace(anchor, replacement, 1)
    path.write_text(html, encoding="utf-8")
    print("Added Kragg / Timewarped Ray restriction")
