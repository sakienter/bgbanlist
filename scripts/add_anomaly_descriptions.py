from __future__ import annotations

import html
import json
import re
import unicodedata
import urllib.request
from collections import defaultdict
from pathlib import Path

INDEX_PATH = Path("index.html")
UNRESOLVED_PATH = Path("unresolved-anomaly-descriptions.txt")
BUILD = "233025"
EN_URL = f"https://api.hearthstonejson.com/v1/{BUILD}/enUS/cards.json"
JA_URL = f"https://api.hearthstonejson.com/v1/{BUILD}/jaJP/cards.json"

MANUAL = {
    "Anomalous Cube": "「謎めいた立方体」を自分の2つ目のヒーローパワーにして開始する。それは5ターン目に解禁される。",
    "Anomalous Expedition": "対戦の開始時、グレード6、4、2のミニオンを1体ずつ発見し、それぞれのグレード到達時にそれらを獲得する。",
    "Lesser Fortune": "「下級水晶玉」を自分の2つ目のヒーローパワーにして開始する。下級水晶玉は、自分が下級装飾品を買う時、それのコピーに変身する。",
    "Oathstone’s Summoning": "7ターン目に小さなタイムワープのミニオンを酒場のプールに入れ、10ターン目に大きなタイムワープのミニオンを同プールに入れる。",
    "Galakrond": "異常名の分類を確認中です。",
}

ALIASES = {
    "Gladiator’s Spoil": "Gladiator's Spoils",
    "The Golden Arena": "The Golden Arena",
    "Mimiron’s Clockwork Stadium": "Mimiron's Clockwork Stadium",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    return " ".join(value.strip().split()).casefold()


def download_json(url: str) -> list[dict]:
    request = urllib.request.Request(url, headers={"User-Agent": "bgbanlist-description-builder/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def strip_markup(value: str) -> str:
    value = value.replace("\\n", " ").replace("\n", " ")
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s*（あと\d+ターン！）\s*$", "", value)
    return value


def english_anomaly_name(display_name: str) -> str:
    match = re.fullmatch(r"【(.+?)/\s*(.+?)】", display_name.strip())
    if match:
        return match.group(1).strip()
    return display_name.strip()


def build_lookup(en_cards: list[dict], ja_cards: list[dict]) -> dict[str, list[tuple[dict, str]]]:
    ja_by_id = {card.get("id"): card for card in ja_cards if card.get("id")}
    lookup: dict[str, list[tuple[dict, str]]] = defaultdict(list)
    for en_card in en_cards:
        card_id = en_card.get("id")
        english_name = en_card.get("name")
        ja_card = ja_by_id.get(card_id)
        if not english_name or not ja_card:
            continue
        japanese_text = ja_card.get("text") or ""
        if japanese_text:
            lookup[normalize(english_name)].append((en_card, japanese_text))
    return lookup


def candidate_score(card: dict) -> tuple[int, int, str]:
    card_id = str(card.get("id", ""))
    score = 0
    if "Anomaly" in card_id or "ANOMALY" in card_id:
        score += 100
    if card_id.startswith(("BG", "BGS", "TB_BaconShop")):
        score += 30
    if card.get("set") == "BATTLEGROUNDS":
        score += 20
    return (-score, len(card_id), card_id)


def description_for(name: str, lookup: dict[str, list[tuple[dict, str]]]) -> str:
    if name in MANUAL:
        return MANUAL[name]

    lookup_name = ALIASES.get(name, name)
    candidates = lookup.get(normalize(lookup_name), [])
    if not candidates:
        return ""

    _, text = sorted(candidates, key=lambda item: candidate_score(item[0]))[0]
    return strip_markup(text)


def insert_or_replace_descriptions(html_text: str, descriptions: dict[str, str]) -> str:
    encoded = json.dumps(descriptions, ensure_ascii=False, separators=(",", ":"))
    declaration = f"const ANOMALY_DESCRIPTIONS = {encoded};\n"

    if "const ANOMALY_DESCRIPTIONS =" in html_text:
        html_text = re.sub(
            r"const ANOMALY_DESCRIPTIONS = \{.*?\};\n",
            declaration,
            html_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        html_text = html_text.replace("const q =", declaration + "const q =", 1)

    if ".anomaly-description" not in html_text:
        html_text = html_text.replace(
            ".anomaly-title { margin:0; font-size:21px; line-height:1.25; letter-spacing:0; }",
            ".anomaly-title { margin:0; font-size:21px; line-height:1.25; letter-spacing:0; }\n.anomaly-description { margin:9px 0 0; max-width:820px; color:var(--muted); font-size:14px; line-height:1.65; }",
            1,
        )

    pattern = re.compile(
        r"function renderAnomaly\(name, anomalyRows\)\{.*?\n\}",
        flags=re.DOTALL,
    )
    replacement = '''function renderAnomaly(name, anomalyRows){
  const description=ANOMALY_DESCRIPTIONS[name]||'';
  const descriptionHtml=description?`<p class="anomaly-description">${esc(description)}</p>`:'';
  const groupsHtml=GROUPS.map(g=>renderGroup(g, anomalyRows.filter(r=>r.group===g.key))).join('');
  return `<article class="anomaly"><header class="anomaly-header"><div><h2 class="anomaly-title">${esc(name)}</h2>${descriptionHtml}</div><div class="count">${anomalyRows.length} entries</div></header><div class="groups">${groupsHtml}</div></article>`;
}'''
    html_text, count = pattern.subn(replacement, html_text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace renderAnomaly function")

    return html_text


def main() -> None:
    source = INDEX_PATH.read_text(encoding="utf-8")
    rows_match = re.search(r"const rows = (\[.*?\]);\nconst ", source, flags=re.DOTALL)
    if not rows_match:
        raise RuntimeError("Could not find rows array")

    rows = json.loads(rows_match.group(1))
    anomaly_names = sorted({row["anomaly"] for row in rows})

    en_cards = download_json(EN_URL)
    ja_cards = download_json(JA_URL)
    lookup = build_lookup(en_cards, ja_cards)

    descriptions: dict[str, str] = {}
    unresolved: list[str] = []
    for display_name in anomaly_names:
        english_name = english_anomaly_name(display_name)
        description = description_for(english_name, lookup)
        if description:
            descriptions[display_name] = description
        else:
            unresolved.append(display_name)

    updated = insert_or_replace_descriptions(source, descriptions)
    INDEX_PATH.write_text(updated, encoding="utf-8")
    UNRESOLVED_PATH.write_text("\n".join(unresolved) + ("\n" if unresolved else ""), encoding="utf-8")


if __name__ == "__main__":
    main()
