# bgbanlist

Hearthstone: Battlegrounds の異常別BAN・利用制限を、異常名と対象種別ごとに整理した静的サイトです。

現行パッチで再確認できる制限だけでなく、公式履歴、旧仕様、再抽選・提示候補からの除外、装飾品プールの制限も、確認状態を区別して掲載しています。

> このリポジトリは非公式の情報整理サイトです。ゲーム内仕様や最新の公式パッチノートも併せて確認してください。

## 最近の更新

### 2026-06-15

- READMEを現在の実装に合わせて再構成
- データ追加、表記統一、ソース追加、表示確認の手順を明文化
- ローカル確認方法とCloudflare Pagesの設定を追記

### 2026-06-14

- 異常別BANデータを大幅に追加
- `【ゴルガンネスの天変地異/Golganneth’s Tempest】` のヒーローBANを35名に修正
- 現行35.6系、公式履歴、旧仕様を同一ページ内で区別して表示
- ヒーロー固有の装飾品BANと装飾品プール禁止事項を追加

## 主な機能

- キーワード検索
  - 異常名、対象名、制限区分、確認状態、注記などを検索
  - 英語名と日本語名の両方で検索可能
- 異常名による絞り込み
- 制限対象を5区分で表示
  - `HERO`
  - `MINION / CARD`
  - `TRINKET`
  - `REROLL / OFFER`
  - `SPECIAL`
- 表示中の件数、異常数、対象数を自動集計
- `source.txt`から公式ソース一覧を読み込み
- ページ上部に次の情報を折りたたみ表示
  - 装飾品プール禁止事項
  - ヒーロー固有の装飾品BAN
- PC・スマートフォン対応
- ビルド処理や外部ライブラリを使用しない単一ページ構成

## ファイル構成

```text
.
├── index.html
├── source.txt
├── hero-names.txt
├── Trinkets.txt
├── card-names.txt
├── _headers
└── README.md
```

| ファイル | 用途 |
|---|---|
| `index.html` | 公開ページ本体。HTML、CSS、JavaScript、BANデータを収録 |
| `source.txt` | `View source`に表示するパッチ名と公式URL |
| `hero-names.txt` | ヒーロー名の英日表記マスター |
| `Trinkets.txt` | 装飾品名の英日表記マスター |
| `card-names.txt` | 補足カード名の英日表記マスター |
| `_headers` | Cloudflare Pages用のセキュリティヘッダー |
| `README.md` | 構成、更新方法、公開設定の説明 |

## データ構造

BAN情報は、`index.html`内の`const rows = [...]`にJSON形式で保持しています。

```javascript
{
  "section": "変更されて復活する異常・現行制限",
  "anomaly": "【ゴルガンネスの天変地異/Golganneth’s Tempest】",
  "restriction": "ヒーローBAN（入手不可）",
  "target": "Galakrond（ガラクロンド）",
  "status": "現行確認",
  "note": ""
}
```

| キー | 内容 |
|---|---|
| `section` | 情報の出典区分や整理用セクション |
| `anomaly` | 異常名。日本語名と英語名を併記 |
| `restriction` | BAN・利用制限の種類 |
| `target` | 対象となるヒーロー、カード、装飾品など |
| `status` | 現行確認、公式履歴、旧仕様などの確認状態 |
| `note` | パッチ番号、適用条件、補足説明など |

異常の効果説明は、同じく`index.html`内の`ANOMALY_DESCRIPTIONS`で管理しています。

## 表記規則

### 異常名

```text
【日本語名/English Name】
```

例：

```text
【偽りの偶像/False Idols】
```

### ヒーロー・カード・装飾品

```text
English Name（日本語名）
```

例：

```text
Galakrond（ガラクロンド）
```

公開ページでは末尾の日本語名を表示し、英語名は検索用データとして保持します。

- ヒーロー名は`hero-names.txt`の表記に合わせる
- 装飾品名は`Trinkets.txt`の表記に合わせる
- 補足カード名は`card-names.txt`の表記に合わせる
- 括弧は全角の`（ ）`を使用する

## 表示カテゴリの判定

表示カテゴリは、`restriction`の文言から自動判定されます。データ追加時は、表記によって表示先が変わることに注意してください。

| 判定に使用する語 | 表示カテゴリ |
|---|---|
| `ヒーロー`、`HERO` | `HERO` |
| `装飾品`、`報酬`、`TRINKET` | `TRINKET` |
| `再抽選`、`提示`、`候補`、`Timewarp`、`Mystery Cube` | `REROLL / OFFER` |
| `カード`、`ミニオン`、`酒場呪文`、`CARD`、`MINION` | `MINION / CARD` |
| 上記以外 | `SPECIAL` |

たとえば、カードに関する制限でも`restriction`に「カード」や「ミニオン」が含まれていない場合は、`SPECIAL`に分類されます。

## ソース一覧の更新

`source.txt`には、見出しとURLを1組ずつ記載します。

```text
35.6.2
https://hearthstone.blizzard.com/en-us/news/24271882/35-6-2-patch-notes
```

ページ上部の`View source`を開くと、`source.txt`の内容がリンク一覧として表示されます。

新しい情報を追加する場合は、BANデータだけでなく、根拠となる公式パッチノートや公式フォーラムも`source.txt`へ追加してください。

## 更新手順

1. 公式パッチノートまたは公式フォーラムで制限内容を確認する
2. `source.txt`へパッチ名とURLを追加する
3. `index.html`の`rows`へデータを追加または修正する
4. 必要に応じて`ANOMALY_DESCRIPTIONS`を追加または更新する
5. 新しい固有名詞を各英日表記マスターへ追加する
6. 検索、異常フィルター、カテゴリ、件数表示、ソース一覧を確認する
7. PC表示とスマートフォン表示を確認する
8. `main`ブランチへコミットする

### 更新時の確認項目

- 異常名が`【日本語名/English Name】`になっているか
- 対象名が`English Name（日本語名）`になっているか
- `restriction`の文言と表示カテゴリが一致しているか
- `status`で現行情報と履歴・旧仕様を区別できているか
- 条件付きの制限を`note`へ記載しているか
- 同一異常・同一対象の重複行がないか
- 公式ソースが`source.txt`に登録されているか

## ローカル確認

`source.txt`を`fetch()`で読み込むため、`index.html`を直接開くのではなく、ローカルHTTPサーバーを使用します。

```bash
python3 -m http.server 8000
```

ブラウザで次を開きます。

```text
http://localhost:8000/
```

Node.js、npm、ビルドコマンドは不要です。

## Cloudflare Pages

| 項目 | 設定 |
|---|---|
| Framework preset | `None` |
| Production branch | `main` |
| Build command | 空欄 |
| Build output directory | `/` |

`main`ブランチへコミットすると、自動的に再デプロイされます。

`_headers`では、次のHTTPヘッダーを設定しています。

- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`
- `Content-Security-Policy`

## 掲載状態について

掲載内容には、次のような異なる確認状態が含まれます。

- 現行パッチで直接確認できる制限
- 過去の公式パッチノートに記載された履歴
- 旧シーズン・旧仕様の情報
- 再抽選後も継続する制限
- 提示候補や専用プールからの除外
- 特定の種族構成やヒーローでのみ適用される制限

`status`と`note`を確認し、すべての項目を現在のゲーム内仕様として一律に扱わないでください。
