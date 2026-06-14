from __future__ import annotations

import json
import re
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path

INDEX_PATH = Path("index.html")
README_PATH = Path("README.md")
UNRESOLVED_PATH = Path("unresolved-targets.txt")
HERO_MASTER_PATH = Path("hero-names.txt")
BUILD = "233025"
EN_URL = f"https://api.hearthstonejson.com/v1/{BUILD}/enUS/cards.json"
JA_URL = f"https://api.hearthstonejson.com/v1/{BUILD}/jaJP/cards.json"

MANUAL = {
    "Demons": "悪魔",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    return " ".join(value.strip().split()).casefold()


def build_hero_master() -> dict[str, str]:
    master: dict[str, str] = {}
    for raw_line in HERO_MASTER_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.fullmatch(r"(.+?)（(.+?)）", line)
        if not match:
            raise RuntimeError(f"Invalid hero master row: {line}")
        english, japanese = match.groups()
        master[normalize(english)] = f"{english}（{japanese}）"

    # Older source text used the short label "Floop".
    master[normalize("Floop")] = master[normalize("Flobbidinous Floop")]
    return master


HERO_MASTER = build_hero_master()


def download_json(url: str) -> list[dict]:
    request = urllib.request.Request(url, headers={"User-Agent": "bgbanlist-localizer/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def english_part(value: str) -> str:
    return re.sub(r"（[^（）]*）\s*$", "", value).strip()


def candidate_score(card: dict, restriction: str) -> tuple[int, int, str]:
    card_id = str(card.get("id", ""))
    card_type = str(card.get("type", ""))
    score = 0
    if card_id.startswith(("BG", "BGS", "TB_BaconShop")):
        score += 20
    if "ヒーロー" in restriction and card_type == "HERO":
        score += 30
    if "装飾品" in restriction and ("TRINKET" in card_id or "MagicItem" in card_id):
        score += 30
    if any(token in restriction for token in ("カード", "Timewarp", "Mystery Cube")) and card_type != "HERO":
        score += 10
    return (-score, len(card_id), card_id)


def build_lookup(en_cards: list[dict], ja_cards: list[dict]) -> dict[str, list[tuple[dict, str]]]:
    ja_by_id = {card.get("id"): card.get("name") for card in ja_cards if card.get("id") and card.get("name")}
    lookup: dict[str, list[tuple[dict, str]]] = defaultdict(list)
    for card in en_cards:
        card_id = card.get("id")
        english_name = card.get("name")
        japanese_name = ja_by_id.get(card_id)
        if english_name and japanese_name:
            lookup[normalize(english_name)].append((card, japanese_name))
    return lookup


def localized_target(target: str, restriction: str, lookup: dict[str, list[tuple[dict, str]]]) -> str:
    english = english_part(target)

    canonical_hero = HERO_MASTER.get(normalize(english))
    if canonical_hero:
        return canonical_hero

    if english in MANUAL:
        return f"{english}（{MANUAL[english]}）"

    candidates = lookup.get(normalize(english), [])
    if candidates:
        _, japanese = sorted(candidates, key=lambda item: candidate_score(item[0], restriction))[0]
        if japanese and normalize(japanese) != normalize(english):
            return f"{english}（{japanese}）"

    existing = re.search(r"（([^（）]+)）\s*$", target)
    if existing:
        return f"{english}（{existing.group(1)}）"
    return target


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    match = re.search(r"const rows = (\[.*?\]);\nconst q", html, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Could not find rows array in index.html")

    rows = json.loads(match.group(1))
    en_cards = download_json(EN_URL)
    ja_cards = download_json(JA_URL)
    lookup = build_lookup(en_cards, ja_cards)

    unresolved: set[str] = set()
    for row in rows:
        original = row["target"]
        row["target"] = localized_target(original, row.get("restriction", ""), lookup)
        if "（" not in row["target"]:
            unresolved.add(original)

    encoded = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    html = html[: match.start(1)] + encoded + html[match.end(1) :]
    INDEX_PATH.write_text(html, encoding="utf-8")

    UNRESOLVED_PATH.write_text("\n".join(sorted(unresolved)) + ("\n" if unresolved else ""), encoding="utf-8")

    if README_PATH.exists():
        readme = README_PATH.read_text(encoding="utf-8")
        line = "- ヒーロー名は `hero-names.txt` の管理用表記を優先\n"
        if line.strip() not in readme:
            readme = readme.replace(
                "- ヒーロー・カード・装飾品などを `English（日本語）` 形式で表示\n",
                "- ヒーロー・カード・装飾品などを `English（日本語）` 形式で表示\n" + line,
            )
            README_PATH.write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
