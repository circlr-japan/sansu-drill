#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""各記事ページに関連記事リンクセクションを追加するスクリプト"""

import os
import re

# ページ情報: {filename: (title, emoji)}
PAGES = {
    "geometry-guide.html":       ("図形・面積・円周の攻略法", "📐"),
    "kuku-tips.html":            ("九九をマスターするコツ", "✖️"),
    "division-guide.html":       ("割り算・わり算の教え方", "➗"),
    "decimal-fraction-guide.html": ("小数・分数の完全ガイド", "🔢"),
    "fractions-guide.html":      ("分数をマスターする方法", "½"),
    "word-problems.html":        ("文章題が得意になる解き方", "📝"),
    "mental-math.html":          ("暗算力を鍛えるトレーニング", "🧠"),
    "calculation-power.html":    ("計算力アップの秘訣", "💪"),
    "no-mistakes.html":          ("計算ミスをなくす方法", "✅"),
    "reduce-mistakes.html":      ("ケアレスミスを減らすコツ", "🎯"),
    "math-anxiety.html":         ("算数嫌いを克服する方法", "💡"),
    "grade-guide.html":          ("学年別・算数の学習ガイド", "📚"),
    "grade-1-tips.html":         ("1年生の算数攻略ガイド", "1️⃣"),
    "grade-2-tips.html":         ("2年生の算数攻略ガイド", "2️⃣"),
    "grade-3-tips.html":         ("3年生の算数攻略ガイド", "3️⃣"),
    "grade-4-tips.html":         ("4年生の算数攻略ガイド", "4️⃣"),
    "grade-5-tips.html":         ("5年生の算数攻略ガイド", "5️⃣"),
    "teaching-tips.html":        ("子どもへの算数の教え方", "👨‍👩‍👧"),
    "study-habits.html":         ("算数の勉強習慣のつくり方", "📅"),
    "study-routine.html":        ("効果的な学習ルーティン", "🔄"),
    "advance-study.html":        ("先取り学習の進め方", "🚀"),
    "test-prep.html":            ("テスト対策の完全ガイド", "📋"),
    "test-strategy.html":        ("算数テストで高得点を取る戦略", "🏆"),
    "summer-math.html":          ("夏休みの算数学習法", "☀️"),
    "percentage-guide.html":     ("割合・百分率の攻略法", "📊"),
    "how-to-use.html":           ("ドリルの効果的な使い方", "🖊️"),
}

