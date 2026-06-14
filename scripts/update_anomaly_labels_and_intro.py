from __future__ import annotations

import json
import re
from pathlib import Path

INDEX_PATH = Path("index.html")

TITLE_RENAMES = {
    "【イレブンスアワー/Eleventh Hour】": "【死に背く士/Eleventh Hour】",
    "【インスタントウォーバンド/Instant Warband】": "【即席戦団/Instant Warband】",
}

TREASURE_HOARD_TITLE = "【お宝貯蔵庫/Treasure Hoard】"
TREASURE_HOARD_TEXT = """9ターン目に、グレード7の ゴールデンミニオンを 1体発見する。
8ターン目に、グレード6の ゴールデンミニオンを 1体発見する。
7ターン目に、グレード5の ゴールデンミニオンを 1体発見する。
6ターン目に、グレード4の ゴールデンミニオンを 1体発見する。
5ターン目に、グレード3の ゴールデンミニオンを 1体発見する。"""

OLD_INTRO = "Grouped by anomaly, then by target type. This keeps the original source rows intact while making the ledger easier to scan."
NEW_INTRO = "Hearthstone Battlegrounds のBAN情報をまとめたサイトです。ソース（情報元）は明記しておりますが、BANの解除やアップデートにより、一部情報が古くなっている場合があります。あらかじめご了承ください。"


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")

    # Header introduction.
    if OLD_INTRO not in html:
        raise RuntimeError("Header introduction text was not found")
    html = html.replace(OLD_INTRO, NEW_INTRO, 1)

    # Preserve line breaks in multi-line anomaly descriptions.
    html = html.replace(
        ".anomaly-description { margin:9px 0 0; max-width:820px; color:var(--muted); font-size:14px; line-height:1.65; }",
        ".anomaly-description { margin:9px 0 0; max-width:820px; color:var(--muted); font-size:14px; line-height:1.65; white-space:pre-line; }",
        1,
    )

    rows_match = re.search(
        r"const rows = (\[.*?\]);\nconst ANOMALY_DESCRIPTIONS",
        html,
        flags=re.DOTALL,
    )
    if not rows_match:
        raise RuntimeError("Could not find rows array")

    rows = json.loads(rows_match.group(1))
    for row in rows:
        row["anomaly"] = TITLE_RENAMES.get(row.get("anomaly"), row.get("anomaly"))

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
    for old_title, new_title in TITLE_RENAMES.items():
        if old_title in descriptions:
            descriptions[new_title] = descriptions.pop(old_title)

    descriptions[TREASURE_HOARD_TITLE] = TREASURE_HOARD_TEXT

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
