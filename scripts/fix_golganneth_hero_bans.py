import json
from pathlib import Path

# Replace only Golganneth's hero restriction rows; keep every other ledger entry unchanged.
path = Path("index.html")
html = path.read_text(encoding="utf-8")

marker = "const rows = "
start = html.find(marker)
if start < 0:
    raise RuntimeError("const rows was not found in index.html")
json_start = start + len(marker)
rows, consumed = json.JSONDecoder().raw_decode(html[json_start:])
json_end = json_start + consumed


def is_golganneth(row):
    anomaly = row.get("anomaly", "")
    return "ゴルガンネス" in anomaly or "Golganneth" in anomaly


def is_target_hero_row(row):
    restriction = row.get("restriction", "")
    return is_golganneth(row) and (
        "ヒーロー" in restriction or "HERO" in restriction.upper()
    )

matching_indices = [i for i, row in enumerate(rows) if is_target_hero_row(row)]
if not matching_indices:
    matching_rows = [row for row in rows if is_golganneth(row)]
    raise RuntimeError(f"Golganneth hero rows were not found. Matching rows: {matching_rows}")

targets = [
    "Galakrond（ガラクロンド）",
    "Trade Prince Gallywix（商大公ガリーウィックス）",
    "The Rat King（ネズミの王）",
    "A. F. Kay（A. F. ケイ）",
    "Sindragosa（シンドラゴサ）",
    "Infinite Toki（無限のトキ）",
    "Yogg-Saron, Hope's End（希望の終焉ヨグ＝サロン）",
    "Elise Starseeker（エリーズ・スターシーカー）",
    "Dinotamer Brann（恐竜使いブラン）",
    "Millhouse Manastorm（ミルハウス・マナストーム）",
    "Tess Greymane（テス・グレイメイン）",
    "Ysera（イセラ）",
    "Fungalmancer Flurgl（菌術師フラァグル）",
    "Nozdormu（ノズドルム）",
    "Maiev Shadowsong（マイエヴ・シャドウソング）",
    "Captain Eudora（ユードラ船長）",
    "Forest Warden Omu（森番オム）",
    "Silas Darkmoon（サイラス・ダークムーン）",
    "Y'Shaarj（ヤシャラージュ）",
    "Tickatus（チケッタス）",
    "Xyrella（ザイレラ）",
    "Overlord Saurfang（サウルファング元帥）",
    "Kurtrus Ashfallen（カートラス・アッシュフォールン）",
    "Scabbs Cutterbutter（スキャブス・カッターバター）",
    "Varden Dawngrasp（ヴァーデン・ドーングラスプ）",
    "Ozumat（オズマット）",
    "Sire Denathrius（デナスリアス陛下）",
    "Enhance-o Mechano（エンハンス・オ・メカーノ）",
    "Professor Putricide（ピュートリサイド教授）",
    "Cap'n Hoggarr（ホガァァァ船長）",
    "E.T.C., Band Manager（バンドマネージャーE.T.C.）",
    "Jim Raynor（ジム・レイナー）",
    "Artanis（アルタニス）",
    "Guff Runetotem（ガフ・ルーントーテム）",
    "Heistbaron Togwaggle（強盗王トグワグル）",
]

if len(targets) != 35 or len(set(targets)) != 35:
    raise RuntimeError("The replacement hero list must contain 35 unique heroes")

template = dict(rows[matching_indices[0]])
first_index = matching_indices[0]
kept_rows = [row for row in rows if not is_target_hero_row(row)]
insert_at = sum(1 for row in rows[:first_index] if not is_target_hero_row(row))

replacement_rows = []
for target in targets:
    row = dict(template)
    row["target"] = target
    row["note"] = ""
    replacement_rows.append(row)

kept_rows[insert_at:insert_at] = replacement_rows
new_json = json.dumps(kept_rows, ensure_ascii=False, separators=(",", ":"))
new_html = html[:json_start] + new_json + html[json_end:]
path.write_text(new_html, encoding="utf-8")

print(
    f"Replaced {len(matching_indices)} Golganneth hero rows with "
    f"{len(replacement_rows)} rows using restriction '{template.get('restriction', '')}'"
)
