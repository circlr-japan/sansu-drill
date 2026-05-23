#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
にじゅうまる。算数ドリル ページ自動生成スクリプト

使い方:
  python3 generate_pages.py           # 未生成のページのみ作成
  python3 generate_pages.py --all     # 全ページ強制再生成
  python3 generate_pages.py --list    # 定義済みページ一覧表示

ページデータを PAGES リストに追加するだけで新ページを生成できます。
"""

import os, sys, json, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.nijumaru-drill.com"

# ============================================================
# HTML テンプレート
# ============================================================
TEMPLATE = """\
<!DOCTYPE html>
<html lang="ja">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Y55CVCFC9P"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag("js", new Date());
  gtag("config", "G-Y55CVCFC9P");
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | にじゅうまる。算数ドリル</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{BASE_URL}/{filename}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3034271297570921" crossorigin="anonymous"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Noto Sans JP',sans-serif;background:#F8FAFC;color:#1E293B;line-height:1.8;}}
@media(min-width:640px){{body{{max-width:680px;margin:0 auto;}}}}
.header{{background:#122A64;padding:20px;}}
.header a{{color:rgba(255,255,255,0.8);font-size:13px;text-decoration:none;display:block;}}
.header h1{{color:#fff;font-size:18px;font-weight:700;margin-top:4px;}}
.content{{padding:24px 20px 48px;}}
.eyecatch{{background:linear-gradient(135deg,#EFF6FF,#DBEAFE);border-radius:12px;padding:20px;margin-bottom:28px;border-left:4px solid #2563EB;}}
.eyecatch p{{font-size:14px;color:#1E3A8A;margin:0;}}
h2{{font-size:17px;font-weight:700;color:#1E293B;margin:32px 0 12px;padding-left:10px;border-left:4px solid #2563EB;}}
h3{{font-size:15px;font-weight:700;color:#1E293B;margin:22px 0 8px;}}
p{{font-size:14px;color:#374151;margin-bottom:14px;}}
ul,ol{{font-size:14px;color:#374151;padding-left:22px;margin-bottom:14px;}}
ul li,ol li{{margin-bottom:8px;}}
.tip-box{{background:#F0FDF4;border-radius:10px;padding:16px 18px;margin:16px 0;border-left:4px solid #22C55E;}}
.tip-box p{{margin:0;font-size:14px;color:#14532D;}}
.warn-box{{background:#FEF9C3;border-radius:10px;padding:16px 18px;margin:16px 0;border-left:4px solid #EAB308;}}
.warn-box p{{margin:0;font-size:14px;color:#713F12;}}
.formula-box{{background:#F5F3FF;border-radius:10px;padding:16px 18px;margin:16px 0;border-left:4px solid #7C3AED;text-align:center;}}
.formula-box p{{margin:0;font-size:16px;color:#4C1D95;font-weight:700;}}
.cta{{background:#122A64;border-radius:14px;padding:22px 20px;margin:32px 0;text-align:center;}}
.cta p{{color:rgba(255,255,255,0.9);font-size:13px;margin-bottom:12px;}}
.cta a{{display:inline-block;background:#fff;color:#1E40AF;font-weight:700;font-size:15px;padding:12px 28px;border-radius:50px;text-decoration:none;}}
.ad-wrap{{margin:24px 0;text-align:center;}}
footer{{text-align:center;padding:16px;font-size:11px;color:#94A3B8;border-top:1px solid #E2E8F0;}}
footer a{{color:#94A3B8;text-decoration:underline;}}
</style>
<script>if(location.hostname==="nijumaru-drill.com"){{location.replace("https://www.nijumaru-drill.com"+location.pathname+location.search+location.hash);}}</script>
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{BASE_URL}/{filename}">
<meta property="og:site_name" content="にじゅうまる。算数ドリル">
<meta property="og:image" content="{BASE_URL}/ogp-default.png">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{BASE_URL}/ogp-default.png">
{faq_json}
</head>
<body>
<div class="header">
  <a href="/">← トップに戻る</a>
  <h1>{h1}</h1>
</div>
<div class="content">
<div class="eyecatch">
  <p>{eyecatch}</p>
</div>
<div class="ad-wrap">
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3034271297570921" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

{body_html}

<div class="cta">
  <p>無料・アプリ不要で今すぐ練習できます！</p>
  <a href="{cta_href}">{cta_label} →</a>
</div>

<div style="margin:32px 0 24px;padding:20px 16px;background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border-radius:14px;border:1.5px solid #F59E0B;">
  <div style="font-size:12px;font-weight:700;color:#92400E;margin-bottom:12px;">📣 この記事に関連するおすすめ教材</div>
  <a href="https://amzn.to/41Avn9J" rel="nofollow" target="_blank" style="display:block;background:#fff;border:1.5px solid #38BDF8;border-radius:12px;padding:14px 16px;text-decoration:none;margin-bottom:10px;">
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="flex-shrink:0;background:#0EA5E9;border-radius:10px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;font-size:22px;">📚</div>
      <div>
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
          <div style="font-size:13px;font-weight:700;color:#0C4A6E;">Amazon Kids+</div>
          <div style="background:#FF9900;color:#fff;border-radius:4px;padding:1px 7px;font-size:10px;font-weight:700;">Amazon</div>
        </div>
        <div style="font-size:12px;color:#0369A1;font-weight:600;margin-bottom:2px;">本・動画・知育アプリ 数千点が読み放題・見放題</div>
        <div style="font-size:11px;color:#0284C7;line-height:1.6;">3歳〜12歳対象。算数・国語の学習本も充実。1か月無料体験あり。</div>
      </div>
    </div>
  </a>
  <div style="overflow:hidden;border-radius:10px;background:#fff;border:1px solid #E2E8F0;">
    <script type="text/javascript">rakuten_design="slide";rakuten_affiliateId="097cb958.bc61ad34.097cb959.eac353a7";rakuten_items="ctsmatch";rakuten_genreId="0";rakuten_size="468x160";rakuten_target="_blank";rakuten_theme="gray";rakuten_border="off";rakuten_auto_mode="on";rakuten_genre_title="off";rakuten_recommend="on";rakuten_ts="1776063409681";</script>
    <script type="text/javascript" src="https://xml.affiliate.rakuten.co.jp/widget/js/rakuten_widget.js?20230106"></script>
  </div>
  <div style="font-size:10px;color:#94A3B8;margin-top:6px;text-align:center;">※ アフィリエイトリンクを含みます</div>
</div>

{related_html}

<div class="ad-wrap">
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3034271297570921" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>
</div>
<footer>
  © 2025 にじゅうまる。算数ドリル. All rights reserved.<br>
  <a href="/privacy.html">プライバシーポリシー</a>&nbsp;|&nbsp;
  <a href="/tokusho.html">特定商取引法に基づく表記</a>&nbsp;|&nbsp;
  <a href="/contact.html">お問い合わせ</a>&nbsp;|&nbsp;
  <a href="/about.html">サイトについて</a>
</footer>
</body>
</html>
"""

# ============================================================
# ページデータ定義
# ============================================================
# 各ページのデータを追加するだけで新ページが生成されます。
#
# 必須キー:
#   filename   : 出力ファイル名 (例: "tani-nagasa.html")
#   title      : <title> + og:title + twitter:title（「| にじゅうまる。」は自動付加）
#   description: meta description
#   h1         : ヘッダーの大見出し
#   eyecatch   : 冒頭のリード文（絵文字から始める）
#   body_html  : メインコンテンツ（h2/h3/p/ul/formula-box など自由に書く）
#   faq        : [{"q": "...", "a": "..."}, ...] 3〜4問
#   cta_href   : CTAボタンのリンク先 (例: "/grade-3.html")
#   cta_label  : CTAボタンのテキスト (例: "3年生のドリルをやってみる")
#   related    : [{"href": "/xxx.html", "emoji": "📐", "text": "ページ名"}, ...]
# ============================================================
PAGES = [

  # ────────────────────────────────
  # 単位換算
  # ────────────────────────────────
  {
    "filename": "tani-nagasa.html",
    "title": "長さの単位換算プリント【無料】mm・cm・m・km｜小学3年生",
    "description": "長さの単位換算（mm・cm・m・km）を印刷不要・スマホで即採点できる無料プリント。小学3年生の算数で学ぶ単位変換をわかりやすく解説。毎回ランダム問題で繰り返し練習できます。",
    "h1": "長さの単位換算プリント【無料】mm・cm・m・km｜小学3年生",
    "eyecatch": "📏 mm・cm・m・km の換算は算数の基礎中の基礎。印刷不要・スマホでその場で練習できます！",
    "body_html": """\
<h2>長さの単位の関係</h2>
<p>長さには4つの単位があり、それぞれ以下の関係になっています。</p>
<div class="formula-box"><p>10mm ＝ 1cm　／　100cm ＝ 1m　／　1000m ＝ 1km</p></div>
<p>小さい単位から大きい単位に変換するときは「÷」、大きい単位から小さい単位に変換するときは「×」を使います。</p>

<h2>換算のコツ</h2>
<ol>
  <li><strong>表を覚える：</strong>mm→cm は÷10、cm→m は÷100、m→km は÷1000</li>
  <li><strong>逆方向は逆の計算：</strong>km→m は×1000、m→cm は×100、cm→mm は×10</li>
  <li><strong>2段階換算：</strong>mm→m は ÷10 してから ÷100（＝÷1000）</li>
</ol>
<div class="tip-box"><p>💡 「1km＝1000m」は「キロ＝1000倍」と覚えると、キログラム（kg）などにも応用できます。</p></div>

<h2>よくあるつまずきポイント</h2>
<ul>
  <li><strong>÷と×の逆：</strong>大きい単位→小さい単位なのに÷にしてしまう。「小さくなるから×」と覚える</li>
  <li><strong>小数の換算：</strong>1.5m＝150cm など小数が絡む問題は筆算で確認する</li>
  <li><strong>混合単位の計算：</strong>3m50cm のような書き方はcmに統一してから計算する</li>
</ul>
<div class="warn-box"><p>⚠️ テストでは「単位を変換してから計算」が必要な問題が多く出ます。先に単位をそろえる習慣をつけましょう。</p></div>""",
    "faq": [
      {"q": "長さの単位換算はいつ習いますか？", "a": "小学2〜3年生で学習します。2年生でmm・cm・mを、3年生でkmを学びます。単位換算の基礎として、その後の体積・重さの単位学習にもつながります。"},
      {"q": "1km は何m ですか？", "a": "1km＝1000m です。「キロ（kilo）」は1000を表す接頭辞で、1kg＝1000g と同じ関係です。"},
      {"q": "cm を mm に直すにはどうしますか？", "a": "cm を mm に直すには「×10」します。例えば 3cm＝30mm です。逆に mm を cm に直すときは「÷10」します。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/unit-conversion.html", "emoji": "📏", "text": "単位換算ガイド"},
      {"href": "/tani-omosa.html",     "emoji": "⚖️", "text": "重さの単位換算プリント【無料】小学3年生"},
      {"href": "/tani-kaseki.html",    "emoji": "🧪", "text": "かさの単位換算プリント【無料】小学2〜3年生"},
      {"href": "/grade-3-tips.html",   "emoji": "📚", "text": "3年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "tani-omosa.html",
    "title": "重さの単位換算プリント【無料】g・kg・t｜小学3年生",
    "description": "重さの単位換算（g・kg・t）を印刷不要・スマホで即採点できる無料プリント。小学3年生の算数で学ぶg・kg・tの変換を丁寧に解説。毎回ランダム問題で繰り返し練習できます。",
    "h1": "重さの単位換算プリント【無料】g・kg・t｜小学3年生",
    "eyecatch": "⚖️ g・kg・t の換算はつまずきやすい単元。印刷不要・スマホでその場で繰り返し練習できます！",
    "body_html": """\
<h2>重さの単位の関係</h2>
<p>重さには主に3つの単位があり、それぞれ以下の関係になっています。</p>
<div class="formula-box"><p>1000g ＝ 1kg　／　1000kg ＝ 1t</p></div>
<p>長さと同じく「キロ（kilo）＝1000倍」の法則が使えます。kgはキログラム、tはトンと読みます。</p>

<h2>換算のコツ</h2>
<ol>
  <li><strong>g → kg：</strong>÷1000（例：5000g ＝ 5kg）</li>
  <li><strong>kg → g：</strong>×1000（例：2.5kg ＝ 2500g）</li>
  <li><strong>kg → t：</strong>÷1000（例：3000kg ＝ 3t）</li>
  <li><strong>t → kg：</strong>×1000（例：0.5t ＝ 500kg）</li>
</ol>
<div class="tip-box"><p>💡 日常生活で体重（kg）や食材の重さ（g）を意識すると単位感覚が身につきます。</p></div>

<h2>よくあるつまずきポイント</h2>
<ul>
  <li><strong>×と÷の混同：</strong>gからkgは小さい数になるから÷1000と覚える</li>
  <li><strong>小数が出てくる換算：</strong>1500g＝1.5kg など、小数点の位置に注意</li>
  <li><strong>tが入る問題：</strong>日常生活でtを使う場面が少ないため実感しにくい。1tはおよそ乗用車1台分と覚える</li>
</ul>
<div class="warn-box"><p>⚠️ g・kg・t すべてに「×1000」「÷1000」の関係があります。長さ（mm・cm・m・km）は一部×10・×100なので混同しないよう注意。</p></div>""",
    "faq": [
      {"q": "重さの単位換算はいつ習いますか？", "a": "小学3年生で学習します。g（グラム）・kg（キログラム）を3年生で、t（トン）を4年生以降で学ぶことが多いです。"},
      {"q": "1kg は何g ですか？", "a": "1kg＝1000g です。「キロ（kilo）＝1000」の接頭辞を覚えると、km・kgどちらにも応用できます。"},
      {"q": "kg を g に直すにはどうしますか？", "a": "kg を g に直すには「×1000」します。例えば 2kg＝2000g です。逆に g を kg に直すときは「÷1000」します。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/unit-conversion.html", "emoji": "📏", "text": "単位換算ガイド"},
      {"href": "/tani-nagasa.html",     "emoji": "📏", "text": "長さの単位換算プリント【無料】小学3年生"},
      {"href": "/tani-kaseki.html",     "emoji": "🧪", "text": "かさの単位換算プリント【無料】小学2〜3年生"},
      {"href": "/grade-3-tips.html",    "emoji": "📚", "text": "3年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "tani-kaseki.html",
    "title": "かさの単位換算プリント【無料】mL・dL・L｜小学2〜3年生",
    "description": "かさの単位換算（mL・dL・L）を印刷不要・スマホで即採点できる無料プリント。小学2〜3年生の算数で学ぶかさの変換をわかりやすく解説。毎回ランダム問題で繰り返し練習できます。",
    "h1": "かさの単位換算プリント【無料】mL・dL・L｜小学2〜3年生",
    "eyecatch": "🧪 mL・dL・L の換算は少しクセがある単元。印刷不要・スマホでその場で確認しながら練習できます！",
    "body_html": """\
<h2>かさの単位の関係</h2>
<p>かさ（液体の量）には3つの単位があり、それぞれ以下の関係になっています。</p>
<div class="formula-box"><p>10dL ＝ 1L　／　1000mL ＝ 1L　／　100mL ＝ 1dL</p></div>
<p>dL（デシリットル）は日常生活ではあまり使いませんが、小学校では重要な単位です。mL（ミリリットル）とL（リットル）の中間にあります。</p>

<h2>換算のコツ</h2>
<ol>
  <li><strong>mL → dL：</strong>÷100（例：300mL ＝ 3dL）</li>
  <li><strong>dL → L：</strong>÷10（例：20dL ＝ 2L）</li>
  <li><strong>mL → L：</strong>÷1000（例：2500mL ＝ 2.5L）</li>
  <li><strong>逆は逆の計算：</strong>L→dL は×10、dL→mL は×100、L→mL は×1000</li>
</ol>
<div class="tip-box"><p>💡 牛乳パック1本（200mL）や500mLのペットボトルなど身近なもので量を実感すると覚えやすいです。</p></div>

<h2>よくあるつまずきポイント</h2>
<ul>
  <li><strong>dLが難しい：</strong>日常では見かけないdLに戸惑う子が多い。「dL＝コップ1杯くらい」と覚えると実感しやすい</li>
  <li><strong>mL↔Lで×1000：</strong>長さのcm↔m（×100）と混同しないよう注意</li>
  <li><strong>小数が出る換算：</strong>1.5L＝15dL＝1500mL など段階的に確認する</li>
</ul>
<div class="warn-box"><p>⚠️ dLは長さや重さにはない単位です。mL・dL・L の3段階の関係を表にまとめて確認しましょう。</p></div>""",
    "faq": [
      {"q": "かさの単位換算はいつ習いますか？", "a": "小学2〜3年生で学習します。2年生でdL・Lを、3年生でmLを学ぶことが多いです。"},
      {"q": "1L は何mL ですか？", "a": "1L＝1000mL です。1dL＝100mL、1L＝10dL の関係もあわせて覚えておきましょう。"},
      {"q": "dL はどんな場面で使いますか？", "a": "dL（デシリットル）は日本の小学校教育で主に使われる単位です。料理レシピで「1デシリットル（約コップ半分）」のように使われることがあります。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/unit-conversion.html", "emoji": "📏", "text": "単位換算ガイド"},
      {"href": "/tani-nagasa.html",     "emoji": "📏", "text": "長さの単位換算プリント【無料】小学3年生"},
      {"href": "/tani-omosa.html",      "emoji": "⚖️", "text": "重さの単位換算プリント【無料】小学3年生"},
      {"href": "/grade-2-tips.html",    "emoji": "📚", "text": "2年生の算数 完全ガイド"},
    ],
  },

  # ────────────────────────────────
  # グラフ・表
  # ────────────────────────────────
  {
    "filename": "graph-boubou.html",
    "title": "棒グラフの読み方・書き方プリント【無料】小学3〜4年生",
    "description": "棒グラフの読み方・書き方を印刷不要・スマホで即採点できる無料プリント。小学3〜4年生の算数で学ぶグラフの読み取り方をわかりやすく解説。毎回ランダム問題で繰り返し練習できます。",
    "h1": "棒グラフの読み方・書き方プリント【無料】小学3〜4年生",
    "eyecatch": "📊 棒グラフはデータを読む力の第一歩。印刷不要・スマホでその場で練習できます！",
    "body_html": """\
<h2>棒グラフとは</h2>
<p>棒グラフは数量を棒の長さで表したグラフです。複数の項目を比べるときや、最大・最小を一目で確認するのに適しています。</p>
<p>小学3年生では縦棒グラフの読み取りと作成を、4年生では折れ線グラフとの組み合わせや複数のデータを扱うグラフを学びます。</p>

<h2>棒グラフの読み方</h2>
<ol>
  <li><strong>タイトルを確認：</strong>何についてのグラフかを把握する</li>
  <li><strong>縦軸（目盛り）を確認：</strong>1目盛りが何を表すか（1・5・10など）確認する</li>
  <li><strong>棒の高さを読む：</strong>棒が目盛りの間にある場合は補間して読む</li>
  <li><strong>単位を確認：</strong>「人」「個」「kg」など単位を忘れず確認する</li>
</ol>
<div class="tip-box"><p>💡 1目盛りの値を最初に確認するクセをつけると、読み間違いが大幅に減ります。</p></div>

<h2>棒グラフの書き方</h2>
<ol>
  <li>縦軸に目盛りを等間隔で書く（最大値より少し大きい数まで）</li>
  <li>横軸に項目名を書く</li>
  <li>各項目の値に合わせて棒を描く（棒の幅は均一に）</li>
  <li>タイトルと単位を書く</li>
</ol>
<div class="warn-box"><p>⚠️ 棒の幅が不均一だったり、目盛りが等間隔でないとグラフの意味が変わってしまいます。丁寧に書く習慣をつけましょう。</p></div>""",
    "faq": [
      {"q": "棒グラフはいつ習いますか？", "a": "小学3年生で棒グラフの基礎を、4年生で折れ線グラフや複合グラフを学びます。中学ではヒストグラムなど発展的な内容につながります。"},
      {"q": "棒グラフと折れ線グラフの違いは何ですか？", "a": "棒グラフは量の大小を比べるのに適し、折れ線グラフは時間の経過に伴う変化を表すのに適しています。"},
      {"q": "棒グラフで1目盛りの読み方がわかりません", "a": "縦軸の数字を見て、隣り合う数字の差を目盛りの数で割ります。例えば0と10の間に5目盛りあれば1目盛り＝2です。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/graph-oretsu.html",   "emoji": "📈", "text": "折れ線グラフの読み方プリント【無料】小学4年生"},
      {"href": "/graph-circle.html",   "emoji": "🥧", "text": "円グラフ・帯グラフの読み方プリント【無料】小学5〜6年生"},
      {"href": "/grade-3-tips.html",   "emoji": "📚", "text": "3年生の算数 完全ガイド"},
      {"href": "/grade-4-tips.html",   "emoji": "📚", "text": "4年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "graph-oretsu.html",
    "title": "折れ線グラフの読み方プリント【無料】小学4年生",
    "description": "折れ線グラフの読み方・書き方を印刷不要・スマホで即採点できる無料プリント。小学4年生の算数で学ぶ折れ線グラフの変化の読み取り方をわかりやすく解説。",
    "h1": "折れ線グラフの読み方プリント【無料】小学4年生",
    "eyecatch": "📈 折れ線グラフは「変化」を読む力。印刷不要・スマホでその場で練習できます！",
    "body_html": """\
<h2>折れ線グラフとは</h2>
<p>折れ線グラフは、時間の経過とともに変化する数量を点と線で表したグラフです。「増えている」「減っている」「変わらない」という変化の傾向を視覚的に捉えることができます。</p>

<h2>折れ線グラフの読み方</h2>
<ol>
  <li><strong>横軸を確認：</strong>何を表すか（時刻・月・年など）確認する</li>
  <li><strong>縦軸の目盛りを確認：</strong>1目盛りの値を把握する</li>
  <li><strong>線の傾きで変化を読む：</strong>右上がり＝増加、右下がり＝減少、水平＝変化なし</li>
  <li><strong>変化が大きい・小さい区間を探す：</strong>線が急＝変化が大きい、線が緩やか＝変化が小さい</li>
</ol>
<div class="tip-box"><p>💡 「どこで一番増えた？」「どこで減り始めた？」と問いかけながら読むと読み取り力が上がります。</p></div>

<h2>棒グラフとの使い分け</h2>
<ul>
  <li><strong>折れ線グラフ：</strong>気温の変化、身長の推移など「時間×変化」を表すとき</li>
  <li><strong>棒グラフ：</strong>各クラスの人数、好きな食べ物など「項目×量」を比べるとき</li>
</ul>
<div class="warn-box"><p>⚠️ 折れ線グラフで縦軸が0から始まっていない場合、変化が実際より大きく見えることがあります。目盛りの数字を必ず確認しましょう。</p></div>""",
    "faq": [
      {"q": "折れ線グラフはいつ習いますか？", "a": "小学4年生で学習します。棒グラフ（3年生）の次に学ぶグラフで、時間の変化を表すために使います。"},
      {"q": "折れ線グラフで「変化が大きい」とはどういう意味ですか？", "a": "線の傾きが急なほど変化が大きいことを意味します。同じ横幅の区間でも線が急に上がっている場合、その期間に大きく増えていることを示します。"},
      {"q": "折れ線グラフと棒グラフを組み合わせた「複合グラフ」はいつ習いますか？", "a": "小学4〜5年生で学習します。異なる種類のデータ（気温と降水量など）を1つのグラフに表すときに使います。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/graph-boubou.html",  "emoji": "📊", "text": "棒グラフの読み方・書き方プリント【無料】小学3〜4年生"},
      {"href": "/graph-circle.html",  "emoji": "🥧", "text": "円グラフ・帯グラフの読み方プリント【無料】小学5〜6年生"},
      {"href": "/grade-4-tips.html",  "emoji": "📚", "text": "4年生の算数 完全ガイド"},
      {"href": "/grade-5-tips.html",  "emoji": "📚", "text": "5年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "graph-circle.html",
    "title": "円グラフ・帯グラフの読み方プリント【無料】小学5〜6年生",
    "description": "円グラフ・帯グラフの読み方を印刷不要・スマホで即採点できる無料プリント。小学5〜6年生の算数で学ぶ割合グラフの読み取りをわかりやすく解説。",
    "h1": "円グラフ・帯グラフの読み方プリント【無料】小学5〜6年生",
    "eyecatch": "🥧 円グラフ・帯グラフは割合を「見える化」したグラフ。印刷不要・スマホで練習できます！",
    "body_html": """\
<h2>円グラフ・帯グラフとは</h2>
<p>円グラフは全体を円で表し、各部分の割合を扇形の大きさで示したグラフです。帯グラフは全体を長方形で表し、帯の中に割合を示します。どちらも「全体のうち何割か」を直感的に把握するのに適しています。</p>

<h2>円グラフの読み方</h2>
<ol>
  <li><strong>全体が100%：</strong>すべての扇形を合計すると必ず100%になる</li>
  <li><strong>%の読み取り：</strong>各扇形に書かれた%の数字を読む</li>
  <li><strong>実際の数値を求める：</strong>全体の数×（%÷100）で実数を求める</li>
</ol>
<div class="formula-box"><p>実際の数 ＝ 全体 × 割合（%÷100）</p></div>

<h2>帯グラフの読み方</h2>
<p>帯グラフは左から順に割合の大きい順に並べることが多いです。円グラフより複数年度や複数グループの比較がしやすい特徴があります。</p>
<div class="tip-box"><p>💡 円グラフは「全体の中での割合」を、帯グラフは「複数グループを比べる」ときに適しています。</p></div>
<div class="warn-box"><p>⚠️ 割合（%）から実際の数値を求める問題では、全体の数が何かを確認してから計算しましょう。</p></div>""",
    "faq": [
      {"q": "円グラフはいつ習いますか？", "a": "小学5〜6年生で学習します。割合の学習（5年生）と関連して、データを割合で表す方法として扱われます。"},
      {"q": "円グラフの%から実際の人数を求める方法は？", "a": "全体の人数×（%÷100）で求めます。例えば全体200人で30%の部分なら、200×0.3＝60人です。"},
      {"q": "円グラフと帯グラフの違いは何ですか？", "a": "円グラフは1つのグループの内訳を見るのに適し、帯グラフは複数のグループを横に並べて比較するのに適しています。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/graph-boubou.html",    "emoji": "📊", "text": "棒グラフの読み方・書き方プリント【無料】小学3〜4年生"},
      {"href": "/graph-oretsu.html",    "emoji": "📈", "text": "折れ線グラフの読み方プリント【無料】小学4年生"},
      {"href": "/percentage-guide.html","emoji": "📚", "text": "割合・百分率ガイド"},
      {"href": "/grade-5-tips.html",    "emoji": "📚", "text": "5年生の算数 完全ガイド"},
    ],
  },

  # ────────────────────────────────
  # 文章題
  # ────────────────────────────────
  {
    "filename": "mondai-tasizan.html",
    "title": "たし算・ひき算の文章題プリント【無料】小学1〜2年生",
    "description": "たし算・ひき算の文章題を印刷不要・スマホで即採点できる無料プリント。小学1〜2年生の算数で学ぶ文章題の読み解き方・立式のコツをわかりやすく解説。",
    "h1": "たし算・ひき算の文章題プリント【無料】小学1〜2年生",
    "eyecatch": "📝 文章題は算数の「読解力」。合わせて・残りで・違いで…キーワードを覚えれば得意になれます！",
    "body_html": """\
<h2>文章題の解き方の基本</h2>
<p>文章題を解くには「問題文を読む→式を立てる→計算する→答えを書く」の4ステップが基本です。計算力だけでなく、文章を読んで場面をイメージする力が必要です。</p>

<h2>たし算になるキーワード</h2>
<ul>
  <li>「合わせて」「全部で」「みんなで」</li>
  <li>「増えた」「もらった」「加わった」</li>
  <li>「〜と〜を合わせると」</li>
</ul>
<div class="formula-box"><p>たし算：全体 ＝ 部分 ＋ 部分</p></div>

<h2>ひき算になるキーワード</h2>
<ul>
  <li>「残りは」「あと何個」「何人少ない」</li>
  <li>「使った」「あげた」「減った」</li>
  <li>「どちらが多い・少ない」「違いは」</li>
</ul>
<div class="formula-box"><p>ひき算：残り ＝ 全体 ー 使った分</p></div>

<div class="tip-box"><p>💡 問題文を読みながら「何が多い・何が少ない」と考えると式が立てやすくなります。絵や図で場面を描くのも効果的です。</p></div>

<h2>よくあるつまずきポイント</h2>
<ul>
  <li><strong>「違い」はひき算：</strong>「AはBより何個多い？」は大きい方から小さい方を引く</li>
  <li><strong>答えの単位を書く：</strong>「〇個」「〇人」「〇枚」と単位まで書く</li>
  <li><strong>「式」と「答え」を分けて書く：</strong>解答欄に式と答えを別々に書く習慣をつける</li>
</ul>""",
    "faq": [
      {"q": "文章題が苦手な子どもへの対策は？", "a": "まず問題文を音読させてみましょう。次に「何が出てきたか」「何を求めるか」を別々に確認します。絵や図を書いて場面をイメージすることも効果的です。"},
      {"q": "たし算とひき算をどう見分けますか？", "a": "「合わせて・全部で・増えた」ならたし算、「残り・使った・違いは」ならひき算がほとんどです。キーワードを覚えておくと判断しやすくなります。"},
      {"q": "文章題で式は必要ですか？", "a": "テストでは式を書くことが求められることが多いです。「□＋□＝□」の形で式を書いてから答えを求める習慣をつけましょう。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/word-problems.html",    "emoji": "📝", "text": "文章題の完全ガイド"},
      {"href": "/mondai-kakizan.html",   "emoji": "📝", "text": "かけ算・わり算の文章題プリント【無料】小学3〜4年生"},
      {"href": "/tasizan-print.html",    "emoji": "➕", "text": "たし算プリントまとめ"},
      {"href": "/hikizan-print.html",    "emoji": "➖", "text": "ひき算プリントまとめ"},
    ],
  },

  {
    "filename": "mondai-kakizan.html",
    "title": "かけ算・わり算の文章題プリント【無料】小学3〜4年生",
    "description": "かけ算・わり算の文章題を印刷不要・スマホで即採点できる無料プリント。小学3〜4年生の算数で学ぶ文章題の立式のコツ・等分除と包含除の違いをわかりやすく解説。",
    "h1": "かけ算・わり算の文章題プリント【無料】小学3〜4年生",
    "eyecatch": "📝 かけ算・わり算の文章題は「1つ分×いくつ分」の考え方が鍵。印刷不要・スマホで練習できます！",
    "body_html": """\
<h2>かけ算の文章題</h2>
<p>かけ算の文章題は「1つ分の数 × いくつ分 ＝ 全体」の形で考えます。</p>
<div class="formula-box"><p>全体 ＝ 1つ分 × いくつ分</p></div>
<ul>
  <li>「1袋に3個入りのあめが5袋あります。全部で何個？」→ 3×5＝15個</li>
  <li>キーワード：「〜ずつ」「1あたり」「何倍」</li>
</ul>

<h2>わり算の2種類</h2>
<p>わり算の文章題には2種類あり、どちらも「÷」を使いますが場面が異なります。</p>
<h3>等分除（とうぶんじょ）</h3>
<p>全体を同じ数に分けるとき。「12個を4人で等しく分けると1人何個？」→ 12÷4＝3個</p>
<h3>包含除（ほうがんじょ）</h3>
<p>いくつずつに分けるとき。「12個を3個ずつ分けると何袋？」→ 12÷3＝4袋</p>
<div class="tip-box"><p>💡 どちらも「÷」で計算しますが、場面をイメージして「分けるか・何袋かを求めるか」を確認しましょう。</p></div>

<h2>よくあるつまずきポイント</h2>
<ul>
  <li><strong>かけ算かわり算か迷う：</strong>「大きくなる（増える）→かけ算」「小さくなる（分ける）→わり算」が目安</li>
  <li><strong>余りのある文章題：</strong>「あと何個必要か」「何回できるか」で答えの扱いが変わる</li>
  <li><strong>単位の書き忘れ：</strong>「個」「人」「袋」など単位まで書く</li>
</ul>""",
    "faq": [
      {"q": "等分除と包含除の違いは何ですか？", "a": "等分除は「全体をいくつかに等しく分けて1つあたりを求める」（12個を4人に分けると1人何個？）、包含除は「全体の中にいくつ含まれるかを求める」（12個を3個ずつ分けると何袋？）です。"},
      {"q": "かけ算の文章題で式の書き方に決まりはありますか？", "a": "「1つ分の数 × いくつ分」の順で書くのが基本です。例えば「1袋3個×5袋」の場合は「3×5」と書きます。"},
      {"q": "余りのある文章題で答えをどう書けばいいですか？", "a": "「何個あまる」か「あと何個必要か」で異なります。余りが出る問題では「商あまり余り」の形で書き、文章に合わせて答えを選びましょう。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/word-problems.html",   "emoji": "📝", "text": "文章題の完全ガイド"},
      {"href": "/mondai-tasizan.html",  "emoji": "📝", "text": "たし算・ひき算の文章題プリント【無料】小学1〜2年生"},
      {"href": "/mondai-wariai.html",   "emoji": "📝", "text": "割合・百分率の文章題プリント【無料】小学5年生"},
      {"href": "/kuku-print.html",      "emoji": "✖️", "text": "九九プリントまとめ"},
    ],
  },

  {
    "filename": "mondai-wariai.html",
    "title": "割合・百分率の文章題プリント【無料】小学5年生",
    "description": "割合・百分率の文章題を印刷不要・スマホで即採点できる無料プリント。小学5年生の算数で学ぶ「もとにする量・比べる量・割合」の関係と文章題の解き方を解説。",
    "h1": "割合・百分率の文章題プリント【無料】小学5年生",
    "eyecatch": "📝 割合の文章題は「もと・くらべ・わりあい」の三角形が鍵。印刷不要・スマホで練習できます！",
    "body_html": """\
<h2>割合の基本公式</h2>
<p>割合の文章題は3つの量の関係を把握することが大切です。</p>
<div class="formula-box"><p>割合 ＝ 比べる量 ÷ もとにする量</p></div>
<div class="formula-box"><p>比べる量 ＝ もとにする量 × 割合</p></div>
<div class="formula-box"><p>もとにする量 ＝ 比べる量 ÷ 割合</p></div>

<h2>百分率（%）との関係</h2>
<p>割合を100倍したものが百分率（%）です。</p>
<ul>
  <li>割合0.1 ＝ 10%（十分の一）</li>
  <li>割合0.5 ＝ 50%（半分）</li>
  <li>割合1.2 ＝ 120%（1割2分多い）</li>
</ul>
<div class="tip-box"><p>💡 「くもわ」の三角形（く＝比べる量、も＝もとにする量、わ＝割合）を書いて公式を確認する方法が覚えやすいです。</p></div>

<h2>よくあるつまずきポイント</h2>
<ul>
  <li><strong>「もとにする量」がわからない：</strong>「〜の割合で」「〜に対して」の前にある量がもとにする量</li>
  <li><strong>%を割合に直し忘れる：</strong>%のまま計算せず、÷100して小数の割合にしてから計算する</li>
  <li><strong>増減の問題：</strong>「30%増し」は×1.3、「20%引き」は×0.8と覚える</li>
</ul>
<div class="warn-box"><p>⚠️ 「定価の20%引き」は「定価×0.8」です。「20%を引く」と考えて「定価−定価×0.2」でも同じ答えになります。</p></div>""",
    "faq": [
      {"q": "割合の文章題が苦手な場合どうすればいいですか？", "a": "「もとにする量・比べる量・割合」の3つを問題文から探す練習をしましょう。問題文に線を引いて3つの量を書き出すと整理しやすくなります。"},
      {"q": "割合と百分率の違いは何ですか？", "a": "割合は0〜1（またはそれ以上）の小数で表した比率、百分率はそれを100倍して「%」で表したものです。計算には割合（小数）を使います。"},
      {"q": "「歩合」（割・分・厘）はいつ習いますか？", "a": "歩合は小学5〜6年生で学びます。1割＝0.1＝10%の関係を覚えると、野球の打率などにも応用できます。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/word-problems.html",   "emoji": "📝", "text": "文章題の完全ガイド"},
      {"href": "/percentage-guide.html","emoji": "📊", "text": "割合・百分率ガイド"},
      {"href": "/mondai-sokudo.html",   "emoji": "📝", "text": "速さ・距離・時間の文章題プリント【無料】小学6年生"},
      {"href": "/grade-5-tips.html",    "emoji": "📚", "text": "5年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "mondai-sokudo.html",
    "title": "速さ・距離・時間の文章題プリント【無料】小学6年生",
    "description": "速さ・距離・時間の文章題を印刷不要・スマホで即採点できる無料プリント。小学6年生の算数で学ぶ「みはじ」の使い方と文章題の解き方をわかりやすく解説。",
    "h1": "速さ・距離・時間の文章題プリント【無料】小学6年生",
    "eyecatch": "📝 速さの文章題は「みはじ」の三角形でスッキリ解ける。印刷不要・スマホで練習できます！",
    "body_html": """\
<h2>速さの基本公式</h2>
<p>速さ・距離・時間の3つは「みはじ」の三角形で覚えます。</p>
<div class="formula-box"><p>速さ ＝ 距離 ÷ 時間　（みはじ：み÷じ）</p></div>
<div class="formula-box"><p>距離 ＝ 速さ × 時間　（はやさ×じ）</p></div>
<div class="formula-box"><p>時間 ＝ 距離 ÷ 速さ　（み÷は）</p></div>

<h2>単位に注意</h2>
<p>速さの問題で最もよくあるミスが単位の不一致です。</p>
<ul>
  <li>km/時（時速）とkm/分（分速）の混在</li>
  <li>時間を分に直さずに計算してしまう</li>
</ul>
<div class="tip-box"><p>💡 問題を解く前に「速さの単位は何か？」「時間の単位は何か？」を確認する習慣をつけましょう。</p></div>

<h2>よくある文章題のパターン</h2>
<ol>
  <li><strong>速さを求める：</strong>「4時間で240km進んだ。時速は？」→ 240÷4＝60km/時</li>
  <li><strong>距離を求める：</strong>「時速60kmで3時間走ると何km？」→ 60×3＝180km</li>
  <li><strong>時間を求める：</strong>「180kmを時速60kmで走ると何時間？」→ 180÷60＝3時間</li>
  <li><strong>追いつき・出会い問題：</strong>中学受験レベルだが基礎ができれば解ける</li>
</ol>
<div class="warn-box"><p>⚠️ 「分速」を使う問題で時間の答えが「分」になっている場合、時間・分に直して答えること。120分＝2時間のように。</p></div>""",
    "faq": [
      {"q": "「みはじ」とは何ですか？", "a": "「み（距離）・は（速さ）・じ（時間）」の頭文字をとった覚え方です。三角形の上に「み」、下左に「は」、下右に「じ」を書いて、求めたいものを隠すと公式が出てきます。"},
      {"q": "時速と分速の変換方法は？", "a": "時速÷60＝分速、分速×60＝時速です。例えば時速120kmは分速2km（120÷60）になります。"},
      {"q": "速さの文章題はいつ習いますか？", "a": "小学6年生で本格的に学習します。中学・高校では方程式を使った速さの問題につながります。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/word-problems.html",   "emoji": "📝", "text": "文章題の完全ガイド"},
      {"href": "/speed-distance.html",  "emoji": "🚗", "text": "速さ・距離・時間ガイド"},
      {"href": "/mondai-wariai.html",   "emoji": "📝", "text": "割合・百分率の文章題プリント【無料】小学5年生"},
      {"href": "/grade-6-tips.html",    "emoji": "📚", "text": "6年生の算数 完全ガイド"},
    ],
  },

  # ────────────────────────────────
  # 未就学児・入学準備
  # ────────────────────────────────
  {
    "filename": "youji-kazu.html",
    "title": "幼児向け数字の練習【無料】1〜10を楽しく覚える方法｜年少・年中・年長",
    "description": "幼児が1〜10の数字を楽しく覚えられる練習方法を解説。印刷不要・スマホで遊びながら数に親しめます。年少・年中・年長のお子さまにぴったりな数字の覚え方・練習法。",
    "h1": "幼児向け数字の練習【無料】1〜10を楽しく覚える方法",
    "eyecatch": "🔢 数字との出会いは「楽しい！」から始まるのが一番。生活の中でできる簡単な練習法を紹介します。",
    "body_html": """\
<h2>数字を覚える前に「数の概念」を育てよう</h2>
<p>数字（1・2・3…という文字）を覚える前に、「3つある」「2つある」という<strong>数の概念</strong>を体験で身につけることが大切です。文字の暗記より先に、「数えること」を楽しみましょう。</p>
<div class="tip-box"><p>💡 おやつの時に「いちご、いくつあるかな？」と一緒に数えるだけで、立派な算数の練習になります。</p></div>

<h2>年齢別の目安</h2>
<h3>年少（3〜4歳）</h3>
<ul>
  <li>1〜5までの数を声に出して数えられる</li>
  <li>「多い・少ない」がわかる</li>
  <li>○△□の形の名前を知っている</li>
</ul>
<h3>年中（4〜5歳）</h3>
<ul>
  <li>1〜10まで数えられる</li>
  <li>数字の1〜10を見て読める</li>
  <li>同じ数を並べて「同じ」とわかる</li>
</ul>
<h3>年長（5〜6歳）</h3>
<ul>
  <li>1〜10の数字を書ける</li>
  <li>簡単な「合わせていくつ？」がわかる</li>
  <li>10より大きい数（〜20）を数えられる</li>
</ul>

<h2>楽しく数に親しむ方法5選</h2>
<ol>
  <li><strong>階段を数えながら上る：</strong>「いち・に・さん…」と声に出して数える習慣</li>
  <li><strong>おやつを数える：</strong>「何個食べる？」「3個だよ」で自然に数の感覚が育つ</li>
  <li><strong>数字カードで神経衰弱：</strong>1〜5のカードで遊びながら数字の形を覚える</li>
  <li><strong>絵本で数を学ぶ：</strong>「だるまちゃんシリーズ」「いちごやいちご」など数が出てくる絵本</li>
  <li><strong>ブロックで積む：</strong>「3つ積んで」「2つ取って」で数の操作に慣れる</li>
</ol>
<div class="warn-box"><p>⚠️ 「早く覚えさせなきゃ」と焦ると逆効果。楽しい・できた！の体験を積み重ねることが一番の近道です。</p></div>

<h2>小学校入学前に身につけると安心なこと</h2>
<ul>
  <li>1〜10の数字を読み書きできる</li>
  <li>10までの数を正しく数えられる</li>
  <li>「前から3番目」など順序がわかる</li>
  <li>簡単な足し算・引き算のイメージが持てる（1+1=2 など）</li>
</ul>""",
    "faq": [
      {"q": "何歳から数字の練習を始めればいいですか？", "a": "個人差がありますが、数の概念（多い・少ない）は2〜3歳頃から、数字の読みは3〜4歳頃から始めるのが自然です。無理に教え込まず、日常生活の中で自然に触れさせましょう。"},
      {"q": "数字をなかなか覚えられません。どうすればいいですか？", "a": "数字カード・積み木・おはじきなど「見て・触って」学べる教材を使いましょう。同じ形を何度も目で見ることで自然と記憶されます。ゲーム感覚で繰り返すのがコツです。"},
      {"q": "幼児向けにおすすめの算数教材はありますか？", "a": "「くもんの数字カード」「タングラム」「百玉そろばん」などが人気です。タブレット教材では、シンプルな数かぞえアプリも効果的です。"},
      {"q": "小学校入学前にどの程度できていれば安心ですか？", "a": "1〜10の数字が読め、10まで数えられればまず安心です。書くことは小学校で丁寧に習うので、入学前は「読める・数えられる」を目標にしましょう。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "小学1年生のドリルをやってみる",
    "related": [
      {"href": "/suji-1to10.html",    "emoji": "🔢", "text": "数字1〜10の書き方・読み方【無料】幼児向け"},
      {"href": "/kazu-kuraberu.html", "emoji": "⚖️", "text": "多い・少ない・同じ数の比べ方【無料】幼児向け"},
      {"href": "/katachi-youji.html", "emoji": "🔵", "text": "丸・三角・四角の形【無料】幼児向け"},
      {"href": "/nyuugaku-mae.html",  "emoji": "🎒", "text": "小学校入学前に身につけたい算数の力"},
    ],
  },

  {
    "filename": "suji-1to10.html",
    "title": "数字1〜10の書き方・読み方【無料】幼児・年長向け練習",
    "description": "数字1〜10の書き方・読み方を幼児向けにわかりやすく解説。印刷不要・スマホで練習できます。書き順・覚え方のコツ・間違えやすいポイントを丁寧に説明。年長・年中のお子さまに。",
    "h1": "数字1〜10の書き方・読み方【無料】幼児・年長向け",
    "eyecatch": "✏️ 数字の書き方は「形」より「書き順」が大事。楽しく練習して小学校入学をスムーズに！",
    "body_html": """\
<h2>数字の読み方（1〜10）</h2>
<p>まず数字の「読み方」を覚えましょう。声に出して何度も読む練習が一番効果的です。</p>
<div class="formula-box"><p>1（いち）　2（に）　3（さん）　4（し・よん）　5（ご）<br>6（ろく）　7（しち・なな）　8（はち）　9（く・きゅう）　10（じゅう）</p></div>
<div class="tip-box"><p>💡 4は「し」より「よん」、7は「しち」より「なな」の読み方の方が日常生活では多く使われます。両方覚えておくと安心です。</p></div>

<h2>数字ごとの書き方のポイント</h2>
<h3>書き間違えやすい数字</h3>
<ul>
  <li><strong>1：</strong>上から下にまっすぐ引くだけ。横線を書きすぎない</li>
  <li><strong>2：</strong>上の丸→右→左下に曲げる→右に引く。曲がりすぎに注意</li>
  <li><strong>6と9：</strong>形が似ているので上下の向きに注意。6は上から丸へ、9は逆</li>
  <li><strong>3と8：</strong>3は開いた形、8は閉じた形。書き始める方向を覚える</li>
</ul>

<h2>楽しく書く練習方法</h2>
<ol>
  <li><strong>指書き：</strong>テーブルや手のひらに指で数字を書く（消せるので気楽）</li>
  <li><strong>砂・塩で書く：</strong>トレーに砂や塩を広げて指で書く感触遊び</li>
  <li><strong>大きく書く：</strong>最初は小さな枠でなく、A4いっぱいに大きく書く練習</li>
  <li><strong>なぞり書き：</strong>点線の数字をなぞる練習プリントを活用する</li>
</ol>
<div class="warn-box"><p>⚠️ 鉛筆の持ち方が定着する前に誤った持ち方で大量に練習させると修正が難しくなります。持ち方を先に確認しましょう。</p></div>

<h2>数字と量をセットで覚えよう</h2>
<p>「3」という文字と「🍎🍎🍎 3つ」をセットで覚えることで、数の概念と文字が結びつきます。カードを使って「数字カード」と「りんごの絵カード」をマッチングする遊びが効果的です。</p>""",
    "faq": [
      {"q": "数字の書き順は重要ですか？", "a": "正しい書き順を覚えると、速く・きれいに書けるようになります。特に小学校入学後は書き順を習うので、入学前から正しい書き順を身につけておくとスムーズです。"},
      {"q": "6と9・1と7など似た数字を混同します。どうすればいいですか？", "a": "「6は丸が下・9は丸が上」「1はただの棒・7は肘がある」などキャラクターのような特徴で覚えさせると混同が減ります。"},
      {"q": "何歳から書く練習を始めればいいですか？", "a": "鉛筆を正しく持てるようになる4〜5歳頃が一般的です。それより前は指書きや大きなクレヨンで形を楽しむ程度にしましょう。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "小学1年生のドリルをやってみる",
    "related": [
      {"href": "/youji-kazu.html",    "emoji": "🔢", "text": "幼児向け数字の練習【無料】1〜10を楽しく覚える方法"},
      {"href": "/kazu-kuraberu.html", "emoji": "⚖️", "text": "多い・少ない・同じ数の比べ方【無料】幼児向け"},
      {"href": "/nyuugaku-mae.html",  "emoji": "🎒", "text": "小学校入学前に身につけたい算数の力"},
      {"href": "/grade-1-tips.html",  "emoji": "📚", "text": "小学1年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "kazu-kuraberu.html",
    "title": "多い・少ない・同じ数の比べ方【無料】幼児・年少〜年長向け",
    "description": "多い・少ない・同じ数の比べ方を幼児向けにわかりやすく解説。印刷不要・スマホで練習できます。数の大小・等しい概念を楽しく身につける遊びと練習法。年少〜年長のお子さまに。",
    "h1": "多い・少ない・同じ数の比べ方【無料】幼児向け",
    "eyecatch": "⚖️ 「どっちが多い？」は算数の比べる力の出発点。遊びの中で自然に身につけましょう！",
    "body_html": """\
<h2>「数を比べる」力はなぜ大切？</h2>
<p>「多い・少ない・同じ」がわかる力は、小学校で学ぶ大小比較・不等号・割合すべての基礎になります。幼児期に遊びを通じて自然に身につけることが理想です。</p>

<h2>発達の目安</h2>
<ul>
  <li><strong>2〜3歳：</strong>「多い」「少ない」の言葉の意味がわかる</li>
  <li><strong>3〜4歳：</strong>2つのグループを並べて「どちらが多いか」がわかる</li>
  <li><strong>4〜5歳：</strong>1対1対応で「同じ数かどうか」を確かめられる</li>
  <li><strong>5〜6歳：</strong>数を数えて比べ、「〇個多い」と言える</li>
</ul>

<h2>遊びながら学ぶ方法</h2>
<h3>🍬 おかし比べゲーム</h3>
<p>おはじきやブロックを2つの皿に分けて「どちらが多い？」と聞く。正解したら1個もらえるルールに。</p>
<h3>🃏 数カード比べ</h3>
<p>1〜5のカードを2枚めくって「大きい方が勝ち」のカードゲーム。神経衰弱アレンジも◎。</p>
<h3>🚗 並べ比べ</h3>
<p>おもちゃの車と人形を1対1で並べて「どちらが余る？」で多い・少ないを体感させる。</p>
<div class="tip-box"><p>💡 1対1対応（並べて比べる）は「数を数えなくてもわかる」比べ方。数の本質的な理解につながります。</p></div>

<h2>不等号の準備（年長向け）</h2>
<p>小学校で学ぶ「3＜5」「7＞4」の記号の前段階として、「どちらが大きいか」をはっきり言葉で言える練習をしましょう。</p>
<div class="formula-box"><p>3は5より小さい　→　3 ＜ 5<br>7は4より大きい　→　7 ＞ 4</p></div>
<div class="warn-box"><p>⚠️ 不等号の向きは「口が大きい方（開いている方）が大きい数」と覚えると混同しにくくなります。</p></div>""",
    "faq": [
      {"q": "何歳から「多い・少ない」を教えていいですか？", "a": "2歳頃から日常会話の中で「こっちの方が多いね」と声かけするだけで十分です。3歳頃には具体物を使った比較遊びが楽しめるようになります。"},
      {"q": "数を数えずに多い・少ないを判断できますか？", "a": "できます。1対1に並べて「余ったほうが多い」と判断する方法（1対1対応）は、数を数えなくても大小を判断できる重要な考え方です。"},
      {"q": "小学校でいつ「大きい・小さい」の記号（不等号）を習いますか？", "a": "小学1年生で「＞・＜」の不等号を学びます。幼児期に「どちらが大きい？」の感覚を育てておくとスムーズに理解できます。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "小学1年生のドリルをやってみる",
    "related": [
      {"href": "/youji-kazu.html",   "emoji": "🔢", "text": "幼児向け数字の練習【無料】1〜10を楽しく覚える方法"},
      {"href": "/suji-1to10.html",   "emoji": "✏️", "text": "数字1〜10の書き方・読み方【無料】幼児向け"},
      {"href": "/nyuugaku-mae.html", "emoji": "🎒", "text": "小学校入学前に身につけたい算数の力"},
      {"href": "/grade-1-tips.html", "emoji": "📚", "text": "小学1年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "katachi-youji.html",
    "title": "丸・三角・四角の形【無料】幼児向け図形の名前と特徴",
    "description": "丸・三角・四角など基本の形を幼児向けにわかりやすく解説。印刷不要・スマホで練習できます。図形の名前・特徴・生活の中での見つけ方を楽しく紹介。年少〜年長のお子さまに。",
    "h1": "丸・三角・四角の形【無料】幼児向け図形の名前と特徴",
    "eyecatch": "🔵🔺🟥 形に気づく力は算数・図工の土台。「あ、あれ三角形だ！」を増やしましょう！",
    "body_html": """\
<h2>幼児が学ぶ基本の形</h2>
<p>幼児期に覚えたい基本の形は4つです。名前と特徴をセットで覚えましょう。</p>

<h3>○ まる（円・えん）</h3>
<ul>
  <li>角（かど）がなく、どこを測っても同じ長さ（半径）</li>
  <li>身近な例：コイン、時計、ボール、お月さま</li>
</ul>

<h3>△ さんかく（三角形）</h3>
<ul>
  <li>3つの角と3つの辺がある</li>
  <li>身近な例：おにぎり、屋根、三角帽子、サンドイッチ</li>
</ul>

<h3>□ しかく（四角形）</h3>
<ul>
  <li>4つの角と4つの辺がある</li>
  <li>身近な例：ドア、窓、本、テレビ、タイル</li>
</ul>

<h3>□ ちょうほうけい（長方形）と せいほうけい（正方形）</h3>
<ul>
  <li>長方形：横長の四角（4つの角がすべて直角）</li>
  <li>正方形：4つの辺がすべて同じ長さの四角（長方形の特別な形）</li>
</ul>

<h2>形を見つける遊び</h2>
<ol>
  <li><strong>形かくれんぼ：</strong>部屋の中から「三角形を3つ見つけよう！」で探す遊び</li>
  <li><strong>型抜きパズル：</strong>形のパズルで「同じ形の穴にはめる」感覚を育てる</li>
  <li><strong>折り紙で形を作る：</strong>正方形を折って三角形・長方形を作ってみる</li>
  <li><strong>粘土でつくる：</strong>「丸を作って」「三角を作って」で手で形を確かめる</li>
</ol>
<div class="tip-box"><p>💡 「あの看板、三角形だね！」など外出先でも形を探す習慣をつけると図形感覚が育ちます。</p></div>

<h2>小学校への接続</h2>
<p>幼児期に○△□の区別がしっかりできていると、小学1年生の図形学習がスムーズです。小学校では三角形・四角形・円・球・立方体などを順次学びます。</p>""",
    "faq": [
      {"q": "幼児に図形を教えるのはいつ頃から始めればいいですか？", "a": "2〜3歳頃から「丸・三角・四角」の名前を日常会話で使い始めると自然に覚えます。4〜5歳になると形の特徴（角の数など）も理解できるようになります。"},
      {"q": "丸・三角・四角以外に幼児期に覚えるべき形はありますか？", "a": "「ひし形（菱形）」「楕円（だえん）」「星形（ほしがた）」も絵本やおもちゃでよく登場します。幼児期は厳密な定義より「見て区別できる」ことを目標にしましょう。"},
      {"q": "正方形と長方形の違いをどう教えればいいですか？", "a": "「正方形は4つの辺が全部同じ長さ、長方形は縦と横が違う長さ」と説明します。折り紙（正方形）を半分に切ると長方形になる、と実体験で見せると理解しやすいです。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "小学1年生のドリルをやってみる",
    "related": [
      {"href": "/youji-kazu.html",    "emoji": "🔢", "text": "幼児向け数字の練習【無料】1〜10を楽しく覚える方法"},
      {"href": "/geometry-guide.html","emoji": "📐", "text": "図形・面積・円周の完全ガイド"},
      {"href": "/nyuugaku-mae.html",  "emoji": "🎒", "text": "小学校入学前に身につけたい算数の力"},
      {"href": "/grade-1-tips.html",  "emoji": "📚", "text": "小学1年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "nyuugaku-mae.html",
    "title": "小学校入学前に身につけたい算数の力【チェックリスト付き】",
    "description": "小学校入学前に身につけておきたい算数の力をチェックリスト付きで解説。数字の読み書き・数え方・図形・簡単なたし算など入学準備の算数を印刷不要・スマホで練習できます。",
    "h1": "小学校入学前に身につけたい算数の力【チェックリスト付き】",
    "eyecatch": "🎒 入学準備の算数、何ができていれば安心？ チェックリストと練習法をまとめました！",
    "body_html": """\
<h2>入学前チェックリスト</h2>
<p>以下の項目を確認してみましょう。全部できなくても大丈夫。できていないところを練習の優先順位にしましょう。</p>

<h3>🔢 数と計算</h3>
<ul>
  <li>☐ 1〜10の数字を見て読める</li>
  <li>☐ 1〜10を順番に声に出して数えられる</li>
  <li>☐ 10個のものを正確に数えられる</li>
  <li>☐ 1〜10の数字を書ける</li>
  <li>☐ 「3と2を合わせると5」など10までの合成・分解がわかる</li>
</ul>

<h3>📏 形・大きさ・比較</h3>
<ul>
  <li>☐ 丸・三角・四角の名前がわかる</li>
  <li>☐ 「大きい・小さい」「長い・短い」「重い・軽い」がわかる</li>
  <li>☐ 「多い・少ない・同じ」がわかる</li>
  <li>☐ 「前から3番目」など順序がわかる</li>
</ul>

<h3>⏰ 時間・生活</h3>
<ul>
  <li>☐ 「朝・昼・夜」の時間帯がわかる</li>
  <li>☐ 時計の数字（1〜12）を読める</li>
</ul>

<div class="tip-box"><p>💡 チェックが半分以下でも焦る必要はありません。小学校1年生は「ゼロから教える」前提で授業が設計されています。</p></div>

<h2>優先順位のつけ方</h2>
<h3>入学前に特に大切なこと（上位3つ）</h3>
<ol>
  <li><strong>1〜10を正確に数えられる</strong>（指を使ってもOK）</li>
  <li><strong>数字1〜10を読める</strong>（書けなくても大丈夫）</li>
  <li><strong>鉛筆を正しく持てる</strong>（数字を書く前提として）</li>
</ol>

<h2>残り時間別・入学準備プラン</h2>
<h3>入学まで3ヶ月以上ある場合</h3>
<p>焦らず遊びの中で数に触れる時間を増やしましょう。カードゲーム・おもちゃ・料理のお手伝いが最高の教材です。</p>
<h3>入学まで1ヶ月以内の場合</h3>
<p>「1〜10の数字を読む・数える」に絞って練習。毎日5〜10分、楽しくできる範囲で続けましょう。</p>
<div class="warn-box"><p>⚠️ 入学直前の詰め込みは「算数嫌い」のリスクがあります。楽しさを維持することを最優先にしてください。</p></div>""",
    "faq": [
      {"q": "入学前に算数の先取り学習は必要ですか？", "a": "必須ではありません。小学校の授業は算数を知らない前提で設計されています。ただし「数字を読める・10まで数えられる」程度はあると授業に入りやすいです。"},
      {"q": "数字を書くのを嫌がります。どうすればいいですか？", "a": "紙に書く前に指書き（テーブルに指で書く）や砂場での文字書きなど「消せる・失敗してもいい」環境から始めましょう。大きく書ける環境も効果的です。"},
      {"q": "保育園・幼稚園で算数の準備はしてもらえますか？", "a": "多くの保育園・幼稚園でも数字・形・比較の学習活動をしています。ご家庭では「楽しく数に触れる」時間を補完する形で関わると効果的です。"},
      {"q": "小学1年生の算数で最初に何を習いますか？", "a": "1年生の算数は「1〜5の数の読み書き・数え方」から始まります。次第に10まで、そして20まで拡張し、後半でたし算・ひき算を学びます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "小学1年生のドリルをやってみる",
    "related": [
      {"href": "/youji-kazu.html",   "emoji": "🔢", "text": "幼児向け数字の練習【無料】1〜10を楽しく覚える方法"},
      {"href": "/suji-1to10.html",   "emoji": "✏️", "text": "数字1〜10の書き方・読み方【無料】幼児向け"},
      {"href": "/kazu-kuraberu.html","emoji": "⚖️", "text": "多い・少ない・同じ数の比べ方【無料】幼児向け"},
      {"href": "/grade-1-tips.html", "emoji": "📚", "text": "小学1年生の算数 完全ガイド"},
    ],
  },

  # ────────────────────────────────
  # 未カバー単元
  # ────────────────────────────────
  {
    "filename": "kakudo-guide.html",
    "title": "角度の測り方・書き方プリント【無料】小学4年生｜分度器の使い方",
    "description": "角度の測り方・分度器の使い方を印刷不要・スマホで即採点できる無料プリント。小学4年生で学ぶ角度の基礎・鋭角・直角・鈍角の見分け方をわかりやすく解説。",
    "h1": "角度の測り方・書き方プリント【無料】小学4年生",
    "eyecatch": "📐 分度器の使い方をマスターしよう！角度は図形問題すべての基礎になります。印刷不要・スマホで練習できます。",
    "body_html": """\
<h2>角度の基本</h2>
<p>角度とは2本の直線が交わる「開き具合」を数字で表したものです。単位は「°（度）」を使います。</p>
<div class="formula-box"><p>直角 ＝ 90°　／　一直線 ＝ 180°　／　一回転 ＝ 360°</p></div>

<h2>角度の種類</h2>
<ul>
  <li><strong>鋭角（えいかく）：</strong>0°より大きく90°より小さい角（シャープな角）</li>
  <li><strong>直角（ちょっかく）：</strong>ちょうど90°の角（四角形の角）</li>
  <li><strong>鈍角（どんかく）：</strong>90°より大きく180°より小さい角（ゆるやかな角）</li>
  <li><strong>平角（へいかく）：</strong>ちょうど180°（一直線）</li>
</ul>

<h2>分度器の使い方</h2>
<ol>
  <li>分度器の中心を角の頂点に合わせる</li>
  <li>分度器の基線（0°の線）を角の一辺に重ねる</li>
  <li>もう一方の辺が指す目盛りを読む</li>
  <li>内側・外側の数字を間違えないよう注意（0°から数える）</li>
</ol>
<div class="tip-box"><p>💡 分度器には内側と外側に2列の数字があります。「0°から数えて何度か」を意識して読みましょう。</p></div>

<h2>三角形の角度の性質</h2>
<div class="formula-box"><p>三角形の3つの角の合計 ＝ 180°</p></div>
<div class="formula-box"><p>四角形の4つの角の合計 ＝ 360°</p></div>
<div class="warn-box"><p>⚠️ 分度器を当てるとき、頂点と基線がずれると正確に測れません。最初にしっかり合わせることが大切です。</p></div>""",
    "faq": [
      {"q": "角度はいつ習いますか？", "a": "小学4年生で学習します。分度器を使った角度の測り方・書き方から始まり、三角形・四角形の角の性質へと進みます。"},
      {"q": "分度器の内側と外側の数字の使い分けは？", "a": "0°から読み始める側の数字を使います。角が右向きに開いているなら右側の0から数える内側の数字、左向きなら左側から数える外側の数字を使います。"},
      {"q": "三角形の角の合計が180°になるのはなぜですか？", "a": "三角形の3つの頂点を一直線に並べると180°（一直線）になることから証明できます。小学生は実際に三角形を切って3つの角を一点に集めて確かめる実験が効果的です。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/geometry-guide.html",   "emoji": "📐", "text": "図形の完全ガイド"},
      {"href": "/menseki-sankakkei.html","emoji": "📐", "text": "三角形の面積プリント"},
      {"href": "/grade-4-tips.html",     "emoji": "📚", "text": "4年生の算数 完全ガイド"},
      {"href": "/grade-5-tips.html",     "emoji": "📚", "text": "5年生の算数 完全ガイド"},
    ],
  },

  {
    "filename": "gaisuu-guide.html",
    "title": "概数・四捨五入プリント【無料】小学4年生｜切り上げ・切り捨ても解説",
    "description": "概数・四捨五入の練習を印刷不要・スマホで即採点できる無料プリント。小学4年生で学ぶ四捨五入・切り上げ・切り捨て・上から〇桁の概数をわかりやすく解説。",
    "h1": "概数・四捨五入プリント【無料】小学4年生",
    "eyecatch": "🔢 概数は「だいたいいくつ？」を求める力。日常生活でも大活躍するスキルです。印刷不要で練習できます！",
    "body_html": """\
<h2>概数とは</h2>
<p>概数（がいすう）とは、ある数を「だいたいいくつ」と表したものです。正確な数より使いやすい場面（大まかな計算・統計など）で活躍します。</p>

<h2>四捨五入のルール</h2>
<div class="formula-box"><p>求める位の1つ下の数字が<br>0〜4 → 切り捨て（その桁を0にする）<br>5〜9 → 切り上げ（その桁を1増やす）</p></div>
<ul>
  <li>例）1234を百の位で四捨五入 → 十の位が3なので切り捨て → 1200</li>
  <li>例）1567を百の位で四捨五入 → 十の位が6なので切り上げ → 1600</li>
</ul>

<h2>「上から〇桁の概数」の求め方</h2>
<ol>
  <li>「上から2桁」なら、上から3桁目を四捨五入する</li>
  <li>例）83642を上から2桁 → 3桁目は6なので切り上げ → 84000</li>
</ol>
<div class="tip-box"><p>💡 「求める位」と「四捨五入する位（1つ下）」を混同しないようにしましょう。まず「どの桁まで残すか」を確認してから計算します。</p></div>

<h2>切り上げ・切り捨て</h2>
<ul>
  <li><strong>切り上げ：</strong>求める位より下の数字が1以上あれば必ず繰り上げる</li>
  <li><strong>切り捨て：</strong>求める位より下の数字をすべて0にする（無視する）</li>
</ul>
<div class="warn-box"><p>⚠️ 四捨五入・切り上げ・切り捨ての使い分けは問題文の指示を読んで判断します。「約〇〇」と書いてあれば四捨五入が多いですが、文脈で変わります。</p></div>""",
    "faq": [
      {"q": "四捨五入はいつ習いますか？", "a": "小学4年生で学習します。大きな数（億・兆）の学習と組み合わせて、概数の意味と四捨五入・切り上げ・切り捨ての方法を学びます。"},
      {"q": "「上から2桁の概数」と「百の位で四捨五入」は違いますか？", "a": "数によって一致する場合と異なる場合があります。「上から2桁」は数の大きさによって四捨五入する桁が変わります。例えば4桁の数なら百の位、5桁の数なら千の位で四捨五入します。"},
      {"q": "概数の計算（見積もり計算）はどうやって使いますか？", "a": "例えば「192×31」を概数で見積もると「200×30＝6000」となり、答えが6000前後であることを事前に確認できます。計算ミスの発見に役立ちます。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/large-numbers.html",  "emoji": "🔢", "text": "大きな数ガイド"},
      {"href": "/grade-4-tips.html",   "emoji": "📚", "text": "4年生の算数 完全ガイド"},
      {"href": "/mental-math.html",    "emoji": "🧠", "text": "暗算・計算力アップガイド"},
      {"href": "/calculation-power.html","emoji":"💪", "text": "計算力を上げる練習法"},
    ],
  },

  {
    "filename": "baisuu-yakusuu.html",
    "title": "倍数・約数プリント【無料】小学5年生｜公倍数・公約数の求め方",
    "description": "倍数・約数・公倍数・公約数の練習を印刷不要・スマホで即採点できる無料プリント。小学5年生で学ぶ最小公倍数・最大公約数の求め方をわかりやすく解説。",
    "h1": "倍数・約数プリント【無料】小学5年生",
    "eyecatch": "🔢 倍数・約数は分数の通分・約分に直結する重要単元。しっかりマスターしましょう！印刷不要で練習できます。",
    "body_html": """\
<h2>倍数とは</h2>
<p>ある数に整数を掛けてできる数を「倍数」といいます。</p>
<div class="formula-box"><p>3の倍数：3・6・9・12・15・18…（3×1, 3×2, 3×3…）</p></div>

<h2>約数とは</h2>
<p>ある数を割り切れる整数を「約数」といいます。</p>
<div class="formula-box"><p>12の約数：1・2・3・4・6・12（12を割り切れる数）</p></div>

<h2>公倍数・最小公倍数</h2>
<p>2つ以上の数に共通する倍数を「公倍数」、その中で最も小さいものを「最小公倍数」といいます。</p>
<ul>
  <li>4の倍数：4・8・12・16・20・<strong>24</strong>…</li>
  <li>6の倍数：6・12・18・<strong>24</strong>…</li>
  <li>4と6の最小公倍数 → <strong>12</strong></li>
</ul>
<div class="tip-box"><p>💡 最小公倍数は分数の「通分」で使います。分母をそろえる際に最小公倍数を見つける力が必要です。</p></div>

<h2>公約数・最大公約数</h2>
<p>2つ以上の数に共通する約数を「公約数」、最も大きいものを「最大公約数」といいます。</p>
<ul>
  <li>12の約数：1・2・3・4・6・12</li>
  <li>18の約数：1・2・3・6・9・18</li>
  <li>12と18の最大公約数 → <strong>6</strong></li>
</ul>
<div class="tip-box"><p>💡 最大公約数は分数の「約分」で使います。分子・分母を同じ数で割る際に最大公約数が便利です。</p></div>
<div class="warn-box"><p>⚠️ 倍数は無限にありますが、約数は有限です。約数を探すときは「1から順番に試す」か「かけ算の組み合わせを探す」方法が確実です。</p></div>""",
    "faq": [
      {"q": "倍数と約数の違いを簡単に説明してください", "a": "倍数は「その数を掛けてできる数」（6の倍数：6・12・18…）、約数は「その数を割り切れる数」（6の約数：1・2・3・6）です。倍数は大きくなる、約数は小さくなるイメージです。"},
      {"q": "最小公倍数の簡単な求め方はありますか？", "a": "「すだれ算（はしご算）」と呼ばれる方法が便利です。2つの数を共通の素因数で割り続けて、最後に残った数と割った数をすべて掛け合わせると最小公倍数が求まります。"},
      {"q": "倍数・約数はどこで使いますか？", "a": "最小公倍数は分数の通分（分母をそろえる）、最大公約数は分数の約分（分母・分子を同じ数で割る）に使います。分数の計算には不可欠な概念です。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/prime-numbers.html",  "emoji": "🔢", "text": "素数・素因数分解ガイド"},
      {"href": "/bunsuu-ibunmo.html",  "emoji": "➗", "text": "異分母の分数・通分プリント"},
      {"href": "/grade-5-tips.html",   "emoji": "📚", "text": "5年生の算数 完全ガイド"},
      {"href": "/fractions-guide.html","emoji": "➗", "text": "分数の完全ガイド"},
    ],
  },

  {
    "filename": "taishou-figure.html",
    "title": "対称図形プリント【無料】小学6年生｜線対称・点対称の書き方",
    "description": "対称図形（線対称・点対称）の練習を印刷不要・スマホで即採点できる無料プリント。小学6年生で学ぶ線対称・点対称の見分け方・かき方をわかりやすく解説。",
    "h1": "対称図形プリント【無料】小学6年生｜線対称・点対称",
    "eyecatch": "🪞 対称図形は「折ったらぴったり重なる」形の話。身近な図形への気づきが深まります！印刷不要で練習できます。",
    "body_html": """\
<h2>線対称とは</h2>
<p>ある直線で折ったとき、ぴったり重なる図形を「線対称な図形」といい、その折り目の直線を「対称の軸」といいます。</p>
<ul>
  <li>正三角形：対称の軸が3本</li>
  <li>正方形：対称の軸が4本</li>
  <li>円：対称の軸が無数にある</li>
</ul>
<div class="tip-box"><p>💡 ひらがなの中にも線対称な文字があります。「の」「つ」「く」は非対称、「大」「山」は縦軸で対称です。</p></div>

<h2>点対称とは</h2>
<p>ある点（対称の中心）を中心に180°回転させたとき、ぴったり重なる図形を「点対称な図形」といいます。</p>
<ul>
  <li>平行四辺形・長方形・正方形・ひし形は点対称</li>
  <li>正三角形は点対称ではない</li>
</ul>

<h2>対称図形の書き方</h2>
<h3>線対称の図形をかく手順</h3>
<ol>
  <li>対称の軸に対して垂直な線を各頂点から引く</li>
  <li>軸からの距離が同じ位置に対応する点を取る</li>
  <li>対応する点を結んで図形を完成させる</li>
</ol>
<div class="warn-box"><p>⚠️ 対称の軸からの「距離」が等しいことを確認しながら点を取りましょう。方眼紙を使うと正確に書けます。</p></div>""",
    "faq": [
      {"q": "線対称と点対称の違いは何ですか？", "a": "線対称は「直線で折ると重なる」、点対称は「1点を中心に180°回すと重なる」です。正方形・長方形・ひし形は両方に当てはまります。"},
      {"q": "対称図形はいつ習いますか？", "a": "小学6年生で学習します。図形の性質の総まとめとして扱われ、中学の合同・相似にも繋がります。"},
      {"q": "身近な線対称な図形の例を教えてください", "a": "蝶の羽・人の顔・漢字の「木」「山」「口」・国旗（日本・スイス・デンマークなど）が線対称です。身の回りを探すと図形感覚が育ちます。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/geometry-guide.html",  "emoji": "📐", "text": "図形の完全ガイド"},
      {"href": "/menseki-en.html",      "emoji": "⭕", "text": "円の面積プリント"},
      {"href": "/grade-6-tips.html",    "emoji": "📚", "text": "6年生の算数 完全ガイド"},
      {"href": "/suken-guide.html",     "emoji": "🏆", "text": "数検（算数検定）ガイド"},
    ],
  },

  {
    "filename": "kongozan.html",
    "title": "四則混合計算プリント【無料】小学4〜6年生｜計算の順序・カッコ",
    "description": "四則混合計算（たし算・ひき算・かけ算・わり算の混合）を印刷不要・スマホで即採点できる無料プリント。計算の順序・カッコの使い方を小学4〜6年生向けに解説。",
    "h1": "四則混合計算プリント【無料】小学4〜6年生",
    "eyecatch": "🔢 四則混合計算は「順番を守る」ことが全て。ルールを覚えて正確に解けるようになりましょう！印刷不要で練習できます。",
    "body_html": """\
<h2>計算の順序のルール</h2>
<p>たし算・ひき算・かけ算・わり算が混ざった式では、計算する順番が決まっています。</p>
<div class="formula-box"><p>① カッコの中を先に計算する<br>② かけ算・わり算を先に計算する<br>③ たし算・ひき算は後から左→右の順に計算する</p></div>

<h2>例題で確認</h2>
<ul>
  <li><strong>3＋4×2</strong>　→　かけ算を先に　→　3＋8＝<strong>11</strong></li>
  <li><strong>(3＋4)×2</strong>　→　カッコを先に　→　7×2＝<strong>14</strong></li>
  <li><strong>20÷4＋3×2</strong>　→　÷と×を先に　→　5＋6＝<strong>11</strong></li>
</ul>
<div class="tip-box"><p>💡 「カッコ・かけわり・たしひき」の優先順位を声に出して唱えながら解くと間違いが減ります。</p></div>

<h2>よくあるミスパターン</h2>
<ul>
  <li><strong>左から順に計算してしまう：</strong>2＋3×4を「(2＋3)×4＝20」と計算（正しくは2＋12＝14）</li>
  <li><strong>カッコを見落とす：</strong>式が長いときカッコを見落としやすい。先にカッコに○をつける</li>
  <li><strong>同じ優先度は左から：</strong>6÷2×3は左から「(6÷2)×3＝9」（÷と×は同順位で左から計算）</li>
</ul>
<div class="warn-box"><p>⚠️ かけ算とわり算は同じ優先度なので、どちらが先でも左から順に計算します。6÷2×3＝9（9ではなく1にしてしまうミスに注意）。</p></div>""",
    "faq": [
      {"q": "四則混合計算はいつ習いますか？", "a": "小学4年生で計算の順序（かけ算・わり算を先に）を学び、5〜6年生でより複雑な混合計算に発展します。"},
      {"q": "カッコがある場合の計算順序は？", "a": "カッコの中を最初に計算します。カッコが入れ子（二重カッコ）になっている場合は、一番内側のカッコから順に計算します。"},
      {"q": "計算の順序を間違えないコツはありますか？", "a": "計算する前に式全体を確認し、①カッコを○で囲む、②かけ算・わり算に下線を引く、③残ったたし算・ひき算を計算する、という手順で進めると間違いが減ります。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/calculation-power.html","emoji":"💪", "text": "計算力を上げる練習法"},
      {"href": "/mental-math.html",     "emoji": "🧠", "text": "暗算・計算力アップガイド"},
      {"href": "/grade-4-tips.html",    "emoji": "📚", "text": "4年生の算数 完全ガイド"},
      {"href": "/no-mistakes.html",     "emoji": "✅", "text": "計算ミスをなくす方法"},
    ],
  },

  # ────────────────────────────────
  # 季節・時期系
  # ────────────────────────────────
  {
    "filename": "natsu-sansu.html",
    "title": "夏休みの算数練習【無料】小学生｜つまずき解消・先取り学習プラン",
    "description": "夏休みに取り組む算数練習を学年別に解説。印刷不要・スマホで即採点できる無料ドリルで苦手単元の克服・2学期の先取りができます。小学1〜6年生向けの夏休み算数プラン。",
    "h1": "夏休みの算数練習【無料】小学生｜つまずき解消・先取り学習プラン",
    "eyecatch": "☀️ 夏休みは算数の苦手を一気に克服するチャンス！学年別の練習プランを紹介します。印刷不要・スマホで練習できます。",
    "body_html": """\
<h2>夏休みの算数練習で大切な2つの目標</h2>
<ol>
  <li><strong>1学期の苦手単元を克服する（復習）</strong></li>
  <li><strong>2学期の内容を先取りする（予習）</strong></li>
</ol>
<p>この2つをバランスよく取り組むことで、2学期のスタートを有利に切ることができます。</p>

<h2>学年別・夏休みの重点単元</h2>
<h3>小学1年生</h3>
<ul>
  <li>復習：繰り上がりのあるたし算・繰り下がりのあるひき算</li>
  <li>先取り：20までの数・時計の読み方</li>
</ul>
<h3>小学2年生</h3>
<ul>
  <li>復習：九九の定着（特に6・7・8の段）</li>
  <li>先取り：かけ算の筆算・長さの単位</li>
</ul>
<h3>小学3年生</h3>
<ul>
  <li>復習：わり算・あまりのあるわり算</li>
  <li>先取り：大きな数・小数の仕組み</li>
</ul>
<h3>小学4年生</h3>
<ul>
  <li>復習：角度・分度器の使い方・概数</li>
  <li>先取り：小数のかけ算・わり算</li>
</ul>
<h3>小学5年生</h3>
<ul>
  <li>復習：割合・百分率・倍数と約数</li>
  <li>先取り：比例・面積の公式発展</li>
</ul>
<h3>小学6年生</h3>
<ul>
  <li>復習：比・円の面積・分数のかけ算わり算</li>
  <li>先取り：中学の文字式の準備・比例・反比例</li>
</ul>

<h2>夏休みの学習スケジュールの作り方</h2>
<ol>
  <li>1学期のテストを見返して苦手単元を3つ書き出す</li>
  <li>1日15〜20分の練習時間を確保する</li>
  <li>苦手単元を前半（7月）に、先取りを後半（8月）に配置</li>
  <li>週1回は「模擬テスト」として総復習問題に取り組む</li>
</ol>
<div class="tip-box"><p>💡 毎日同じ時間（例：朝10時〜）に取り組むと習慣化しやすくなります。ゲーム・遊びの前に終わらせるルールも効果的です。</p></div>
<div class="warn-box"><p>⚠️ 夏休みに詰め込みすぎると算数嫌いになるリスクがあります。1日15〜30分を毎日続けることが最も効果的です。</p></div>""",
    "faq": [
      {"q": "夏休みの算数練習はいつから始めればいいですか？", "a": "夏休みに入ったらすぐ（7月下旬）から始めるのが理想です。8月後半は宿題の追い込みや体験学習で忙しくなることが多いため、前半に集中的に取り組むとよいでしょう。"},
      {"q": "夏休みに市販のドリルと無料プリントどちらがいいですか？", "a": "苦手単元が明確な場合は無料プリントで集中練習、総合的に力をつけたい場合は市販のドリル（学年別まとめ問題集）が適しています。両方を組み合わせるのも効果的です。"},
      {"q": "夏休みに1学期の内容を全部復習するのは無理ですか？", "a": "全範囲の完璧な復習は現実的ではありません。1学期の単元テストで60点以下だった単元に絞って重点的に練習するのが効率的です。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/",
    "cta_label": "学年を選んでドリルをスタート",
    "related": [
      {"href": "/study-routine.html",   "emoji": "📅", "text": "算数の学習習慣の作り方"},
      {"href": "/advance-study.html",   "emoji": "📚", "text": "先取り学習ガイド"},
      {"href": "/summer-math.html",     "emoji": "☀️", "text": "夏休みの算数攻略ガイド"},
      {"href": "/test-prep.html",       "emoji": "📝", "text": "テスト対策ガイド"},
    ],
  },

  # ────────────────────────────────
  # 親向けガイド
  # ────────────────────────────────
  {
    "filename": "sansu-kirai.html",
    "title": "算数が嫌いな子への対策【親向けガイド】原因と克服法",
    "description": "算数が嫌いになる原因と克服法を親向けに解説。印刷不要・スマホで即採点できる無料ドリルで楽しく算数に取り組める環境づくりのコツをまとめました。",
    "h1": "算数が嫌いな子への対策【親向けガイド】原因と克服法",
    "eyecatch": "😢 「算数嫌い」には必ず理由があります。原因を知れば対策できます。親ができるサポートを解説します。",
    "body_html": """\
<h2>算数嫌いになる主な原因</h2>
<ol>
  <li><strong>どこかでつまずいたまま先に進んでしまった</strong>（最多）</li>
  <li>テストで悪い点を取り「自分はできない」と思い込んだ</li>
  <li>親や先生に否定された経験がある</li>
  <li>計算ミスが多く、正しく解けた実感が持てない</li>
  <li>暗記（九九など）が苦手で達成感を得られなかった</li>
</ol>
<div class="tip-box"><p>💡 ほとんどの「算数嫌い」は「どこかの単元でつまずいたまま先に進んだ」が原因です。つまずき箇所に戻ることが最も効果的です。</p></div>

<h2>学年別・つまずきやすいポイント</h2>
<ul>
  <li><strong>1年生：</strong>繰り上がり・繰り下がりの計算</li>
  <li><strong>2年生：</strong>九九の暗記（特に7・8の段）</li>
  <li><strong>3年生：</strong>わり算・あまりのあるわり算</li>
  <li><strong>4年生：</strong>分数・小数の概念・角度</li>
  <li><strong>5年生：</strong>割合・百分率（0.3と30%の結びつき）</li>
  <li><strong>6年生：</strong>比・分数のわり算</li>
</ul>

<h2>親ができる6つのサポート</h2>
<ol>
  <li><strong>間違いを責めない：</strong>「なんで間違えるの」ではなく「どこで詰まったの？」と聞く</li>
  <li><strong>つまずき単元に戻る：</strong>今の学年より前の単元に戻って練習し直す</li>
  <li><strong>1日15分に絞る：</strong>長時間の勉強より毎日短時間の方が効果的</li>
  <li><strong>正解を褒める：</strong>結果でなくプロセス（「諦めずに考えた」）を褒める</li>
  <li><strong>ゲーム感覚を取り入れる：</strong>タイムアタック・点数記録など楽しみを作る</li>
  <li><strong>日常生活で算数を使う：</strong>お釣りの計算・料理の分量・時刻の計算を一緒に</li>
</ol>
<div class="warn-box"><p>⚠️ 「算数ができないと将来困る」という脅しは逆効果です。プレッシャーが増すと算数嫌いがさらに悪化します。</p></div>""",
    "faq": [
      {"q": "算数嫌いはいつ頃から始まりますか？", "a": "多くの場合、小学2年生の「九九」か小学3年生の「わり算」の時期につまずきが始まります。ここで克服できないと4年生以降の分数・小数に影響が出ます。"},
      {"q": "算数の家庭教師か塾に行かせるべきですか？", "a": "つまずきの単元が特定できていれば、まず無料の練習ドリルで自学を試みましょう。2〜3ヶ月改善が見られない場合は専門家のサポートを検討してください。"},
      {"q": "算数が嫌いな子に向いているドリルの種類はありますか？", "a": "問題数が少なく達成感を得やすいもの（1日5〜10問）、正解した時に視覚的なフィードバックがあるもの（スタンプ・シールなど）が向いています。オンラインの即採点ドリルも効果的です。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/",
    "cta_label": "学年を選んでドリルをスタート",
    "related": [
      {"href": "/math-anxiety.html",   "emoji": "😰", "text": "算数への苦手意識をなくす方法"},
      {"href": "/study-habits.html",   "emoji": "📚", "text": "算数の学習習慣ガイド"},
      {"href": "/teaching-tips.html",  "emoji": "👨‍👩‍👧", "text": "お子さまへの教え方ガイド"},
      {"href": "/parent-support.html", "emoji": "💪", "text": "保護者向けサポートガイド"},
    ],
  },

  {
    "filename": "shukudai-oshiekata.html",
    "title": "算数の宿題・教え方【親向けガイド】教えすぎずに伸ばすコツ",
    "description": "算数の宿題を子どもが嫌がらない教え方を親向けに解説。答えを教えすぎない・考える時間を与える・褒め方のコツなど、算数を好きにする宿題サポートの方法。",
    "h1": "算数の宿題・教え方【親向けガイド】教えすぎずに伸ばすコツ",
    "eyecatch": "📖 「すぐ教えてしまう」「逆に怒ってしまう」親御さんへ。子どもが自分で考える力を育てる教え方のコツを解説します。",
    "body_html": """\
<h2>算数の宿題サポートでよくある失敗</h2>
<ul>
  <li>❌ すぐに答えを教えてしまう（考える機会を奪う）</li>
  <li>❌ 間違いを強く叱る（算数嫌いの原因に）</li>
  <li>❌ 親が全部解いてしまう（本人の力がつかない）</li>
  <li>❌ 長時間やらせる（集中力の限界を超える）</li>
</ul>

<h2>効果的な宿題サポートの手順</h2>
<ol>
  <li><strong>まず自分で考えさせる（3〜5分）：</strong>「どこからわからない？」と聞いて、わかっている部分を確認する</li>
  <li><strong>ヒントを出す（答えは言わない）：</strong>「3×4はいくつだっけ？」など小さなヒントで考えるきっかけを作る</li>
  <li><strong>図や絵で一緒に考える：</strong>文章題は絵を描いて場面をイメージさせる</li>
  <li><strong>正解したら必ず褒める：</strong>「自分で気づけたね！」とプロセスを褒める</li>
</ol>
<div class="tip-box"><p>💡 「答えを教えない」ことが最重要です。答えを見せても力はつきません。「どうすればわかるか」を一緒に考えることが親のサポートです。</p></div>

<h2>宿題を嫌がるときの対処法</h2>
<ul>
  <li><strong>時間を短く区切る：</strong>「15分だけやろう」と時間を限定する</li>
  <li><strong>先に簡単な問題から：</strong>解ける問題から始めて「できた感」を作る</li>
  <li><strong>場所を変える：</strong>リビング・ダイニングテーブルなど気分転換できる場所で</li>
  <li><strong>ご褒美を設定する：</strong>「終わったら好きなことをしていい」ルールで動機づける</li>
</ul>
<div class="warn-box"><p>⚠️ 宿題の時間が毎日1時間以上かかる場合は、量が多いか理解が追いついていない可能性があります。担任の先生や塾への相談も検討してください。</p></div>""",
    "faq": [
      {"q": "算数の宿題で子どもが泣いてしまいます。どうすればいいですか？", "a": "泣いているときは一旦宿題を止め、気持ちが落ち着くのを待ちましょう。「難しいよね」と共感してから、できる問題から再挑戦します。無理に続けさせると算数嫌いが悪化します。"},
      {"q": "親が算数が苦手な場合、どうやって教えればいいですか？", "a": "答えがわからなくても大丈夫です。「一緒に考えよう」と子どもと並んで取り組む姿勢が一番大切です。教科書・ドリルの解説を一緒に読む方法も有効です。"},
      {"q": "宿題を自分でやろうとしない子への対策は？", "a": "宿題の「開始時間」を固定するのが効果的です。帰宅後すぐ・夕食前など毎日同じタイミングにすると習慣化します。「宿題が終わったらゲーム」のルールも動機づけになります。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/",
    "cta_label": "学年を選んでドリルをスタート",
    "related": [
      {"href": "/teaching-tips.html",  "emoji": "👨‍👩‍👧", "text": "お子さまへの教え方ガイド"},
      {"href": "/sansu-kirai.html",    "emoji": "😢", "text": "算数が嫌いな子への対策"},
      {"href": "/parent-support.html", "emoji": "💪", "text": "保護者向けサポートガイド"},
      {"href": "/study-habits.html",   "emoji": "📚", "text": "算数の学習習慣ガイド"},
    ],
  },

  {
    "filename": "slow-sansu.html",
    "title": "ゆっくり学ぶ子の算数練習法【支援学級・発達特性あり向け】",
    "description": "ゆっくり学ぶお子さま・発達特性のある子向けの算数練習法を解説。印刷不要・スマホで即採点できる無料ドリルで、つまずき単元から丁寧に学び直せます。支援学級でも活用できます。",
    "h1": "ゆっくり学ぶ子の算数練習法【支援学級・発達特性あり向け】",
    "eyecatch": "🌱 「わからない」は恥ずかしいことじゃない。どこからでも始められる算数練習法を紹介します。",
    "body_html": """\
<h2>ゆっくり学ぶ子が算数でつまずきやすい理由</h2>
<ul>
  <li>抽象的な概念（数の大きさ・割合など）がイメージしにくい</li>
  <li>手順が多い計算（筆算・分数）でステップを覚えきれない</li>
  <li>時間のプレッシャーで焦ってしまう</li>
  <li>ワーキングメモリの課題で「覚えながら計算する」が難しい</li>
</ul>

<h2>効果的な学習アプローチ</h2>
<h3>① 具体物から始める</h3>
<p>おはじき・ブロック・おもちゃなど実際に手で触れるものを使って数の概念を体感させます。「3個と2個を合わせると5個」を目で見て確かめてから、式（3＋2＝5）に結びつけます。</p>

<h3>② スモールステップで進む</h3>
<p>「1桁＋1桁」が完全にできてから「2桁＋1桁」へ。「余りなしのわり算」が完全にできてから「余りあり」へ。焦らず確実にできることを積み上げます。</p>

<h3>③ 視覚支援を使う</h3>
<p>計算の手順をカードや手順表に書いて手元に置いておく。筆算の位をそろえるための方眼紙を使う。</p>

<h3>④ 短時間・高頻度</h3>
<p>1日5〜10分を毎日続ける方が、週1回2時間よりはるかに効果的です。</p>

<div class="tip-box"><p>💡 「学年相当の内容」にこだわらず、「本人が確実にできるレベル」から始めることが最も大切です。1〜2学年前の内容に戻ることは決して恥ずかしいことではありません。</p></div>

<h2>にじゅうまる。が支援学習に向いている理由</h2>
<ul>
  <li>初級〜上級の3段階で本人のレベルに合わせられる</li>
  <li>時間制限なし（プレッシャーなく取り組める）</li>
  <li>毎回ランダム問題で繰り返し練習できる</li>
  <li>印刷不要でいつでも・どこでも始められる</li>
</ul>
<div class="warn-box"><p>⚠️ 発達障害（LD・ADHD・ASDなど）が疑われる場合は、学校の特別支援コーディネーターや医療機関への相談もあわせてご検討ください。</p></div>""",
    "faq": [
      {"q": "支援学級の子でもにじゅうまる。は使えますか？", "a": "はい、使えます。難易度を「初級」に設定し、学年も実際の学習レベルに合わせて選ぶことができます。1年生レベルから始めることも可能です。"},
      {"q": "算数の学習障害（LD/算数障害）とはどのようなものですか？", "a": "算数障害（ディスカリキュリア）は、知的発達に問題がないにも関わらず算数の習得に著しい困難を示す学習障害です。数の大小判断・計算・数的推論などに困難が出ます。専門家の診断が必要です。"},
      {"q": "何度やっても九九が覚えられません。どうすればいいですか？", "a": "視覚・聴覚・運動感覚を組み合わせる方法が効果的です。歌で覚える・リズムに合わせて唱える・体を動かしながら覚えるなど、一つの方法に固執せず複数試してみましょう。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルから始めてみる",
    "related": [
      {"href": "/sansu-kirai.html",    "emoji": "😢", "text": "算数が嫌いな子への対策"},
      {"href": "/math-anxiety.html",   "emoji": "😰", "text": "算数への苦手意識をなくす方法"},
      {"href": "/teaching-tips.html",  "emoji": "👨‍👩‍👧", "text": "お子さまへの教え方ガイド"},
      {"href": "/study-habits.html",   "emoji": "📚", "text": "算数の学習習慣ガイド"},
    ],
  },

  # ────────────────────────────────
  # 受験・検定・中学準備
  # ────────────────────────────────
  {
    "filename": "chuugaku-junbi.html",
    "title": "中学入学前に復習すべき算数まとめ【小6向け】中学数学の準備",
    "description": "中学入学前に復習すべき算数の単元を解説。印刷不要・スマホで即採点できる無料ドリルで分数・比・比例・文字式の準備を。小学6年生向けの中学数学入門ガイド。",
    "h1": "中学入学前に復習すべき算数まとめ【小6向け】",
    "eyecatch": "🎒 中学数学は小学算数の続き。入学前に押さえておくべき単元を総チェックしましょう！印刷不要で練習できます。",
    "body_html": """\
<h2>中学数学につながる小学算数の単元</h2>
<p>中学1年生の数学は「小学算数の拡張」です。以下の単元が特に重要です。</p>

<h2>絶対に固めておきたい5単元</h2>
<h3>① 分数の四則計算</h3>
<p>中学では分数を含む方程式・文字式を扱います。分数のたし算・ひき算（通分）・かけ算・わり算が速く正確にできることが必須です。</p>

<h3>② 比と比例</h3>
<p>中学の「比例・反比例」「一次関数」の直接の基礎。「a:b＝c:d」の比の計算と、比例グラフの読み方を確認しましょう。</h3>

<h3>③ 速さ・距離・時間</h3>
<p>中学では方程式を使った速さの問題が頻出。「みはじ」の公式を使いこなせることが前提になります。</p>

<h3>④ 文字を使った式の準備</h3>
<p>小学6年生では「□を使った式」を学びますが、これが中学の「x・yを使った式」の入門です。「□＋3＝7」を解く感覚を養っておきましょう。</p>

<h3>⑤ 負の数の準備</h3>
<p>小学算数では出てきませんが、中学1年生最初の単元が「負の数（−1・−2など）」です。温度計や地下・標高などで「0より小さい数」のイメージを持っておくと入りやすいです。</p>

<div class="tip-box"><p>💡 中学入学前の春休みに、小学6年生の内容を一通り復習するだけで、中学1年生の1学期が大きく変わります。</p></div>

<h2>中学でつまずかないための心がけ</h2>
<ul>
  <li>わからない問題をそのままにしない習慣をつける</li>
  <li>計算のスピードより正確さを優先する</li>
  <li>式を書いてから計算する習慣をつける</li>
</ul>""",
    "faq": [
      {"q": "中学数学は小学算数より難しいですか？", "a": "内容は難しくなりますが、小学算数の基礎がしっかりしていれば対応できます。特に分数・比・比例の理解が中学数学の土台になります。"},
      {"q": "小学算数のどの単元が中学数学に最も影響しますか？", "a": "分数の四則計算・比と比例・速さの公式の3つが特に重要です。この3つが自信を持って解ければ、中学数学のスタートは有利です。"},
      {"q": "中学受験と中学入学後の学習は別ですか？", "a": "中学受験は小学校範囲の発展問題、中学入学後の学習は中学校範囲の新内容です。受験対策と入学後の準備は別のものとして考えましょう。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルで総復習する",
    "related": [
      {"href": "/grade-6-tips.html",   "emoji": "📚", "text": "6年生の算数 完全ガイド"},
      {"href": "/ratio-guide.html",    "emoji": "📊", "text": "比と比例ガイド"},
      {"href": "/speed-distance.html", "emoji": "🚗", "text": "速さ・距離・時間ガイド"},
      {"href": "/suken-guide.html",    "emoji": "🏆", "text": "数検（算数検定）ガイド"},
    ],
  },

  # ────────────────────────────────
  # 計算力・学習法
  # ────────────────────────────────
  {
    "filename": "anzan-tips.html",
    "title": "暗算を速くする練習法【無料】小学生向け計算スピードアップ",
    "description": "暗算を速くする練習法を小学生向けに解説。印刷不要・スマホで即採点できる無料ドリルで計算スピードを上げるコツ・練習方法・暗算テクニックをまとめました。",
    "h1": "暗算を速くする練習法【無料】小学生向け",
    "eyecatch": "⚡ 暗算が速い子は算数テストで圧倒的に有利！練習すれば必ず速くなります。印刷不要で毎日練習できます。",
    "body_html": """\
<h2>暗算が速くなる3つの条件</h2>
<ol>
  <li><strong>九九の完全暗記：</strong>1〜9の段を即答できることがすべての基礎</li>
  <li><strong>数の分解・合成：</strong>「8＝5＋3」「7＝10−3」などの補数を瞬時に出せる</li>
  <li><strong>計算パターンの暗記：</strong>よく出る計算の答えを記憶する</li>
</ol>

<h2>暗算テクニック集</h2>
<h3>たし算の暗算</h3>
<ul>
  <li><strong>10の補数を使う：</strong>7＋8 → 7＋3＋5 ＝ 10＋5＝15</li>
  <li><strong>切り上げて引く：</strong>47＋19 → 47＋20−1＝66</li>
</ul>
<h3>ひき算の暗算</h3>
<ul>
  <li><strong>切り上げて足す：</strong>53−29 → 53−30＋1＝24</li>
  <li><strong>補数を使う：</strong>100−37 → 「37の補数」63</li>
</ul>
<h3>かけ算の暗算</h3>
<ul>
  <li><strong>×11の法則：</strong>23×11＝253（2と3を足して真ん中に入れる）</li>
  <li><strong>×5は÷2×10：</strong>24×5＝24÷2×10＝120</li>
  <li><strong>×9は×10−元の数：</strong>7×9＝70−7＝63</li>
</ul>
<div class="tip-box"><p>💡 暗算テクニックは「覚えるより慣れる」もの。毎日10問ずつ練習するだけで1ヶ月後には別人のように速くなります。</p></div>

<h2>1日5分の暗算トレーニング法</h2>
<ol>
  <li>タイマーを1分セット</li>
  <li>「今日は2桁＋1桁」など1種類に絞る</li>
  <li>できるだけ速く、できるだけ多く解く</li>
  <li>正解数を記録して毎日グラフをつける</li>
</ol>
<div class="warn-box"><p>⚠️ スピードばかり追うと計算ミスが増えます。「正確さ→スピード」の順番で練習しましょう。</p></div>""",
    "faq": [
      {"q": "暗算が速くなるには何から始めればいいですか？", "a": "まず九九の完全暗記から始めましょう。九九がすぐに出てこない場合、2桁以上の暗算は難しいです。次に10の補数（1と9、2と8、3と7…）を覚えます。"},
      {"q": "そろばんは暗算に効果的ですか？", "a": "そろばんは暗算力育成に非常に効果的です。珠算式暗算（頭の中でそろばんを動かす）は、処理速度と集中力を同時に鍛えます。"},
      {"q": "暗算の練習はどのくらいの期間で効果が出ますか？", "a": "毎日10〜15分の練習を続ければ、1〜2ヶ月で明らかな変化が出ます。特に九九の暗記は集中的に取り組めば2〜3週間で完成します。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/",
    "cta_label": "今すぐドリルで暗算練習",
    "related": [
      {"href": "/mental-math.html",      "emoji": "🧠", "text": "暗算・計算力アップガイド"},
      {"href": "/calculation-power.html","emoji": "💪", "text": "計算力を上げる練習法"},
      {"href": "/kuku-print.html",       "emoji": "✖️", "text": "九九プリントまとめ"},
      {"href": "/no-mistakes.html",      "emoji": "✅", "text": "計算ミスをなくす方法"},
    ],
  },

  {
    "filename": "tesuto-100ten.html",
    "title": "算数テストで100点を取る方法【小学生向け】見直し・時間配分",
    "description": "算数テストで100点を取るための戦略を小学生向けに解説。印刷不要・スマホで練習できます。見直しの方法・時間配分・ケアレスミスをなくすコツをまとめました。",
    "h1": "算数テストで100点を取る方法【小学生向け】",
    "eyecatch": "📝 100点は「計算力」だけじゃない。見直し・時間配分・書き方の習慣が合否を分けます！印刷不要で練習できます。",
    "body_html": """\
<h2>算数テストで点を落とす主な原因</h2>
<ol>
  <li><strong>ケアレスミス（最多）：</strong>計算は合っているのに写し間違い・単位忘れ・符号ミス</li>
  <li><strong>時間切れ：</strong>難しい問題に時間をかけすぎて簡単な問題が解けない</li>
  <li><strong>問題の読み間違い：</strong>「何を求めるか」を確認せずに解き始める</li>
  <li><strong>見直し不足：</strong>時間が余っても見直しをしない</li>
</ol>

<h2>テスト本番の時間配分</h2>
<div class="formula-box"><p>前半（1/2の時間）：全問題をサッと解く<br>後半（1/2の時間）：難問に再挑戦＋見直し</p></div>
<p>解けない問題は飛ばして後回しにするのがコツ。簡単な問題を先に全部取りきってから難しい問題に戻ります。</p>

<h2>ケアレスミスを減らす5つの習慣</h2>
<ol>
  <li><strong>答えを書いたら単位を確認する：</strong>「cm²」「個」「人」など単位を書いたか確認</li>
  <li><strong>式を必ず書く：</strong>暗算でなく式を書くことでミスの発見が容易になる</li>
  <li><strong>数字を丁寧に書く：</strong>1と7、6と0の読み間違いが多い。大きく丁寧に書く</li>
  <li><strong>計算は筆算で確認：</strong>頭の中だけで計算せず、かけ算・わり算は筆算で</li>
  <li><strong>見直しは「逆算」で確認：</strong>答えから逆算して問題の数字と一致するか確かめる</li>
</ol>
<div class="tip-box"><p>💡 「早く終わった！」と思ったら必ず見直しの時間に使いましょう。テストは先に出ても有利になりません。</p></div>
<div class="warn-box"><p>⚠️ ケアレスミスは「注意力不足」ではなく「確認習慣の不足」です。習慣は練習で身につきます。普段のドリルから見直しを必ずする癖をつけましょう。</p></div>""",
    "faq": [
      {"q": "算数テストの見直しは何をすればいいですか？", "a": "①単位が書いてあるか、②式と答えが一致しているか、③繰り上がり・繰り下がりのミスがないか、の3点を優先的に確認しましょう。"},
      {"q": "難しい問題と簡単な問題、どちらから解くべきですか？", "a": "必ず簡単な問題から解きましょう。難しい問題で時間を使い、簡単な問題が解けなかったという失敗が多いです。「解けない問題は3分考えたら飛ばす」ルールを決めておきましょう。"},
      {"q": "時間が余ったときは何をすればいいですか？", "a": "必ず見直しをしましょう。全問解いた後、①単位の確認、②計算の逆算確認、③問題文の読み直しの順で見直します。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/",
    "cta_label": "ドリルでテスト対策する",
    "related": [
      {"href": "/test-strategy.html",  "emoji": "📝", "text": "テスト戦略ガイド"},
      {"href": "/test-prep.html",      "emoji": "📝", "text": "テスト対策ガイド"},
      {"href": "/no-mistakes.html",    "emoji": "✅", "text": "計算ミスをなくす方法"},
      {"href": "/reduce-mistakes.html","emoji": "✅", "text": "ミスを減らす練習法"},
    ],
  },

  {
    "filename": "mainichi-drill.html",
    "title": "算数を毎日続けるコツ【無料】子どもが自分から取り組む習慣づけ",
    "description": "算数ドリルを毎日続けるための習慣づけのコツを解説。印刷不要・スマホで即採点できる無料ドリルを使って、子どもが自分から取り組む仕組みの作り方をまとめました。",
    "h1": "算数を毎日続けるコツ【無料】習慣づけの方法",
    "eyecatch": "📅 「続けること」が算数上達の最大の秘訣。毎日5分でも続ける仕組みを作りましょう！印刷不要で今日から始められます。",
    "body_html": """\
<h2>続かない理由のトップ3</h2>
<ol>
  <li>時間が決まっていない（いつやるか曖昧）</li>
  <li>量が多すぎる（1回にやりすぎて疲れる）</li>
  <li>達成感がない（頑張っても何も変わらない気がする）</li>
</ol>

<h2>毎日続くための「仕組み」の作り方</h2>
<h3>① 時間を固定する</h3>
<p>「毎日〇時に算数」と決めます。おすすめは「帰宅後すぐ」か「夕食前」。習慣は「いつも同じタイミング」で定着します。</p>

<h3>② 1日の量を小さく設定する</h3>
<p>「毎日25問（にじゅうまる1回分）」を目安にしましょう。少なく感じるくらいがちょうど良い。やる気がある日は2回分やってもOK。</p>

<h3>③ 記録して可視化する</h3>
<p>カレンダーにシールを貼る・スコアをノートに記録するなど、続けた実績を目で見えるようにします。連続記録を途切れさせたくない「継続欲」が生まれます。</p>

<h3>④ 小さなご褒美を設定する</h3>
<p>「7日続いたらゲームを1時間」など、子どもが喜ぶご褒美を一緒に決めます。</p>

<div class="tip-box"><p>💡 「今日は気分じゃない」という日でも「1問だけ」解けばOKというルールにすると、完全に途切れるのを防げます。</p></div>

<h2>スランプの乗り越え方</h2>
<ul>
  <li><strong>難易度を下げる：</strong>上級が続いているなら中級・初級に戻す</li>
  <li><strong>学年を下げる：</strong>前の学年の復習をして「できる感覚」を取り戻す</li>
  <li><strong>1〜2日休む：</strong>完全に力が抜けているなら短期休息も有効</li>
</ul>
<div class="warn-box"><p>⚠️ 「続けること」の目的は算数の力をつけること。苦しい状態で無理に続けると逆効果です。楽しく続けられる量・難易度を常に調整しましょう。</p></div>""",
    "faq": [
      {"q": "算数の毎日練習は何分が適切ですか？", "a": "小学生の集中力は学年×10分が目安です（1年生10分・6年生60分）。最初は5〜15分から始め、慣れてきたら増やしましょう。"},
      {"q": "土日も練習させた方がいいですか？", "a": "理想は毎日ですが、週5〜6日でも十分効果があります。土日は量を減らして「1問だけ解く」という形で習慣を途切れさせないのがコツです。"},
      {"q": "子どもがドリルを嫌がります。どうすれば自分からやるようになりますか？", "a": "「やらなければいけないもの」から「やると楽しいもの」に変えることが大切です。タイムアタック（自己ベスト更新）・スコア記録・ランキング挑戦など、ゲーム性を取り入れましょう。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/",
    "cta_label": "今日から毎日ドリルを始める",
    "related": [
      {"href": "/study-routine.html",  "emoji": "📅", "text": "算数の学習習慣の作り方"},
      {"href": "/study-habits.html",   "emoji": "📚", "text": "算数の学習習慣ガイド"},
      {"href": "/sansu-kirai.html",    "emoji": "😢", "text": "算数が嫌いな子への対策"},
      {"href": "/math-game.html",      "emoji": "🎮", "text": "算数ゲームで楽しく練習"},
    ],
  },

  # ────────────────────────────────
  # 学年・時期別まとめページ
  # ────────────────────────────────
  {
    "filename": "grade-1-matome.html",
    "title": "小学1年生 算数まとめ【無料】1学期〜3学期の全単元復習",
    "description": "小学1年生の算数全単元を無料で復習。印刷不要・スマホで即採点できるドリルでたし算・ひき算・繰り上がり・繰り下がり・時計・形を完全マスター。",
    "h1": "小学1年生 算数まとめ【無料】全単元復習",
    "eyecatch": "📚 1年生で学んだ算数を総まとめ！苦手な単元を見つけて、2年生に向けて完璧に仕上げましょう。印刷不要で練習できます。",
    "body_html": """\
<h2>小学1年生で学ぶ算数の全単元</h2>
<h3>1学期</h3>
<ul>
  <li>10までの数（数える・読む・書く）</li>
  <li>いくつといくつ（数の合成・分解）</li>
  <li>たし算の基礎（1桁＋1桁、答えが10以下）</li>
  <li>ひき算の基礎（1桁−1桁）</li>
</ul>
<h3>2学期</h3>
<ul>
  <li>繰り上がりのあるたし算（8＋6など）</li>
  <li>繰り下がりのあるひき算（13−7など）</li>
  <li>20までの数・大きな数の基礎</li>
  <li>長さ・広さ・かさの比較</li>
</ul>
<h3>3学期</h3>
<ul>
  <li>100までの数</li>
  <li>時計の読み方（何時・何時半）</li>
  <li>図形（三角形・四角形・円）</li>
  <li>3つの数のたし算・ひき算</li>
</ul>

<h2>1年生でつまずきやすいポイント</h2>
<ul>
  <li><strong>繰り上がりのたし算：</strong>「8＋6＝？」で10の補数を使う方法が定着するまで時間がかかる</li>
  <li><strong>繰り下がりのひき算：</strong>「13−7＝？」で「10から借りる」概念がわかりにくい</li>
  <li><strong>時計の読み方：</strong>30分・45分など長針の読み方で混乱する</li>
</ul>
<div class="tip-box"><p>💡 繰り上がり・繰り下がりは1年生最大の山場。ここをしっかり理解できると2年生の九九・筆算が格段に楽になります。</p></div>

<h2>2年生に向けての確認ポイント</h2>
<ul>
  <li>繰り上がりのたし算（全18パターン）が暗算でスラスラ言える</li>
  <li>繰り下がりのひき算（全18パターン）が暗算でスラスラ言える</li>
  <li>100までの数を読み書きできる</li>
  <li>時計の「何時何分」が読める</li>
</ul>""",
    "faq": [
      {"q": "小学1年生の算数で最も大切な単元はどれですか？", "a": "繰り上がりのあるたし算・繰り下がりのあるひき算が最も重要です。この2つが確実にできないと、2年生以降の筆算・九九の理解に支障が出ます。"},
      {"q": "時計の読み方がなかなか覚えられません", "a": "まず「何時」（短針）から始め、完全に読めるようになってから「何分」（長針）に進みましょう。長針は「5の倍数」のマス目で読む練習をすると覚えやすいです。"},
      {"q": "いくつといくつ（数の分解）の練習方法は？", "a": "おはじきを使って「5はいくつといくつ？」と実際に分けて確かめる練習が効果的です。5の分解（5＝1＋4, 2＋3）→6の分解…と順番に練習しましょう。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルで復習する",
    "related": [
      {"href": "/grade-1-tips.html",           "emoji": "📚", "text": "1年生の算数 完全ガイド"},
      {"href": "/tasizan-kuriagari-ari.html",   "emoji": "➕", "text": "繰り上がりあり たし算プリント"},
      {"href": "/hikizan-kurisagari-ari.html",  "emoji": "➖", "text": "繰り下がりあり ひき算プリント"},
      {"href": "/jikan-tokei.html",             "emoji": "🕐", "text": "時計の読み方プリント"},
    ],
  },

  {
    "filename": "grade-3-matome.html",
    "title": "小学3年生 算数まとめ【無料】わり算・小数・大きな数の全単元復習",
    "description": "小学3年生の算数全単元を無料で復習。印刷不要・スマホで即採点できるドリルでわり算・かけ算の筆算・小数・分数の基礎・時刻の計算を完全マスター。",
    "h1": "小学3年生 算数まとめ【無料】全単元復習",
    "eyecatch": "📚 3年生は算数の転換点！わり算・小数・分数と新しい概念が一気に増えます。苦手を早めに潰しましょう。印刷不要で練習できます。",
    "body_html": """\
<h2>小学3年生で学ぶ算数の全単元</h2>
<h3>1学期</h3>
<ul>
  <li>かけ算の筆算（2桁×1桁）</li>
  <li>わり算の基礎（九九の逆・余りなし）</li>
  <li>時刻と時間の計算</li>
  <li>長さ（mm・cm・m・km）</li>
</ul>
<h3>2学期</h3>
<ul>
  <li>大きな数（1万以上・億など）</li>
  <li>かけ算の筆算（3桁×1桁・2桁×2桁）</li>
  <li>あまりのあるわり算</li>
  <li>分数の基礎（分数の意味・大小）</li>
</ul>
<h3>3学期</h3>
<ul>
  <li>小数の基礎（0.1の概念・小数の大小）</li>
  <li>三角形（二等辺三角形・正三角形）</li>
  <li>重さ（g・kg）</li>
  <li>表とグラフ（棒グラフ）</li>
</ul>

<h2>3年生でつまずきやすいポイント</h2>
<ul>
  <li><strong>わり算：</strong>「24÷6」を九九の逆で考える発想の転換が難しい</li>
  <li><strong>あまりのあるわり算：</strong>余りの出し方・余りの確かめ算で詰まる</li>
  <li><strong>小数：</strong>0.1という概念・小数の大小比較で混乱する</li>
  <li><strong>時刻の計算：</strong>60進法の繰り上がりが10進法と違って難しい</li>
</ul>
<div class="tip-box"><p>💡 3年生でわり算をしっかり理解しておくと、4年生以降の分数・比率の学習がスムーズになります。</p></div>

<h2>4年生に向けての確認ポイント</h2>
<ul>
  <li>九九（1〜9の段）が即答できる</li>
  <li>2桁×2桁の筆算が正確にできる</li>
  <li>余りのあるわり算の確かめ算ができる</li>
  <li>小数の大小（0.3＜0.7など）がわかる</li>
</ul>""",
    "faq": [
      {"q": "3年生のわり算がまだ不安です。何から練習すればいいですか？", "a": "まず九九をすべて暗記することから始めましょう。わり算は九九の逆なので、九九が完璧になるとわり算も自然とできるようになります。"},
      {"q": "小数の概念をわかりやすく教える方法は？", "a": "1Lのペットボトルを使って「0.1Lはこのくらい」と実物で見せると理解しやすいです。目盛りのある容器で量を測ると小数の感覚が身につきます。"},
      {"q": "3年生で分数も習うのですか？", "a": "3年生では「分数の意味（半分・3等分）」と「分数の大小比較」の基礎を学びます。通分・約分などの計算は4〜5年生で学びます。"},
      {"q": "プリントは印刷できますか？", "a": "はい、PDF印刷に対応しています。ドリルページのPDF保存ボタンからA4サイズでダウンロードできます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルで復習する",
    "related": [
      {"href": "/grade-3-tips.html",    "emoji": "📚", "text": "3年生の算数 完全ガイド"},
      {"href": "/warizan-kantan.html",  "emoji": "➗", "text": "かんたんなわり算プリント"},
      {"href": "/warizan-amari.html",   "emoji": "➗", "text": "余りのあるわり算プリント"},
      {"href": "/syousuu-tasizan.html", "emoji": "🔢", "text": "小数のたし算・ひき算プリント"},
    ],
  },

]  # PAGES リストここまで


# ============================================================
# ヘルパー関数
# ============================================================

def build_faq_json(faq_list):
    items = []
    for item in faq_list:
        items.append({
            "@type": "Question",
            "name": item["q"],
            "acceptedAnswer": {"@type": "Answer", "text": item["a"]}
        })
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    json_str = json.dumps(schema, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{json_str}\n</script>'


def build_related_html(related_list):
    links = "\n".join(
        f'    <a href="{r["href"]}" style="display:block;background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;text-decoration:none;">'
        f'<span style="font-size:18px;margin-right:8px;">{r["emoji"]}</span>'
        f'<span style="font-size:13px;font-weight:600;color:#1E40AF;">{r["text"]}</span></a>'
        for r in related_list
    )
    return (
        '<div style="margin:32px 0;padding:20px 16px;background:#F8FAFC;border-radius:14px;border:1px solid #E2E8F0;">\n'
        '  <div style="font-size:13px;font-weight:700;color:#475569;margin-bottom:14px;">📖 関連記事</div>\n'
        '  <div style="display:grid;gap:8px;">\n'
        + links + '\n  </div>\n</div>'
    )


def generate(page, force=False):
    fpath = os.path.join(BASE_DIR, page["filename"])
    if not force and os.path.exists(fpath):
        return False  # スキップ

    html = TEMPLATE.format(
        BASE_URL   = BASE_URL,
        filename   = page["filename"],
        title      = page["title"],
        description= page["description"],
        h1         = page["h1"],
        eyecatch   = page["eyecatch"],
        body_html  = page["body_html"],
        faq_json   = build_faq_json(page["faq"]),
        cta_href   = page["cta_href"],
        cta_label  = page["cta_label"],
        related_html = build_related_html(page["related"]),
    )
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    return True


# ============================================================
# メイン
# ============================================================
if __name__ == "__main__":
    force = "--all" in sys.argv
    list_only = "--list" in sys.argv

    if list_only:
        print(f"定義済みページ一覧（{len(PAGES)}件）:")
        for p in PAGES:
            exists = "✅" if os.path.exists(os.path.join(BASE_DIR, p["filename"])) else "🆕"
            print(f"  {exists} {p['filename']}")
        sys.exit(0)

    created, skipped = [], []
    for page in PAGES:
        if generate(page, force=force):
            created.append(page["filename"])
            print(f"  ✅ 生成: {page['filename']}")
        else:
            skipped.append(page["filename"])
            print(f"  ⏭  スキップ（既存）: {page['filename']}")

    print(f"\n完了: 生成 {len(created)}件 / スキップ {len(skipped)}件")
    if created:
        print("サイトマップへの追加を忘れずに。")
