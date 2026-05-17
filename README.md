# Mermaid 入門 — 理工系大学生のためのチュートリアル

理工系大学生が **Mermaid** でフローチャート・シーケンス図・クラス図・
状態遷移図・ER 図・ガントチャートを描けるようになることを目的とした
日本語チュートリアルです。MkDocs Material で組まれており、GitHub Pages
で公開されます。

## ローカルでプレビュー

```bash
uv sync
uv run mkdocs serve
```

ブラウザで <http://127.0.0.1:8000> を開きます。

## ビルド

```bash
uv run mkdocs build
```

`site/` ディレクトリに静的サイトが生成されます。

## 写真の再取得

Wikimedia Commons から CC/PD 画像をダウンロードしなおすには：

```bash
uv run scripts/download_photos.py
```

## GitHub Pages への公開手順

1. GitHub 上に新しいリポジトリを作る
2. このディレクトリで以下を実行（リポジトリ URL を置き換えて）：
   ```bash
   git remote add origin https://github.com/<USER>/<REPO>.git
   git branch -M main
   git push -u origin main
   ```
3. GitHub のリポジトリ設定 → **Settings → Pages** で  
   **Source: GitHub Actions** を選択
4. `main` への push 後、Actions タブで `Deploy MkDocs site to GitHub Pages`
   ワークフローが緑になれば、公開 URL は `https://<USER>.github.io/<REPO>/`

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
