from pathlib import Path

OLD = "カブーン・ボットの肖像画"
NEW = "ブーマーロボの肖像画"

for filename in ("index.html", "Trinkets.txt"):
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    if OLD not in text:
        raise RuntimeError(f"{OLD} was not found in {filename}")
    path.write_text(text.replace(OLD, NEW), encoding="utf-8")
