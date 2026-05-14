#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Claude APIを使って週次記事を自動生成してサイトに追加するスクリプト"""

import anthropic
import os
import re
import glob
import datetime
import json
import random

ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3034271297570921" crossorigin="anonymous"></script>'
GA = '''<script async src="https://www.googletagmanager.com/gtag/js?id=G-Y55CVCFC9P"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag("js", new Date());
  gtag("config", "G-Y55CVCFC9P");
</script>'''

CSS = """*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans JP',sans-serif;background:#F8FAFC;color:#1E293B;line-height:1.8;}
@media(min-width:640px){body{max-width:680px;margin:0 auto;}}
.header{background:#122A64;padding:20px;}
.header a{color:rgba(255,255,255,0.8);font-size:13px;text-decoration:none;display:block;}
.header h1{color:#fff;font-size:18px;font-weight:700;margin-top:4px;}
.content{padding:24px 20px 48px;}
.eyecatch{background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:12px;padding:20px;margin-bottom:28px;border-left:4px solid #2563EB;}
.eyecatch p{font-size:14px;color:#1E3A8A;margin:0;}
h2{font-size:17px;font-weight:700;color:#1E293B;margin:32px 0 12px;padding-left:10px;border-left:4px solid #2563EB;}
h3{font-size:15px;font-weight:700;color:#1E293B;margin:22px 0 8px;}
p{font-size:14px;color:#374151;margin-bottom:14px;}
ul,ol{font-size:14px;color:#374151;padding-left:22px;margin-bottom:14px;}
ul li,ol li{margin-bottom:8px;}
.tip-box{background:#F0FDF4;border-radius:10px;padding:16px 18px;margin:16px 0;border-left:4px solid #22C55E;}
.tip-box p{margin:0;font-size:14px;color:#14532D;}
.warn-box{background:#FEF9C3;border-radius:10px;padding:16px 18px;margin:16px 0;border-left:4px solid #EAB308;}
.warn-box p{margin:0;font-size:14px;color:#713F12;}
.cta{background:#122A64;border-radius:14px;padding:22px 20px;margin:32px 0;text-align:center;}
.cta p{color:rgba(255,255,255,0.9);font-size:13px;margin-bottom:12px;}
.cta a{display:inline-block;background:#fff;color:#1E40AF;font-weight:700;font-size:15px;padding:12px 28px;border-radius:50px;text-decoration:none;}
footer{text-align:center;padding:16px;font-size:11px;color:#94A3B8;border-top:1px solid #E2E8F0;}
footer a{color:#94A3B8;text-decoration:underline;}"""

AD_UNIT = """<div style="margin:24px 0;text-align:center;">
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3034271297570921" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>"""

AFFILIATE_SECTION = """<div style="margin:32px 0 24px;padding:20px 16px;background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border-radius:14px;border:1.5px solid #F59E0B;">
  <div style="font-size:12px;font-weight:700;color:#92400E;margin-bottom:12px;">📣 おすすめ教材</div>
  <a href="https://amzn.to/41Avn9J" rel="nofollow" target="_blank" style="display:block;background:#fff;border:1.5px solid #38BDF8;border-radius:12px;padding:14px 16px;text-decoration:none;margin-bottom:10px;">
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="flex-shrink:0;background:#0EA5E9;border-radius:10px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;font-size:22px;">📚</div>
      <div>
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
          <div style="font-size:13px;font-weight:700;color:#0C4A6E;">Amazon Kids+</div>
          <div style="background:#FF9900;color:#fff;border-radius:4px;padding:1px 7px;font-size:10px;font-weight:700;">Amazon</div>
        </div>
        <div style="font-size:12px;color:#0369A1;font-weight:600;">本・動画・知育アプリ 数千点が読み放題</div>
        <div style="font-size:11px;color:#0284C7;">3歳〜12歳対象。1か月無料体験あり。</div>
      </div>
    </div>
  </a>
  <div style="font-size:10px;color:#94A3B8;margin-top:6px;text-align:center;">※ アフィリエイトリンクを含みます</div>
</div>"""

