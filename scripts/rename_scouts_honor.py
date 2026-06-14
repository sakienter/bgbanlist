from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")
old = "スカウトの名誉"
new = "先行する斥候"
if old not in html:
    raise RuntimeError(f"{old} was not found in index.html")
path.write_text(html.replace(old, new), encoding="utf-8")
