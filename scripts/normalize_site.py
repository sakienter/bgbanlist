from __future__ import annotations

import json
import re
from pathlib import Path

INDEX_PATH = Path("index.html")
README_PATH = Path("README.md")

ANOMALY_NAMES = {
    "A Faire Reward": "【A Faire Reward/ フェア報酬】",
    "Anomalous Cube / Mystery Cube (異常なキューブ)": "【Anomalous Cube/ 異常な立方体】",
    "Anomalous Expedition (異常な探検)": "【Anomalous Expedition/ 異常な探検】",
    "Anomalous Wisdomball": "【Anomalous Wisdomball/ 異常な教育球】",
    "Audience’s Choice": "【Audience’s Choice/ 観客の選択】",
    "Big League": "【Big League/ 大リーグ】",
    "Bring Home the Bacon": "【Bring Home the Bacon/ ベーコン熟成】",
    "Bring in the Buddies": "【Bring in the Buddies/ カモン、エブリバディ】",
    "Continuing Education": "【Continuing Education/ 生涯教育】",
    "Elven Elite": "【Elven Elite/ エルフのエリート】",
    "Emergency Landing": "【Emergency Landing/ 緊急着水】",
    "False Idols (偽りの偶像)": "【False Idols/ 偽りの偶像】",
    "Galakrond": "【Galakrond/ ガラクロンド】",
    "Gladiator’s Spoils": "【Gladiator’s Spoil/ 剣闘士の戦利品】",
    "Golden Arrow": "【Golden Arrow/ 黄金の矢】",
    "Golden Friendship": "【Golden Friendship/ 黄金の友情】",
    "Golganneth’s Tempest (ゴルガンネスの天変地異)": "【Golganneth’s Tempest/ ゴルガンネスの天変地異】",
    "Greater Pouches": "【Greater Pouches/ 上級袋】",
    "Impressive Foresight": "【Impressive Foresight/ 素晴らしい先見性】",
    "Incubation Mutation": "【Incubation Mutation/ 培養変異体】",
    "Lesser Fortune (下級の幸運)": "【Lesser Fortune/ 下級運勢】",
    "Lesser Pouches": "【Lesser Pouches/ 下級袋】",
    "Light the Way": "【Light the Way/ 道を照らす光】",
    "Line in the Sand": "【Line in the Sand/ 砂の覚醒】",
    "Magic Shop": "【Magic Shop/ 魔法の店】",
    "Match Fixing": "【Match Fixing/ 八百長】",
    "Money Match": "【Money Match/ マネーマッチ】",
    "No Face, No Case": "【No Face, No Case/ 貌ナシ不起訴処分】",
    "Oathstone’s Summoning (オースストーンの召喚)": "【Oathstone’s Summoning/ オースストーンの召喚】",
    "Packed Stands": "【Packed Stands/ スタンド満員】",
    "Path of the Treasure-Seeker": "【Path of the Treasure-Seeker/ トレジャーシーカーの道】",
    "Pooled Resources": "【Pooled Resources/ 現金書留】",
    "Secrets of Norgannon": "【Secrets of Norgannon/ ノルガノンの秘密】",
    "Tavern Special": "【Tavern Special/ 酒場スペシャル】",
    "Treasure Hoard": "【Treasure Hoard/ お宝貯蔵庫】",
    "Uncompensated Upset": "【Uncompensated Upset/ 補償なき市場】",
    "ゴールデン闘技場": "【The Golden Arena/ ゴールデン闘技場】",
    "ミミロンの時計仕掛けスタジアム": "【Mimiron’s Clockwork Stadium/ ミミロンの時計仕掛けスタジアム】",
    "偽りの偶像": "【False Idols/ 偽りの偶像】",
}

PLAIN_ITEM_CSS = """.items { display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:0 18px; align-content:start; padding:7px 14px 12px; }
.item { display:block; max-width:100%; border:0; border-bottom:1px solid #ecebe5; border-radius:0; background:transparent; padding:9px 0; line-height:1.35; font-size:14px; }
.item::before { content:\"— \"; color:var(--muted); }
.item.hero, .item.card, .item.trinket, .item.reroll, .item.special { background:transparent; border-color:#ecebe5; }
"""


def update_rows(html: str) -> str:
    match = re.search(r"const rows = (\[.*?\]);\nconst q", html, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Could not find the rows array in index.html")

    rows = json.loads(match.group(1))
    unknown = sorted({row["anomaly"] for row in rows if row["anomaly"] not in ANOMALY_NAMES and not row["anomaly"].startswith("【")})
    if unknown:
        raise RuntimeError(f"Missing anomaly name mappings: {unknown}")

    for row in rows:
        row["anomaly"] = ANOMALY_NAMES.get(row["anomaly"], row["anomaly"])

    new_rows = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    return html[: match.start(1)] + new_rows + html[match.end(1) :]


def update_item_style(html: str) -> str:
    pattern = re.compile(
        r"\.items \{[^\n]*\} \.item \{[^\n]*\}\n"
        r"\.item\.hero \{[^\n]*\} \.item\.card \{[^\n]*\} \.item\.trinket \{[^\n]*\} \.item\.reroll \{[^\n]*\} \.item\.special \{[^\n]*\}\n"
    )
    updated, count = pattern.subn(PLAIN_ITEM_CSS, html, count=1)
    if count != 1:
        raise RuntimeError("Could not replace the rounded item styles")
    return updated


def update_readme() -> None:
    if not README_PATH.exists():
        return
    readme = README_PATH.read_text(encoding="utf-8")
    marker = "- 異常名を `【英語名/ 日本語名】` 形式で表示\n- ヒーロー・カードなどの対象を囲みのないテキスト一覧で表示\n"
    if "異常名を `【英語名/ 日本語名】` 形式で表示" not in readme:
        readme = readme.replace("## 主な機能\n\n", "## 主な機能\n\n" + marker)
        README_PATH.write_text(readme, encoding="utf-8")


def main() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")
    html = update_rows(html)
    html = update_item_style(html)
    INDEX_PATH.write_text(html, encoding="utf-8")
    update_readme()


if __name__ == "__main__":
    main()
