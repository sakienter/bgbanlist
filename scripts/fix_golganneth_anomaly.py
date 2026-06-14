from __future__ import annotations

import json
import re
from pathlib import Path

INDEX_PATH = Path("index.html")
OLD_NAME = "【Galakrond/ ガラクロンド】"
NEW_NAME = "【Golganneth’s Tempest/ ゴルガンネスの天変地異】"


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")

    rows_match = re.search(
        r"const rows = (\[.*?\]);\nconst ANOMALY_DESCRIPTIONS",
        html,
        flags=re.DOTALL,
    )
    if not rows_match:
        raise RuntimeError("Could not find the rows array")

    rows = json.loads(rows_match.group(1))
    changed = 0
    for row in rows:
        if row.get("anomaly") == OLD_NAME:
            row["anomaly"] = NEW_NAME
            changed += 1

    encoded_rows = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    html = html[: rows_match.start(1)] + encoded_rows + html[rows_match.end(1) :]

    descriptions_match = re.search(
        r"const ANOMALY_DESCRIPTIONS = (\{.*?\});\nconst q",
        html,
        flags=re.DOTALL,
    )
    if not descriptions_match:
        raise RuntimeError("Could not find the anomaly description map")

    descriptions = json.loads(descriptions_match.group(1))
    descriptions.pop(OLD_NAME, None)
    descriptions.setdefault(
        NEW_NAME,
        "最初の7ターンの終了時、自分の戦団の左端のミニオンに+1/+1を付与する。その後、付与する値を2倍にする。",
    )

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
    print(f"Merged {changed} rows into {NEW_NAME}")


if __name__ == "__main__":
    main()
