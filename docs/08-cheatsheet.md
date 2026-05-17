# 付録A — チートシート

一画面に押し込んだリファレンス。困ったらここに戻ってきてください。

## 図の種類と最初の行

| 図 | 最初の行 |
|---|---|
| フローチャート（上→下） | `flowchart TD` |
| フローチャート（左→右） | `flowchart LR` |
| シーケンス図 | `sequenceDiagram` |
| クラス図 | `classDiagram` |
| 状態遷移図 | `stateDiagram-v2` |
| ER 図 | `erDiagram` |
| ガントチャート | `gantt` |

## フローチャート — ノードの形

| コード | 形 | 用途 |
|---|---|---|
| `A[テキスト]` | 長方形 | 処理 |
| `A(テキスト)` | 角丸長方形 | 通常 |
| `A([テキスト])` | スタジアム | 開始・終了 |
| `A{テキスト}` | ひし形 | 判断 |
| `A((テキスト))` | 円 | 接続点 |
| `A[/テキスト/]` | 平行四辺形 | 入出力 |
| `A[(テキスト)]` | 円柱 | データベース |
| `A>テキスト]` | 旗 | 注記 |

## フローチャート — 矢印

| コード | 意味 |
|---|---|
| `A --> B` | 実線矢印 |
| `A -.-> B` | 点線矢印 |
| `A ==> B` | 太線矢印 |
| `A --- B` | 線（矢印なし） |
| `A -->|ラベル| B` | ラベル付き矢印 |
| `A -- ラベル --> B` | 同上（別記法） |

## シーケンス図

```text
sequenceDiagram
    participant A as 表示名
    A->>B: メッセージ       # 実線（依頼）
    B-->>A: 返事            # 点線（応答）
    A-)B: 非同期
    A-xB: 失敗
    Note over A,B: 注釈
    loop 5 回
        A->>B: 繰り返し
    end
    alt 条件1
        A->>B: 1の場合
    else 条件2
        A->>B: 2の場合
    end
    opt 任意の場合
        A->>B: 条件成立時のみ
    end
```

## クラス図

```text
classDiagram
    class クラス名 {
        +公開フィールド: 型
        -秘匿フィールド: 型
        +メソッド名(引数: 型) 戻り値型
    }
    親 <|-- 子                    # 継承
    全体 *-- 部品                  # コンポジション
    全体 o-- 部品                  # 集約
    A --> B : 関係名               # 関連
    A "1" --> "0..*" B : 名前      # 多重度
```

## 状態遷移図

```text
stateDiagram-v2
    [*] --> 状態A                # 開始
    状態A --> 状態B : イベント
    状態B --> [*]                # 終了
    state 複合状態 {
        [*] --> 内部A
        内部A --> 内部B
        内部B --> [*]
    }
    state 並行 {
        [*] --> X
        --
        [*] --> Y
    }
```

## ER 図

| 記号 | 意味 |
|---|---|
| `||` | ちょうど 1 |
| `o|` | 0 または 1 |
| `|{` | 1 以上 |
| `o{` | 0 以上 |

```text
erDiagram
    BOOK {
        int id PK
        string title
        int author_id FK
    }
    AUTHOR ||--o{ BOOK : 執筆
```

## ガントチャート

```text
gantt
    title タイトル
    dateFormat YYYY-MM-DD
    excludes weekends, 2026-05-03

    section セクション名
    タスク名         :id, 2026-04-01, 14d
    依存タスク       :id2, after id, 7d
    完了済みタスク   :done, id3, 2026-04-01, 7d
    進行中タスク     :active, id4, 2026-04-08, 7d
    重要タスク       :crit, id5, after id4, 5d
    マイルストーン   :milestone, m1, after id5, 0d
```

## 共通ルール

- 1 行 = 1 命令（セミコロン不要）
- インデントは任意（揃えると読みやすい）
- コメントは行頭に `%%`
- ID は英数字、ラベル/表示名は日本語 OK

## ライブエディタ

開いてすぐ試せる場所：

- [Mermaid Live Editor](https://mermaid.live/) — 公式、URL 共有可

## よく使う Mermaid 対応サービス

- GitHub（README.md、Issue、PR）
- GitLab
- Notion
- Obsidian（公式プラグインなしで動作）
- HackMD / CodiMD
- VS Code（Markdown プレビュー時に拡張機能で対応）
- Quarto
- MkDocs Material（このサイトもこれ）

→ [付録B つまずきポイント FAQ](09-faq.md)
