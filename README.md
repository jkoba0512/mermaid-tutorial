# Mermaid 入門 — 理工系大学生のためのチュートリアル

理工系大学生が **Mermaid** でフローチャート・シーケンス図・クラス図・
状態遷移図・ER 図・ガントチャートを描けるようになることを目的とした
日本語チュートリアルです。

**👉 公開サイト: <https://jkoba0512.github.io/mermaid-tutorial/>**

MkDocs Material で組まれており、`main` ブランチへの push をトリガーに
GitHub Actions が自動でビルド・デプロイします。

## ファイル構成

```
.
├── docs/                       # チュートリアル本文（Markdown）
│   ├── index.md                # 表紙
│   ├── 00-setup.md             # 5分で試す
│   ├── 01-basics.md            # 文法ルール
│   ├── 02-flowchart.md         # フローチャート
│   ├── 03-sequence.md          # シーケンス図
│   ├── 04-class.md             # クラス図
│   ├── 05-state.md             # 状態遷移図
│   ├── 06-er.md                # ER 図
│   ├── 07-gantt.md             # ガントチャート
│   ├── 08-cheatsheet.md        # 付録A: チートシート
│   ├── 09-faq.md               # 付録B: FAQ
│   ├── credits.md              # 画像の出典
│   ├── images/                 # Wikimedia の写真
│   └── stylesheets/extra.css
├── scripts/
│   └── download_photos.py      # 写真取得（uv inline script）
├── .github/workflows/deploy.yml
├── mkdocs.yml
├── pyproject.toml
├── .gitignore
└── README.md
```

## ライセンス

- 本文（`docs/*.md`）: CC BY 4.0
- 画像: 各画像のページに記載のライセンス（[credits.md](docs/credits.md)）
