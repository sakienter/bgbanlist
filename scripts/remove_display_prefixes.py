from __future__ import annotations

import json
import re
from pathlib import Path

INDEX_PATH = Path("index.html")


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")

    descriptions_match = re.search(
        r"const ANOMALY_DESCRIPTIONS = (\{.*?\});\nconst q",
        html,
        flags=re.DOTALL,
    )
    if not descriptions_match:
        raise RuntimeError("Could not find ANOMALY_DESCRIPTIONS")

    descriptions = json.loads(descriptions_match.group(1))
    descriptions = {
        key: re.sub(r"^\s*\[x\]\s*", "", value).strip()
        for key, value in descriptions.items()
    }

    encoded = json.dumps(descriptions, ensure_ascii=False, separators=(",", ":"))
    html = (
        html[: descriptions_match.start(1)]
        + encoded
        + html[descriptions_match.end(1) :]
    )

    html = re.sub(
        r"\s*\.item::before\s*\{\s*content:\s*[\"']—\s*[\"'];\s*color:\s*var\(--muted\);\s*\}\s*",
        "\n",
        html,
        count=1,
    )

    INDEX_PATH.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
