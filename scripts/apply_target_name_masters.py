from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

INDEX_PATH = Path("index.html")
TRINKETS_PATH = Path("Trinkets.txt")
CARDS_PATH = Path("card-names.txt")
README_PATH = Path("README.md")


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    return " ".join(value.strip().split()).casefold()


def english_part(value: str) -> str:
    return re.sub(r"（[^（）]*）\s*$", "", value).strip()


def load_master(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.fullmatch(r"(.+?)（(.+?)）", line)
        if not match:
            raise RuntimeError(f"Invalid master entry in {path}: {line}")
        english, japanese = match.groups()
        result[normalize(english)] = f"{english}（{japanese}）"
    return result


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    match = re.search(r"const rows = (\[.*?\]);\nconst ANOMALY_DESCRIPTIONS", html, flags=re.DOTALL)
    if not match:
        match = re.search(r"const rows = (\[.*?\]);\nconst q", html, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Could not find rows array in index.html")

    rows = json.loads(match.group(1))
    masters = {}
    masters.update(load_master(TRINKETS_PATH))
    masters.update(load_master(CARDS_PATH))

    changed = 0
    for row in rows:
        current = row["target"]
        canonical = masters.get(normalize(english_part(current)))
        if canonical and canonical != current:
            row["target"] = canonical
            changed += 1

    encoded = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    updated = html[: match.start(1)] + encoded + html[match.end(1) :]
    INDEX_PATH.write_text(updated, encoding="utf-8")

    if README_PATH.exists():
        readme = README_PATH.read_text(encoding="utf-8")
        readme = readme.replace(
            "├── hero-names.txt\n├── _headers",
            "├── hero-names.txt\n├── Trinkets.txt\n├── card-names.txt\n├── _headers",
        )
        if "`Trinkets.txt`" not in readme:
            readme += "\n- `Trinkets.txt`: 装飾品名の英日表記マスター\n"
        if "`card-names.txt`" not in readme:
            readme += "- `card-names.txt`: 補足カード名の英日表記マスター\n"
        README_PATH.write_text(readme, encoding="utf-8")

    print(f"Updated {changed} target rows.")


if __name__ == "__main__":
    main()
