# bgbanlist

ハースストーン：バトルグラウンドの異常別BAN・利用制限を、異常名と対象種別ごとにまとめた静的サイトです。

## 構成

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

- `index.html`: 公開ページ本体
- `source.txt`: `View source` に表示するパッチ名と公式URL
- `hero-names.txt`: ヒーロー名の英日表記マスター
- `Trinkets.txt`: 装飾品名の英日表記マスター
- `card-names.txt`: 補足カード名の英日表記マスター
- `_headers`: Cloudflare Pages用HTTPヘッダー

## 表記

- 異常名：`【日本語名/English Name】`
- ヒーロー・カード・装飾品：公開ページでは日本語名のみ表示
- 検索用の元データには英語名と日本語名の両方を保持
- ヒーロー名は `hero-names.txt` の表記を使用
- 装飾品名は `Trinkets.txt` の表記を使用

## ヒーロー固有の装飾品BAN

公開ページ上部に、次の3区分を独立したセクションとして掲載しています。

- 現行のヒーロー固有BAN
- 過去の公式BAN履歴
- ヒーローパワー専用装飾品プールからの除外

通常の異常別一覧とは別の情報として管理します。

## ソース一覧の更新

`source.txt` に、見出しとURLを1組ずつ記載します。

```text
35.6
https://example.com/patch-notes
```

ページ上部の `View source` ボタンを押すと、内容がリンク一覧として表示されます。

## Cloudflare Pages

- Framework preset: `None`
- Production branch: `main`
- Build command: 空欄
- Build output directory: `/`

`main` ブランチへコミットすると自動的に再デプロイされます。

## 注意

掲載内容には、現行確認・公式履歴・旧仕様など異なる確認状態が含まれます。最新制限として追加した項目は、再抽選後も制限が継続する前提で掲載しています。
