from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")
old = "return {...group,label:'バディの内容が変更されるヒーロー',hint:''};"
new = "return {...group,label:'登場しないバディ',hint:''};"
if old not in html:
    raise RuntimeError("Buddy change group label was not found")
path.write_text(html.replace(old, new, 1), encoding="utf-8")