FOOTER = """<footer>
  © 2025 にじゅうまる。算数ドリル. All rights reserved.<br>
  <a href="/privacy.html">プライバシーポリシー</a>&nbsp;|&nbsp;
  <a href="/tokusho.html">特定商取引法に基づく表記</a>&nbsp;|&nbsp;
  <a href="/contact.html">お問い合わせ</a>&nbsp;|&nbsp;
  <a href="/about.html">サイトについて</a>
</footer>"""

REDIRECT_JS = 'if(location.hostname==="nijumaru-drill.com"){location.replace("https://www.nijumaru-drill.com"+location.pathname+location.search+location.hash);}'

# 記事テーマのプール（毎週1つずつ消化）
ARTICLE_THEMES = [
    ("addition-guide.html", "たし算が得意になる方法【1〜3年生向け完全ガイド】",
     "小学1〜3年生のたし算を得意にするための練習法と教え方を解説。繰り上がりのコツから2桁・3桁の筆算まで丁寧に説明します。"),
    ("subtraction-guide.html", "ひき算のつまずきポイントと克服法【完全ガイド】",
     "ひき算が苦手な子のつまずきポイントと、家庭でできる練習法を解説。繰り下がりのある引き算を確実にマスターする方法を紹介します。"),
    ("multiplication-guide.html", "かけ算をマスターする方法【九九から筆算まで】",
     "かけ算の概念理解から九九の覚え方、2桁かけ算の筆算まで、段階的にマスターするための方法を解説します。"),
    ("large-numbers.html", "大きな数の読み方・書き方【万・億・兆の覚え方】",
     "小学生が学ぶ大きな数（万・億・兆）の読み方・書き方・計算のポイントを分かりやすく解説します。"),
    ("geometry-guide.html", "図形の問題が得意になる方法【面積・体積・角度】",
     "小学生の図形問題（面積・体積・角度）のつまずきポイントと解き方のコツを学年別に解説します。"),
    ("ratio-guide.html", "割合・百分率の攻略法【5年生の最難関単元】",
     "小学5年生の最難関「割合・百分率」を確実にマスターするための理解法と練習法を詳しく解説します。"),
    ("speed-distance.html", "速さ・距離・時間の問題の解き方【みはじの使い方】",
     "速さ・距離・時間の問題をスムーズに解くための「みはじ」の使い方と、つまずきポイントの対処法を解説します。"),
    ("prime-numbers.html", "素数・公倍数・公約数の覚え方【中学準備にも】",
     "小学生で学ぶ素数・最大公約数・最小公倍数の意味と求め方を分かりやすく解説。中学数学の準備にもなります。"),
    ("time-calculation.html", "時刻と時間の計算【間違えやすいポイント完全解説】",
     "時刻と時間の計算でよく間違えるポイントと、確実に正解するための方法を学年別に解説します。"),
    ("unit-conversion.html", "単位の換算が苦手な子への教え方【長さ・重さ・かさ】",
     "長さ・重さ・かさなどの単位換算でつまずく子へ、理解しやすい教え方と覚え方のコツを解説します。"),
    ("math-game.html", "算数が楽しくなるゲーム・遊び10選【家庭でできる】",
     "算数を楽しみながら練習できるゲームや遊びを10種類紹介。子どもが自然と計算に親しめる工夫を解説します。"),
    ("notebook-method.html", "算数ノートの上手な使い方【成績が上がる書き方】",
     "算数の成績を上げるノートの取り方・書き方を解説。字の大きさ、式の書き方、図の描き方まで具体的に紹介します。"),
    ("review-method.html", "算数の復習の仕方【効果的な振り返り学習法】",
     "算数の成績を伸ばす効果的な復習方法を解説。毎日の復習習慣と、テスト後の振り返り方法を具体的に紹介します。"),
    ("tablet-learning.html", "タブレット・スマホを使った算数学習のコツ",
     "タブレットやスマホを使った算数学習の効果的な活用法と注意点を解説。デジタルツールを味方にする方法を紹介します。"),
    ("parent-support.html", "親が算数が苦手でも子どもをサポートする方法",
     "親自身が算数が苦手でも、子どもの算数学習を効果的にサポートできる方法を解説します。"),
]