# 関連記事マッピング: {filename: [関連ページのfilename, ...]}
RELATED = {
    "geometry-guide.html": ["kuku-tips.html", "division-guide.html", "grade-5-tips.html", "decimal-fraction-guide.html"],
    "kuku-tips.html": ["division-guide.html", "mental-math.html", "calculation-power.html", "grade-3-tips.html"],
    "division-guide.html": ["kuku-tips.html", "decimal-fraction-guide.html", "fractions-guide.html", "grade-4-tips.html"],
    "decimal-fraction-guide.html": ["fractions-guide.html", "division-guide.html", "percentage-guide.html", "grade-5-tips.html"],
    "fractions-guide.html": ["decimal-fraction-guide.html", "percentage-guide.html", "division-guide.html", "grade-4-tips.html"],
    "word-problems.html": ["grade-guide.html", "teaching-tips.html", "no-mistakes.html", "test-strategy.html"],
    "mental-math.html": ["kuku-tips.html", "calculation-power.html", "no-mistakes.html", "study-habits.html"],
    "calculation-power.html": ["mental-math.html", "kuku-tips.html", "study-routine.html", "no-mistakes.html"],
    "no-mistakes.html": ["reduce-mistakes.html", "calculation-power.html", "test-strategy.html", "study-habits.html"],
    "reduce-mistakes.html": ["no-mistakes.html", "test-prep.html", "study-habits.html", "mental-math.html"],
    "math-anxiety.html": ["teaching-tips.html", "study-habits.html", "grade-guide.html", "how-to-use.html"],
    "grade-guide.html": ["grade-1-tips.html", "grade-2-tips.html", "grade-3-tips.html", "teaching-tips.html"],
    "grade-1-tips.html": ["grade-2-tips.html", "kuku-tips.html", "teaching-tips.html", "grade-guide.html"],
    "grade-2-tips.html": ["grade-1-tips.html", "grade-3-tips.html", "kuku-tips.html", "teaching-tips.html"],
    "grade-3-tips.html": ["grade-2-tips.html", "grade-4-tips.html", "kuku-tips.html", "division-guide.html"],
    "grade-4-tips.html": ["grade-3-tips.html", "grade-5-tips.html", "division-guide.html", "fractions-guide.html"],
    "grade-5-tips.html": ["grade-4-tips.html", "decimal-fraction-guide.html", "percentage-guide.html", "geometry-guide.html"],
    "teaching-tips.html": ["math-anxiety.html", "study-habits.html", "grade-guide.html", "word-problems.html"],
    "study-habits.html": ["study-routine.html", "teaching-tips.html", "math-anxiety.html", "test-prep.html"],
    "study-routine.html": ["study-habits.html", "advance-study.html", "summer-math.html", "test-prep.html"],
    "advance-study.html": ["study-routine.html", "grade-guide.html", "test-strategy.html", "summer-math.html"],
    "test-prep.html": ["test-strategy.html", "no-mistakes.html", "study-habits.html", "reduce-mistakes.html"],
    "test-strategy.html": ["test-prep.html", "no-mistakes.html", "reduce-mistakes.html", "calculation-power.html"],
    "summer-math.html": ["study-routine.html", "grade-guide.html", "advance-study.html", "study-habits.html"],
    "percentage-guide.html": ["decimal-fraction-guide.html", "fractions-guide.html", "grade-5-tips.html", "word-problems.html"],
    "how-to-use.html": ["grade-guide.html", "study-habits.html", "math-anxiety.html", "teaching-tips.html"],
}

def build_related_section(filename):
    related_files = RELATED.get(filename, [])
    if not related_files:
        return ""

    cards = ""
    for rel_file in related_files[:4]:
        if rel_file not in PAGES:
            continue
        title, emoji = PAGES[rel_file]
        cards += f"""    <a href="/{rel_file}" style="display:block;background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;text-decoration:none;transition:box-shadow .2s;">
      <span style="font-size:18px;margin-right:8px;">{emoji}</span>
      <span style="font-size:13px;font-weight:600;color:#1E40AF;">{title}</span>
    </a>
"""

    return f"""<div style="margin:32px 0;padding:20px 16px;background:#F8FAFC;border-radius:14px;border:1px solid #E2E8F0;">
  <div style="font-size:13px;font-weight:700;color:#475569;margin-bottom:14px;">📖 関連記事</div>
  <div style="display:grid;gap:8px;">
{cards}  </div>
</div>"""

def add_related_links(filepath, filename):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 既に関連記事セクションがある場合はスキップ
    if "関連記事" in content and "display:grid;gap:8px;" in content:
        print(f"  スキップ（既存）: {filename}")
        return False

    related_html = build_related_section(filename)
    if not related_html:
        print(f"  スキップ（定義なし）: {filename}")
        return False

    # CTAセクションの直前に挿入
    marker = '<div class="cta">'
    if marker not in content:
        print(f"  スキップ（マーカーなし）: {filename}")
        return False

    # 最初のCTAの前に挿入
    new_content = content.replace(marker, related_html + "\n" + marker, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  ✅ 追加: {filename}")
    return True

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    updated = 0

    for filename in RELATED.keys():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            print(f"  ❌ ファイルなし: {filename}")
            continue
        if add_related_links(filepath, filename):
            updated += 1

    print(f"\n🎉 完了: {updated}ページに関連記事リンクを追加しました")

if __name__ == "__main__":
    main()
