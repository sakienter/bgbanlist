from __future__ import annotations

import json
import re
from pathlib import Path

INDEX_PATH = Path("index.html")
TITLE = "【装飾品プール禁止事項/Trinket Pool Restrictions】"
DESCRIPTION = "特定の種族構成またはヒーローでは、以下の装飾品は装飾品プールに登場しない。"

NEW_ROWS = [
    {
        "section": "装飾品プール禁止事項",
        "anomaly": TITLE,
        "restriction": "装飾品プールBAN（マーロック出場時）",
        "target": "Double Stitch Needle（ダブルステッチの針）",
        "status": "現行確認",
        "note": "マーロックが出場する対戦では使用不可",
    },
    {
        "section": "装飾品プール禁止事項",
        "anomaly": TITLE,
        "restriction": "装飾品プールBAN（特定ヒーロー）",
        "target": "Chillmere Mosaic（チルメアモザイク）",
        "status": "現行確認",
        "note": "ミルハウス・マナストーム、シンドラゴサでは装飾品プールから除外",
    },
]


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")

    rows_match = re.search(
        r"const rows = (\[.*?\]);\nconst ANOMALY_DESCRIPTIONS",
        html,
        flags=re.DOTALL,
    )
    if not rows_match:
        raise RuntimeError("Could not find rows array")

    rows = json.loads(rows_match.group(1))
    rows = [row for row in rows if row.get("anomaly") != TITLE]
    rows.extend(NEW_ROWS)

    encoded_rows = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    html = html[: rows_match.start(1)] + encoded_rows + html[rows_match.end(1) :]

    descriptions_match = re.search(
        r"const ANOMALY_DESCRIPTIONS = (\{.*?\});\nconst q",
        html,
        flags=re.DOTALL,
    )
    if not descriptions_match:
        raise RuntimeError("Could not find anomaly descriptions")

    descriptions = json.loads(descriptions_match.group(1))
    descriptions[TITLE] = DESCRIPTION

    encoded_descriptions = json.dumps(
        descriptions,
        ensure_ascii=False,
        separators=(",", ":"),
    )
    html = (
        html[: descriptions_match.start(1)]
        + encoded_descriptions
        + html[descriptions_match.end(1) :]
    )

    INDEX_PATH.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
