#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Wikimedia Commons から各章用の CC/PD 画像をダウンロードする。

実行: uv run scripts/download_photos.py
出力先: docs/images/  と  docs/credits.md
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "docs" / "images"
CREDITS_MD = ROOT / "docs" / "credits.md"

# 各 (出力ファイル名, [候補となる Commons の File: 名のリスト], 用途メモ)
# 先頭から試して取れたものを採用
TARGETS: list[tuple[str, list[str], str]] = [
    (
        "flowchart-lamp",
        ["File:LampFlowchart.svg"],
        "第2章 フローチャート — 電球がつかないときの判断フロー（PD）",
    ),
    (
        "sequence-switchboard",
        [
            "File:Switchboard_operators_1952.jpg",
            "File:Women_working_at_a_Bell_System_telephone_switchboard_(3660047829).jpg",
            "File:Telephone_operators,_1952.jpg",
        ],
        "第3章 シーケンス図 — 電話交換手（PD）",
    ),
    (
        "class-linnaeus",
        [
            "File:Linnaeus_-_Nationalmuseum_-_15201.tif",
            "File:Carl_von_Linné.jpg",
            "File:Carl_Linnaeus.jpg",
        ],
        "第4章 クラス図 — 分類学の父 Carl Linnaeus（PD）",
    ),
    (
        "state-water",
        [
            "File:Iceberg_with_hole_near_Sandersons_Hope_2007-07-28_2.jpg",
            "File:Iceberg_in_the_Arctic_with_its_underside_exposed.jpg",
            "File:Antarctic_iceberg.jpg",
        ],
        "第5章 状態遷移図 — 氷山（水の状態のメタファー、CC）",
    ),
    (
        "er-cardcatalog",
        [
            "File:Card_catalog_(University_of_Graz_library).jpg",
            "File:Manuscripts_catalog,_Bavarian_State_Library.jpg",
            "File:Card_catalog_in_a_library.jpg",
            "File:Schlagwortkatalog.jpg",
            "File:Library-shelves-bibliographies-Graz.jpg",
        ],
        "第6章 ER 図 — 図書館の目録カード（CC）",
    ),
    (
        "gantt-henry",
        [
            "File:Henry_Laurence_Gantt.jpg",
            "File:Henry_Gantt.jpg",
            "File:HenryGantt.jpg",
        ],
        "第7章 ガントチャート — Henry Laurence Gantt（PD）",
    ),
    (
        "cover-notebook",
        [
            "File:Leonardo_da_Vinci_-_Codex_on_the_Flight_of_Birds.jpg",
            "File:Leonardo_da_Vinci_-_Codex_on_the_Flight_of_Birds_-_22r.jpg",
            "File:Leonardo_da_Vinci_-_RCIN_912283,_Recto-_Anatomical_studies_of_the_shoulder_c.1510-11.jpg",
        ],
        "表紙 — ダ・ヴィンチの手稿（PD）— 図とテキストで思考をまとめる例として",
    ),
]

API = "https://commons.wikimedia.org/w/api.php"
UA = "mermaid-tutorial-bot/0.1 (educational; contact: jkoba)"


def fetch_image_info(title: str, max_retries: int = 4) -> dict | None:
    """Wikimedia API から画像URLとメタデータを取得（429対応リトライ付き）"""
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size|mime",
        "titles": title,
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
                break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 3 * (attempt + 1)
                print(f"  . 429 rate-limited, sleeping {wait}s ...")
                time.sleep(wait)
                continue
            print(f"  ! API error for {title}: {e}")
            return None
        except Exception as e:
            print(f"  ! API error for {title}: {e}")
            return None
    if data is None:
        return None
    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        if "imageinfo" not in page:
            continue
        info = page["imageinfo"][0]
        return {
            "title": title,
            "url": info["url"],
            "mime": info.get("mime", ""),
            "width": info.get("width"),
            "height": info.get("height"),
            "meta": info.get("extmetadata", {}),
        }
    return None


def download(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  ! download error: {e}")
        return False


def ext_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    return Path(path).suffix.lower()


def html_unescape(s: str) -> str:
    import html
    return html.unescape(s)


def strip_html(s: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", s).strip()


def meta_field(meta: dict, key: str) -> str:
    v = meta.get(key, {})
    if isinstance(v, dict):
        return strip_html(html_unescape(v.get("value", "")))
    return ""


def main() -> int:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    credits_lines = [
        "# 画像の出典",
        "",
        "本チュートリアル内で使用している写真・画像は、Wikimedia Commons から取得した",
        "パブリックドメインまたはクリエイティブ・コモンズライセンスの画像です。",
        "",
    ]
    results = []
    for stem, candidates, purpose in TARGETS:
        print(f"[{stem}] {purpose}")
        # 既に取れているならスキップ
        existing = list(IMG_DIR.glob(f"{stem}.*"))
        existing = [p for p in existing if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".svg", ".webp"}]
        chosen = None
        for title in candidates:
            print(f"  - trying {title} ...")
            time.sleep(1.0)  # 礼儀正しい間隔
            info = fetch_image_info(title)
            if info is None:
                continue
            ext = ext_from_url(info["url"])
            # 巨大な TIFF は避ける(MkDocs/ブラウザ非対応)
            if ext == ".tif" or ext == ".tiff":
                print("    (skip: TIFF)")
                continue
            dest = IMG_DIR / f"{stem}{ext}"
            ok = download(info["url"], dest)
            if ok:
                chosen = (title, info, dest)
                print(f"    saved -> {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB)")
                break
        if chosen is None:
            print(f"  ! NO IMAGE for {stem}\n")
            credits_lines.append(f"## {stem}\n\n（取得失敗 — 後ほど手動で追加してください）\n")
            continue

        title, info, dest = chosen
        m = info["meta"]
        artist = meta_field(m, "Artist") or "不明"
        license_short = meta_field(m, "LicenseShortName") or meta_field(m, "License") or "不明"
        credit = meta_field(m, "Credit") or ""
        descr = meta_field(m, "ImageDescription") or ""
        commons_url = f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title)}"

        credits_lines.append(f"## `{dest.name}`")
        credits_lines.append("")
        credits_lines.append(f"- **用途**: {purpose}")
        if descr:
            credits_lines.append(f"- **説明**: {descr[:200]}")
        credits_lines.append(f"- **作者**: {artist[:200]}")
        credits_lines.append(f"- **ライセンス**: {license_short}")
        if credit:
            credits_lines.append(f"- **クレジット**: {credit[:200]}")
        credits_lines.append(f"- **出典**: [{title}]({commons_url})")
        credits_lines.append("")
        results.append((stem, dest.name, license_short))

    CREDITS_MD.write_text("\n".join(credits_lines) + "\n", encoding="utf-8")
    print()
    print("=== サマリ ===")
    for stem, name, lic in results:
        print(f"  {stem:25} -> {name:35} [{lic}]")
    print(f"\n書き込み: {CREDITS_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
