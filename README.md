# bgbanlist

ハースストーン：バトルグラウンドの、異常ごとのBAN・利用制限を検索できる静的サイトです。

## 構成

```text
.
├── index.html        # ページ本体
├── styles.css        # 最小限の表示スタイル
├── app.js            # 検索・絞り込み処理
├── data/
│   ├── rows-01.js    # 一覧データ
│   ├── rows-02.js
│   ├── rows-03.js
│   ├── rows-04.js
│   └── rows-05.js
├── _headers          # Cloudflare Pages用HTTPヘッダー
└── README.md
```

## ローカル確認

単純に `index.html` を開くこともできます。ローカルサーバーを使う場合は、リポジトリ直下で次を実行します。

```bash
python3 -m http.server 8000
```

その後、ブラウザで `http://localhost:8000` を開きます。

## Cloudflare Pages

GitHub連携でこのリポジトリを選択し、以下の設定で公開できます。

- Framework preset: `None`
- Production branch: `main`
- Build command: 空欄
- Build output directory: `/`

`main` ブランチにコミットすると、Cloudflare Pages側で自動的に再デプロイされます。

## データ更新

一覧データは `data/rows-01.js` から `data/rows-05.js` に分割されています。各ファイルの配列へ、次の形式で行を追加します。

```js
{
  section: "区分",
  anomaly: "異常名",
  restriction: "制限内容",
  target: "対象",
  status: "確認状態",
  note: "備考"
}
```

データ変更後は、カンマの不足や余分なカンマに注意してください。

## 注意

掲載内容には、現行確認・公式履歴・旧仕様など異なる確認状態が含まれます。データの正確性は各行の状態と備考を確認してください。
