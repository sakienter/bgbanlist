from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

INDEX_PATH = Path("index.html")
HERO_MASTER_PATH = Path("hero-names.txt")


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    return " ".join(value.strip().split()).casefold()


def load_hero_master() -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in HERO_MASTER_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        match = re.fullmatch(r"(.+?)（(.+?)）", line)
        if not match:
            raise RuntimeError(f"Invalid hero master line: {line}")
        english, japanese = match.groups()
        result[normalize(english)] = f"{english}（{japanese}）"
    return result


HERO_MASTER = load_hero_master()


def hero(name: str) -> str:
    value = HERO_MASTER.get(normalize(name))
    if not value:
        raise RuntimeError(f"Hero not found in hero-names.txt: {name}")
    return value


def swap_anomaly_title(value: str) -> str:
    match = re.fullmatch(r"【(.+?)/\s*(.+?)】", value.strip())
    if not match:
        return value
    first, second = match.groups()
    # Current data is English first. Avoid swapping twice when Japanese is already first.
    if re.search(r"[ぁ-んァ-ヶ一-龠々]", first):
        return f"【{first}/{second}】"
    return f"【{second}/{first}】"


CANONICAL_TITLE_BY_ENGLISH = {
    "Double Header": "【ダブルヘッダー/Double Header】",
    "Eleventh Hour": "【イレブンスアワー/Eleventh Hour】",
    "Elven Elite": "【エルフのエリート/Elven Elite】",
    "Factory Line": "【ファクトリーライン/Factory Line】",
    "Gladiator’s Spoil": "【剣闘士の戦利品/Gladiator’s Spoil】",
    "Gladiator’s Spoils": "【剣闘士の戦利品/Gladiator’s Spoil】",
    "Golden Arrow": "【黄金の矢/Golden Arrow】",
    "Golganneth’s Tempest": "【ゴルガンネスの天変地異/Golganneth’s Tempest】",
    "Titan’s Hook": "【タイタンの鉤爪/Titan’s Hook】",
    "Instant Warband": "【インスタントウォーバンド/Instant Warband】",
    "Match Fixing": "【八百長/Match Fixing】",
    "Mimiron’s Clockwork Stadium": "【ミミロンの時計仕掛けスタジアム/Mimiron’s Clockwork Stadium】",
    "Money Match": "【マネーマッチ/Money Match】",
    "No Face, No Case": "【貌ナシ不起訴処分/No Face, No Case】",
    "Overseer’s Orb": "【監督官のオーブ/Overseer’s Orb】",
    "Path of the Treasure-Seeker": "【トレジャーシーカーの道/Path of the Treasure-Seeker】",
    "Dimensional Displacement": "【次元の配置/Dimensional Displacement】",
    "Scout’s Honor": "【スカウトの名誉/Scout’s Honor】",
    "Secrets of Norgannon": "【ノルガノンの秘密/Secrets of Norgannon】",
    "Tavern Special": "【酒場スペシャル/Tavern Special】",
    "The Golden Arena": "【ゴールデン闘技場/The Golden Arena】",
    "Yogg-iseum": "【ヨッグ座/Yogg-iseum】",
    "Treasure Hoard": "【お宝貯蔵庫/Treasure Hoard】",
    "Lesser Pouches": "【下級袋/Lesser Pouches】",
    "Greater Pouches": "【上級袋/Greater Pouches】",
    "Marin’s Treasure Chest": "【マリンの宝箱/Marin’s Treasure Chest】",
    "Pooled Resources": "【現金書留/Pooled Resources】",
    "Unexpected Portal": "【予想外のポータル/Unexpected Portal】",
}


def english_from_title(value: str) -> str:
    match = re.fullmatch(r"【(.+?)/(.+?)】", value.strip())
    if not match:
        return value
    first, second = match.groups()
    if re.search(r"[ぁ-んァ-ヶ一-龠々]", first):
        return second.strip()
    return first.strip()


def canonical_title(value: str) -> str:
    swapped = swap_anomaly_title(value)
    english = english_from_title(swapped)
    return CANONICAL_TITLE_BY_ENGLISH.get(english, swapped)


