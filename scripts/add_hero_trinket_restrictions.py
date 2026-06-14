from __future__ import annotations

from pathlib import Path

INDEX_PATH = Path("index.html")
TRINKETS_PATH = Path("Trinkets.txt")

TITLE_REPLACEMENTS = {
    "【ヨッグ座/Yogg-iseum】": "【ヨグ＝シアム/Yogg-iseum】",
    "【ファクトリーライン/Factory Line】": "【工場ライン/Factory Line】",
}

TRINKET_ADDITIONS = {
    "Kaboom Bot Portrait（カブーン・ボットの肖像画）",
    "Felblood Portrait（フェルブラッドの肖像画）",
    "Goose Portrait（ガチョウの肖像画）",
}

STYLES = '''
.hero-trinket-section { margin:0 0 18px; border:1px solid var(--line); border-radius:8px; background:var(--panel); box-shadow:var(--shadow); overflow:hidden; }
.hero-trinket-heading { padding:16px 18px 14px; border-bottom:1px solid var(--line); background:var(--paper); }
.hero-trinket-heading h2 { margin:0; font-size:20px; line-height:1.3; }
.hero-trinket-heading p { margin-top:6px; font-size:13px; }
.hero-trinket-categories { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); }
.hero-trinket-category { min-width:0; padding:16px 18px 18px; border-right:1px solid #eeeeea; }
.hero-trinket-category:last-child { border-right:0; }
.hero-trinket-category h3 { margin:0 0 12px; font-size:15px; line-height:1.4; }
.hero-trinket-entry { padding:10px 0; border-top:1px solid #ecebe5; }
.hero-trinket-entry:first-of-type { border-top:0; padding-top:0; }
.hero-trinket-hero { display:block; margin-bottom:5px; font-size:14px; font-weight:650; }
.hero-trinket-name { display:block; color:var(--ink); font-size:14px; line-height:1.55; }
.hero-trinket-note { display:block; margin-top:5px; color:var(--muted); font-size:12px; line-height:1.5; }
.hero-trinket-list { display:grid; gap:4px; }
@media (max-width:900px) { .hero-trinket-categories { grid-template-columns:1fr; } .hero-trinket-category { border-right:0; border-bottom:1px solid #eeeeea; } .hero-trinket-category:last-child { border-bottom:0; } }
'''

SECTION = '''
<section class="hero-trinket-section" aria-labelledby="heroTrinketTitle">
  <div class="hero-trinket-heading">
    <h2 id="heroTrinketTitle">ヒーロー固有の装飾品BAN</h2>
    <p>特定のヒーローに対する装飾品の利用制限と、ヒーローパワー専用プールからの除外情報です。</p>
  </div>
  <div class="hero-trinket-categories">
    <section class="hero-trinket-category">
      <h3>現行35.6.2</h3>
      <div class="hero-trinket-entry">
        <span class="hero-trinket-hero">ミルハウス・マナストーム</span>
        <span class="hero-trinket-name">チルメアモザイク</span>
      </div>
      <div class="hero-trinket-entry">
        <span class="hero-trinket-hero">シンドラゴサ</span>
        <span class="hero-trinket-name">チルメアモザイク</span>
      </div>
    </section>
    <section class="hero-trinket-category">
      <h3>過去の公式BAN履歴</h3>
      <div class="hero-trinket-entry">
        <span class="hero-trinket-hero">ミルハウス・マナストーム</span>
        <span class="hero-trinket-name">リサイクルのステッカー</span>
        <span class="hero-trinket-note">32.4.2時点</span>
      </div>
      <div class="hero-trinket-entry">
        <span class="hero-trinket-hero">オニクシア</span>
        <span class="hero-trinket-name">甲虫のバンド</span>
        <span class="hero-trinket-note">32.2.2時点</span>
      </div>
    </section>
    <section class="hero-trinket-category">
      <h3>ヒーローパワー専用装飾品プールから除外</h3>
      <div class="hero-trinket-entry">
        <span class="hero-trinket-hero">支配人のマリン</span>
        <div class="hero-trinket-list">
          <span class="hero-trinket-name">カブーン・ボットの肖像画</span>
          <span class="hero-trinket-name">永劫の肖像画</span>
          <span class="hero-trinket-name">フェルブラッドの肖像画</span>
          <span class="hero-trinket-name">木彫りのトラ</span>
          <span class="hero-trinket-name">土産物店</span>
          <span class="hero-trinket-name">ガチョウの肖像画</span>
          <span class="hero-trinket-name">魔鏡</span>
        </div>
        <span class="hero-trinket-note">31.2時点。通常の装飾品提示ではなく、ヒーローパワー専用プール。</span>
      </div>
    </section>
  </div>
</section>
'''


def update_index() -> None:
    html = INDEX_PATH.read_text(encoding="utf-8")

    for old, new in TITLE_REPLACEMENTS.items():
        html = html.replace(old, new)

    if ".hero-trinket-section" not in html:
        anchor = ".controls { position:sticky;"
        if anchor not in html:
            raise RuntimeError("Could not find controls style anchor")
        html = html.replace(anchor, STYLES + "\n" + anchor, 1)

    if 'id="heroTrinketTitle"' not in html:
        anchor = '<div class="summary" id="summary"></div>'
        if anchor not in html:
            raise RuntimeError("Could not find summary anchor")
        html = html.replace(anchor, SECTION + anchor, 1)

    INDEX_PATH.write_text(html, encoding="utf-8")


def update_trinket_master() -> None:
    lines = {
        line.strip()
        for line in TRINKETS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    lines.update(TRINKET_ADDITIONS)
    ordered = sorted(lines, key=lambda value: value.casefold())
    TRINKETS_PATH.write_text("\n".join(ordered) + "\n", encoding="utf-8")


def main() -> None:
    update_index()
    update_trinket_master()


if __name__ == "__main__":
    main()
