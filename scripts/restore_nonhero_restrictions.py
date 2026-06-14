from __future__ import annotations

import json
import re
from pathlib import Path

INDEX_PATH = Path("index.html")

ROWS_TO_KEEP = [
    {
        "section": "A. 現行35.6系で直接再確認できるBAN",
        "anomaly": "【ゴルガンネスの天変地異/Golganneth’s Tempest】",
        "restriction": "装飾品BAN",
        "target": "Wisdomball Supply（教育球の補給品）",
        "status": "現行確認",
        "note": "",
    },
    {
        "section": "E. T.C., Band Manager",
        "anomaly": "【ゴルガンネスの天変地異/Golganneth’s Tempest】",
        "restriction": "カードBAN",
        "target": "Knockoff Wisdomball（模倣の教育球）",
        "status": "公式履歴",
        "note": "",
    },
    {
        "section": "O. Elven Elite",
        "anomaly": "【エルフのエリート/Elven Elite】",
        "restriction": "装飾品BAN",
        "target": "Bob-blehead（ボブルヘッド）",
        "status": "公式履歴",
        "note": "",
    },
    {
        "section": "O. Elven Elite",
        "anomaly": "【エルフのエリート/Elven Elite】",
        "restriction": "装飾品BAN",
        "target": "Innkeeper's Stein（酒場の親父のジョッキ）",
        "status": "公式履歴",
        "note": "",
    },
]


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    match = re.search(
        r"const rows = (\[.*?\]);\nconst ANOMALY_DESCRIPTIONS",
        html,
        flags=re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not find rows array")

    rows = json.loads(match.group(1))
    existing = {
        (row.get("anomaly"), row.get("restriction"), row.get("target"))
        for row in rows
    }
    for row in ROWS_TO_KEEP:
        key = (row["anomaly"], row["restriction"], row["target"])
        if key not in existing:
            rows.append(row)
            existing.add(key)

    encoded = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    html = html[: match.start(1)] + encoded + html[match.end(1) :]
    INDEX_PATH.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
