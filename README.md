# bgbanlist

ハースストーン：バトルグラウンドの異常別BAN・利用制限を、異常名と対象種別ごとにまとめた静的サイトです。

## 構成

```text
.
├── index.html   # HTML・CSS・JavaScript・一覧データを含むページ本体
├── _headers     # Cloudflare Pages用HTTPヘッダー
└── README.md
```

## 主な機能

- 異常名・対象・備考の検索
- 対象グループによる絞り込み
- 確認状態による絞り込み
- 異常ごとのグループ表示
- スマートフォン対応

## Cloudflare Pages

GitHub連携でこのリポジトリを選択し、次の設定で公開します。

- Framework preset: `None`
- Production branch: `main`
- Build command: 空欄
- Build output directory: `/`

`main` ブランチへコミットすると、Cloudflare Pages側で自動的に再デプロイされます。

## 更新方法

ページの内容、表示、一覧データはすべて `index.html` にあります。GitHub上で `index.html` を編集してコミットしてください。

## 注意

掲載内容には、現行確認・公式履歴・旧仕様など異なる確認状態が含まれます。各項目の状態表示を確認してください。
