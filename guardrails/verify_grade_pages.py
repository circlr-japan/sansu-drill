#!/usr/bin/env python3
"""学年別ページ（grade-N.html）の構造チェック。exit 0 で合格。

チェック内容:
 1. すべての JSON-LD が JSON としてパースできる
 2. 本文の FAQ 見出し数と FAQPage の Question 数が一致し、質問文も一致する
 3. 本文中の内部リンク（/xxx.html）の実ファイルが存在する
 4. 使用している CSS クラスが同ファイルの <style> 内に定義されている
 5. <div> の開閉数が一致する
 6. 必須セクション（直答／学期別カリキュラム／チェックリスト）が存在する
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKED_CLASSES = [
    "answer-box", "cur-table", "check-item", "check-box", "check-text",
    "note", "topic-card", "mistake-box", "tip-item", "next-box", "section",
]
REQUIRED_HEADINGS = ["【直答】", "学期別カリキュラム", "チェックリスト"]


def check(path: Path) -> list[str]:
    errors: list[str] = []
    s = path.read_text(encoding="utf-8")
    name = path.name

    # 1. JSON-LD
    faq_names: list[str] = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            errors.append(f"{name}: JSON-LD parse error: {e}")
            continue
        if data.get("@type") == "FAQPage":
            faq_names = [q["name"] for q in data.get("mainEntity", [])]

    # 2. FAQ の本文と構造化データの一致
    html_qs = re.findall(r">Q\d+\.\s*(.+?)</div>", s)
    if not html_qs:
        errors.append(f"{name}: 本文に FAQ が見つからない")
    if len(html_qs) != len(faq_names):
        errors.append(f"{name}: FAQ 数の不一致 本文{len(html_qs)}件 / JSON-LD{len(faq_names)}件")
    for q in html_qs:
        q = q.strip()
        if q not in faq_names:
            errors.append(f"{name}: JSON-LD に無い FAQ: {q}")

    # 3. 内部リンク
    for href in set(re.findall(r'href="/([a-z0-9\-]+\.html)"', s)):
        if not (ROOT / href).exists():
            errors.append(f"{name}: リンク切れ /{href}")

    # 4. CSS クラス定義
    style = "\n".join(re.findall(r"<style>(.*?)</style>", s, re.S))
    for cls in CHECKED_CLASSES:
        if f'class="{cls}"' in s and f".{cls}" not in style:
            errors.append(f"{name}: CSS 未定義のクラス .{cls}")

    # 5. div の開閉
    opened, closed = len(re.findall(r"<div\b", s)), s.count("</div>")
    if opened != closed:
        errors.append(f"{name}: div 不一致 開き{opened} / 閉じ{closed}")

    # 6. 必須セクション
    headings = " ".join(re.findall(r"<h2>(.*?)</h2>", s))
    for req in REQUIRED_HEADINGS:
        if req not in headings:
            errors.append(f"{name}: 必須セクション欠落「{req}」")

    return errors


def main() -> int:
    targets = [Path(a) for a in sys.argv[1:]] or sorted(ROOT.glob("grade-[1-6].html"))
    all_errors: list[str] = []
    for path in targets:
        errs = check(path)
        print(f"{'FAIL' if errs else ' OK '}  {path.name}")
        all_errors += errs
    for e in all_errors:
        print(f"  - {e}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