LATEST_RESTRICTIONS = {
    "Double Header": ("ヒーローBAN（利用不可）", ["Queen Azshara", "Fungalmancer Flurgl"]),
    "Eleventh Hour": ("ヒーローBAN（利用不可）", ["Alexstrasza"]),
    "Elven Elite": ("ヒーローBAN（利用不可）", ["Patches the Pirate", "Lord Barov", "Heistbaron Togwaggle", "Forest Warden Omu", "Infinite Toki", "Galakrond", "Jim Raynor"]),
    "Factory Line": ("ヒーローBAN（利用不可）", ["N'Zoth"]),
    "Gladiator’s Spoils": ("ヒーローBAN（入手不可）", ["Trade Prince Gallywix"]),
    "Golden Arrow": ("ヒーローBAN（入手不可）", ["Rock Master Voone"]),
    "Golganneth’s Tempest": ("ヒーローBAN（入手不可）", ["Guff Runetotem", "Heistbaron Togwaggle"]),
    "Titan’s Hook": ("ヒーローBAN（入手不可）", ["Guff Runetotem"]),
    "Instant Warband": ("ヒーローBAN（利用不可）", ["Alexstrasza"]),
    "Match Fixing": ("ヒーローBAN（利用不可）", ["A. F. Kay", "Alexstrasza", "Guff Runetotem"]),
    "Mimiron’s Clockwork Stadium": ("ヒーローBAN（利用不可）", ["Jim Raynor", "Fungalmancer Flurgl", "Guff Runetotem", "Elise Starseeker", "Professor Putricide"]),
    "Money Match": ("ヒーローBAN（利用不可）", ["Guff Runetotem"]),
    "No Face, No Case": ("ヒーローBAN（入手不可）", ["Galakrond"]),
    "Overseer’s Orb": ("ヒーローBAN（入手不可）", ["E.T.C., Band Manager", "Nozdormu"]),
    "Path of the Treasure-Seeker": ("ヒーローBAN（利用不可）", ["Arch-Villain Rafaam"]),
    "Dimensional Displacement": ("ヒーローBAN（利用不可）", ["Trade Prince Gallywix", "Fungalmancer Flurgl", "Queen Azshara"]),
    "Scout’s Honor": ("ヒーローBAN（入手不可）", ["Arch-Villain Rafaam"]),
    "Secrets of Norgannon": ("ヒーローBAN（入手不可）", ["Alexstrasza", "Guff Runetotem"]),
    "Tavern Special": ("ヒーローBAN（利用不可）", ["Guff Runetotem", "Artanis", "Lord Jaraxxus", "A. F. Kay"]),
    "The Golden Arena": ("ヒーローBAN（利用不可）", ["Queen Azshara", "Jim Raynor"]),
    "Yogg-iseum": ("ヒーローBAN（利用不可）", ["Queen Azshara", "Galakrond"]),
    "Treasure Hoard": ("ヒーローBAN（入手不可）", ["Zerek, Master Cloner"]),
}