def get_existing_filenames():
    """既存のHTMLファイル名一覧を取得"""
    return set(os.path.basename(f) for f in glob.glob("*.html"))

def get_next_theme(existing_files):
    """次に生成すべきテーマを選択"""
    for theme in ARTICLE_THEMES:
        if theme[0] not in existing_files:
            return theme
    return None

def generate_article_content(title, description):
    """Claude APIを使って記事本文を生成"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""あなたは小学生向け算数教育サイト「にじゅうまる。算数ドリル」のコンテンツライターです。
以下の記事タイトルと概要に基づいて、記事の本文HTMLを生成してください。

タイトル: {title}
概要: {description}

要件:
- 日本語で書く
- 実質テキスト量：2000文字以上
- HTMLタグを使って構造化する（h2, h3, p, ul, ol, li）
- 以下のクラスを活用する：
  - tip-box（💡アドバイスボックス）: <div class="tip-box"><p>内容</p></div>
  - warn-box（⚠️注意ボックス）: <div class="warn-box"><p>内容</p></div>
- 保護者・子ども両方に役立つ実践的な内容
- 「にじゅうまる。算数ドリル」への言及を自然に1〜2回含める
- <body>タグや<html>タグは含めない（本文のみ）
- eyecatchセクションから始める: <div class="eyecatch"><p>リード文</p></div>
- h2見出しを4〜6個含む
- 具体的な例、数字、手順を含める"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def build_html(filename, title, description, body_html):
    """完全なHTMLページを組み立て"""
    canonical = f"https://www.nijumaru-drill.com/{filename}"
    h1 = title.split("【")[0].strip() if "【" in title else title

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
{GA}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | にじゅうまる。算数ドリル</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
{ADSENSE}
<style>
{CSS}
</style>
<script>{REDIRECT_JS}</script>
</head>
<body>
<div class="header">
  <a href="/">← トップに戻る</a>
  <h1>{h1}</h1>
</div>
<div class="content">
{body_html}
{AD_UNIT}
{AFFILIATE_SECTION}
<div class="cta">
  <p>無料・アプリ不要で今すぐ練習できます！</p>
  <a href="/">にじゅうまる。算数ドリルをやってみる →</a>
</div>
{AD_UNIT}
<div class="cta" style="background:linear-gradient(135deg,#7C3AED,#8B5CF6);">
  <p>100問まとめドリルや苦手特化はプレミアムで。</p>
  <a href="/premium.html" style="color:#6D28D9;">プレミアム機能を見る</a>
</div>
</div>
{FOOTER}
</body>
</html>"""

def update_sitemap(filename, title):
    """sitemap.xmlに新しいURLを追加"""
    today = datetime.date.today().isoformat()
    sitemap_path = "sitemap.xml"

    if not os.path.exists(sitemap_path):
        return

    content = open(sitemap_path, "r", encoding="utf-8").read()
    url = f"https://www.nijumaru-drill.com/{filename}"

    if url in content:
        return  # 既に存在する

    new_entry = f'  <url><loc>{url}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    content = content.replace('</urlset>', new_entry + '</urlset>')
    open(sitemap_path, "w", encoding="utf-8").write(content)
    print(f"📍 sitemap更新: {filename}")

def main():
    existing = get_existing_filenames()
    theme = get_next_theme(existing)

    if not theme:
        print("✅ 全テーマ生成済みです")
        return

    filename, title, description = theme
    print(f"📝 生成中: {title}")

    # Claude APIで本文生成
    body_html = generate_article_content(title, description)

    # HTMLページ組み立て
    html = build_html(filename, title, description, body_html)

    # ファイル保存
    open(filename, "w", encoding="utf-8").write(html)
    print(f"✅ 保存完了: {filename}")

    # サイトマップ更新
    update_sitemap(filename, title)

    print(f"\n🎉 新記事を追加しました: {title}")

if __name__ == "__main__":
    main()
