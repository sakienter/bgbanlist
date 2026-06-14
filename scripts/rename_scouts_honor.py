from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

replacements = {
    "スカウトの名誉": "先行する斥候",
    "タイタンの鉤爪": "タイタンの引っかけ錨",
}

for old, new in replacements.items():
    if old in html:
        html = html.replace(old, new)
    elif new not in html:
        raise RuntimeError(f"Neither {old} nor {new} was found in index.html")

path.write_text(html, encoding="utf-8")