DESCRIPTION_UPDATES = {
    "Lesser Pouches": "「素敵な宝物」を自分の2つ目のヒーローパワーにして開始する。",
    "Greater Pouches": "「増え続けるコレクション」を自分の2つ目のヒーローパワーにして開始する。",
    "Marin’s Treasure Chest": "全ヒーローが「支配人のマリン」になる。「増え続けるコレクション」を自分の2つ目のヒーローパワーにする。",
    "Pooled Resources": "各ターン、チームメイトに最大2ゴールドを送れる。",
    "Unexpected Portal": "この対戦中、ランダムなターンに1回タイムワープを訪れる。",
}


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

    desc_match = re.search(
        r"const ANOMALY_DESCRIPTIONS = (\{.*?\});\nconst q",
        html,
        flags=re.DOTALL,
    )
    if not desc_match:
        raise RuntimeError("Could not find ANOMALY_DESCRIPTIONS")
    descriptions = json.loads(desc_match.group(1))

    # Reorder all anomaly names to Japanese / English.
    for row in rows:
        row["anomaly"] = canonical_title(row["anomaly"])

    reordered_descriptions: dict[str, str] = {}
    for key, value in descriptions.items():
        reordered_descriptions[canonical_title(key)] = value
    descriptions = reordered_descriptions

    # Replace old rows for anomalies covered by the supplied latest restriction list.
    replaced_titles = {
        CANONICAL_TITLE_BY_ENGLISH[english]
        for english in LATEST_RESTRICTIONS
    }
    rows = [row for row in rows if row.get("anomaly") not in replaced_titles]

    for english, (restriction, heroes) in LATEST_RESTRICTIONS.items():
        title = CANONICAL_TITLE_BY_ENGLISH[english]
        for hero_name in heroes:
            rows.append(
                {
                    "section": "変更されて復活する異常・現行制限",
                    "anomaly": title,
                    "restriction": restriction,
                    "target": hero(hero_name),
                    "status": "現行確認",
                    "note": "",
                }
            )

    for english, description in DESCRIPTION_UPDATES.items():
        descriptions[CANONICAL_TITLE_BY_ENGLISH[english]] = description

    encoded_rows = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    html = html[: rows_match.start(1)] + encoded_rows + html[rows_match.end(1) :]

    # Re-find the descriptions after replacing the rows, because offsets changed.
    desc_match = re.search(
        r"const ANOMALY_DESCRIPTIONS = (\{.*?\});\nconst q",
        html,
        flags=re.DOTALL,
    )
    if not desc_match:
        raise RuntimeError("Could not re-find ANOMALY_DESCRIPTIONS")
    encoded_descriptions = json.dumps(descriptions, ensure_ascii=False, separators=(",", ":"))
    html = html[: desc_match.start(1)] + encoded_descriptions + html[desc_match.end(1) :]

    # Display only the Japanese part of target names while retaining bilingual source data.
    if "function displayTarget(" not in html:
        html = html.replace(
            "function renderItem(row){",
            "function displayTarget(value){ const match=String(value??'').match(/（([^（）]+)）$/); return match?match[1]:String(value??''); }\nfunction renderItem(row){",
            1,
        )
    html = html.replace("${esc(row.target)}${note}", "${esc(displayTarget(row.target))}${note}")

    # Include description-only anomalies in the dropdown and the ledger.
    old_fill = "[...new Set(rows.map(r=>r.anomaly).filter(Boolean))]"
    html = html.replace(
        old_fill,
        "[...new Set([...rows.map(r=>r.anomaly),...Object.keys(ANOMALY_DESCRIPTIONS)].filter(Boolean))]",
        1,
    )

    old_by = "function byAnomaly(filtered){ const map=new Map(); filtered.forEach(row => { if(!map.has(row.anomaly)) map.set(row.anomaly, []); map.get(row.anomaly).push(row); }); return [...map.entries()].sort((a,b)=>a[0].localeCompare(b[0],'ja')); }"
    new_by = """function byAnomaly(filtered){
  const map=new Map();
  filtered.forEach(row=>{ if(!map.has(row.anomaly)) map.set(row.anomaly,[]); map.get(row.anomaly).push(row); });
  const needle=q.value.trim().toLowerCase();
  Object.keys(ANOMALY_DESCRIPTIONS).forEach(name=>{
    if(anomalyFilter.value && name!==anomalyFilter.value) return;
    const hay=`${name} ${ANOMALY_DESCRIPTIONS[name]}`.toLowerCase();
    if(needle && !hay.includes(needle) && !map.has(name)) return;
    if(!map.has(name)) map.set(name,[]);
  });
  return [...map.entries()].sort((a,b)=>a[0].localeCompare(b[0],'ja'));
}"""
    if old_by not in html:
        raise RuntimeError("Could not find byAnomaly function")
    html = html.replace(old_by, new_by, 1)

    old_return = "return `<article class=\"anomaly\"><header class=\"anomaly-header\"><div><h2 class=\"anomaly-title\">${esc(name)}</h2>${descriptionHtml}</div><div class=\"count\">${anomalyRows.length} entries</div></header><div class=\"groups\">${groupsHtml}</div></article>`;"
    new_return = "const countHtml=anomalyRows.length?`<div class=\"count\">${anomalyRows.length}件</div>`:''; return `<article class=\"anomaly\"><header class=\"anomaly-header\"><div><h2 class=\"anomaly-title\">${esc(name)}</h2>${descriptionHtml}</div>${countHtml}</header><div class=\"groups\">${groupsHtml}</div></article>`;"
    if old_return not in html:
        raise RuntimeError("Could not find renderAnomaly return")
    html = html.replace(old_return, new_return, 1)

    # Add the reroll persistence notice once.
    if "restriction-note" not in html:
        html = html.replace(
            ".summary { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; }",
            ".restriction-note { margin:0 0 14px; padding:12px 14px; border:1px solid var(--line); background:var(--paper); color:var(--muted); font-size:14px; line-height:1.6; }\n.summary { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; }",
            1,
        )
        html = html.replace(
            '<main><div class="summary" id="summary"></div>',
            '<main><p class="restriction-note">特定の異常が発生している間、以下のヒーローは使用できない、または使用制限が適用されます。これらの制限は再抽選後も継続されます。</p><div class="summary" id="summary"></div>',
            1,
        )

    INDEX_PATH.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
