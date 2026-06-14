# bgbanlist

ハースストーン：バトルグラウンドの異常別BAN・利用制限を、異常名と対象種別ごとにまとめた静的サイトです。

## 構成

```text
.
├── index.html
├── hero-names.txt
├── Trinkets.txt
├── card-names.txt
├── _headers
└── README.md
```

- `index.html`: 公開ページ本体
- `hero-names.txt`: ヒーロー名の英日表記マスター
- `_headers`: Cloudflare Pages用HTTPヘッダー

## 表記

- 異常名：`【英語名/ 日本語名】`
- ヒーロー・カード・装飾品：`English（日本語）`
- ヒーロー名は `hero-names.txt` の表記を使用

## Cloudflare Pages

- Framework preset: `None`
- Production branch: `main`
- Build command: 空欄
- Build output directory: `/`

`main` ブランチへコミットすると自動的に再デプロイされます。

## 注意

掲載内容には、現行確認・公式履歴・旧仕様など異なる確認状態が含まれます。

- `Trinkets.txt`: 装飾品名の英日表記マスター
- `card-names.txt`: 補足カード名の英日表記マスター
