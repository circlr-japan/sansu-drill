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
<meta name="description" content="{description}｜無料・印刷不要で小学生が使える算数ドリルサイト「にじゅうまる。」">
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

  # ============================================================
  # 学年別まとめページ (grade-2, 4, 5, 6)
  # ============================================================
  {
    "filename": "grade-2-matome.html",
    "title": "小学2年生 算数まとめ｜全単元を総復習",
    "description": "印刷不要・スマホで即採点。小学2年生の算数全単元をまとめて総復習。たし算・ひき算の筆算、九九、長さ・水のかさ、時こくと時間をわかりやすく解説。",
    "h1": "小学2年生 算数まとめ｜全単元を総復習",
    "eyecatch": "2年生の算数は「九九」が最大の山場！9月から始まる九九を制覇すれば3年生以降がぐっと楽になります。このページで全単元をまとめて確認しましょう。",
    "body_html": """
<h2>2年生で学ぶ算数の全単元</h2>
<p>小学2年生では、1年生で学んだたし算・ひき算を発展させ、かけ算（九九）という新しい世界が始まります。</p>
<ul>
  <li><strong>たし算・ひき算の筆算</strong>：繰り上がり・繰り下がりを含む2桁〜3桁</li>
  <li><strong>かけ算（九九）</strong>：2〜9の段を完全暗記</li>
  <li><strong>長さの単位</strong>：mm・cm・m の換算</li>
  <li><strong>水のかさ</strong>：dL・L・mL の換算</li>
  <li><strong>時こくと時間</strong>：何時間後・何分後の計算</li>
  <li><strong>100より大きい数</strong>：1000までの数の概念</li>
  <li><strong>三角形と四角形</strong>：正方形・長方形・直角三角形</li>
</ul>

<h2>たし算・ひき算の筆算</h2>
<p>1年生で学んだ繰り上がりを発展させ、2桁・3桁の筆算を習得します。</p>
<div class="formula-box"><p>47 + 35 = ？　→　筆算で一の位から計算</p></div>
<div class="tip-box"><p>💡 筆算は右端（一の位）から計算する習慣をつけましょう。「右から計算！」と声に出すと定着します。</p></div>

<h2>かけ算（九九）完全マスター</h2>
<p>2年生最大の山場が九九です。2学期から始まる九九は、繰り返しの暗唱で覚えます。</p>
<ul>
  <li>まず「5の段・2の段・1の段」から始める</li>
  <li>「6の段・7の段」が覚えにくい→特訓ポイント</li>
  <li>毎日お風呂で1段ずつ唱える</li>
  <li>「逆九九」（9×4 → 4の段の9番目）も練習</li>
</ul>
<div class="warn-box"><p>⚠️ 九九は丸暗記でOK。理解は後からついてきます。まず「音」で覚えることが大切。</p></div>

<h2>長さ・水のかさ・時間の単位</h2>
<p>2年生では様々な単位を学びます。日常生活と結びつけて覚えましょう。</p>
<div class="formula-box"><p>1m = 100cm = 1000mm　／　1L = 10dL = 1000mL</p></div>

<h2>2年生でつまずきやすいポイント</h2>
<ol>
  <li>九九の6・7・8の段（特に7の段）</li>
  <li>時こくと時間の違い（「3時」と「3時間」）</li>
  <li>3桁の筆算での繰り上がり・繰り下がり</li>
</ol>
<div class="tip-box"><p>💡 時こくと時間は「今何時？（時こく）」「何時間たった？（時間）」と使い分けて説明すると伝わります。</p></div>
""",
    "faq": [
      {"q": "九九は何年生で習いますか？", "a": "小学2年生の2学期（9月〜12月ごろ）に習います。2の段から9の段まで順番に覚えていきます。"},
      {"q": "九九を覚えるコツは？", "a": "毎日お風呂で1段ずつ声に出して唱えるのが効果的です。歌のリズムで覚える「九九の歌」も人気です。"},
      {"q": "2年生で算数が苦手になる原因は？", "a": "九九の暗記でつまずくケースが最も多いです。早めに特訓を始め、毎日少しずつ練習する習慣が大切です。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/kuku-tips.html",    "emoji": "✖️", "text": "九九 完全攻略ガイド"},
      {"href": "/kuku-2dan.html",    "emoji": "✖️", "text": "2の段ドリル"},
      {"href": "/tasizan-hissan.html","emoji": "➕", "text": "たし算の筆算ドリル"},
      {"href": "/hikizan-hissan.html","emoji": "➖", "text": "ひき算の筆算ドリル"},
    ],
  },
  {
    "filename": "grade-4-matome.html",
    "title": "小学4年生 算数まとめ｜全単元を総復習",
    "description": "印刷不要・スマホで即採点。小学4年生の算数全単元を総復習。わり算の筆算・小数・分数・角度・面積・折れ線グラフをわかりやすく解説。",
    "h1": "小学4年生 算数まとめ｜全単元を総復習",
    "eyecatch": "4年生は「小数・分数・面積」と抽象的な概念が一気に増える学年。ここでの理解が5・6年生の基盤になります。苦手を残さず攻略しましょう！",
    "body_html": """
<h2>4年生で学ぶ算数の全単元</h2>
<ul>
  <li><strong>わり算の筆算</strong>：2桁÷1桁・3桁÷2桁</li>
  <li><strong>大きな数</strong>：億・兆の単位</li>
  <li><strong>小数</strong>：小数のたし算・ひき算・かけ算・わり算</li>
  <li><strong>分数</strong>：真分数・仮分数・帯分数、同分母の計算</li>
  <li><strong>角度</strong>：度数・分度器の使い方</li>
  <li><strong>面積</strong>：正方形・長方形の面積</li>
  <li><strong>折れ線グラフ</strong>：変化の読み取り</li>
  <li><strong>垂直と平行</strong>：直線の位置関係</li>
</ul>

<h2>わり算の筆算</h2>
<p>3年生で習ったわり算を発展させ、大きな数のわり算を筆算で解きます。</p>
<div class="formula-box"><p>84 ÷ 4 = ？　　256 ÷ 8 = ？</p></div>
<div class="tip-box"><p>💡 「たてる・かける・ひく・おろす」の4ステップを声に出しながら解くと定着します。</p></div>

<h2>小数と分数の基礎</h2>
<p>4年生で初めて本格的に学ぶ小数と分数。日常生活と結びつけて理解しましょう。</p>
<ul>
  <li>小数 → 「0.1が何個あるか」で考える</li>
  <li>分数 → 「ピザを何等分した何切れか」でイメージ</li>
  <li>仮分数・帯分数の変換を確実にマスター</li>
</ul>
<div class="warn-box"><p>⚠️ 分母が違う分数の計算は4年生では学びません（通分は5年生）。焦らず同分母の計算を固めましょう。</p></div>

<h2>面積の公式</h2>
<div class="formula-box"><p>長方形の面積 = たて × よこ　／　正方形の面積 = 一辺 × 一辺</p></div>

<h2>4年生でつまずきやすいポイント</h2>
<ol>
  <li>わり算の筆算（特に3桁÷2桁）</li>
  <li>小数点の位置（かけ算・わり算で動く）</li>
  <li>仮分数と帯分数の変換</li>
  <li>角度の読み取り（分度器の向き）</li>
</ol>
""",
    "faq": [
      {"q": "4年生の算数で最も重要な単元は？", "a": "小数と分数の基礎が最重要です。これが不完全だと5・6年生の学習全体に影響します。"},
      {"q": "わり算の筆算のコツは？", "a": "「たてる・かける・ひく・おろす」の4ステップを繰り返し練習するのが最も効果的です。"},
      {"q": "4年生の面積はどこまで学びますか？", "a": "4年生では長方形と正方形の面積を学びます。三角形・平行四辺形・円の面積は5〜6年生で学びます。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-hissan-2keta.html", "emoji": "➗", "text": "2桁のわり算筆算ドリル"},
      {"href": "/syousuu-tasizan.html",       "emoji": "🔢", "text": "小数のたし算・ひき算"},
      {"href": "/bunsuu-ibunmo.html",          "emoji": "½", "text": "分数のたし算・ひき算"},
      {"href": "/menseki-seihokei.html",       "emoji": "📐", "text": "面積の練習問題"},
    ],
  },
  {
    "filename": "grade-5-matome.html",
    "title": "小学5年生 算数まとめ｜全単元を総復習",
    "description": "印刷不要・スマホで即採点。小学5年生の算数全単元を総復習。通分・約分・体積・割合・速さ・平均・図形の合同をわかりやすく解説。",
    "h1": "小学5年生 算数まとめ｜全単元を総復習",
    "eyecatch": "5年生は算数で最も難しい学年とも言われます。「割合・速さ」という概念的な単元が登場し、つまずく子が急増。丁寧に基礎を固めることが最重要です。",
    "body_html": """
<h2>5年生で学ぶ算数の全単元</h2>
<ul>
  <li><strong>小数のかけ算・わり算</strong>：小数×小数、小数÷小数</li>
  <li><strong>分数の通分・約分</strong>：異分母の計算</li>
  <li><strong>分数のかけ算・わり算</strong>：帯分数も含む</li>
  <li><strong>体積</strong>：直方体・立方体の体積</li>
  <li><strong>割合</strong>：もとにする量・比べる量・割合の関係</li>
  <li><strong>百分率・歩合</strong>：%・割・分・厘</li>
  <li><strong>速さ</strong>：速さ・時間・距離の関係</li>
  <li><strong>平均</strong>：平均の求め方</li>
  <li><strong>図形の合同</strong>：合同な図形の性質</li>
  <li><strong>三角形・四角形の面積</strong>：公式の理解</li>
</ul>

<h2>割合の考え方</h2>
<p>5年生で最もつまずきやすい単元が「割合」です。3つの量の関係を確実に理解しましょう。</p>
<div class="formula-box"><p>割合 = 比べる量 ÷ もとにする量　（×100で%）</p></div>
<div class="tip-box"><p>💡 「くもわ」で覚える：く（比べる量）= も（もとにする量）× わ（割合）。図を描いて考えると分かりやすいです。</p></div>

<h2>速さの公式</h2>
<div class="formula-box"><p>速さ = 距離 ÷ 時間　／　距離 = 速さ × 時間　／　時間 = 距離 ÷ 速さ</p></div>
<div class="tip-box"><p>💡 「みはじ」（道のり・速さ・時間）の三角形を書いて覚えましょう。求めたいものを指で隠すと式が分かります。</p></div>

<h2>分数の通分・約分</h2>
<p>4年生の分数知識を発展させ、分母が違う分数の計算を学びます。</p>
<ul>
  <li><strong>通分</strong>：分母を最小公倍数に揃える</li>
  <li><strong>約分</strong>：分子・分母を最大公約数で割る</li>
</ul>
<div class="warn-box"><p>⚠️ 通分・約分はこの後ずっと使い続けます。確実にマスターしてから次に進みましょう。</p></div>

<h2>体積の公式</h2>
<div class="formula-box"><p>直方体の体積 = たて × よこ × 高さ　（cm³）</p></div>

<h2>5年生でつまずきやすいポイントTOP3</h2>
<ol>
  <li>割合（もとにする量・比べる量の取り違え）</li>
  <li>速さ（単位変換：km/h ↔ m/分）</li>
  <li>分数のわり算（逆数のかけ算への変換）</li>
</ol>
""",
    "faq": [
      {"q": "5年生の算数が難しいのはなぜですか？", "a": "割合・速さなど「数量の関係」を抽象的に考える単元が多いためです。具体的な例で考える練習を繰り返しましょう。"},
      {"q": "割合の「もとにする量」の見つけ方は？", "a": "「〜の何割」「〜の何%」という文の「〜」がもとにする量です。文章をよく読んで何を基準にしているか確認しましょう。"},
      {"q": "速さの計算でよく間違える点は？", "a": "単位変換（時速→分速、km→m）のミスが最も多いです。計算前に単位を揃える習慣をつけましょう。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/percentage-guide.html",  "emoji": "📊", "text": "割合・百分率の完全ガイド"},
      {"href": "/speed-distance.html",    "emoji": "🚗", "text": "速さ・時間・距離の解き方"},
      {"href": "/bunsuu-warizan.html",    "emoji": "½", "text": "分数のわり算ドリル"},
      {"href": "/taiseki-kantan.html",    "emoji": "📦", "text": "体積の練習問題"},
    ],
  },
  {
    "filename": "grade-6-matome.html",
    "title": "小学6年生 算数まとめ｜全単元を総復習・中学準備",
    "description": "印刷不要・スマホで即採点。小学6年生の算数全単元を総復習。比・比例・反比例・場合の数・円・柱体の体積・文字式を解説。中学数学の準備にも。",
    "h1": "小学6年生 算数まとめ｜全単元を総復習・中学準備",
    "eyecatch": "小学算数の集大成・6年生。比・比例・反比例・場合の数など中学数学に直結する内容が満載。ここを固めれば中学入学が楽になります！",
    "body_html": """
<h2>6年生で学ぶ算数の全単元</h2>
<ul>
  <li><strong>分数の計算</strong>：分数×分数、分数÷分数（完全マスター）</li>
  <li><strong>比と比の値</strong>：比の簡単な表し方</li>
  <li><strong>比例・反比例</strong>：グラフと式の関係</li>
  <li><strong>円の面積</strong>：π（pi）の概念</li>
  <li><strong>柱体の体積</strong>：角柱・円柱</li>
  <li><strong>拡大図・縮図</strong>：縮尺の読み取り</li>
  <li><strong>場合の数</strong>：組み合わせと順列の基礎</li>
  <li><strong>データの活用</strong>：平均・度数分布</li>
  <li><strong>文字を使った式</strong>：□や△、x・yの基礎</li>
</ul>

<h2>比と比例</h2>
<p>6年生の核心は「比・比例・反比例」。中学の一次関数・関数に直結します。</p>
<div class="formula-box"><p>比例：y = x × k （kは一定）　反比例：y = k ÷ x</p></div>
<div class="tip-box"><p>💡 比例は「x が2倍になるとy も2倍」、反比例は「x が2倍になるとy は½」で覚えましょう。</p></div>

<h2>円の面積</h2>
<div class="formula-box"><p>円の面積 = 半径 × 半径 × 3.14（π）</p></div>
<p>円周率 π ≒ 3.14 を使った計算。小数のかけ算が正確にできることが前提です。</p>

<h2>場合の数</h2>
<p>「何通り？」を数える力は、中学数学・高校数学の確率の基礎です。</p>
<ul>
  <li><strong>樹形図</strong>：順番に分岐を書いて数える</li>
  <li><strong>表を使う</strong>：縦横の組み合わせを数える</li>
</ul>
<div class="tip-box"><p>💡 場合の数は「もれなく・重複なく」数えることが大原則。樹形図を書く習慣をつけましょう。</p></div>

<h2>文字を使った式（中学数学の入口）</h2>
<p>□や△の代わりにx・yを使う考え方。中学の方程式に直結します。</p>
<div class="formula-box"><p>□ + 3 = 7 → x + 3 = 7 → x = 4</p></div>

<h2>中学数学につながる重要ポイント</h2>
<ol>
  <li>分数の計算（完全習得）</li>
  <li>比例・反比例（関数の基礎）</li>
  <li>文字式（方程式の入口）</li>
  <li>場合の数（確率の基礎）</li>
</ol>
<div class="warn-box"><p>⚠️ 6年生の内容で不安なまま中学に進むと、1年生の最初でつまずきます。苦手単元は今のうちに解決！</p></div>
""",
    "faq": [
      {"q": "6年生の算数で最も重要な単元は？", "a": "比・比例・反比例と分数の計算です。これらは中学数学の根幹で、理解が不十分だと中学でも苦労します。"},
      {"q": "場合の数の効率的な解き方は？", "a": "必ず樹形図か表を書いて整理する習慣をつけましょう。頭の中だけで数えようとすると漏れや重複が起きます。"},
      {"q": "円周率はなぜ3.14を使うのですか？", "a": "本来は無限小数（π≒3.14159...）ですが、小学校では計算しやすい3.14を使います。中学からはπをそのまま使います。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/ratio-guide.html",       "emoji": "📊", "text": "比・割合の完全ガイド"},
      {"href": "/bunsuu-warizan.html",    "emoji": "½", "text": "分数のわり算ドリル"},
      {"href": "/menseki-en.html",        "emoji": "⭕", "text": "円の面積ドリル"},
      {"href": "/chuugaku-junbi.html",    "emoji": "🎒", "text": "中学入学前の算数復習"},
    ],
  },

  # ============================================================
  # 季節ページ (春・秋・冬)
  # ============================================================
  {
    "filename": "haru-sansu.html",
    "title": "春休み・新学期の算数復習｜進級前にやっておくべき練習",
    "description": "印刷不要・スマホで即採点。春休みや新学期に最適な算数復習プリント。進級前の総まとめ・新学期の予習を無料でスマホから練習できます。",
    "h1": "春休み・新学期の算数復習｜進級前にやっておくべき練習",
    "eyecatch": "進級前の春休みは「前の学年の苦手をリセットする絶好のチャンス」！新学期を自信を持って迎えるために、今からできる算数復習を始めましょう。",
    "body_html": """
<h2>春休みに算数復習が重要な理由</h2>
<p>3月〜4月の春休みは、学年をまたぐ大切な時期。前の学年で残った苦手をそのままにすると、新学年でさらにつまずきやすくなります。</p>
<div class="tip-box"><p>💡 春休みの復習は「前の学年の苦手克服」が最優先。新学年の予習より、基礎の穴を埋めることを意識しましょう。</p></div>

<h2>学年別・春休みにやるべき復習リスト</h2>
<h3>1年生 → 2年生になる子</h3>
<ul>
  <li>繰り上がりのたし算（8+7など）が即答できるか確認</li>
  <li>繰り下がりのひき算（15-8など）の確認</li>
  <li>10のまとまりの概念</li>
</ul>
<h3>2年生 → 3年生になる子</h3>
<ul>
  <li>九九の全段を完全暗記（逆九九も）</li>
  <li>2桁の筆算（たし算・ひき算）</li>
  <li>時こくと時間の計算</li>
</ul>
<h3>3年生 → 4年生になる子</h3>
<ul>
  <li>わり算の基礎（九九を使ったわり算）</li>
  <li>3桁×1桁の筆算</li>
  <li>分数の意味（等分した1つ分）</li>
</ul>
<h3>4年生 → 5年生になる子</h3>
<ul>
  <li>小数の意味と比較</li>
  <li>わり算の筆算（3桁÷2桁）</li>
  <li>分数の基礎（真分数・仮分数）</li>
</ul>
<h3>5年生 → 6年生になる子</h3>
<ul>
  <li>通分・約分の確実な理解</li>
  <li>割合の計算（もとにする量・比べる量）</li>
  <li>面積の公式（三角形・平行四辺形）</li>
</ul>

<h2>新学期に向けた予習ポイント</h2>
<p>復習が終わったら、次学年の「最初の単元」だけ予習しておくと、新学期の授業がスムーズに始まります。</p>
<div class="warn-box"><p>⚠️ 予習のしすぎは禁物。「授業で習うことが分かってつまらない」になると逆効果です。最初の単元だけにとどめましょう。</p></div>

<h2>春休みの効果的な学習スケジュール</h2>
<ul>
  <li>1日15〜20分を目安にする</li>
  <li>朝食後か夕食前など「習慣の時間」に組み込む</li>
  <li>1日1単元ずつ進める</li>
  <li>完璧にできなくてもOK、「慣れる」が目的</li>
</ul>
""",
    "faq": [
      {"q": "春休みは何日くらい算数の勉強をすればいい？", "a": "毎日15〜20分を目標にしましょう。春休みが2週間なら合計3〜4時間の学習で前学年の苦手を十分カバーできます。"},
      {"q": "子供が勉強を嫌がる場合はどうすれば？", "a": "「勉強しなさい」ではなく「一緒にやってみよう」と誘うのが効果的です。ゲーム感覚で取り組める問題から始めましょう。"},
      {"q": "新学年の予習と復習、どちらを優先すべき？", "a": "まず前学年の復習を優先してください。基礎の穴を埋めることが、新学年での成功に最も直結します。"},
    ],
    "cta_href": "/index.html",
    "cta_label": "今すぐ算数ドリルをやってみる",
    "related": [
      {"href": "/review-method.html",          "emoji": "📝", "text": "算数の復習法・勉強法ガイド"},
      {"href": "/mainichi-drill.html",          "emoji": "📅", "text": "毎日続ける算数ドリルのコツ"},
      {"href": "/parent-support.html",          "emoji": "👨‍👩‍👧", "text": "親のサポート方法ガイド"},
      {"href": "/shukudai-oshiekata.html",      "emoji": "✏️", "text": "宿題の教え方・親の関わり方"},
    ],
  },
  {
    "filename": "aki-sansu.html",
    "title": "秋の算数復習｜2学期の苦手克服プリント無料",
    "description": "印刷不要・スマホで即採点。秋の2学期に多い算数の苦手を克服。九九・わり算・小数・分数・速さなど学年別の重要ポイントを無料で練習できます。",
    "h1": "秋の算数復習｜2学期の苦手克服プリント無料",
    "eyecatch": "2学期は算数の難易度が一気に上がる時期。九九・わり算・分数など各学年の難関単元が続々登場します。秋のうちに苦手を潰しておきましょう！",
    "body_html": """
<h2>秋の算数が難しい理由</h2>
<p>2学期（9〜12月）は、1学期の内容を発展させた難易度の高い単元が集中する時期です。</p>
<ul>
  <li>2年生：九九が始まる（最大の難関）</li>
  <li>3年生：わり算・あまりのあるわり算</li>
  <li>4年生：小数・分数・角度</li>
  <li>5年生：分数の計算・割合</li>
  <li>6年生：比例・場合の数</li>
</ul>
<div class="tip-box"><p>💡 2学期に苦手を作ると冬休みの宿題が大変になります。週末の15分復習でつまずきを早めに発見しましょう。</p></div>

<h2>学年別・2学期の重要ポイント</h2>
<h3>2年生：九九の攻略法</h3>
<p>9月から始まる九九は毎日の積み重ねが全て。1日1段のペースで進め、前の段を必ず復習してから新しい段へ。</p>
<div class="formula-box"><p>2の段→5の段→3の段→4の段→の順が覚えやすい！</p></div>

<h3>3年生：わり算とかけ算の筆算</h3>
<p>九九を使ったわり算は、九九が完璧でないとつまずきます。まず九九の確認から。</p>

<h3>4〜6年生：小数・分数の深化</h3>
<p>学年が上がるほど計算の複雑さが増します。前学年の基礎が土台になるので、遡って確認することも大切。</p>

<h2>秋の算数を乗り越えるための5つの習慣</h2>
<ol>
  <li><strong>毎日15分の復習</strong>：その日習ったことをその日中に確認</li>
  <li><strong>テストの見直し</strong>：間違えた問題を翌日もう一度解く</li>
  <li><strong>計算問題を毎朝5問</strong>：脳のウォームアップに最適</li>
  <li><strong>苦手単元の特定</strong>：「どこで間違えるか」をはっきりさせる</li>
  <li><strong>週末に前の週の復習</strong>：忘れる前に繰り返す</li>
</ol>
<div class="warn-box"><p>⚠️ 「分からないまま放置」が最も危険。分からない問題は次の日に先生に質問するか、保護者の方に聞きましょう。</p></div>
""",
    "faq": [
      {"q": "2学期から算数が急に難しくなった気がします", "a": "正しい感覚です。2学期は各学年の難関単元が集中します。1学期の基礎が固まっていれば乗り越えられますので、1学期の復習から始めてみてください。"},
      {"q": "九九をなかなか覚えられない場合は？", "a": "毎日お風呂で声に出して唱えるのが効果的です。また、6・7・8の段の中でも特定の組み合わせ（7×8など）を重点的に練習しましょう。"},
      {"q": "算数の苦手が2学期に発覚した場合、どう対処すれば？", "a": "まず「どの単元が分からないか」を特定することが大切。前の学年まで遡る必要がある場合も、早く気づくほど挽回が容易です。"},
    ],
    "cta_href": "/index.html",
    "cta_label": "今すぐ算数ドリルをやってみる",
    "related": [
      {"href": "/kuku-tips.html",      "emoji": "✖️", "text": "九九 完全攻略ガイド"},
      {"href": "/review-method.html",  "emoji": "📝", "text": "算数の復習法ガイド"},
      {"href": "/tesuto-100ten.html",  "emoji": "💯", "text": "算数テスト100点の取り方"},
      {"href": "/natsu-sansu.html",    "emoji": "☀️", "text": "夏休みの算数ドリル"},
    ],
  },
  {
    "filename": "fuyu-sansu.html",
    "title": "冬休み・冬の算数復習｜2学期の総まとめプリント無料",
    "description": "印刷不要・スマホで即採点。冬休みの算数復習に最適。2学期の総まとめと3学期の予習を無料でスマホから練習。九九・筆算・小数・分数を完全攻略。",
    "h1": "冬休み・冬の算数復習｜2学期の総まとめプリント無料",
    "eyecatch": "冬休みは短いからこそ、集中して「2学期の苦手をリセット」できる貴重な時間。あと少しで3学期・進級です。ここで差をつけましょう！",
    "body_html": """
<h2>冬休みに算数復習が重要な理由</h2>
<p>冬休み（12月末〜1月初旬）は通常2週間程度。短い休みですが、2学期で蓄積した苦手を一気に解消できる絶好の機会です。</p>
<div class="tip-box"><p>💡 冬休みの算数復習は「2学期の苦手克服」を中心に。年明けすぐのテスト対策にもなります。</p></div>

<h2>学年別・冬休みにやるべきこと</h2>
<h3>1〜2年生</h3>
<ul>
  <li>九九の全段確認（2年生）</li>
  <li>2桁の筆算の見直し</li>
  <li>時こくと時間の計算</li>
</ul>
<h3>3〜4年生</h3>
<ul>
  <li>わり算の筆算の確認</li>
  <li>小数・分数の基礎の確認</li>
  <li>面積・体積の公式チェック</li>
</ul>
<h3>5〜6年生</h3>
<ul>
  <li>割合・速さの解き方の確認</li>
  <li>分数の計算（通分・約分）</li>
  <li>比・比例の関係の復習</li>
</ul>

<h2>冬休みの効率的な学習スケジュール（例）</h2>
<ul>
  <li><strong>12/26〜28（3日間）</strong>：2学期の苦手単元を特定・集中練習</li>
  <li><strong>12/29〜31（3日間）</strong>：2学期の計算問題を広く復習</li>
  <li><strong>1/2〜3（2日間）</strong>：3学期の最初の単元を軽く予習</li>
  <li><strong>1/4〜（学校再開まで）</strong>：漢字・国語も含めて最終確認</li>
</ul>
<div class="warn-box"><p>⚠️ お正月は休んでOK！休みすぎると学習習慣が切れるので、1日10分だけでも続けることを意識しましょう。</p></div>

<h2>冬休みの算数ドリル活用法</h2>
<p>にじゅうまる算数ドリルは印刷不要でスマホから即採点できるので、帰省先でも旅行先でも練習できます。</p>
<ul>
  <li>移動中の電車・車の中でスマホドリル</li>
  <li>祖父母の家でもタブレットで練習</li>
  <li>1日5〜10問でも習慣を維持</li>
</ul>
""",
    "faq": [
      {"q": "冬休みは何時間くらい算数の勉強をすればいい？", "a": "1日20〜30分を目安にしましょう。2週間で合計5〜7時間の学習で2学期の苦手を十分カバーできます。"},
      {"q": "冬休み明けのテストはどの範囲から出ますか？", "a": "学校によりますが、2学期後半の内容が出ることが多いです。2学期後半に習った単元を中心に復習しましょう。"},
      {"q": "お正月の間も勉強が必要ですか？", "a": "無理する必要はありませんが、1日10分だけでも続けると年明けのリスタートがスムーズです。スマホドリルなら気軽に続けられます。"},
    ],
    "cta_href": "/index.html",
    "cta_label": "今すぐ算数ドリルをやってみる",
    "related": [
      {"href": "/natsu-sansu.html",   "emoji": "☀️", "text": "夏休みの算数ドリル"},
      {"href": "/haru-sansu.html",    "emoji": "🌸", "text": "春休みの算数復習"},
      {"href": "/aki-sansu.html",     "emoji": "🍂", "text": "秋の算数復習"},
      {"href": "/review-method.html", "emoji": "📝", "text": "算数の復習法ガイド"},
    ],
  },

  # ============================================================
  # 親向け・サポート系追加
  # ============================================================
  {
    "filename": "keisan-machigai.html",
    "title": "計算ミスをなくす方法｜小学生の見直し習慣づけ",
    "description": "印刷不要・スマホで即採点。小学生が計算ミスをなくすための具体的な方法を解説。見直しの習慣、ケアレスミスの原因と対策を保護者向けに紹介。",
    "h1": "計算ミスをなくす方法｜小学生の見直し習慣づけ",
    "eyecatch": "「分かっているのにミスする」は算数あるある。計算ミスは「不注意」ではなく「習慣」で防げます。正しい見直し方法を身につけましょう！",
    "body_html": """
<h2>計算ミスの主な原因</h2>
<p>子供の計算ミスにはパターンがあります。原因を理解すれば、効果的な対策が打てます。</p>
<ul>
  <li><strong>書き写しミス</strong>：問題の数字を読み間違える・書き間違える</li>
  <li><strong>繰り上がり・繰り下がりの忘れ</strong>：筆算で小さい数字を書いたまま忘れる</li>
  <li><strong>計算の手抜き</strong>：暗算でやろうとして間違える</li>
  <li><strong>焦り</strong>：テストで急ぐあまりミスが増える</li>
  <li><strong>問題の読み違い</strong>：「+」を「×」と見間違えるなど</li>
</ul>
<div class="tip-box"><p>💡 ミスが多い問題を記録しておくと「自分がどこでよく間違えるか」のパターンが見えてきます。</p></div>

<h2>計算ミスを減らす5つの習慣</h2>
<h3>1. 筆算を丁寧に書く</h3>
<p>位をきちんと揃えて書く。マス目のあるノートを使うのが効果的です。</p>
<h3>2. 繰り上がりを必ず書く</h3>
<p>「覚えているから書かなくていい」は禁物。小さくてもいいので必ず書く習慣を。</p>
<h3>3. 計算後に検算する</h3>
<p>答えが出たら、逆算で確認。たし算なら引いて元の数に戻るかチェック。</p>
<h3>4. 問題を指でなぞりながら読む</h3>
<p>書き写しミスを防ぐために、数字を声に出しながら読む習慣をつける。</p>
<h3>5. テストでは「見直し時間」を作る</h3>
<p>全問解き終えたら、最初から見直す時間を必ず確保する。</p>
<div class="warn-box"><p>⚠️ 「早く終わらせること」をほめると、丁寧さより速さを優先するようになります。正確さを先にほめましょう。</p></div>

<h2>親ができるサポート</h2>
<ul>
  <li>間違えた問題を「怒らずに」一緒に見直す</li>
  <li>「どこで間違えたと思う？」と本人に考えさせる</li>
  <li>正確に解けたときは「丁寧にできたね」とほめる</li>
  <li>見直しの時間を一緒に習慣にする</li>
</ul>

<h2>学年別・よくある計算ミス</h2>
<ul>
  <li><strong>1〜2年生</strong>：繰り上がりを忘れる、数字の書き間違い</li>
  <li><strong>3年生</strong>：九九のうっかりミス、筆算の位の間違い</li>
  <li><strong>4〜5年生</strong>：小数点の位置、通分・約分の忘れ</li>
  <li><strong>6年生</strong>：単位変換のミス、計算の手順を省く</li>
</ul>
""",
    "faq": [
      {"q": "計算ミスは何歳になったら減りますか？", "a": "正しい習慣を身につければ、どの学年でも改善できます。「見直しの習慣」「丁寧に書く習慣」が身につくと劇的に減ります。"},
      {"q": "うちの子は見直しをしません。どうすれば？", "a": "最初は保護者が「一緒に見直そう」と誘って習慣化しましょう。5分間の見直し時間をルールとして設けるのも効果的です。"},
      {"q": "計算ミスが多い子は算数が苦手なのですか？", "a": "必ずしもそうではありません。計算の概念は理解できているがミスが多いケースは多いです。習慣改善で大きく改善できます。"},
    ],
    "cta_href": "/index.html",
    "cta_label": "今すぐ算数ドリルで練習する",
    "related": [
      {"href": "/tesuto-100ten.html",      "emoji": "💯", "text": "算数テスト100点の取り方"},
      {"href": "/review-method.html",      "emoji": "📝", "text": "算数の復習法ガイド"},
      {"href": "/shukudai-oshiekata.html", "emoji": "✏️", "text": "宿題の教え方ガイド"},
      {"href": "/parent-support.html",     "emoji": "👨‍👩‍👧", "text": "保護者のサポート方法"},
    ],
  },
  {
    "filename": "sansu-test-taisaku.html",
    "title": "算数テスト対策｜直前1週間でできる得点アップ法",
    "description": "印刷不要・スマホで即採点。算数のテスト直前1週間の勉強法を解説。苦手単元の絞り込み・計算練習・見直し習慣まで具体的な対策を紹介。",
    "h1": "算数テスト対策｜直前1週間でできる得点アップ法",
    "eyecatch": "テスト1週間前から何をすれば点数が上がるの？効果的な算数テスト対策を学年別にまとめました。今すぐ実践できる方法だけを紹介します！",
    "body_html": """
<h2>テスト前の準備：まず「出題範囲の確認」から</h2>
<p>テスト勉強の第一歩は、範囲を正確に把握すること。テスト範囲の教科書・ノートをチェックしましょう。</p>
<div class="tip-box"><p>💡 テストの日程と範囲を最初に確認し、「1日あたり何ページ復習できるか」から逆算して計画を立てましょう。</p></div>

<h2>テスト1週間前のスケジュール</h2>
<ul>
  <li><strong>7日前</strong>：テスト範囲の確認・苦手単元のリストアップ</li>
  <li><strong>6〜5日前</strong>：苦手単元の集中練習（公式・解き方の確認）</li>
  <li><strong>4〜3日前</strong>：教科書の例題・練習問題を全て解く</li>
  <li><strong>2日前</strong>：間違えた問題を中心に再チャレンジ</li>
  <li><strong>前日</strong>：計算問題を20〜30問解いて脳を活性化</li>
  <li><strong>当日朝</strong>：公式・ポイントを見直す（新しいことはしない）</li>
</ul>

<h2>得点を上げる3つの重点ポイント</h2>
<h3>1. 基本問題を確実に取る</h3>
<p>テストの7〜8割は基本問題です。難問より基本問題を確実に解ける練習を優先しましょう。</p>
<h3>2. 計算ミスゼロを目指す</h3>
<p>見直し習慣をつけるだけで5〜10点アップも珍しくありません。検算の方法を必ず実践。</p>
<h3>3. 途中式を必ず書く</h3>
<p>答えが間違っていても途中式が正しければ部分点がもらえることも。作業を省かずに書きましょう。</p>
<div class="warn-box"><p>⚠️ テスト前日の夜更かしは絶対NG。睡眠不足は計算ミスを増やします。いつも通り寝ることが最重要。</p></div>

<h2>学年別・テストで狙われやすい問題</h2>
<ul>
  <li><strong>1〜2年生</strong>：繰り上がり・繰り下がり計算、文章題</li>
  <li><strong>3年生</strong>：あまりのあるわり算、□を使った計算</li>
  <li><strong>4年生</strong>：わり算の筆算、小数・分数の計算</li>
  <li><strong>5年生</strong>：通分・約分、割合の文章題</li>
  <li><strong>6年生</strong>：比例・反比例、場合の数</li>
</ul>

<h2>テスト当日の過ごし方</h2>
<ol>
  <li>いつも通りに起きて朝ごはんをしっかり食べる</li>
  <li>移動中に公式を頭の中で確認</li>
  <li>テストは問題を全部見てから時間配分を決める</li>
  <li>難しい問題は後回しにして、解けるものから解く</li>
  <li>早く終わっても必ず見直す</li>
</ol>
""",
    "faq": [
      {"q": "テスト前日に何を勉強すれば効果的ですか？", "a": "前日は新しいことはせず、「公式の確認」と「計算練習20問」だけにしましょう。それ以上は焦りを生むだけです。"},
      {"q": "テスト勉強で教科書とドリル、どちらを使えばいい？", "a": "まず教科書の例題で解き方を確認し、ドリルで量をこなすのが最も効果的です。この順番が重要です。"},
      {"q": "算数が苦手でも1週間で点数は上がりますか？", "a": "基本問題に集中すれば確実に上がります。全問正解より「基本問題を全て取る」を目標にしましょう。"},
    ],
    "cta_href": "/index.html",
    "cta_label": "今すぐドリルで実力確認",
    "related": [
      {"href": "/tesuto-100ten.html",   "emoji": "💯", "text": "算数テスト100点の取り方"},
      {"href": "/keisan-machigai.html", "emoji": "✏️", "text": "計算ミスをなくす方法"},
      {"href": "/review-method.html",   "emoji": "📝", "text": "算数の効果的な復習法"},
      {"href": "/anzan-tips.html",      "emoji": "🧮", "text": "暗算を速くする練習法"},
    ],
  },
  {
    "filename": "grade-2-tips.html",
    "title": "2年生の算数完全ガイド｜九九・筆算の攻略法",
    "description": "印刷不要・スマホで即採点。小学2年生の算数を完全攻略。九九の覚え方・筆算のコツ・時こくと時間の理解など、2年生の全単元をわかりやすく解説。",
    "h1": "2年生の算数完全ガイド｜九九・筆算の攻略法",
    "eyecatch": "小学2年生の算数最大の山場は「九九」！九九さえ克服すれば3年生以降がずっと楽になります。2年生の算数を完全攻略しましょう。",
    "body_html": """
<h2>2年生算数の全体像</h2>
<p>2年生の算数は「1年生の基礎の発展」＋「かけ算（九九）」が中心です。</p>

<h2>たし算・ひき算の筆算</h2>
<p>1年生の繰り上がり・繰り下がりを2桁・3桁に拡張します。</p>
<div class="formula-box"><p>38 + 45 = ？　一の位：8+5=13（繰り上がり1）　十の位：3+4+1=8　→ 答え：83</p></div>
<div class="tip-box"><p>💡 「右から計算」「繰り上がりは小さく書く」の2つを習慣にするだけでミスが激減します。</p></div>

<h2>九九の完全攻略ガイド</h2>
<p>2学期から始まる九九は、毎日の音読で覚えるのが一番の近道です。</p>
<h3>覚えやすい順番</h3>
<ol>
  <li>1の段・2の段・5の段（パターンが単純）</li>
  <li>3の段・4の段</li>
  <li>6の段・9の段</li>
  <li>7の段・8の段（最難関）</li>
</ol>
<h3>どうしても覚えられない組み合わせ</h3>
<ul>
  <li>7×8=56、8×7=56（「なな・や・ごじゅうろく」でリズムで覚える）</li>
  <li>6×7=42、7×6=42</li>
  <li>8×9=72、9×8=72</li>
</ul>
<div class="warn-box"><p>⚠️ 九九を覚える前に「理解しようとする」必要はありません。まず丸暗記、理解は後からついてきます。</p></div>

<h2>時こくと時間の問題</h2>
<p>「時こく（今何時？）」と「時間（何時間？）」の違いをしっかり理解することが大切です。</p>
<div class="formula-box"><p>午後2時30分 + 1時間20分 = 午後3時50分</p></div>
<div class="tip-box"><p>💡 時計の模型（アナログ時計のおもちゃ）を使って実際に針を動かしながら練習すると理解が早まります。</p></div>

<h2>長さ・水のかさの単位換算</h2>
<div class="formula-box"><p>1m=100cm　1km=1000m　1L=10dL=1000mL</p></div>
<p>単位換算は生活の中で実際に測ってみると記憶に定着しやすいです。</p>
""",
    "faq": [
      {"q": "九九は何ヶ月くらいで覚えられますか？", "a": "毎日15分練習すれば、2〜3ヶ月で全段覚えられます。2年生の2学期（9〜12月）が九九の期間なので、この期間に集中しましょう。"},
      {"q": "2年生の算数で特に気をつけることは？", "a": "九九の完全習得です。九九が不完全なまま3年生に進むと、かけ算・わり算の筆算で大きくつまずきます。"},
      {"q": "筆算を嫌がる子どもへのアドバイスは？", "a": "「なぜ筆算が必要か」を説明してあげましょう。「大きな数でも確実に計算できる魔法の方法」として紹介すると興味を持ちやすいです。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/grade-2-matome.html",   "emoji": "📚", "text": "2年生 全単元まとめ"},
      {"href": "/kuku-tips.html",        "emoji": "✖️", "text": "九九 完全攻略ガイド"},
      {"href": "/tasizan-hissan.html",   "emoji": "➕", "text": "たし算の筆算ドリル"},
      {"href": "/jikan-tokei.html",      "emoji": "⏰", "text": "時こくと時間のドリル"},
    ],
  },

  # ============================================================
  # 1年生 単元別ページ
  # ============================================================
  {
    "filename": "10made-no-kazu.html",
    "title": "10までの数 練習プリント｜数える・読む・書く（小学1年生）",
    "description": "印刷不要・スマホで即採点。小学1年生「10までの数」の練習プリント。数える・読む・書く・大小比較を無料で練習。算数の最初の一歩をスマホで学べます。",
    "h1": "10までの数 練習プリント｜数える・読む・書く",
    "eyecatch": "算数のスタートは「10までの数」から。1〜10を正確に数えて・読んで・書く力を身につけましょう。ここが全ての算数の土台になります！",
    "body_html": """
<h2>10までの数とは？</h2>
<p>小学1年生の最初に学ぶのが「1から10までの数」です。数を数える・読む・書く・比べる力が算数の土台になります。</p>
<ul>
  <li><strong>数える</strong>：りんごが「いくつあるか」を数える</li>
  <li><strong>読む</strong>：「5」を「ご」と読む</li>
  <li><strong>書く</strong>：数字の正しい書き方を覚える</li>
  <li><strong>比べる</strong>：「3と7、どちらが大きい？」</li>
</ul>

<h2>数字の読み方・書き方</h2>
<div class="formula-box"><p>1(いち)　2(に)　3(さん)　4(し)　5(ご)　6(ろく)　7(しち)　8(はち)　9(く)　10(じゅう)</p></div>
<div class="tip-box"><p>💡 数字を書くときは「書き順」も正しく覚えましょう。特に「4」「7」「9」の書き順を間違える子が多いです。</p></div>

<h2>大きい数・小さい数の比べ方</h2>
<p>数直線（0から10まで並べた線）を使うと、どちらが大きいか一目でわかります。</p>
<div class="formula-box"><p>0 ← 1 - 2 - 3 - 4 - 5 - 6 - 7 - 8 - 9 - 10 →　右にいくほど大きい</p></div>

<h2>0（ゼロ）の理解</h2>
<p>「何もない」を「0（ゼロ）」で表します。0は1より小さい数です。</p>
<div class="tip-box"><p>💡 「りんごが0個」＝「りんごが1つもない」という感覚をゲームや絵を使って教えると伝わりやすいです。</p></div>

<h2>練習のコツ</h2>
<ul>
  <li>実物（ブロック・おはじき・指）を使って数える練習をする</li>
  <li>毎日数字を書く練習（ノートに1〜10を3回ずつ）</li>
  <li>日常生活で「いくつある？」を習慣にする（階段の段数・食器の数など）</li>
</ul>
<div class="warn-box"><p>⚠️ 「なんとなく数えられる」より「正確に・素早く」数えられることが重要。急がず丁寧に練習しましょう。</p></div>
""",
    "faq": [
      {"q": "10までの数はいつ習いますか？", "a": "小学1年生の1学期（4〜5月ごろ）に最初に学びます。算数の土台となる最重要単元です。"},
      {"q": "子どもが数字を書き間違える場合は？", "a": "書き順を確認しましょう。特に「4」「7」「9」は書き順を間違えやすいです。マス目のあるノートで練習すると効果的です。"},
      {"q": "数えるのが遅い子への対処法は？", "a": "焦らず実物を使って練習しましょう。指やブロックを使いながら、ゆっくり「いち・に・さん...」と声に出す練習が効果的です。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/ikutsu-ikutsu.html",           "emoji": "🔢", "text": "いくつといくつ（数の合成・分解）"},
      {"href": "/tasizan-kuriagari-nashi.html",  "emoji": "➕", "text": "繰り上がりなしのたし算"},
      {"href": "/grade-1-matome.html",           "emoji": "📚", "text": "1年生 全単元まとめ"},
      {"href": "/youji-kazu.html",               "emoji": "🌟", "text": "未就学児向け 数の練習"},
    ],
  },
  {
    "filename": "ikutsu-ikutsu.html",
    "title": "いくつといくつ 練習プリント｜数の合成・分解（小学1年生）",
    "description": "印刷不要・スマホで即採点。小学1年生「いくつといくつ」の練習プリント。10の合成・分解をスマホで無料練習。繰り上がりたし算の土台をしっかり固めます。",
    "h1": "いくつといくつ 練習プリント｜数の合成・分解",
    "eyecatch": "「いくつといくつ」は繰り上がりたし算の土台！5は「1と4」「2と3」に分けられる感覚を身につけると、後の計算がグンと楽になります。",
    "body_html": """
<h2>「いくつといくつ」とは？</h2>
<p>ある数が「いくつといくつ」に分けられるか（分解）、または「いくつとどれだけ合わせる」と指定の数になるか（合成）を学ぶ単元です。</p>
<div class="formula-box"><p>5 = 1+4 = 2+3 = 3+2 = 4+1 = 5+0</p></div>
<p>この感覚が身につくと、繰り上がりたし算（8+6など）を「10のかたまり」で考えられるようになります。</p>

<h2>数ごとの合成・分解一覧</h2>
<h3>10の合成（最重要！）</h3>
<div class="formula-box"><p>1+9　2+8　3+7　4+6　5+5　6+4　7+3　8+2　9+1</p></div>
<div class="tip-box"><p>💡 「10の合成」は繰り上がりたし算で毎回使います。指を使わずに即答できるまで練習しましょう。</p></div>

<h3>5の合成</h3>
<div class="formula-box"><p>1+4　2+3　3+2　4+1　0+5　5+0</p></div>

<h3>7・8・9の合成</h3>
<ul>
  <li>7 = 1+6 = 2+5 = 3+4 = 4+3 = 5+2 = 6+1</li>
  <li>8 = 1+7 = 2+6 = 3+5 = 4+4 = 5+3 = 6+2 = 7+1</li>
  <li>9 = 1+8 = 2+7 = 3+6 = 4+5 = 5+4 = 6+3 = 7+2 = 8+1</li>
</ul>

<h2>練習方法</h2>
<h3>おはじきを使う</h3>
<p>5個のおはじきを左右に分けて、「1と4」「2と3」を視覚で確認します。手を使った練習は記憶に残りやすいです。</p>

<h3>カードを使う</h3>
<p>「□ + □ = 10」の□を埋めるカードゲームをするのが効果的です。楽しく覚えられます。</p>

<h3>声に出して練習</h3>
<div class="formula-box"><p>「10は 1と9！」「10は 2と8！」...と声に出して暗唱する</p></div>
<div class="warn-box"><p>⚠️ 10の合成・分解が瞬時に出てこない状態で繰り上がりたし算に進むと混乱します。確実に覚えてから次へ進みましょう。</p></div>

<h2>繰り上がりたし算との関係</h2>
<p>「8+6」を計算するとき、「8にいくつ足せば10になる？→2」「6から2を取ると？→4」「10+4=14」という考え方をします。これが「いくつといくつ」の力です。</p>
""",
    "faq": [
      {"q": "いくつといくつはいつ習いますか？", "a": "小学1年生の1学期後半（5〜6月ごろ）に学びます。繰り上がりたし算の前の重要なステップです。"},
      {"q": "なかなか覚えられない場合はどうすれば？", "a": "おはじきや指など「実物」を使って視覚・触覚で体感させましょう。特に「10の合成」はゲーム感覚で繰り返し練習することが効果的です。"},
      {"q": "いくつといくつが理解できれば繰り上がりたし算は楽になりますか？", "a": "大きく楽になります。「10の合成」が瞬時に出てくれば、繰り上がりたし算は「10のかたまりを作るゲーム」として自然に理解できます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/10made-no-kazu.html",          "emoji": "🔟", "text": "10までの数の練習"},
      {"href": "/tasizan-kuriagari-nashi.html",  "emoji": "➕", "text": "繰り上がりなしのたし算"},
      {"href": "/tasizan-kuriagari-ari.html",    "emoji": "➕", "text": "繰り上がりありのたし算"},
      {"href": "/grade-1-matome.html",           "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },
  {
    "filename": "100made-no-kazu.html",
    "title": "100までの数 練習プリント｜1年生3学期の数の学習",
    "description": "印刷不要・スマホで即採点。小学1年生「100までの数」の練習プリント。十の位・一の位の概念、数の大小・順序をスマホで無料練習。2年生の筆算の土台に。",
    "h1": "100までの数 練習プリント｜1年生3学期の数の学習",
    "eyecatch": "1年生3学期のクライマックス「100までの数」。十の位・一の位の概念を理解すると、2年生の筆算がスムーズに始まられます！",
    "body_html": """
<h2>100までの数とは？</h2>
<p>1年生の3学期に学ぶ「100までの数」では、2桁の数を読み書きし、数の大小・順序を理解します。</p>
<ul>
  <li><strong>十の位・一の位</strong>：「35」は「十の位が3、一の位が5」</li>
  <li><strong>数の読み書き</strong>：「47」を「よんじゅうなな」と読む</li>
  <li><strong>大小比較</strong>：「68と86、どちらが大きい？」</li>
  <li><strong>数の順序</strong>：「45の次の数は？」「99の次は？」</li>
</ul>

<h2>十の位と一の位の考え方</h2>
<div class="formula-box"><p>73 = 十の位(7) × 10 + 一の位(3) × 1 = 70 + 3</p></div>
<div class="tip-box"><p>💡 「10のかたまり」がいくつあるかで十の位を考えます。ブロックを10個ずつ束ねて視覚化すると理解が早まります。</p></div>

<h2>数の大小の比べ方</h2>
<p>2桁の数を比べるときは「十の位から見る」のが基本です。</p>
<ul>
  <li>まず十の位を比べる → 大きい方が大きい数</li>
  <li>十の位が同じなら一の位を比べる</li>
</ul>
<div class="formula-box"><p>58 と 63 → 十の位: 5 < 6 → 58 < 63</p></div>

<h2>100までの数の数え方のコツ</h2>
<ul>
  <li>10ずつ数える（10・20・30...）を先に覚える</li>
  <li>数直線を使って視覚的に確認する</li>
  <li>「29の次は？」「30」をすぐに言えるよう練習</li>
</ul>
<div class="warn-box"><p>⚠️ 「49→50」「59→60」などの十の位が繰り上がる場面で混乱しやすいです。特に練習しましょう。</p></div>

<h2>2年生の計算への準備</h2>
<p>「100までの数」の理解が完成すると、2年生の2桁・3桁の筆算がスムーズに始められます。十の位・一の位の概念が筆算の土台です。</p>
""",
    "faq": [
      {"q": "100までの数はいつ習いますか？", "a": "小学1年生の3学期（1〜2月ごろ）に学びます。1年生の算数の総仕上げとなる単元です。"},
      {"q": "十の位・一の位の概念を簡単に教える方法は？", "a": "ブロックやおはじきを「10個ずつ束ねる」作業をさせると視覚的に理解しやすいです。「何束と何個」で数を表現させましょう。"},
      {"q": "100までの数が理解できると2年生で役に立ちますか？", "a": "非常に役立ちます。2年生の2桁・3桁の筆算は「十の位・一の位」の概念が完全に理解できていることが前提です。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/10made-no-kazu.html",          "emoji": "🔟", "text": "10までの数の練習"},
      {"href": "/ikutsu-ikutsu.html",           "emoji": "🔢", "text": "いくつといくつ（数の合成）"},
      {"href": "/tasizan-kuriagari-ari.html",    "emoji": "➕", "text": "繰り上がりありのたし算"},
      {"href": "/grade-1-matome.html",           "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },
  {
    "filename": "3tsu-no-kazu.html",
    "title": "3つの数のたし算・ひき算 練習プリント｜小学1年生",
    "description": "印刷不要・スマホで即採点。小学1年生「3つの数のたし算・ひき算」の練習プリント。2+3+4や10-3-2などの計算を左から順に解く練習を無料でできます。",
    "h1": "3つの数のたし算・ひき算 練習プリント",
    "eyecatch": "「2+3+4=?」「10-3-2=?」のように数が3つ出てくる計算。左から順番に計算するルールを身につけましょう！",
    "body_html": """
<h2>3つの数の計算とは？</h2>
<p>1年生の3学期に学ぶ「3つの数の計算」は、たし算やひき算が3つの数をまたぐ計算です。</p>
<div class="formula-box"><p>2 + 3 + 4 = ？　　10 − 3 − 2 = ？　　8 − 5 + 4 = ？</p></div>

<h2>基本ルール：左から順番に計算する</h2>
<p>3つの数の計算は、<strong>左から順番に2つずつ計算</strong>します。</p>
<div class="formula-box"><p>2 + 3 + 4　→　(2+3) + 4　→　5 + 4　→　9</p></div>
<div class="tip-box"><p>💡 「左から順番に！」を声に出して確認しながら解く習慣をつけましょう。答えを一度に出そうとするとミスが増えます。</p></div>

<h2>たし算が3つの場合</h2>
<div class="formula-box"><p>3 + 4 + 2 = ?　→　3+4=7　→　7+2=9</p></div>

<h2>ひき算が混ざる場合</h2>
<div class="formula-box"><p>9 − 4 − 2 = ?　→　9-4=5　→　5-2=3</p></div>

<h2>たし算とひき算が混ざる場合</h2>
<div class="formula-box"><p>5 + 3 − 4 = ?　→　5+3=8　→　8-4=4</p></div>
<div class="warn-box"><p>⚠️ たし算とひき算が混ざっても、計算の順番は変わりません。必ず左から順番に計算しましょう。</p></div>

<h2>よくある間違いパターン</h2>
<ul>
  <li>✗ 右から計算してしまう（例：2+3+4 を 3+4=7→2+7=9 ※結果は同じだが…）</li>
  <li>✗ たし算を先に計算してしまう（例：5+3-4 で 3-4を先にしようとする）</li>
  <li>✗ 途中の答えを忘れて最初から計算し直す</li>
</ul>
<div class="tip-box"><p>💡 途中の答えを小さくメモする習慣をつけましょう。「5+3=8（←書く）→8-4=4」と段階的に。</p></div>
""",
    "faq": [
      {"q": "3つの数の計算はいつ習いますか？", "a": "小学1年生の3学期（1〜2月ごろ）に学びます。2つの数の計算が完全に定着した後に取り組む発展内容です。"},
      {"q": "3つの数の計算で一番多いミスは？", "a": "途中の答えを忘れてしまうことです。計算の途中でも必ずメモする習慣をつけましょう。"},
      {"q": "たし算とひき算が混ざった場合でも左から計算しますか？", "a": "はい、左から順番に計算します。かけ算・わり算が混ざる場合（高学年）は順番が変わりますが、1年生の範囲はすべて左から計算します。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/tasizan-kuriagari-nashi.html", "emoji": "➕", "text": "繰り上がりなしのたし算"},
      {"href": "/tasizan-kuriagari-ari.html",   "emoji": "➕", "text": "繰り上がりありのたし算"},
      {"href": "/hikizan-kurisagari-ari.html",  "emoji": "➖", "text": "繰り下がりありのひき算"},
      {"href": "/grade-1-matome.html",          "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  # ============================================================
  # 2年生 単元別ページ
  # ============================================================
  {
    "filename": "mizu-no-kasa.html",
    "title": "水のかさ 練習プリント｜dL・L・mL の単位換算（小学2年生）",
    "description": "印刷不要・スマホで即採点。小学2年生「水のかさ」の練習プリント。dL・L・mLの単位と換算をスマホで無料練習。かさの比較・足し引き計算まで対応。",
    "h1": "水のかさ 練習プリント｜dL・L・mL の単位換算",
    "eyecatch": "「1Lって何dL？」「500mLはLに直すと？」水のかさの単位換算は日常生活でも使う重要スキル。確実にマスターしましょう！",
    "body_html": """
<h2>水のかさの単位</h2>
<p>小学2年生では、水や液体の量を表す3つの単位を学びます。</p>
<div class="formula-box"><p>1L（リットル）= 10dL（デシリットル）= 1000mL（ミリリットル）</p></div>
<div class="tip-box"><p>💡 身近なもので確認しよう：牛乳パック1本＝1L、缶ジュース1本≒350mL、計量カップ1杯≒200mL</p></div>

<h2>単位換算の練習</h2>
<h3>L → dL に直す（×10）</h3>
<div class="formula-box"><p>3L = 30dL　　5L = 50dL　　2L5dL = 25dL</p></div>
<h3>dL → L に直す（÷10）</h3>
<div class="formula-box"><p>40dL = 4L　　25dL = 2L5dL</p></div>
<h3>L → mL に直す（×1000）</h3>
<div class="formula-box"><p>2L = 2000mL　　0.5L = 500mL</p></div>

<h2>かさの足し算・引き算</h2>
<p>同じ単位に揃えてから計算します。</p>
<div class="formula-box"><p>3L2dL + 1L5dL = 4L7dL</p></div>
<div class="warn-box"><p>⚠️ dLが10以上になったらLに繰り上げます。3L8dL + 1L4dL = 4L12dL → 5L2dL</p></div>

<h2>大小比較</h2>
<ul>
  <li>単位が違う場合は同じ単位に揃えてから比べる</li>
  <li>例：3L と 25dL → 30dL と 25dL → 3L の方が大きい</li>
</ul>
""",
    "faq": [
      {"q": "dL（デシリットル）はいつ習いますか？", "a": "小学2年生で習います。日本独自の単位で、海外ではあまり使われません。"},
      {"q": "水のかさの単位換算を覚えるコツは？", "a": "実際に計量カップや牛乳パックを使って体感するのが一番です。「牛乳パック1本＝1L」など身近な量と結びつけましょう。"},
      {"q": "mLはいつ習いますか？", "a": "2年生で習いますが、日常生活（ジュースの缶など）でよく見かけます。1L=1000mLの関係を生活の中で確認しましょう。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/tani-nagasa.html",   "emoji": "📏", "text": "長さの単位（mm・cm・m）"},
      {"href": "/tani-omosa.html",    "emoji": "⚖️", "text": "重さの単位（g・kg）"},
      {"href": "/jikan-tani.html",    "emoji": "⏱️", "text": "時間の単位換算"},
      {"href": "/grade-2-matome.html","emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },
  {
    "filename": "1000made-no-kazu.html",
    "title": "1000までの数 練習プリント｜百の位・十の位・一の位（小学2年生）",
    "description": "印刷不要・スマホで即採点。小学2年生「1000までの数」の練習プリント。百の位・十の位・一の位の概念と3桁の数の読み書き・大小比較を無料で練習。",
    "h1": "1000までの数 練習プリント｜百の位・十の位・一の位",
    "eyecatch": "2年生後半に学ぶ「1000までの数」。百の位が加わり3桁の数を扱います。ここをしっかり理解すると3年生の大きな数・筆算がスムーズに！",
    "body_html": """
<h2>1000までの数とは</h2>
<p>1年生で学んだ「100までの数」を拡張し、3桁の数（100〜999）と1000を学びます。</p>
<div class="formula-box"><p>百の位 | 十の位 | 一の位　例：356 = 300 + 50 + 6</p></div>

<h2>数の読み書き</h2>
<ul>
  <li>356 → 「さんびゃくごじゅうろく」</li>
  <li>708 → 「ななひゃくはち」（十の位が0のとき）</li>
  <li>1000 → 「せん」</li>
</ul>
<div class="tip-box"><p>💡 十の位が0のとき「ゼロ」は読みません。708は「ななひゃくはち」（「ゼロはち」ではない）</p></div>

<h2>位ごとの分解</h2>
<div class="formula-box"><p>537 = 500 + 30 + 7 = 百が5・十が3・一が7</p></div>

<h2>大小比較</h2>
<ul>
  <li>まず百の位を比べる → 大きければその数が大きい</li>
  <li>百の位が同じなら十の位、さらに同じなら一の位を比べる</li>
</ul>
<div class="formula-box"><p>472 と 489 → 百の位: 4=4 → 十の位: 7 < 8 → 472 < 489</p></div>

<h2>100ずつ・10ずつ数える練習</h2>
<ul>
  <li>100・200・300・400・500・600・700・800・900・1000</li>
  <li>399の次は？ → 400（百の位が繰り上がる）</li>
  <li>999の次は？ → 1000</li>
</ul>
<div class="warn-box"><p>⚠️ 「99→100」「199→200」のように桁が増える場面でつまずきやすいです。特に練習しましょう。</p></div>
""",
    "faq": [
      {"q": "1000までの数はいつ習いますか？", "a": "小学2年生の後半（11〜12月ごろ）に習います。1年生の100までの数の延長です。"},
      {"q": "百の位の概念をわかりやすく教えるには？", "a": "ブロックを「10個ずつの束」と「10束をまとめた大きな束」で視覚化すると理解しやすいです。"},
      {"q": "708のように十の位が0の数の読み方は？", "a": "「ななひゃくはち」と読みます。0は読みません。書くときは必ず0を書く点に注意しましょう。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/100made-no-kazu.html", "emoji": "💯", "text": "100までの数（1年生）"},
      {"href": "/tasizan-hissan.html",  "emoji": "➕", "text": "たし算の筆算ドリル"},
      {"href": "/hikizan-hissan.html",  "emoji": "➖", "text": "ひき算の筆算ドリル"},
      {"href": "/grade-2-matome.html",  "emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },
  {
    "filename": "sankakkei-shikaku.html",
    "title": "三角形・四角形 練習プリント｜正方形・長方形・直角三角形（小学2年生）",
    "description": "印刷不要・スマホで即採点。小学2年生「三角形と四角形」の練習プリント。正方形・長方形・直角三角形の特徴と見分け方を無料で学べます。",
    "h1": "三角形・四角形 練習プリント｜正方形・長方形・直角三角形",
    "eyecatch": "辺・頂点・直角の概念を正しく理解することが、4年生以降の図形学習の土台になります。2年生の図形をしっかりマスターしましょう！",
    "body_html": """
<h2>2年生で学ぶ図形の種類</h2>
<ul>
  <li><strong>正方形</strong>：4つの辺が全て同じ長さ、4つの角が全て直角</li>
  <li><strong>長方形</strong>：向かい合う辺が同じ長さ、4つの角が全て直角</li>
  <li><strong>直角三角形</strong>：1つの角が直角（90°）の三角形</li>
  <li><strong>三角形</strong>：3つの辺と3つの頂点を持つ図形</li>
  <li><strong>四角形</strong>：4つの辺と4つの頂点を持つ図形</li>
</ul>

<h2>辺・頂点・直角とは？</h2>
<div class="formula-box"><p>辺 = 図形の線のこと　頂点 = 辺と辺が交わる点　直角 = 90°の角</p></div>
<div class="tip-box"><p>💡 直角は「四角いもの（教科書の角・ノートの角）と同じ角度」と覚えると分かりやすいです。</p></div>

<h2>正方形と長方形の違い</h2>
<ul>
  <li>正方形：全ての辺の長さが等しい（特別な長方形）</li>
  <li>長方形：向かい合う辺の長さが等しい（直角がある）</li>
</ul>
<div class="warn-box"><p>⚠️ 「正方形は長方形の一種」ですが、2年生では別の図形として学びます。混同しないように注意。</p></div>

<h2>図形の数え方・見つけ方</h2>
<p>複合図形から三角形・四角形を見つける問題が出ます。</p>
<ul>
  <li>辺の数で判断：3本→三角形、4本→四角形</li>
  <li>直角かどうかを確認する（三角定規や紙の角を使う）</li>
</ul>
""",
    "faq": [
      {"q": "直角三角形と普通の三角形の違いは？", "a": "直角三角形は3つの角のうち1つが必ず直角（90°）です。普通の三角形は直角がありません。"},
      {"q": "正方形は長方形に含まれますか？", "a": "数学的には正方形は長方形の特別な場合です。しかし2年生では別の図形として学びますので、試験では区別して答えましょう。"},
      {"q": "子どもに図形を教えるコツは？", "a": "実際の四角いもの（本・箱）や三角形のもの（おにぎり・サンドイッチ）を使って形を実感させることが効果的です。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/katachi-youji.html",   "emoji": "🔷", "text": "図形の基礎（未就学児向け）"},
      {"href": "/kakudo-guide.html",    "emoji": "📐", "text": "角度の学習（4年生）"},
      {"href": "/menseki-seihokei.html","emoji": "📐", "text": "面積（長方形・正方形）"},
      {"href": "/grade-2-matome.html",  "emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },

  # ============================================================
  # 3年生 単元別ページ
  # ============================================================
  {
    "filename": "syousuu-kiso.html",
    "title": "小数の基礎 練習プリント｜0.1の概念・大小比較（小学3年生）",
    "description": "印刷不要・スマホで即採点。小学3年生「小数の基礎」の練習プリント。0.1の意味・小数の読み書き・大小比較を無料で練習。4年生の小数計算の土台に。",
    "h1": "小数の基礎 練習プリント｜0.1の概念・大小比較",
    "eyecatch": "3年生で初めて出会う「小数」。0.1という概念を正しく理解することが、4年生以降の小数計算すべての土台になります！",
    "body_html": """
<h2>小数とは？</h2>
<p>1より小さい数を表すために使う数が「小数」です。小数点（.）で整数部分と小数部分を区切ります。</p>
<div class="formula-box"><p>1を10等分した1つ分 = 0.1（ゼロてんいち）</p></div>
<div class="tip-box"><p>💡 1Lのジュースを10等分すると1dL。1dL = 0.1L という感覚で理解しましょう。</p></div>

<h2>小数の読み書き</h2>
<ul>
  <li>0.3 → 「ゼロてんさん」</li>
  <li>1.7 → 「いってんなな」</li>
  <li>2.0 → 「に」（2と同じ）</li>
</ul>

<h2>小数の仕組み</h2>
<div class="formula-box"><p>1.4 = 1 + 0.4 = 1 + 0.1が4個分</p></div>
<p>小数点の左が整数部分、右が小数部分（小数第一位）です。</p>

<h2>大小比較</h2>
<p>整数部分→小数部分の順で比べます。</p>
<div class="formula-box"><p>1.3 と 1.7 → 整数部分: 1=1 → 小数部分: 3 < 7 → 1.3 < 1.7</p></div>
<div class="warn-box"><p>⚠️ 0.9 と 1.0 では 1.0 が大きい。整数部分を先に比べることを忘れずに。</p></div>

<h2>数直線で確認</h2>
<p>0〜2の数直線に0.1刻みで点を打つ練習が効果的です。どこにどの小数があるかを視覚で確認しましょう。</p>
""",
    "faq": [
      {"q": "小数は何年生で習いますか？", "a": "小学3年生で小数の基礎（一位小数）を学びます。4年生で小数の計算、5年生でさらに発展した内容を学びます。"},
      {"q": "小数の概念を子どもにわかりやすく教えるには？", "a": "1Lのジュースを10等分して「1つ分が0.1L」と実感させる方法が効果的です。定規のmmとcmの関係も使えます。"},
      {"q": "0.9より大きくて1.0より小さい数はありますか？", "a": "3年生の範囲（一位小数）では0.9の次は1.0です。0.95など二位小数は4〜5年生で学びます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/syousuu-tasizan.html", "emoji": "🔢", "text": "小数のたし算・ひき算"},
      {"href": "/syousuu-kakizan.html", "emoji": "🔢", "text": "小数のかけ算"},
      {"href": "/bunsuu-kiso.html",     "emoji": "½",  "text": "分数の基礎（3年生）"},
      {"href": "/grade-3-matome.html",  "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },
  {
    "filename": "bunsuu-kiso.html",
    "title": "分数の基礎 練習プリント｜等分・分子・分母の意味（小学3年生）",
    "description": "印刷不要・スマホで即採点。小学3年生「分数の基礎」の練習プリント。等分・分子・分母の意味・分数の大小比較を無料で練習。4年生の分数計算の土台に。",
    "h1": "分数の基礎 練習プリント｜等分・分子・分母の意味",
    "eyecatch": "「ピザを4等分した3切れ分＝4分の3（3/4）」分数は「等分した何個分か」という考え方がすべての土台！まずここをしっかり理解しましょう。",
    "body_html": """
<h2>分数とは？</h2>
<p>1つのものをいくつかに等分したとき、その何個分かを表す数が分数です。</p>
<div class="formula-box"><p>3/4（4分の3）= 4等分した3つ分　← 分子: 3　分母: 4</p></div>
<div class="tip-box"><p>💡 「分母」は分け方（何等分するか）、「分子」は数え方（何個分か）と覚えましょう。</p></div>

<h2>分母・分子の意味</h2>
<ul>
  <li><strong>分母</strong>（下の数）：何等分するかを示す</li>
  <li><strong>分子</strong>（上の数）：何個分かを示す</li>
</ul>
<div class="formula-box"><p>□/△ = △等分した□個分</p></div>

<h2>分数の種類（3年生の範囲）</h2>
<ul>
  <li><strong>単位分数</strong>：分子が1の分数（1/2・1/3・1/4）</li>
  <li><strong>真分数</strong>：分子が分母より小さい分数（3/4・2/5）</li>
  <li><strong>分数の読み方</strong>：3/4 →「4分の3」（分母を先に読む）</li>
</ul>

<h2>同じ分母の大小比較</h2>
<p>分母が同じなら、分子が大きいほど大きい分数です。</p>
<div class="formula-box"><p>3/5 と 4/5 → 分子を比べる: 3 < 4 → 3/5 < 4/5</p></div>

<h2>分数と整数の関係</h2>
<div class="formula-box"><p>4/4 = 1　　8/4 = 2　　分母と分子が同じ = 1</p></div>
<div class="warn-box"><p>⚠️ 「3/4より大きい分数」を聞かれたら分子を増やすか分母を減らします。分母の概念がまだあいまいな場合は具体物で確認しましょう。</p></div>
""",
    "faq": [
      {"q": "分数はいつから習いますか？", "a": "小学3年生で分数の基礎（意味・読み方・大小比較）を学びます。4年生で仮分数・帯分数、5年生で通分・約分と発展します。"},
      {"q": "分母と分子の読み方を覚えるコツは？", "a": "「分母は母だから下（土台）にある」と覚えましょう。母親が土台・基盤というイメージです。"},
      {"q": "3年生の分数で計算問題はありますか？", "a": "3年生では同じ分母のたし算・ひき算の基礎を学びます。通分が必要な計算（分母が違う計算）は5年生です。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-doubunmo.html", "emoji": "½", "text": "分数のたし算・ひき算（同分母）"},
      {"href": "/bunsuu-ibunmo.html",   "emoji": "½", "text": "分数のたし算・ひき算（異分母）"},
      {"href": "/syousuu-kiso.html",    "emoji": "🔢", "text": "小数の基礎（3年生）"},
      {"href": "/grade-3-matome.html",  "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  # ============================================================
  # 4年生 単元別ページ
  # ============================================================
  {
    "filename": "ookina-kazu.html",
    "title": "大きな数 練習プリント｜億・兆の単位（小学4年生）",
    "description": "印刷不要・スマホで即採点。小学4年生「大きな数（億・兆）」の練習プリント。億・兆の位・読み書き・大小比較を無料で練習できます。",
    "h1": "大きな数 練習プリント｜億・兆の単位",
    "eyecatch": "1億・1兆という巨大な数。桁が増えると難しく感じますが、「4桁ずつ区切る」ルールを覚えれば簡単！数字が読めるようになるともっと算数が楽しくなります。",
    "body_html": """
<h2>大きな数の単位</h2>
<div class="formula-box"><p>一・十・百・千 / 一万・十万・百万・千万 / 一億・十億・百億・千億 / 一兆</p></div>
<div class="tip-box"><p>💡 4桁ずつ区切って読む！「一・十・百・千」のパターンが繰り返されます。</p></div>

<h2>数の読み方</h2>
<p>大きな数は4桁ずつ「，」で区切って読みます。</p>
<ul>
  <li>12,345,678 → 「1234万5678」→「千二百三十四万五千六百七十八」</li>
  <li>3,500,000,000 → 「35億」→「三十五億」</li>
</ul>
<div class="formula-box"><p>1億 = 10,000万 = 100,000,000（1の後ろに0が8個）</p></div>
<div class="formula-box"><p>1兆 = 10,000億 = 1,000,000,000,000（1の後ろに0が12個）</p></div>

<h2>大小比較</h2>
<p>桁数が多い方が大きな数。桁数が同じなら左（高い位）から順に比べます。</p>
<div class="formula-box"><p>3億7000万 と 4億2000万 → 億の位: 3 < 4 → 3億7000万 < 4億2000万</p></div>

<h2>日常生活での大きな数</h2>
<ul>
  <li>日本の人口：約1億2500万人</li>
  <li>国家予算：約100兆円</li>
  <li>地球の円周：約4万km</li>
</ul>
<div class="warn-box"><p>⚠️ 0が多い数の読み間違いに注意。1000万と1億は10倍違います。桁を数える習慣をつけましょう。</p></div>
""",
    "faq": [
      {"q": "億・兆はいつ習いますか？", "a": "小学4年生で習います。1億・1兆という単位とその読み書きを学びます。"},
      {"q": "大きな数をすらすら読めるようになるコツは？", "a": "「4桁ずつ区切る」習慣をつけることです。数字を書くときは必ずカンマ（，）を3桁ごとに入れて視覚的に確認しましょう。"},
      {"q": "1億と10000万は同じですか？", "a": "同じです。10000万=1億です。「万」が10000個集まると「億」になります。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/large-numbers.html",      "emoji": "🔢", "text": "大きな数の学習ガイド"},
      {"href": "/gaisuu-guide.html",       "emoji": "🔢", "text": "概数・四捨五入"},
      {"href": "/warizan-hissan-2keta.html","emoji": "➗", "text": "わり算の筆算（2桁）"},
      {"href": "/grade-4-matome.html",     "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },
  {
    "filename": "suichoku-heiko.html",
    "title": "垂直と平行 練習プリント｜直線の位置関係（小学4年生）",
    "description": "印刷不要・スマホで即採点。小学4年生「垂直と平行」の練習プリント。垂直・平行の意味と見分け方、作図の基礎を無料で練習できます。",
    "h1": "垂直と平行 練習プリント｜直線の位置関係",
    "eyecatch": "「垂直」「平行」は4年生図形学習の基礎。この概念をしっかり理解すれば、台形・平行四辺形・対角線など高学年の図形が楽になります！",
    "body_html": """
<h2>垂直とは？</h2>
<p>2本の直線が90°（直角）で交わるとき、「垂直に交わる」といいます。</p>
<div class="formula-box"><p>直線ℓ ⊥ 直線m = 直線ℓと直線mは垂直</p></div>
<div class="tip-box"><p>💡 ノートの縦線と横線は垂直。十字路の道路も垂直に交わっています。身近な垂直を探してみましょう。</p></div>

<h2>平行とは？</h2>
<p>2本の直線がどこまで延ばしても交わらないとき、「平行である」といいます。</p>
<div class="formula-box"><p>直線ℓ ∥ 直線m = 直線ℓと直線mは平行</p></div>
<div class="tip-box"><p>💡 線路のレール・ノートの罫線が平行の例。平行な2直線の間の距離はどこでも等しくなります。</p></div>

<h2>垂直と平行の見分け方</h2>
<ul>
  <li><strong>垂直の確認</strong>：三角定規の直角部分を当てて90°か確認</li>
  <li><strong>平行の確認</strong>：1本の直線に対して垂直な直線を2本引き、その2本が重なるか確認</li>
</ul>
<div class="warn-box"><p>⚠️ 「交わっていない=平行」は誤り。交わっていなくても延長線上で交わる場合は平行ではありません。</p></div>

<h2>図形との関係</h2>
<ul>
  <li>正方形・長方形：向かい合う辺が平行、隣り合う辺が垂直</li>
  <li>平行四辺形：向かい合う辺が平行（垂直ではない）</li>
  <li>台形：少なくとも1組の辺が平行</li>
</ul>
""",
    "faq": [
      {"q": "垂直と平行はいつ習いますか？", "a": "小学4年生で習います。図形学習の基礎となる重要な概念です。"},
      {"q": "垂直と直角の違いは？", "a": "直角は「90°の角」のこと。垂直は「2本の直線が直角で交わる関係」のことです。"},
      {"q": "作図（垂直・平行を書く）の方法は？", "a": "三角定規2枚を使います。垂直は1枚の直角を利用、平行は2枚をスライドさせて引きます。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/kakudo-guide.html",       "emoji": "📐", "text": "角度の学習"},
      {"href": "/menseki-seihokei.html",   "emoji": "📐", "text": "面積（長方形・正方形）"},
      {"href": "/taishou-figure.html",     "emoji": "🔷", "text": "対称な図形"},
      {"href": "/grade-4-matome.html",     "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  # ============================================================
  # 5年生 単元別ページ
  # ============================================================
  {
    "filename": "heikin-guide.html",
    "title": "平均の求め方 練習プリント｜合計÷個数（小学5年生）",
    "description": "印刷不要・スマホで即採点。小学5年生「平均」の練習プリント。平均の意味・求め方・仮の平均を使った計算を無料で練習。データ活用の基礎を学べます。",
    "h1": "平均の求め方 練習プリント｜合計÷個数",
    "eyecatch": "「平均」はテストの点数・気温・身長など日常生活でよく使う概念。「合計÷個数」のシンプルな式で求められます！",
    "body_html": """
<h2>平均とは？</h2>
<p>いくつかのデータを「均等にならした値」が平均です。データの全体的な傾向を1つの数で表せます。</p>
<div class="formula-box"><p>平均 = 合計 ÷ 個数</p></div>

<h2>平均の求め方</h2>
<p>例：5回のテストの点数が 80, 70, 90, 65, 85 のとき</p>
<div class="formula-box"><p>合計: 80+70+90+65+85 = 390　　平均: 390 ÷ 5 = 78点</p></div>
<div class="tip-box"><p>💡 「平均」は実際には存在しない値でもOK。78.5点のような小数になることもあります。</p></div>

<h2>合計を平均から求める</h2>
<p>逆算で合計を求めることもできます。</p>
<div class="formula-box"><p>合計 = 平均 × 個数　　例: 平均75点 × 4回 = 合計300点</p></div>

<h2>0を含むデータの平均</h2>
<p>データに0が含まれる場合も個数に入れます。</p>
<div class="formula-box"><p>4, 0, 6, 2 の平均 → (4+0+6+2) ÷ 4 = 12 ÷ 4 = 3　（÷3ではない！）</p></div>
<div class="warn-box"><p>⚠️ 0のデータを「ないもの」として除外するミスが多いです。0も個数に数えましょう。</p></div>

<h2>文章題での平均</h2>
<ul>
  <li>「5日間で平均○個、合計は？」→ 平均×日数</li>
  <li>「4人の平均が○点、1人加わると平均が○点、5人目は？」→ 5人の合計 - 4人の合計</li>
</ul>
""",
    "faq": [
      {"q": "平均はいつ習いますか？", "a": "小学5年生で習います。データの活用・統計の基礎として中学数学にも発展します。"},
      {"q": "平均の計算で小数の答えが出るのはなぜですか？", "a": "均等に割り切れない場合は小数になります。「5人で分ける」ときに人数で割り切れないのと同じです。"},
      {"q": "「0のデータ」はなぜ個数に含めますか？", "a": "0も立派なデータです。「ゼロ回しかできなかった」という情報も平均に影響します。含めないと実態と異なる平均になってしまいます。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/percentage-guide.html", "emoji": "📊", "text": "割合・百分率"},
      {"href": "/graph-circle.html",     "emoji": "🥧", "text": "円グラフ"},
      {"href": "/graph-boubou.html",     "emoji": "📊", "text": "棒グラフ"},
      {"href": "/grade-5-matome.html",   "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },
  {
    "filename": "goudo-figure.html",
    "title": "図形の合同 練習プリント｜合同な図形の条件（小学5年生）",
    "description": "印刷不要・スマホで即採点。小学5年生「図形の合同」の練習プリント。合同の意味・対応する辺と角・合同な図形の描き方を無料で練習できます。",
    "h1": "図形の合同 練習プリント｜合同な図形の条件",
    "eyecatch": "「合同」とは形も大きさも同じ図形のこと。重ねるとぴったり重なる関係です。対応する辺・角の関係を正しく理解しましょう！",
    "body_html": """
<h2>合同とは？</h2>
<p>2つの図形を重ねたときにぴったり重なる関係を「合同」といいます。</p>
<div class="formula-box"><p>合同な図形 → 形も大きさも同じ（向きや裏返しはOK）</p></div>
<div class="tip-box"><p>💡 「向きが違う」「裏返し」でも合同です。切り取って重ねたときに一致すれば合同。</p></div>

<h2>合同な図形の性質</h2>
<ul>
  <li><strong>対応する辺</strong>：重なり合う辺の長さは等しい</li>
  <li><strong>対応する角</strong>：重なり合う角の大きさは等しい</li>
</ul>
<div class="formula-box"><p>△ABC ≡ △DEF → AB=DE, BC=EF, CA=FD, ∠A=∠D, ∠B=∠E, ∠C=∠F</p></div>

<h2>三角形の合同条件（参考）</h2>
<ul>
  <li>3辺の長さが全て等しい</li>
  <li>2辺の長さとその間の角が等しい</li>
  <li>1辺の長さとその両端の角が等しい</li>
</ul>
<div class="warn-box"><p>⚠️ 5年生では「合同の意味と対応する辺・角」が中心。合同条件（証明）は中学数学の範囲です。</p></div>

<h2>合同な図形の作図</h2>
<p>コンパスと定規を使って合同な三角形を作図する問題が出ます。</p>
<ul>
  <li>辺の長さをコンパスでうつし取る</li>
  <li>角をコンパスと定規で写す</li>
</ul>
""",
    "faq": [
      {"q": "合同と相似の違いは？", "a": "合同は「形も大きさも同じ」、相似は「形は同じだが大きさが違う（拡大・縮小の関係）」です。相似は6年生で学びます。"},
      {"q": "裏返しにした図形も合同ですか？", "a": "合同です。合同は「重なればOK」なので、裏返しにして重なれば合同と認められます。"},
      {"q": "対応する頂点・辺・角の見つけ方は？", "a": "実際に図形を切り取って重ねてみるのが一番確実です。どの頂点がどの頂点と重なるかを確認しましょう。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/taishou-figure.html",  "emoji": "🔷", "text": "対称な図形"},
      {"href": "/kakudo-guide.html",    "emoji": "📐", "text": "角度の学習"},
      {"href": "/menseki-sankakkei.html","emoji": "📐", "text": "三角形の面積"},
      {"href": "/grade-5-matome.html",  "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  # ============================================================
  # 6年生 単元別ページ
  # ============================================================
  {
    "filename": "hirei-hanpirei.html",
    "title": "比例・反比例 練習プリント｜グラフと式（小学6年生）",
    "description": "印刷不要・スマホで即採点。小学6年生「比例・反比例」の練習プリント。比例・反比例の式・グラフ・表を使った問題を無料で練習できます。中学数学の準備にも。",
    "h1": "比例・反比例 練習プリント｜グラフと式",
    "eyecatch": "比例・反比例は中学数学の「一次関数・関数」への入口。6年生でしっかり理解しておくと、中学1年の数学がグンと楽になります！",
    "body_html": """
<h2>比例とは？</h2>
<p>xが2倍・3倍・…になると、yも2倍・3倍・…になる関係を「比例」といいます。</p>
<div class="formula-box"><p>y = x × k （kは比例定数・決まった数）</p></div>
<div class="tip-box"><p>💡 身近な比例の例：時速50kmで走る車の「時間と距離」→ 距離 = 50 × 時間</p></div>

<h2>比例の式の作り方</h2>
<p>x=1のときのyの値がkになります。</p>
<div class="formula-box"><p>x=1でy=3 → k=3 → y = 3x</p></div>

<h2>比例のグラフ</h2>
<ul>
  <li>原点（0,0）を通る直線になる</li>
  <li>kが正の数 → 右上がりの直線</li>
  <li>kが負の数 → 右下がりの直線（小6の範囲外が多い）</li>
</ul>

<h2>反比例とは？</h2>
<p>xが2倍・3倍になると、yが1/2・1/3になる関係を「反比例」といいます。</p>
<div class="formula-box"><p>y = k ÷ x （x×y = k が一定）</p></div>
<div class="tip-box"><p>💡 身近な反比例の例：面積が一定の長方形の「たてとよこ」→ たて = 面積 ÷ よこ</p></div>

<h2>比例と反比例の見分け方</h2>
<ul>
  <li>比例：表でxが2倍→yが2倍（y÷xが一定）</li>
  <li>反比例：表でxが2倍→yが1/2（x×yが一定）</li>
</ul>
<div class="warn-box"><p>⚠️ 「xが増えるとyが増える=比例」は誤り。必ず「何倍の関係か」を確認しましょう。</p></div>
""",
    "faq": [
      {"q": "比例・反比例は中学数学とどう関係しますか？", "a": "中学1年で学ぶ「比例・反比例」「関数」の直接の土台です。小6でしっかり理解しておくと中学数学のスタートがスムーズです。"},
      {"q": "比例定数とは何ですか？", "a": "y=kxのkのことです。「xが1のときのy」とも言えます。この値が決まることで比例の式が決まります。"},
      {"q": "反比例のグラフはどんな形ですか？", "a": "双曲線（なめらかに曲がった2本の曲線）になります。直線にはなりません。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/ratio-guide.html",       "emoji": "📊", "text": "比の学習"},
      {"href": "/speed-distance.html",    "emoji": "🚗", "text": "速さ・時間・距離"},
      {"href": "/graph-oretsu.html",      "emoji": "📈", "text": "折れ線グラフ"},
      {"href": "/grade-6-matome.html",    "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },
  {
    "filename": "baai-no-kazu.html",
    "title": "場合の数 練習プリント｜樹形図・組み合わせ（小学6年生）",
    "description": "印刷不要・スマホで即採点。小学6年生「場合の数」の練習プリント。樹形図・表を使った順列・組み合わせの数え方を無料で練習。中学の確率の基礎に。",
    "h1": "場合の数 練習プリント｜樹形図・組み合わせ",
    "eyecatch": "「何通りあるか？」を正確に数える力が場合の数。「もれなく・重複なく」数えるコツを樹形図・表で身につけましょう！",
    "body_html": """
<h2>場合の数とは？</h2>
<p>あることが起こる全ての「場合（パターン）の数」を求める問題です。</p>
<div class="tip-box"><p>💡 大原則：「もれなく・重複なく」数えること。これを守るために樹形図や表を使います。</p></div>

<h2>樹形図を使った数え方</h2>
<p>A・B・Cの3人を1列に並べる場合の数：</p>
<div class="formula-box"><p>A→B→C / A→C→B / B→A→C / B→C→A / C→A→B / C→B→A = 6通り</p></div>
<p>樹形図：枝を分岐させながら全パターンを書き出します。</p>

<h2>表を使った数え方</h2>
<p>サイコロを2個振ったときの組み合わせ（全36通り）は、縦横6×6の表で整理します。</p>
<div class="tip-box"><p>💡 「順番が関係する」問題は樹形図、「2つ以上の要素の組み合わせ」は表が整理しやすいです。</p></div>

<h2>順列と組み合わせの違い</h2>
<ul>
  <li><strong>順列</strong>：並ぶ順番が関係する（ABC と BCA は別のもの）</li>
  <li><strong>組み合わせ</strong>：並ぶ順番が関係しない（ABC と BCA は同じ）</li>
</ul>
<div class="formula-box"><p>3人を2人選ぶ組み合わせ: AB, AC, BC = 3通り（BA=ABなので重複しない）</p></div>
<div class="warn-box"><p>⚠️ 「順番あり（並べ方）」か「順番なし（選び方）」かを問題文から正確に読み取ることが大切です。</p></div>

<h2>よく出る問題パターン</h2>
<ul>
  <li>3〜5枚のカードから作れる数（順列）</li>
  <li>4人から2人を選ぶ（組み合わせ）</li>
  <li>サイコロの目の合計・積（表で整理）</li>
  <li>コインを3回投げた表・裏の組み合わせ</li>
</ul>
""",
    "faq": [
      {"q": "場合の数はいつ習いますか？", "a": "小学6年生で習います。中学・高校の「確率」の土台となる重要な単元です。"},
      {"q": "樹形図をきれいに書くコツは？", "a": "最初の選択肢を縦に並べ、そこから枝を横に伸ばしていきます。同じ階層は同じ高さにそろえて書くと見やすくなります。"},
      {"q": "場合の数で一番多いミスは何ですか？", "a": "「重複して数える」または「一部を数え忘れる」ミスです。必ず樹形図や表で整理してから数えましょう。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/hirei-hanpirei.html",  "emoji": "📈", "text": "比例・反比例"},
      {"href": "/ratio-guide.html",     "emoji": "📊", "text": "比の学習"},
      {"href": "/grade-6-matome.html",  "emoji": "📚", "text": "6年生 全単元まとめ"},
      {"href": "/chuugaku-junbi.html",  "emoji": "🎒", "text": "中学入学前の算数復習"},
    ],
  },
  {
    "filename": "kakudai-shukuzu.html",
    "title": "拡大図・縮図 練習プリント｜縮尺の読み取り（小学6年生）",
    "description": "印刷不要・スマホで即採点。小学6年生「拡大図・縮図」の練習プリント。相似な図形の性質・縮尺の計算・実際の距離の求め方を無料で練習できます。",
    "h1": "拡大図・縮図 練習プリント｜縮尺の読み取り",
    "eyecatch": "地図の縮尺を読んで実際の距離を計算する力が身につく単元。拡大図・縮図は「相似」の考え方で、中学数学に直結します！",
    "body_html": """
<h2>拡大図・縮図とは？</h2>
<p>ある図形と「形は同じで大きさだけ違う」図形を拡大図・縮図といいます。</p>
<div class="formula-box"><p>拡大図：元の図形より大きくした図　縮図：元の図形より小さくした図</p></div>
<div class="tip-box"><p>💡 拡大・縮小しても「角度は変わらない」「辺の比は一定」が重要なポイントです。</p></div>

<h2>拡大図・縮図の性質</h2>
<ul>
  <li><strong>対応する角の大きさ</strong>：変わらない（同じ）</li>
  <li><strong>対応する辺の長さの比</strong>：一定（同じ割合で変わる）</li>
</ul>
<div class="formula-box"><p>2倍の拡大図：全ての辺が2倍、角度は同じ</p></div>

<h2>縮尺とは？</h2>
<p>地図や設計図で「実際の長さを何分の1に縮めたか」を表すのが縮尺です。</p>
<div class="formula-box"><p>縮尺 1/25000 = 図上1cm → 実際25000cm（250m）</p></div>

<h2>縮尺を使った計算</h2>
<p>地図上の距離から実際の距離を求める：</p>
<div class="formula-box"><p>実際の距離 = 地図上の距離 × 縮尺の分母</p></div>
<div class="tip-box"><p>💡 縮尺1/50000の地図で3cmの場合 → 3 × 50000 = 150000cm = 1500m = 1.5km</p></div>
<div class="warn-box"><p>⚠️ 単位換算（cm→m→km）を忘れないようにしましょう。計算後に必ず単位を確認。</p></div>

<h2>拡大図の描き方</h2>
<ul>
  <li>全ての辺を同じ割合で拡大する</li>
  <li>角度はそのままにする</li>
  <li>基準点を決めて、そこからの距離を拡大する方法もある</li>
</ul>
""",
    "faq": [
      {"q": "拡大図・縮図はいつ習いますか？", "a": "小学6年生で習います。中学数学の「相似な図形」の基礎になる重要単元です。"},
      {"q": "縮尺1/50000とはどういう意味ですか？", "a": "実際の距離を50000分の1に縮めているということです。地図上の1cmが実際の50000cm（500m）に対応します。"},
      {"q": "拡大図と縮図で変わらないものは何ですか？", "a": "角度（内角の大きさ）は変わりません。辺の長さは変わりますが、辺の比（割合）は一定です。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/taishou-figure.html", "emoji": "🔷", "text": "対称な図形"},
      {"href": "/goudo-figure.html",   "emoji": "🔷", "text": "図形の合同（5年生）"},
      {"href": "/ratio-guide.html",    "emoji": "📊", "text": "比の学習"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },


  # ────────────────────────────────
  # 足し算
  # ────────────────────────────────
  {
    "filename": "tasizan-kiso.html",
    "title": "足し算の基礎プリント【無料】1年生からわかりやすく解説",
    "description": "足し算の基礎を印刷不要・スマホで練習できる無料プリント。1桁＋1桁から始めて繰り上がりまで丁寧に解説。小学1年生から使えます。",
    "h1": "足し算の基礎プリント【無料】小学1年生",
    "eyecatch": "➕ 足し算は算数の一番の基礎。1桁どうしの計算からしっかり練習して、繰り上がりまで完全攻略しましょう！",
    "body_html": """\
<h2>足し算とは？</h2>
<p>足し算は「合わせていくつ？」という計算です。たとえば「りんごが3個とみかんが2個、合わせて何個？」というのが足し算の考え方です。</p>
<div class="formula-box"><p>3 ＋ 2 ＝ 5　（3と2を合わせると5）</p></div>

<h2>1桁の足し算（繰り上がりなし）</h2>
<p>まずは答えが10以下になる足し算を練習します。指を使っても構いません。慣れてきたら頭の中で計算できるようにしましょう。</p>
<ul>
  <li>2＋3＝5、4＋1＝5、3＋3＝6 など</li>
  <li>数の合成（7は3と4、8は5と3…）を覚えると速くなる</li>
</ul>
<div class="tip-box"><p>💡 「いくつといくつ」で10までの数の組み合わせをマスターすると、足し算がぐっと速くなります。</p></div>

<h2>繰り上がりのある足し算</h2>
<p>答えが10を超える足し算では「繰り上がり」が起きます。「10のまとまり」を作る考え方が大切です。</p>
<div class="formula-box"><p>8 ＋ 5 ＝ 8 ＋ 2 ＋ 3 ＝ 10 ＋ 3 ＝ 13</p></div>
<p>8に2を足して10を作り、残りの3を足すと13。この「10の補数」を使う考え方を覚えましょう。</p>

<h2>練習のコツ</h2>
<ol>
  <li>毎日少しずつ（5〜10分）練習する</li>
  <li>計算カード（フラッシュカード）で反射的に答えられるようにする</li>
  <li>間違えた問題を繰り返し解く</li>
</ol>
<div class="warn-box"><p>⚠️ 最初は指を使っても大丈夫。大事なのは「なぜその答えになるか」を理解することです。</p></div>""",
    "faq": [
      {"q": "足し算はいつから習いますか？", "a": "小学1年生の最初から学習します。1学期に1桁の足し算、2学期以降に繰り上がりのある足し算を習います。"},
      {"q": "繰り上がりの足し算のコツは？", "a": "「10の補数」を使う方法が効果的です。8+5なら8に2を足して10を作り、残り3を足して13とする考え方です。"},
      {"q": "足し算が苦手な子への教え方は？", "a": "具体物（おはじき・ブロック）を使って量感を養うことが大切です。数え上げから始めて、徐々に暗算へ移行しましょう。"},
      {"q": "毎日何問練習すればいいですか？", "a": "1日10〜20問を毎日続けることが効果的です。短時間でも継続することで計算力が着実に伸びます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/tasizan-kuriagari.html", "emoji": "➕", "text": "繰り上がりのある足し算"},
      {"href": "/hikizan-kiso.html",      "emoji": "➖", "text": "引き算の基礎"},
      {"href": "/ikutsu-ikutsu.html",     "emoji": "🔢", "text": "いくつといくつ"},
      {"href": "/grade-1-matome.html",    "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  {
    "filename": "tasizan-kuriagari.html",
    "title": "繰り上がりのある足し算プリント【無料】小学1年生",
    "description": "繰り上がりのある足し算（9＋3など）を印刷不要・スマホで練習できる無料プリント。10の補数を使った解き方をわかりやすく解説。",
    "h1": "繰り上がりのある足し算プリント【無料】",
    "eyecatch": "➕ 繰り上がりのある足し算は1年生最大の山場。「10のまとまり」を使えば必ず解けます！",
    "body_html": """\
<h2>繰り上がりの足し算とは？</h2>
<p>答えが10を超える足し算のことです。例えば「8＋6」「9＋3」などが繰り上がりの足し算です。</p>

<h2>解き方：「10の補数」を使う</h2>
<p>大きい数を10にするために、小さい数を分割する方法です。</p>
<div class="formula-box"><p>9 ＋ 4 ＝ 9 ＋ 1 ＋ 3 ＝ 10 ＋ 3 ＝ 13</p></div>
<ol>
  <li>9に足りない1を4から借りる（4→1と3に分ける）</li>
  <li>9＋1＝10 にする</li>
  <li>10＋3＝13</li>
</ol>
<div class="tip-box"><p>💡 「9は1足りない」「8は2足りない」と覚えると素早く計算できます。</p></div>

<h2>練習一覧（よく出る問題）</h2>
<ul>
  <li>9のたし算：9＋2＝11、9＋3＝12…9＋9＝18</li>
  <li>8のたし算：8＋3＝11、8＋4＝12…8＋9＝17</li>
  <li>7のたし算：7＋4＝11、7＋5＝12…7＋9＝16</li>
</ul>

<h2>つまずきポイント</h2>
<ul>
  <li>どちらの数を分けるか迷う →「大きい方を10にする」と決める</li>
  <li>計算ミスが多い →数え上げと並行して「指さし確認」する</li>
</ul>""",
    "faq": [
      {"q": "繰り上がりの足し算はいつ習いますか？", "a": "小学1年生の2学期（10月〜11月頃）に習います。1年生算数の中で最も重要な単元の一つです。"},
      {"q": "「さくらんぼ計算」とは何ですか？", "a": "数を2つに分けて10の補数を作る計算方法です。例えば8+5なら、5を2と3に分け、8+2=10、10+3=13と計算します。"},
      {"q": "繰り上がりが苦手な場合はどうすれば？", "a": "おはじきやブロックを使って「10のまとまりを作る」動作を繰り返すことが効果的です。体で覚えてから暗算に移行しましょう。"},
      {"q": "何度練習すれば覚えますか？", "a": "1日10問を毎日2〜3週間続けると、反射的に答えられるようになります。計算カードも効果的です。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/tasizan-kiso.html",      "emoji": "➕", "text": "足し算の基礎"},
      {"href": "/hikizan-kurisagari.html","emoji": "➖", "text": "繰り下がりのある引き算"},
      {"href": "/10made-no-kazu.html",    "emoji": "🔢", "text": "10までの数"},
      {"href": "/grade-1-matome.html",    "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  {
    "filename": "tasizan-2keta.html",
    "title": "2桁の足し算プリント【無料】筆算のやり方｜小学2年生",
    "description": "2桁の足し算・筆算を印刷不要・スマホで練習できる無料プリント。繰り上がりありの2桁＋2桁を丁寧に解説。小学2年生向け。",
    "h1": "2桁の足し算（筆算）プリント【無料】小学2年生",
    "eyecatch": "➕ 2桁の足し算は筆算の第一歩。位をそろえて書く習慣をつけることが大切です！",
    "body_html": """\
<h2>2桁の足し算の筆算の書き方</h2>
<p>2桁の足し算では「筆算」を使います。位（くらい）をそろえて縦に書き、一の位から計算します。</p>
<div class="formula-box"><p>　　47<br>＋ 35<br>─────<br>　　82</p></div>
<ol>
  <li>一の位：7＋5＝12　→ 2を書いて1を繰り上げる</li>
  <li>十の位：4＋3＋1（繰り上がり）＝8　→ 8を書く</li>
  <li>答え：82</li>
</ol>
<div class="tip-box"><p>💡 位をそろえて書くには、方眼ノートを使うと書きやすくなります。</p></div>

<h2>繰り上がりのある筆算のコツ</h2>
<ul>
  <li>繰り上がった「1」は十の位の上に小さく書く</li>
  <li>足し忘れや2重に足すミスに注意</li>
  <li>計算後に確認（引き算で検算）する習慣をつける</li>
</ul>

<h2>よくあるミス</h2>
<ul>
  <li>位がずれて書いてしまう</li>
  <li>繰り上がりの「1」を忘れる</li>
  <li>一の位を先に計算しない（十の位から計算してしまう）</li>
</ul>
<div class="warn-box"><p>⚠️ 必ず一の位から計算する習慣をつけましょう。</p></div>""",
    "faq": [
      {"q": "2桁の足し算はいつ習いますか？", "a": "小学2年生で学習します。繰り上がりなしから始めて、繰り上がりありの筆算まで段階的に学びます。"},
      {"q": "筆算で位がずれてしまう場合の対策は？", "a": "方眼ノートや算数専用ノートを使うことが効果的です。罫線を利用して一の位・十の位の列を決めて書きましょう。"},
      {"q": "暗算でもできますか？", "a": "2桁の足し算は暗算でもできますが、まず筆算の方法をしっかり覚えることが大切です。筆算の理解が暗算の基礎になります。"},
      {"q": "何桁の足し算まで小学校で習いますか？", "a": "小学3年生までに3桁、4桁の足し算を学習します。基本の手順は同じで、桁数が増えるだけです。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/tasizan-kiso.html",      "emoji": "➕", "text": "足し算の基礎"},
      {"href": "/hikizan-2keta.html",     "emoji": "➖", "text": "2桁の引き算"},
      {"href": "/kongozan.html",          "emoji": "🔢", "text": "たし算・ひき算の混合計算"},
      {"href": "/grade-2-matome.html",    "emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # 引き算
  # ────────────────────────────────
  {
    "filename": "hikizan-kiso.html",
    "title": "引き算の基礎プリント【無料】1年生からわかりやすく解説",
    "description": "引き算の基礎を印刷不要・スマホで練習できる無料プリント。1桁の引き算から繰り下がりまで丁寧に解説。小学1年生から使えます。",
    "h1": "引き算の基礎プリント【無料】小学1年生",
    "eyecatch": "➖ 引き算は「残りはいくつ？」という計算。足し算と一緒に覚えることでどちらも得意になります！",
    "body_html": """\
<h2>引き算とは？</h2>
<p>引き算は「残りはいくつ？」「違いはいくつ？」という計算です。たとえば「りんごが5個あって2個食べたら何個残る？」が引き算です。</p>
<div class="formula-box"><p>5 ー 2 ＝ 3　（5から2を引くと3残る）</p></div>

<h2>引き算の2つの意味</h2>
<ol>
  <li><strong>残りを求める（求残）：</strong>「5個のうち2個食べた。残りは？」→5－2＝3</li>
  <li><strong>違いを求める（求差）：</strong>「5個と3個、どちらが何個多い？」→5－3＝2</li>
</ol>
<div class="tip-box"><p>💡 足し算と引き算は「逆の関係」。3＋2＝5 が分かれば 5－2＝3 も分かります。</p></div>

<h2>練習のポイント</h2>
<ul>
  <li>具体物（おはじき・ブロック）で「取り去る」動作を体験する</li>
  <li>「5－□＝3」のような穴埋め問題も練習する</li>
  <li>足し算カードと引き算カードをセットで覚える</li>
</ul>

<h2>よくある間違い</h2>
<ul>
  <li>大きい数から小さい数を引くのに、逆に計算してしまう</li>
  <li>「0を引く」「同じ数を引く」の結果を間違える（5－0＝5、5－5＝0）</li>
</ul>""",
    "faq": [
      {"q": "引き算はいつから習いますか？", "a": "小学1年生の1学期から習います。足し算と同じ時期に学び始め、2学期には繰り下がりのある引き算を学習します。"},
      {"q": "足し算と引き算、どちらを先に教えるべきですか？", "a": "足し算を先に習いますが、両方は表裏一体です。3＋2＝5と5－2＝3を一緒に覚えると定着しやすくなります。"},
      {"q": "引き算が苦手な子への教え方は？", "a": "具体物で「取り去る」動作を見せることが効果的です。また「たし算の逆」という見方で理解を助けることもできます。"},
      {"q": "引き算でゼロになる計算は教えるべきですか？", "a": "「5－5＝0」のように同じ数を引くと0になることは1年生で学びます。0の概念は大切なのでしっかり教えましょう。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/hikizan-kurisagari.html","emoji": "➖", "text": "繰り下がりのある引き算"},
      {"href": "/tasizan-kiso.html",      "emoji": "➕", "text": "足し算の基礎"},
      {"href": "/kongozan.html",          "emoji": "🔢", "text": "たし算・ひき算 混合"},
      {"href": "/grade-1-matome.html",    "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  {
    "filename": "hikizan-kurisagari.html",
    "title": "繰り下がりのある引き算プリント【無料】小学1年生",
    "description": "繰り下がりのある引き算（13－7など）を印刷不要・スマホで練習できる無料プリント。「10のまとまり」を使った解き方をわかりやすく解説。",
    "h1": "繰り下がりのある引き算プリント【無料】",
    "eyecatch": "➖ 繰り下がりは1年生算数の難関。「10から引く」考え方をマスターすれば大丈夫！",
    "body_html": """\
<h2>繰り下がりの引き算とは？</h2>
<p>一の位だけでは引けないため、十の位から1くり下げる引き算です。例えば「13－7」などです。</p>

<h2>解き方①：「10から引く」方法（減加法）</h2>
<div class="formula-box"><p>13 ー 7 ＝ 10 ー 7 ＋ 3 ＝ 3 ＋ 3 ＝ 6</p></div>
<ol>
  <li>13を「10と3」に分ける</li>
  <li>10から7を引く → 3</li>
  <li>残りの3を足す → 3＋3＝6</li>
</ol>

<h2>解き方②：「引かれる数を分ける」方法（減々法）</h2>
<div class="formula-box"><p>13 ー 7 ＝ 13 ー 3 ー 4 ＝ 10 ー 4 ＝ 6</p></div>
<ol>
  <li>7を「3と4」に分ける（13の一の位3に合わせる）</li>
  <li>13から3を引く → 10</li>
  <li>10から4を引く → 6</li>
</ol>
<div class="tip-box"><p>💡 どちらの方法でも答えは同じ。子どもが理解しやすい方法で練習しましょう。</p></div>

<h2>よくある間違い</h2>
<ul>
  <li>繰り下げを忘れて計算する</li>
  <li>10から引く計算（10の減法）が苦手なまま進んでしまう</li>
</ul>
<div class="warn-box"><p>⚠️ まず「10－□」の計算（10の減法）を完璧に覚えてから繰り下がりに進みましょう。</p></div>""",
    "faq": [
      {"q": "繰り下がりの引き算はいつ習いますか？", "a": "小学1年生の2学期（11月〜12月頃）に学習します。繰り上がりの足し算の直後に習うことが多いです。"},
      {"q": "「さくらんぼ計算」は引き算にも使いますか？", "a": "はい、使います。引き算では「10から引く」方法（10を使って引く）が基本で、これもさくらんぼ計算の一種です。"},
      {"q": "繰り下がりが苦手な場合は？", "a": "「10の減法（10－1〜10－9）」を先に完璧にすることが大切です。ここが自動化されると繰り下がり全体がスムーズになります。"},
      {"q": "繰り下がりは暗記した方がいいですか？", "a": "最終的には暗記（自動化）が目標ですが、まず仕組みを理解することが先です。仕組みが分かると忘れても自分で計算できます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/hikizan-kiso.html",       "emoji": "➖", "text": "引き算の基礎"},
      {"href": "/tasizan-kuriagari.html",  "emoji": "➕", "text": "繰り上がりのある足し算"},
      {"href": "/hikizan-2keta.html",      "emoji": "➖", "text": "2桁の引き算"},
      {"href": "/grade-1-matome.html",     "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  {
    "filename": "hikizan-2keta.html",
    "title": "2桁の引き算プリント【無料】筆算のやり方｜小学2年生",
    "description": "2桁の引き算・筆算を印刷不要・スマホで練習できる無料プリント。繰り下がりありの2桁－2桁を丁寧に解説。小学2年生向け。",
    "h1": "2桁の引き算（筆算）プリント【無料】小学2年生",
    "eyecatch": "➖ 2桁の引き算は繰り下がりがポイント。筆算の手順を覚えて確実に解けるようになろう！",
    "body_html": """\
<h2>2桁の引き算の筆算の手順</h2>
<div class="formula-box"><p>　　73<br>ー 45<br>─────<br>　　28</p></div>
<ol>
  <li>一の位：3から5は引けない → 十の位から1くり下げる</li>
  <li>10＋3＝13、13－5＝8 → 8を一の位に書く</li>
  <li>十の位：7－1（くり下げた分）＝6、6－4＝2 → 2を十の位に書く</li>
  <li>答え：28</li>
</ol>
<div class="tip-box"><p>💡 くり下げたら十の位の数を1小さくする（頭に小さい印をつける）と忘れにくい。</p></div>

<h2>検算の方法</h2>
<p>答えに引く数を足すと、もとの数に戻ることで確認できます。</p>
<div class="formula-box"><p>28 ＋ 45 ＝ 73　✓</p></div>

<h2>よくある間違い</h2>
<ul>
  <li>くり下げた後の十の位を減らし忘れる</li>
  <li>大きい数から小さい数を引いてしまう（逆算）</li>
  <li>0がある問題（例：70－34）でくり下がりに戸惑う</li>
</ul>
<div class="warn-box"><p>⚠️ 「0がある数の引き算」は特に間違いやすいので集中して練習しましょう。</p></div>""",
    "faq": [
      {"q": "2桁の引き算はいつ習いますか？", "a": "小学2年生で学習します。繰り下がりなしから始めて、繰り下がりありの筆算まで段階的に学びます。"},
      {"q": "「0から引けない」問題はどう教えますか？", "a": "70－34のような場合、7から1くり下げてまず一の位を10にします。この手順を具体物で見せると理解しやすくなります。"},
      {"q": "筆算のくり下がりを覚えるコツは？", "a": "くり下げた箇所に小さく印（'）をつける習慣をつけましょう。計算後に印のついた位の数が1減っているか確認します。"},
      {"q": "2桁の引き算でよく使われる検算方法は？", "a": "答えに引いた数を足してもとの数になるか確認します（例：28＋45＝73）。計算が合っているか素早く確認できます。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/hikizan-kiso.html",       "emoji": "➖", "text": "引き算の基礎"},
      {"href": "/hikizan-kurisagari.html", "emoji": "➖", "text": "繰り下がりのある引き算"},
      {"href": "/tasizan-2keta.html",      "emoji": "➕", "text": "2桁の足し算"},
      {"href": "/grade-2-matome.html",     "emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # かけ算
  # ────────────────────────────────
  {
    "filename": "kakizan-kiso.html",
    "title": "かけ算の基礎プリント【無料】意味と九九の覚え方｜小学2年生",
    "description": "かけ算の意味と九九を印刷不要・スマホで練習できる無料プリント。かけ算の意味（同じ数のまとまり）から丁寧に解説。小学2年生向け。",
    "h1": "かけ算の基礎プリント【無料】小学2年生",
    "eyecatch": "✖️ かけ算は「同じ数のまとまり」を素早く計算するための方法。九九をマスターすれば算数がぐんと速くなります！",
    "body_html": """\
<h2>かけ算とは？</h2>
<p>「同じ数のまとまりがいくつあるか」を一度に求める計算です。</p>
<div class="formula-box"><p>3 × 4 ＝ 12　（3のまとまりが4つ ＝ 12）</p></div>
<p>3＋3＋3＋3＝12 と同じですが、かけ算の方がずっと速く計算できます。</p>

<h2>かけ算の用語</h2>
<ul>
  <li><strong>3 × 4 ＝ 12</strong>のとき</li>
  <li>3：1つ分の数（かけられる数）</li>
  <li>4：いくつ分（かける数）</li>
  <li>12：積（かけ算の答え）</li>
</ul>
<div class="tip-box"><p>💡 「3×4」と「4×3」は答えが同じ12。これをかけ算の「交換法則」といいます。</p></div>

<h2>九九の覚え方</h2>
<ol>
  <li>声に出して繰り返す（音で覚える）</li>
  <li>歌や語呂合わせを使う</li>
  <li>九九カードでランダムに練習する</li>
  <li>毎日少しずつ（1段ずつ）覚える</li>
</ol>

<h2>九九マスター後にできること</h2>
<ul>
  <li>2桁の筆算が速くなる</li>
  <li>割り算の基礎になる</li>
  <li>分数・比の計算にも活かせる</li>
</ul>
<div class="warn-box"><p>⚠️ 九九は小学2年生の算数の最重要事項。完璧に覚えるまで毎日練習しましょう。</p></div>""",
    "faq": [
      {"q": "かけ算はいつから習いますか？", "a": "小学2年生の2学期から学習します。かけ算の意味を学んだ後、九九（1の段〜9の段）を覚えます。"},
      {"q": "九九はどのくらいで覚えられますか？", "a": "個人差がありますが、毎日練習すれば1〜2か月で全段覚えられます。1段ずつ確実に覚えていく方法が効果的です。"},
      {"q": "かけ算と足し算の違いは？", "a": "足し算は「異なる数を合わせる」のに対し、かけ算は「同じ数のまとまりがいくつあるか」を求めます。例：3+5は3と5を合わせる。3×5は3が5つで15。"},
      {"q": "九九は全部で何通りありますか？", "a": "1〜9の段それぞれ9問で、合計81通りあります。交換法則を使うと半分以下に減らせます。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/kuku-tips.html",     "emoji": "✖️", "text": "九九の覚え方ガイド"},
      {"href": "/kakizan-hissan.html","emoji": "✖️", "text": "かけ算の筆算"},
      {"href": "/warizan-kiso.html",  "emoji": "➗", "text": "わり算の基礎"},
      {"href": "/grade-2-matome.html","emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },

  {
    "filename": "kakizan-hissan.html",
    "title": "かけ算の筆算プリント【無料】2桁×1桁・2桁×2桁｜小学3・4年生",
    "description": "かけ算の筆算（2桁×1桁・2桁×2桁・3桁×2桁）を印刷不要・スマホで練習できる無料プリント。手順を丁寧に解説。小学3〜4年生向け。",
    "h1": "かけ算の筆算プリント【無料】小学3〜4年生",
    "eyecatch": "✖️ かけ算の筆算は手順を覚えれば必ず解ける！2桁×1桁から丁寧にステップアップしましょう。",
    "body_html": """\
<h2>2桁×1桁の筆算</h2>
<div class="formula-box"><p>　　34<br>× 　7<br>─────<br>　238</p></div>
<ol>
  <li>一の位：4×7＝28 → 8を書いて2を繰り上げる</li>
  <li>十の位：3×7＝21、21＋2（繰り上がり）＝23 → 23を書く</li>
  <li>答え：238</li>
</ol>

<h2>2桁×2桁の筆算</h2>
<div class="formula-box"><p>　　34<br>×　25<br>─────<br>　170　（34×5）<br>＋680　（34×20）<br>─────<br>　850</p></div>
<ol>
  <li>まず34×5（一の位）を計算 → 170</li>
  <li>次に34×2（十の位）を計算してひとつ左にずらす → 680</li>
  <li>足し合わせる：170＋680＝850</li>
</ol>
<div class="tip-box"><p>💡 2段目は1つ左にずらして書く（×10のため）。忘れないように「0を書いてからずらす」方法もあります。</p></div>

<h2>よくある間違い</h2>
<ul>
  <li>繰り上がりを忘れる、または2重に足す</li>
  <li>2段目のずらし忘れ</li>
  <li>部分積の足し算でのミス</li>
</ul>""",
    "faq": [
      {"q": "かけ算の筆算はいつ習いますか？", "a": "2桁×1桁は小学3年生、2桁×2桁・3桁×2桁は小学4年生で学習します。"},
      {"q": "2段目をずらして書く理由は？", "a": "2桁×2桁の筆算で十の位にかける計算は「×10」が含まれるため、1桁左（＝×10の位置）にずらして書きます。"},
      {"q": "筆算の繰り上がりを間違えないコツは？", "a": "繰り上がりの数を小さく問題の上に書き、計算後に確認する習慣をつけましょう。書き忘れ・消し忘れに注意です。"},
      {"q": "3桁×2桁はいつ習いますか？", "a": "小学4年生で習います。手順は2桁×2桁と同じで、桁数が増えるだけです。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/kakizan-kiso.html",   "emoji": "✖️", "text": "かけ算の基礎・九九"},
      {"href": "/warizan-hissan.html", "emoji": "➗", "text": "わり算の筆算"},
      {"href": "/kuku-tips.html",      "emoji": "✖️", "text": "九九の覚え方"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # わり算
  # ────────────────────────────────
  {
    "filename": "warizan-kiso.html",
    "title": "わり算の基礎プリント【無料】意味と九九を使った計算｜小学3年生",
    "description": "わり算の意味と九九を使った計算を印刷不要・スマホで練習できる無料プリント。等分除・包含除の2つの意味から丁寧に解説。小学3年生向け。",
    "h1": "わり算の基礎プリント【無料】小学3年生",
    "eyecatch": "➗ わり算は「等しく分ける」計算。九九が使えれば大丈夫！2つの意味をしっかり理解しましょう。",
    "body_html": """\
<h2>わり算とは？</h2>
<p>わり算には2つの意味があります。</p>
<div class="formula-box"><p>12 ÷ 3 ＝ 4</p></div>
<ul>
  <li><strong>等分除：</strong>「12個を3人で分けると1人何個？」→ 4個</li>
  <li><strong>包含除：</strong>「12個を3個ずつ分けると何人分？」→ 4人分</li>
</ul>

<h2>九九を使ったわり算</h2>
<p>わり算は九九の逆引きで解きます。</p>
<div class="formula-box"><p>24 ÷ 4 ＝ □ → 4 × □ ＝ 24 → □ ＝ 6</p></div>
<p>「4の段で24になるのは？」と考えると 4×6＝24 なので答えは6。</p>
<div class="tip-box"><p>💡 わり算がすぐに解けない場合は九九を暗唱して答えを探しましょう。九九の完璧な習熟がわり算の近道です。</p></div>

<h2>わり算の用語</h2>
<ul>
  <li><strong>12 ÷ 3 ＝ 4</strong>のとき</li>
  <li>12：割られる数</li>
  <li>3：割る数</li>
  <li>4：商（わり算の答え）</li>
</ul>

<h2>0と1のわり算</h2>
<ul>
  <li>0 ÷ □ ＝ 0（0を何で割っても0）</li>
  <li>□ ÷ 1 ＝ □（1で割ると変わらない）</li>
  <li>□ ÷ □ ＝ 1（同じ数で割ると1）</li>
</ul>""",
    "faq": [
      {"q": "わり算はいつから習いますか？", "a": "小学3年生の1学期から学習します。まずあまりのないわり算を学び、その後あまりのあるわり算へ進みます。"},
      {"q": "わり算は九九が必要ですか？", "a": "はい、九九の逆引きがわり算の基礎です。九九が完璧でないと、わり算が苦手になります。2年生のうちに九九を完璧にしておきましょう。"},
      {"q": "等分除と包含除の違いは？", "a": "等分除は「何個ずつ？」、包含除は「何人分？」を求めます。式は同じでも問題の場面が異なります。どちらの場面か読み取る練習が大切です。"},
      {"q": "0で割ることはできますか？", "a": "0で割ることは定義されていません（計算できません）。一方「0÷□＝0」は正しいです。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-amari.html",  "emoji": "➗", "text": "あまりのあるわり算"},
      {"href": "/warizan-hissan.html", "emoji": "➗", "text": "わり算の筆算"},
      {"href": "/kakizan-kiso.html",   "emoji": "✖️", "text": "かけ算の基礎"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "warizan-amari.html",
    "title": "あまりのあるわり算プリント【無料】小学3年生",
    "description": "あまりのあるわり算を印刷不要・スマホで練習できる無料プリント。あまりの意味・検算の方法をわかりやすく解説。小学3年生向け。",
    "h1": "あまりのあるわり算プリント【無料】小学3年生",
    "eyecatch": "➗ あまりのあるわり算は日常生活でもよく使う計算。あまりの意味と検算方法をしっかり学ぼう！",
    "body_html": """\
<h2>あまりのあるわり算とは？</h2>
<p>割り切れないわり算で、余った数（あまり）が出るものです。</p>
<div class="formula-box"><p>17 ÷ 5 ＝ 3 あまり 2</p></div>
<p>「17個を5人で分けると1人3個で、2個余る」という意味です。</p>

<h2>解き方</h2>
<ol>
  <li>商（答えの整数部分）を九九で探す：5×3＝15、5×4＝20 → 15が17以下で最大なので3</li>
  <li>あまりを計算：17－15＝2</li>
  <li>確認：あまり（2）は割る数（5）より小さいこと</li>
</ol>
<div class="tip-box"><p>💡 あまりは必ず割る数より小さくなります。あまりが割る数以上なら商が小さすぎます。</p></div>

<h2>検算の方法</h2>
<div class="formula-box"><p>割る数 × 商 ＋ あまり ＝ 割られる数<br>5 × 3 ＋ 2 ＝ 17 ✓</p></div>

<h2>文章題でのあまりの扱い</h2>
<ul>
  <li>「何人に配れますか？」→ 商が答え（あまりは配れない）</li>
  <li>「何個必要ですか？」→ 商＋1が答え（あまりがあるなら1つ追加）</li>
</ul>
<div class="warn-box"><p>⚠️ 文章題ではあまりを「切り捨て」か「切り上げ」かで答えが変わります。問題文をよく読みましょう。</p></div>""",
    "faq": [
      {"q": "あまりのあるわり算はいつ習いますか？", "a": "小学3年生で学習します。まずあまりのないわり算を覚えてから、あまりのあるわり算へ進みます。"},
      {"q": "あまりが割る数より大きくなってしまう場合は？", "a": "商が小さすぎます。あまりは必ず割る数より小さくなるので、商を1増やして計算し直しましょう。"},
      {"q": "「あまりを切り上げる」問題の見分け方は？", "a": "「何袋必要か」「何台必要か」など、容量を超えた分も数える場合に切り上げます。「何人分配れるか」は切り捨てです。問題文の内容で判断します。"},
      {"q": "検算は必ずしなければなりませんか？", "a": "テストでは時間があれば必ず検算することをおすすめします。「割る数×商＋あまり＝割られる数」で確認できます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-kiso.html",   "emoji": "➗", "text": "わり算の基礎"},
      {"href": "/warizan-hissan.html", "emoji": "➗", "text": "わり算の筆算"},
      {"href": "/mondai-wariai.html",  "emoji": "📝", "text": "わり算の文章題"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "warizan-hissan.html",
    "title": "わり算の筆算プリント【無料】2桁÷1桁・3桁÷2桁｜小学4年生",
    "description": "わり算の筆算（2桁÷1桁・3桁÷1桁・3桁÷2桁）を印刷不要・スマホで練習できる無料プリント。「たてる・かける・ひく・おろす」の手順を解説。",
    "h1": "わり算の筆算プリント【無料】小学4年生",
    "eyecatch": "➗ わり算の筆算は「たてる・かける・ひく・おろす」の4ステップ。手順をマスターすれば必ず解けます！",
    "body_html": """\
<h2>わり算の筆算の4ステップ</h2>
<div class="formula-box"><p>「たてる」→「かける」→「ひく」→「おろす」</p></div>

<h2>例：96 ÷ 4 の計算</h2>
<ol>
  <li><strong>たてる：</strong>9÷4＝2あまり1 → 商の2を書く</li>
  <li><strong>かける：</strong>4×2＝8 → 9の下に書く</li>
  <li><strong>ひく：</strong>9－8＝1 → 差を書く</li>
  <li><strong>おろす：</strong>次の桁（6）をおろして16にする</li>
  <li>繰り返す：16÷4＝4 → 商に4を書く、4×4＝16、16－16＝0</li>
  <li>答え：24</li>
</ol>
<div class="tip-box"><p>💡 商の見当をつけるには「割る数×□がちょうど良い大きさ」になる□を九九で探します。</p></div>

<h2>3桁÷2桁のポイント</h2>
<ul>
  <li>商の見当を「割られる数の上2桁÷割る数」で考える</li>
  <li>商が大きすぎた場合は1減らす、小さすぎた場合は1増やす</li>
</ul>

<h2>よくある間違い</h2>
<ul>
  <li>商の位置がずれる</li>
  <li>「おろす」を忘れる</li>
  <li>商の見当が外れた時に修正しない</li>
</ul>""",
    "faq": [
      {"q": "わり算の筆算はいつ習いますか？", "a": "小学4年生で学習します。2桁÷1桁から始まり、3桁÷2桁まで学びます。"},
      {"q": "「たてる・かける・ひく・おろす」とは何ですか？", "a": "わり算筆算の4ステップです。①商をたてる②かけ算をする③差を引く④次の桁をおろす、この繰り返しで計算します。"},
      {"q": "商の見当が外れた場合はどうしますか？", "a": "引き算の結果が割る数以上になった場合は商を1増やし、引き算の結果がマイナスになった場合は商を1減らします。"},
      {"q": "筆算でよく使われる確認方法は？", "a": "「割る数×商＋あまり＝割られる数」で検算します。この式が成り立てば正解です。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-kiso.html",   "emoji": "➗", "text": "わり算の基礎"},
      {"href": "/warizan-amari.html",  "emoji": "➗", "text": "あまりのあるわり算"},
      {"href": "/kakizan-hissan.html", "emoji": "✖️", "text": "かけ算の筆算"},
      {"href": "/grade-4-matome.html", "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },


  # ────────────────────────────────
  # 分数
  # ────────────────────────────────
  {
    "filename": "bunsuu-tasizan.html",
    "title": "分数のたし算プリント【無料】同分母・異分母の計算｜小学5年生",
    "description": "分数のたし算（同分母・異分母の通分）を印刷不要・スマホで練習できる無料プリント。通分のやり方から丁寧に解説。小学5年生向け。",
    "h1": "分数のたし算プリント【無料】小学5年生",
    "eyecatch": "½ 分数のたし算は通分がポイント。手順さえ覚えれば必ず解けます！",
    "body_html": """\
<h2>同分母の分数のたし算</h2>
<p>分母が同じ場合は、分子だけを足します。</p>
<div class="formula-box"><p>2/5 ＋ 1/5 ＝ (2＋1)/5 ＝ 3/5</p></div>
<div class="tip-box"><p>💡 分母は変えずに分子だけ足す。「分母は器の大きさ、分子は入っている量」とイメージすると分かりやすいです。</p></div>

<h2>異分母の分数のたし算（通分）</h2>
<p>分母が違う場合は先に通分（分母をそろえること）が必要です。</p>
<div class="formula-box"><p>1/3 ＋ 1/4 ＝ 4/12 ＋ 3/12 ＝ 7/12</p></div>
<ol>
  <li>3と4の最小公倍数を求める → 12</li>
  <li>1/3 → 4/12（分母・分子に同じ数をかける）</li>
  <li>1/4 → 3/12</li>
  <li>4/12 ＋ 3/12 ＝ 7/12</li>
</ol>

<h2>帯分数のたし算</h2>
<p>帯分数（1と2/3のような形）は整数部分と分数部分をそれぞれ足します。</p>
<div class="formula-box"><p>1と2/3 ＋ 2と1/3 ＝ 3と3/3 ＝ 3＋1 ＝ 4</p></div>
<div class="warn-box"><p>⚠️ 答えが仮分数になった場合は帯分数か整数に直しましょう。また約分できる場合は必ず約分します。</p></div>""",
    "faq": [
      {"q": "分数のたし算はいつ習いますか？", "a": "同分母の分数のたし算は小学3〜4年生で、異分母（通分）は小学5年生で学習します。"},
      {"q": "通分の最小公倍数が分からない場合は？", "a": "分母どうしをかけ算した数を共通の分母として使う方法もあります（例：3と4なら12）。ただし最小公倍数を使う方が約分が少なくて済みます。"},
      {"q": "答えが仮分数になったらどうしますか？", "a": "帯分数か整数に直します。例えば7/4は1と3/4、6/3は2になります。"},
      {"q": "約分はどの時点でしますか？", "a": "答えを出してから最後に約分するのが基本です。ただし途中で約分できる場合は早めに約分すると計算が楽になります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-hikizan.html", "emoji": "½", "text": "分数のひき算"},
      {"href": "/bunsuu-tsuubun.html", "emoji": "½", "text": "通分のやり方"},
      {"href": "/bunsuu-yakubun.html", "emoji": "½", "text": "約分のやり方"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "bunsuu-hikizan.html",
    "title": "分数のひき算プリント【無料】同分母・異分母の計算｜小学5年生",
    "description": "分数のひき算（同分母・通分）を印刷不要・スマホで練習できる無料プリント。帯分数のひき算も解説。小学5年生向け。",
    "h1": "分数のひき算プリント【無料】小学5年生",
    "eyecatch": "½ 分数のひき算も通分がポイント。たし算と同じ手順で確実に解けます！",
    "body_html": """\
<h2>同分母の分数のひき算</h2>
<div class="formula-box"><p>4/5 ー 1/5 ＝ (4ー1)/5 ＝ 3/5</p></div>

<h2>異分母の分数のひき算（通分）</h2>
<div class="formula-box"><p>3/4 ー 1/3 ＝ 9/12 ー 4/12 ＝ 5/12</p></div>
<ol>
  <li>4と3の最小公倍数 → 12</li>
  <li>3/4 → 9/12、1/3 → 4/12</li>
  <li>9/12 ー 4/12 ＝ 5/12</li>
</ol>

<h2>帯分数のひき算（繰り下がりあり）</h2>
<div class="formula-box"><p>3と1/4 ー 1と3/4 ＝ ?</p></div>
<ol>
  <li>1/4 から 3/4 は引けないので整数部分から1借りる</li>
  <li>3と1/4 → 2と5/4</li>
  <li>2と5/4 ー 1と3/4 ＝ 1と2/4 ＝ 1と1/2</li>
</ol>
<div class="tip-box"><p>💡 帯分数のひき算で「分数部分が引けない場合」は、整数部分から1をくり下げて分数に変換します。</p></div>
<div class="warn-box"><p>⚠️ 答えは必ず約分できるか確認しましょう。2/4は1/2に約分できます。</p></div>""",
    "faq": [
      {"q": "分数のひき算はいつ習いますか？", "a": "同分母は小学3〜4年生で、通分を使う異分母は小学5年生で学習します。"},
      {"q": "帯分数のひき算で繰り下がりが難しい場合は？", "a": "まず仮分数に直してから計算する方法もあります。例えば3と1/4を13/4にしてから計算すると分かりやすいです。"},
      {"q": "通分した後に約分が必要ですか？", "a": "必要な場合があります。答えの分子と分母に公約数があれば約分します。最小公倍数で通分すれば約分の手間が減ります。"},
      {"q": "仮分数と帯分数どちらで答えますか？", "a": "小学校では帯分数で答えるのが一般的です。ただし整数になる場合（例：4/4＝1）は整数で答えます。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-tasizan.html", "emoji": "½", "text": "分数のたし算"},
      {"href": "/bunsuu-kakizan.html", "emoji": "½", "text": "分数のかけ算"},
      {"href": "/bunsuu-tsuubun.html", "emoji": "½", "text": "通分のやり方"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "bunsuu-tsuubun.html",
    "title": "通分のやり方プリント【無料】最小公倍数の使い方｜小学5年生",
    "description": "通分（分母をそろえる方法）を印刷不要・スマホで練習できる無料プリント。最小公倍数の求め方から丁寧に解説。小学5年生向け。",
    "h1": "通分のやり方プリント【無料】小学5年生",
    "eyecatch": "½ 通分は異分母分数計算の基本スキル。最小公倍数を使いこなせば分数が得意になります！",
    "body_html": """\
<h2>通分とは？</h2>
<p>分母の違う分数を、同じ分母の分数に直すことです。分数のたし算・ひき算・大小比較で必要になります。</p>

<h2>最小公倍数の求め方</h2>
<p>通分では分母の最小公倍数（LCM）を共通の分母にします。</p>
<div class="formula-box"><p>1/3 と 1/4 を通分する → 最小公倍数は12</p></div>
<ul>
  <li>3の倍数：3, 6, 9, <strong>12</strong>, 15…</li>
  <li>4の倍数：4, 8, <strong>12</strong>, 16…</li>
  <li>最小公倍数＝12</li>
</ul>

<h2>通分の手順</h2>
<ol>
  <li>分母の最小公倍数を求める（例：3と4 → 12）</li>
  <li>各分数の分母を最小公倍数にそろえる</li>
  <li>分母にかけた数と同じ数を分子にもかける</li>
</ol>
<div class="formula-box"><p>1/3 ＝ 4/12　（分母・分子に4をかける）<br>1/4 ＝ 3/12　（分母・分子に3をかける）</p></div>
<div class="tip-box"><p>💡 分母どうしをかけた数（12）を共通分母にする方法もありますが、最小公倍数の方が計算が楽になります。</p></div>

<h2>3つの分数の通分</h2>
<p>1/2、1/3、1/4 を通分する場合は2・3・4の最小公倍数12を使います。</p>
<div class="formula-box"><p>1/2＝6/12　1/3＝4/12　1/4＝3/12</p></div>""",
    "faq": [
      {"q": "通分はいつ習いますか？", "a": "小学5年生で習います。最小公倍数の学習（4年生）が基礎になります。"},
      {"q": "最小公倍数が分からない時は？", "a": "分母どうしをかけた数を共通の分母に使う方法があります（例：3と4なら12）。最小公倍数でなくても通分できますが、約分の手間が増えます。"},
      {"q": "通分と約分の違いは何ですか？", "a": "通分は分母をそろえて大きくする操作、約分は分母と分子を同じ数で割って小さくする操作です。方向が逆です。"},
      {"q": "通分はどんな時に使いますか？", "a": "①異分母の分数のたし算・ひき算、②分数の大小比較の時に使います。分母が違うままでは計算や比較ができません。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-yakubun.html", "emoji": "½", "text": "約分のやり方"},
      {"href": "/bunsuu-tasizan.html", "emoji": "½", "text": "分数のたし算"},
      {"href": "/baisuu-yakusuu.html", "emoji": "🔢", "text": "倍数と約数"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "bunsuu-yakubun.html",
    "title": "約分のやり方プリント【無料】最大公約数の使い方｜小学5年生",
    "description": "約分（分数を簡単にする方法）を印刷不要・スマホで練習できる無料プリント。最大公約数の求め方から丁寧に解説。小学5年生向け。",
    "h1": "約分のやり方プリント【無料】小学5年生",
    "eyecatch": "½ 約分は分数をシンプルにする技術。最大公約数を使いこなせば計算がぐっと楽になります！",
    "body_html": """\
<h2>約分とは？</h2>
<p>分数の分母と分子を同じ数（公約数）で割って、より簡単な形にすることです。</p>
<div class="formula-box"><p>6/8 ÷ 2/2 ＝ 3/4</p></div>
<p>6と8の公約数は2なので、分母・分子をともに2で割ると3/4になります。</p>

<h2>最大公約数（GCD）で一気に約分</h2>
<p>最大公約数で割ると一回で最も簡単な形になります。</p>
<div class="formula-box"><p>12/18 → 12と18のGCDは6 → 12÷6/18÷6 ＝ 2/3</p></div>
<ul>
  <li>12の約数：1, 2, 3, 4, 6, 12</li>
  <li>18の約数：1, 2, 3, 6, 9, 18</li>
  <li>最大公約数＝6</li>
</ul>

<h2>約分のポイント</h2>
<ul>
  <li>分母と分子を<strong>同じ数で割る</strong>（分数の値は変わらない）</li>
  <li>約分できなくなるまで繰り返す</li>
  <li>最大公約数で割ると一度で完成</li>
</ul>
<div class="tip-box"><p>💡 答えを出したら「約分できるかな？」と確認する習慣をつけましょう。</p></div>
<div class="warn-box"><p>⚠️ 分母だけ、または分子だけを割ってはいけません。必ず両方を同じ数で割りましょう。</p></div>""",
    "faq": [
      {"q": "約分はいつ習いますか？", "a": "小学5年生で習います。4年生で習った最大公約数の知識が必要です。"},
      {"q": "最大公約数の求め方は？", "a": "両方の数を割り切れる最大の整数を探します。小さい方の数の約数を大きい順に調べると効率的です。"},
      {"q": "約分を忘れると減点されますか？", "a": "小学校のテストでは約分しない答えは「不正解」になることがあります。分数の答えは必ず既約分数（これ以上約分できない形）にしましょう。"},
      {"q": "「既約分数」とは何ですか？", "a": "分母と分子の公約数が1だけ（GCDが1）の分数です。これ以上約分できない最もシンプルな形です。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-tsuubun.html", "emoji": "½", "text": "通分のやり方"},
      {"href": "/bunsuu-tasizan.html", "emoji": "½", "text": "分数のたし算"},
      {"href": "/baisuu-yakusuu.html", "emoji": "🔢", "text": "倍数と約数"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "bunsuu-kakizan.html",
    "title": "分数のかけ算プリント【無料】整数・分数×分数の計算｜小学6年生",
    "description": "分数のかけ算（分数×整数・分数×分数）を印刷不要・スマホで練習できる無料プリント。途中約分のコツも解説。小学6年生向け。",
    "h1": "分数のかけ算プリント【無料】小学6年生",
    "eyecatch": "½ 分数のかけ算は分子どうし・分母どうしをかけるだけ！途中約分でミスを減らしましょう。",
    "body_html": """\
<h2>分数×分数の計算</h2>
<div class="formula-box"><p>2/3 × 3/4 ＝ (2×3)/(3×4) ＝ 6/12 ＝ 1/2</p></div>
<p>分子どうしをかけて新しい分子、分母どうしをかけて新しい分母にします。</p>

<h2>途中約分（効率アップ）</h2>
<p>かける前に対角線の数で約分すると計算が楽になります。</p>
<div class="formula-box"><p>2/3 × 3/4 → 2と4の公約数2で約分 → 1/3 × 3/2 ＝ 3/6 ＝ 1/2</p></div>
<div class="tip-box"><p>💡 途中約分は「斜めの関係」（一方の分子と他方の分母）で行います。</p></div>

<h2>分数×整数</h2>
<div class="formula-box"><p>2/5 × 3 ＝ (2×3)/5 ＝ 6/5 ＝ 1と1/5</p></div>
<p>整数を「整数/1」の形に直してから計算することもできます。</p>

<h2>3つ以上の分数のかけ算</h2>
<div class="formula-box"><p>1/2 × 2/3 × 3/4 ＝ (1×2×3)/(2×3×4) ＝ 6/24 ＝ 1/4</p></div>
<div class="warn-box"><p>⚠️ 答えは必ず約分して既約分数（または帯分数）にしましょう。</p></div>""",
    "faq": [
      {"q": "分数のかけ算はいつ習いますか？", "a": "小学6年生で学習します。分数のたし算・ひき算（5年生）の後に習います。"},
      {"q": "途中約分はしないといけませんか？", "a": "必須ではありませんが、計算が楽になりミスが減ります。最終的に答えを約分すれば正解になりますが、数が大きくなりすぎる場合は途中約分を活用しましょう。"},
      {"q": "帯分数のかけ算はどうしますか？", "a": "帯分数を仮分数に直してから計算します。例：1と2/3 ＝ 5/3 として計算します。"},
      {"q": "分数×整数と分数÷整数の違いは？", "a": "かけ算は分子にかけます（2/5×3＝6/5）。割り算は分母にかけます（2/5÷3＝2/15）。逆数を使う割り算との違いに注意しましょう。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-warizan.html", "emoji": "½", "text": "分数のわり算"},
      {"href": "/bunsuu-tasizan.html", "emoji": "½", "text": "分数のたし算"},
      {"href": "/bunsuu-yakubun.html", "emoji": "½", "text": "約分のやり方"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  {
    "filename": "bunsuu-warizan.html",
    "title": "分数のわり算プリント【無料】逆数を使った計算｜小学6年生",
    "description": "分数のわり算（逆数のかけ算に直す方法）を印刷不要・スマホで練習できる無料プリント。逆数の意味から丁寧に解説。小学6年生向け。",
    "h1": "分数のわり算プリント【無料】小学6年生",
    "eyecatch": "½ 分数のわり算は「逆数のかけ算」に変えるだけ！この1つのルールを覚えれば全部解けます。",
    "body_html": """\
<h2>逆数とは？</h2>
<p>分母と分子をひっくり返した数が逆数です。かけると1になります。</p>
<div class="formula-box"><p>2/3 の逆数は 3/2　（2/3 × 3/2 ＝ 1）</p></div>

<h2>分数のわり算の解き方</h2>
<p>「÷分数」を「×逆数」に変えるだけです。</p>
<div class="formula-box"><p>2/3 ÷ 4/5 ＝ 2/3 × 5/4 ＝ 10/12 ＝ 5/6</p></div>
<ol>
  <li>割る数（4/5）を逆数（5/4）に変える</li>
  <li>÷を×に変える</li>
  <li>あとはかけ算と同じ</li>
</ol>
<div class="tip-box"><p>💡 「わる」→「ひっくり返してかける」。このルール1つを確実に覚えましょう。</p></div>

<h2>÷整数の場合</h2>
<div class="formula-box"><p>3/4 ÷ 2 ＝ 3/4 × 1/2 ＝ 3/8</p></div>
<p>整数の逆数は「1/整数」です。2の逆数は1/2です。</p>

<h2>よくある間違い</h2>
<ul>
  <li>割られる数（左側）もひっくり返してしまう</li>
  <li>逆数に変えたのに÷のままにしている</li>
  <li>答えの約分を忘れる</li>
</ul>
<div class="warn-box"><p>⚠️ ひっくり返すのは「割る数（右側）だけ」。割られる数はそのままです！</p></div>""",
    "faq": [
      {"q": "分数のわり算はいつ習いますか？", "a": "小学6年生で学習します。分数のかけ算を学んだ後に習います。"},
      {"q": "なぜ逆数をかけるとわり算になるのですか？", "a": "a÷bはa×(1/b)と同じという定義から来ています。小学生には「割ることとひっくり返してかけることは同じ結果になる」と覚えてもらうのが実用的です。"},
      {"q": "整数÷分数はどう計算しますか？", "a": "整数を「整数/1」の形にして、分数の逆数をかけます。例：3÷2/5＝3/1×5/2＝15/2＝7と1/2。"},
      {"q": "帯分数÷帯分数はどうしますか？", "a": "両方の帯分数を仮分数に直してから、逆数のかけ算に変えて計算します。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-kakizan.html", "emoji": "½", "text": "分数のかけ算"},
      {"href": "/bunsuu-hikizan.html", "emoji": "½", "text": "分数のひき算"},
      {"href": "/bunsuu-kiso.html",    "emoji": "½", "text": "分数の基礎"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # 小数
  # ────────────────────────────────
  {
    "filename": "syousuu-tasizan.html",
    "title": "小数のたし算プリント【無料】小数点の位置に注意｜小学4年生",
    "description": "小数のたし算を印刷不要・スマホで練習できる無料プリント。小数点をそろえる方法を丁寧に解説。小学4年生向け。",
    "h1": "小数のたし算プリント【無料】小学4年生",
    "eyecatch": "🔢 小数のたし算は「小数点をそろえる」がすべて。この一点さえ守れば整数の筆算と同じです！",
    "body_html": """\
<h2>小数のたし算の手順</h2>
<p>小数のたし算では、小数点の位置をそろえて縦に書くことが最重要です。</p>
<div class="formula-box"><p>　3.7<br>＋ 1.45<br>──────<br>　5.15</p></div>
<ol>
  <li>小数点の位置をそろえて書く（3.70として書くと分かりやすい）</li>
  <li>小数点以下を右からそろえる（空いた桁は0として計算）</li>
  <li>整数の筆算と同じように一の位から計算</li>
  <li>小数点を真下におろす</li>
</ol>
<div class="tip-box"><p>💡 「3.7を3.70と書く」テクニックを使うと桁がそろって計算ミスが減ります。</p></div>

<h2>小数点のそろえ方</h2>
<ul>
  <li>3.7 と 1.45 → 小数点の位置をそろえると右端がずれる</li>
  <li>3.70 と 1.45 → 右端もそろう（計算しやすい）</li>
</ul>

<h2>よくある間違い</h2>
<ul>
  <li>小数点を右端でそろえてしまう</li>
  <li>答えの小数点を書き忘れる</li>
  <li>0を補わずに位がずれる</li>
</ul>
<div class="warn-box"><p>⚠️ 答えの小数点を忘れずに！「5.15」→「515」にならないよう注意。</p></div>""",
    "faq": [
      {"q": "小数のたし算はいつ習いますか？", "a": "小学3〜4年生で学習します。3年生で小数の基礎を習い、4年生で小数のたし算・ひき算を学びます。"},
      {"q": "小数点をどうそろえればいいですか？", "a": "整数の部分と小数の部分の境目（小数点）をタテにそろえます。右端ではなく小数点をそろえるのがポイントです。"},
      {"q": "答えの末尾が0になったらどうしますか？", "a": "小数のたし算で末尾が0になった場合は0を消します。例えば3.70は3.7と書きます（ただし途中計算では0を補うのは正しい）。"},
      {"q": "電卓で確認してもいいですか？", "a": "練習問題の確認に使うのは構いません。ただしテストでは使えないので、計算の手順を確実に理解しておきましょう。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/syousuu-hikizan.html","emoji": "🔢", "text": "小数のひき算"},
      {"href": "/syousuu-kakizan.html","emoji": "🔢", "text": "小数のかけ算"},
      {"href": "/syousuu-kiso.html",   "emoji": "🔢", "text": "小数の基礎"},
      {"href": "/grade-4-matome.html", "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "syousuu-hikizan.html",
    "title": "小数のひき算プリント【無料】小数点の位置に注意｜小学4年生",
    "description": "小数のひき算を印刷不要・スマホで練習できる無料プリント。小数点をそろえる方法と繰り下がりを丁寧に解説。小学4年生向け。",
    "h1": "小数のひき算プリント【無料】小学4年生",
    "eyecatch": "🔢 小数のひき算も「小数点をそろえる」がポイント。たし算と同じルールで確実に解けます！",
    "body_html": """\
<h2>小数のひき算の手順</h2>
<div class="formula-box"><p>　5.3<br>ー 2.45<br>──────<br>　2.85</p></div>
<ol>
  <li>小数点の位置をそろえて書く</li>
  <li>5.3 → 5.30 として桁を補う</li>
  <li>右から順に引き算（繰り下がりも整数と同じ）</li>
  <li>小数点を真下におろす</li>
</ol>
<div class="tip-box"><p>💡 5.3 は 5.30 と同じ。末尾に0を補うと計算しやすくなります。</p></div>

<h2>整数から小数を引く</h2>
<div class="formula-box"><p>7 ー 2.3 ＝ 7.0 ー 2.3 ＝ 4.7</p></div>
<p>整数を「整数.0」として小数点をつけてから計算します。</p>

<h2>よくある間違い</h2>
<ul>
  <li>繰り下がりのある計算で間違える</li>
  <li>末尾の0の補い忘れ</li>
  <li>整数から引く時に小数点を忘れる</li>
</ul>
<div class="warn-box"><p>⚠️ 答えの小数点の位置を必ず確認しましょう。検算（答え＋引いた数＝もとの数）も効果的です。</p></div>""",
    "faq": [
      {"q": "小数のひき算で繰り下がりが苦手な場合は？", "a": "整数のひき算の繰り下がりと全く同じです。小数点より右側も左側も、通常の筆算と同じ手順で計算できます。"},
      {"q": "整数から小数を引く時の注意点は？", "a": "整数に小数点と0を補います（例：7を7.0に）。これで小数点をそろえて計算できます。"},
      {"q": "答えの末尾の0はどうしますか？", "a": "小数のひき算で答えの末尾が0になった場合は消します（例：2.50→2.5）。ただし一の位の0は消しません（例：0.5の0は必要）。"},
      {"q": "検算の方法を教えてください。", "a": "「答え＋引いた数＝引かれた数」で確認できます。例：4.7＋2.3＝7.0となれば正解です。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/syousuu-tasizan.html","emoji": "🔢", "text": "小数のたし算"},
      {"href": "/syousuu-kakizan.html","emoji": "🔢", "text": "小数のかけ算"},
      {"href": "/syousuu-kiso.html",   "emoji": "🔢", "text": "小数の基礎"},
      {"href": "/grade-4-matome.html", "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "syousuu-kakizan.html",
    "title": "小数のかけ算プリント【無料】小数点の位置の決め方｜小学5年生",
    "description": "小数のかけ算（小数×整数・小数×小数）を印刷不要・スマホで練習できる無料プリント。小数点の移動のルールをわかりやすく解説。小学5年生向け。",
    "h1": "小数のかけ算プリント【無料】小学5年生",
    "eyecatch": "🔢 小数のかけ算は「小数点の位置」がポイント。桁数の合計分だけ小数点を動かせばOK！",
    "body_html": """\
<h2>小数×整数</h2>
<div class="formula-box"><p>2.4 × 3 ＝ 7.2</p></div>
<p>2.4を24と考えて計算し、最後に小数点を1桁左に動かします。</p>

<h2>小数×小数</h2>
<div class="formula-box"><p>2.4 × 1.5 ＝ 3.60 ＝ 3.6</p></div>
<ol>
  <li>小数点を無視して計算：24 × 15 ＝ 360</li>
  <li>小数点の桁数を数える：2.4（1桁）× 1.5（1桁）＝ 合計2桁</li>
  <li>答えを右から2桁目に小数点を打つ：360 → 3.60 → 3.6</li>
</ol>
<div class="tip-box"><p>💡 「積の小数点の位置＝かける数の小数点以下の桁数の合計」。この法則を覚えましょう。</p></div>

<h2>小数×小数で答えが整数より小さくなる場合</h2>
<p>0.3 × 0.4 ＝ 0.12（1 より小さくなる！）</p>
<p>「かける数が1より小さいと積はかけられる数より小さくなる」という感覚を持ちましょう。</p>
<div class="warn-box"><p>⚠️ 小数のかけ算では答えが元の数より小さくなることがあります（0以上1未満の数をかける場合）。直感と逆なので注意！</p></div>""",
    "faq": [
      {"q": "小数のかけ算はいつ習いますか？", "a": "小学5年生で学習します。4年生で小数のたし算・ひき算を習い、5年生でかけ算・わり算へ進みます。"},
      {"q": "小数点の位置はどう決めますか？", "a": "かけられる数とかける数の小数点以下の桁数を合計した分だけ、積の右から小数点を打ちます。例：1.2×3.4なら1桁＋1桁＝2桁で4.08。"},
      {"q": "0.3×0.4＝0.12で、なぜ小さくなるのですか？", "a": "0.3は「0.1が3つ」、0.4は「0.1が4つ」を表します。細かい単位どうしのかけ算なので、答えがさらに小さくなります。"},
      {"q": "筆算で小数点を間違えないコツは？", "a": "整数として計算した後、最後に小数点を打つ位置を確認する手順を守りましょう。小数点を先に無視して計算するのがポイントです。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/syousuu-warizan.html","emoji": "🔢", "text": "小数のわり算"},
      {"href": "/syousuu-tasizan.html","emoji": "🔢", "text": "小数のたし算"},
      {"href": "/syousuu-kiso.html",   "emoji": "🔢", "text": "小数の基礎"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "syousuu-warizan.html",
    "title": "小数のわり算プリント【無料】商の小数点の求め方｜小学5年生",
    "description": "小数のわり算（小数÷整数・整数÷小数・小数÷小数）を印刷不要・スマホで練習できる無料プリント。小数点の移動のルールをわかりやすく解説。小学5年生向け。",
    "h1": "小数のわり算プリント【無料】小学5年生",
    "eyecatch": "🔢 小数のわり算は「割る数を整数にする」がコツ。小数点を移動させる方法をマスターしましょう！",
    "body_html": """\
<h2>小数÷整数（基本）</h2>
<div class="formula-box"><p>7.2 ÷ 3 ＝ 2.4</p></div>
<p>筆算では割られる数の小数点の真上に商の小数点を置きます。</p>

<h2>整数÷小数・小数÷小数（割る数を整数に変換）</h2>
<div class="formula-box"><p>6 ÷ 0.3 ＝ 60 ÷ 3 ＝ 20</p></div>
<ol>
  <li>割る数（0.3）の小数点を右に1桁移動して整数にする</li>
  <li>割られる数（6）も同じだけ（1桁）右に移動：60</li>
  <li>60 ÷ 3 ＝ 20 を計算</li>
</ol>
<div class="tip-box"><p>💡 「割る数と割られる数を同じ倍数にしても商は変わらない」という性質を使います。</p></div>

<h2>割り切れない場合</h2>
<p>小数のわり算は割り切れないことがあります。問題の指示に従い「四捨五入して〇の位まで求める」場合は1桁多く計算してから四捨五入します。</p>

<h2>よくある間違い</h2>
<ul>
  <li>商の小数点の位置を間違える</li>
  <li>割られる数だけ（または割る数だけ）小数点を移動する</li>
</ul>
<div class="warn-box"><p>⚠️ 小数点は割る数と割られる数を「両方とも同じ桁数」移動させます。片方だけ動かすと商が変わってしまいます。</p></div>""",
    "faq": [
      {"q": "小数のわり算はいつ習いますか？", "a": "小学5年生で学習します。小数のかけ算と同じ学期に習うことが多いです。"},
      {"q": "6÷0.3＝20なのはなぜですか？", "a": "両方に10をかけて60÷3にしても商は変わりません（わり算の性質）。0.3を整数の3にするため10倍し、6も同じく10倍して60にします。"},
      {"q": "商の小数点はどこに打ちますか？", "a": "割られる数の小数点を移動した後の位置の真上に打ちます。割る数を整数にした後の筆算で、割られる数の小数点の真上が商の小数点の位置になります。"},
      {"q": "割り切れない場合はどうしますか？", "a": "問題の指示に従います。「上から2桁」や「小数第一位まで」などの指示がある場合は1桁多く計算して四捨五入します。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/syousuu-kakizan.html","emoji": "🔢", "text": "小数のかけ算"},
      {"href": "/syousuu-tasizan.html","emoji": "🔢", "text": "小数のたし算"},
      {"href": "/syousuu-kiso.html",   "emoji": "🔢", "text": "小数の基礎"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # 面積（追加）
  # ────────────────────────────────
  {
    "filename": "menseki-sankakukei.html",
    "title": "三角形の面積プリント【無料】公式と求め方｜小学5年生",
    "description": "三角形の面積（底辺×高さ÷2）を印刷不要・スマホで練習できる無料プリント。高さの見つけ方や鈍角三角形の求め方も解説。小学5年生向け。",
    "h1": "三角形の面積プリント【無料】小学5年生",
    "eyecatch": "📐 三角形の面積は「底辺×高さ÷2」。高さの見つけ方が分かれば全部解けます！",
    "body_html": """\
<h2>三角形の面積の公式</h2>
<div class="formula-box"><p>三角形の面積 ＝ 底辺 × 高さ ÷ 2</p></div>
<p>長方形の半分が三角形、という考え方から「÷2」します。</p>

<h2>高さの見つけ方</h2>
<ul>
  <li><strong>直角三角形：</strong>直角の2辺のどちらかが底辺で、もう一方が高さ</li>
  <li><strong>鋭角三角形：</strong>底辺に対して垂直に引いた線が高さ（三角形の中にある）</li>
  <li><strong>鈍角三角形：</strong>底辺を延長した線に垂直に引いた線が高さ（三角形の外に出ることがある）</li>
</ul>
<div class="tip-box"><p>💡 「高さ」は必ず底辺に対して垂直（90°）な長さです。斜めの辺は高さではありません。</p></div>

<h2>よくある間違い</h2>
<ul>
  <li>斜めの辺を高さだと間違える</li>
  <li>÷2を忘れる</li>
  <li>鈍角三角形で高さの位置が分からない</li>
</ul>
<div class="warn-box"><p>⚠️ 高さは必ず底辺に対して直角に引いた線の長さ。問題によっては図の外に高さが出ることもあります。</p></div>""",
    "faq": [
      {"q": "三角形の面積はいつ習いますか？", "a": "小学5年生で学習します。平行四辺形の面積と一緒に学ぶことが多いです。"},
      {"q": "三角形の面積が「底辺×高さ÷2」になるのはなぜですか？", "a": "三角形は同じ形の三角形を2つ組み合わせると平行四辺形になります。平行四辺形の面積（底辺×高さ）の半分なので÷2します。"},
      {"q": "鈍角三角形の高さはどう求めますか？", "a": "底辺の延長線上に垂線を引き、その垂線の長さが高さです。図形の外に高さが出る場合があります。"},
      {"q": "底辺は3辺のどれを使っても良いですか？", "a": "はい、どの辺を底辺にしても答えは同じです。ただし底辺に対応する高さを使わないといけません。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/menseki-heikoushikakkei.html","emoji": "📐", "text": "平行四辺形の面積"},
      {"href": "/menseki-enza.html",            "emoji": "📐", "text": "円の面積"},
      {"href": "/grade-5-matome.html",          "emoji": "📚", "text": "5年生 全単元まとめ"},
      {"href": "/suichoku-heiko.html",          "emoji": "📐", "text": "垂直・平行と四角形"},
    ],
  },

  {
    "filename": "menseki-heikoushikakkei.html",
    "title": "平行四辺形の面積プリント【無料】底辺×高さの求め方｜小学5年生",
    "description": "平行四辺形の面積（底辺×高さ）を印刷不要・スマホで練習できる無料プリント。高さの見つけ方を丁寧に解説。小学5年生向け。",
    "h1": "平行四辺形の面積プリント【無料】小学5年生",
    "eyecatch": "📐 平行四辺形の面積は「底辺×高さ」。長方形と同じ公式で求められます！",
    "body_html": """\
<h2>平行四辺形の面積の公式</h2>
<div class="formula-box"><p>平行四辺形の面積 ＝ 底辺 × 高さ</p></div>
<p>平行四辺形を切って並べ替えると長方形になります。だから長方形と同じ「たて×よこ（底辺×高さ）」で求められます。</p>

<h2>高さの見つけ方</h2>
<ul>
  <li>高さは底辺に対して垂直（90°）な長さ</li>
  <li>斜めの辺（＝高さではない）と混同しないこと</li>
  <li>図の中に点線で書かれている場合が多い</li>
</ul>
<div class="tip-box"><p>💡 平行四辺形の「斜めの辺」を高さにしてしまうミスが多発。高さは必ず底辺への垂線です。</p></div>

<h2>底辺と高さの対応</h2>
<p>向かい合う辺（底辺）が変われば、それに対応する高さも変わります。どの辺を底辺にしても面積は同じです。</p>

<h2>よくある間違い</h2>
<ul>
  <li>斜辺を高さとして使う</li>
  <li>三角形の公式（÷2）を使ってしまう</li>
</ul>
<div class="warn-box"><p>⚠️ 三角形と混合しないように。平行四辺形は÷2しません！</p></div>""",
    "faq": [
      {"q": "平行四辺形の面積はいつ習いますか？", "a": "小学5年生で習います。三角形・ひし形・台形の面積と一緒に学びます。"},
      {"q": "平行四辺形の面積が「底辺×高さ」になる理由は？", "a": "平行四辺形の一部を切り取って反対側に移動すると長方形になります。面積は変わらないので、長方形と同じ公式が使えます。"},
      {"q": "斜辺と高さはなぜ違うのですか？", "a": "高さは底辺に対して垂直（直角）な距離です。斜辺は傾いているため、必ず高さより長くなります。"},
      {"q": "どの辺を底辺にしてもいいですか？", "a": "はい、どの辺を底辺にしても面積は同じになります。ただし使う底辺に対応した高さを使う必要があります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/menseki-sankakukei.html","emoji": "📐", "text": "三角形の面積"},
      {"href": "/menseki-enza.html",       "emoji": "📐", "text": "円の面積"},
      {"href": "/suichoku-heiko.html",     "emoji": "📐", "text": "垂直・平行と四角形"},
      {"href": "/grade-5-matome.html",     "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "menseki-enza.html",
    "title": "円の面積プリント【無料】半径×半径×3.14の求め方｜小学6年生",
    "description": "円の面積（半径×半径×3.14）を印刷不要・スマホで練習できる無料プリント。公式の意味から半円・おうぎ形まで丁寧に解説。小学6年生向け。",
    "h1": "円の面積プリント【無料】小学6年生",
    "eyecatch": "⭕ 円の面積は「半径×半径×3.14」。この公式を覚えて複合図形も解いてみよう！",
    "body_html": """\
<h2>円の面積の公式</h2>
<div class="formula-box"><p>円の面積 ＝ 半径 × 半径 × 3.14（π）</p></div>
<p>3.14は円周率（π＝3.14159…）を小学校では3.14として使います。</p>

<h2>直径が与えられた場合</h2>
<p>直径が8cmなら半径は4cm。まず半径を求めてから公式に代入します。</p>
<div class="formula-box"><p>半径 ＝ 直径 ÷ 2</p></div>

<h2>よく出る問題</h2>
<ul>
  <li><strong>半円の面積：</strong>円の面積 ÷ 2</li>
  <li><strong>1/4の円（おうぎ形）：</strong>円の面積 ÷ 4</li>
  <li><strong>複合図形：</strong>正方形 ー 円の部分（または＋）で求める</li>
</ul>
<div class="tip-box"><p>💡 3.14との計算は先に整数部分を計算してから3.14をかけると楽になります（先に3.14をかけると小数が入り複雑になる）。</p></div>

<h2>よくある間違い</h2>
<ul>
  <li>直径を半径と間違える（直径×直径×3.14にしてしまう）</li>
  <li>3.14との計算ミス</li>
  <li>公式に当てはめる前に半径を求め忘れる</li>
</ul>
<div class="warn-box"><p>⚠️ 「半径×半径」であって「直径×直径」ではありません。問題をよく読んで直径か半径かを確認しましょう。</p></div>""",
    "faq": [
      {"q": "円の面積はいつ習いますか？", "a": "小学6年生で学習します。円周・直径・半径・円周率の復習から入ります。"},
      {"q": "なぜ半径×半径×3.14なのですか？", "a": "円周率π（≒3.14）はπ×r²（rは半径）という公式で求められます。小学校ではπ＝3.14として計算します。"},
      {"q": "3.14を使った計算のコツは？", "a": "3.14×整数の計算は覚えておくと便利です（3.14×2＝6.28、×3＝9.42、×4＝12.56など）。また先に整数の計算をして最後に3.14をかける順番にすると楽です。"},
      {"q": "おうぎ形の面積の求め方は？", "a": "おうぎ形は円の一部です。面積＝円の面積×（中心角÷360）で求めます。中心角が90°なら円の面積×1/4です。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/menseki-sankakukei.html",     "emoji": "📐", "text": "三角形の面積"},
      {"href": "/menseki-heikoushikakkei.html","emoji": "📐", "text": "平行四辺形の面積"},
      {"href": "/grade-6-matome.html",         "emoji": "📚", "text": "6年生 全単元まとめ"},
      {"href": "/kakudai-shukuzu.html",        "emoji": "📐", "text": "拡大図・縮図"},
    ],
  },

  # ────────────────────────────────
  # 体積
  # ────────────────────────────────
  {
    "filename": "taiseki-kiso.html",
    "title": "体積の基礎プリント【無料】直方体・立方体の求め方｜小学5年生",
    "description": "体積の基礎（直方体・立方体の体積）を印刷不要・スマホで練習できる無料プリント。体積の意味と公式をわかりやすく解説。小学5年生向け。",
    "h1": "体積の基礎プリント【無料】小学5年生",
    "eyecatch": "📦 体積は「空間の大きさ」を表す量。直方体・立方体の公式をマスターして立体問題に強くなろう！",
    "body_html": """\
<h2>体積とは？</h2>
<p>体積とは立体が占める空間の大きさです。単位は cm³（立方センチメートル）や m³（立方メートル）です。</p>
<p>1cm³ ＝ 1辺が1cmの立方体の体積です。</p>

<h2>直方体の体積の公式</h2>
<div class="formula-box"><p>直方体の体積 ＝ たて × よこ × 高さ</p></div>
<p>例：たて3cm、よこ4cm、高さ5cmの直方体 → 3×4×5＝60cm³</p>

<h2>立方体の体積の公式</h2>
<div class="formula-box"><p>立方体の体積 ＝ 一辺 × 一辺 × 一辺</p></div>
<p>例：1辺が4cmの立方体 → 4×4×4＝64cm³</p>
<div class="tip-box"><p>💡 立方体は直方体の特別な形（たて＝よこ＝高さ）。どちらも「3辺をかける」という考え方は同じです。</p></div>

<h2>体積の単位換算</h2>
<ul>
  <li>1L ＝ 1000cm³（1辺10cmの立方体の体積）</li>
  <li>1m³ ＝ 1000000cm³ ＝ 1000L</li>
</ul>

<h2>よくある間違い</h2>
<ul>
  <li>面積（2次元）と体積（3次元）を混同する</li>
  <li>3辺ではなく2辺だけかける</li>
  <li>単位をcm²と書いてしまう（体積はcm³）</li>
</ul>
<div class="warn-box"><p>⚠️ 体積の単位は cm³（立方センチメートル）。面積のcm²（平方センチメートル）と混同しないように！</p></div>""",
    "faq": [
      {"q": "体積はいつ習いますか？", "a": "小学5年生で学習します。直方体・立方体の体積と体積の単位（L・cm³・m³）を学びます。"},
      {"q": "面積と体積の違いは何ですか？", "a": "面積は「平面の広さ」（2次元）、体積は「立体の大きさ」（3次元）です。面積は2辺のかけ算、体積は3辺のかけ算で求めます。単位も面積はcm²、体積はcm³と異なります。"},
      {"q": "1L は何cm³ ですか？", "a": "1L＝1000cm³です。1辺が10cmの立方体の体積が1Lになります。日常の液体の量（ジュースのパックなど）と関連させると覚えやすいです。"},
      {"q": "L字型など複雑な立体の体積はどう求めますか？", "a": "2つの直方体に分けて、それぞれの体積を足し合わせます。または大きい直方体から引き算する方法もあります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/mizu-no-kasa.html",   "emoji": "🧪", "text": "水のかさの単位換算"},
      {"href": "/tani-nagasa.html",    "emoji": "📏", "text": "長さの単位換算"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
      {"href": "/heikin-guide.html",   "emoji": "📊", "text": "平均の求め方"},
    ],
  },

  # ────────────────────────────────
  # 時間
  # ────────────────────────────────
  {
    "filename": "jikan-yomikata.html",
    "title": "時計の読み方プリント【無料】アナログ時計の見方｜小学1〜2年生",
    "description": "アナログ時計の読み方を印刷不要・スマホで練習できる無料プリント。長針・短針の意味から「〇時〇分」の読み方まで丁寧に解説。小学1〜2年生向け。",
    "h1": "時計の読み方プリント【無料】小学1〜2年生",
    "eyecatch": "🕐 時計が読めると生活が便利になります。長針・短針の見方をゼロから学んでいきましょう！",
    "body_html": """\
<h2>時計の2本の針</h2>
<ul>
  <li><strong>短い針（時針）：</strong>「〇時」を表す。1周すると12時間</li>
  <li><strong>長い針（分針）：</strong>「〇分」を表す。1周すると60分（1時間）</li>
</ul>
<div class="tip-box"><p>💡 「短い針が時、長い針が分」。「時間は短く（数が少ない）、分は長く（数が多い）」と覚えると分かりやすいです。</p></div>

<h2>分針の読み方</h2>
<p>長針が指す数字×5が「〇分」です。</p>
<ul>
  <li>12を指す → 0分（ちょうど）</li>
  <li>1を指す → 5分</li>
  <li>3を指す → 15分（15分＝1/4時間）</li>
  <li>6を指す → 30分（30分＝半時間）</li>
  <li>9を指す → 45分（45分＝3/4時間）</li>
</ul>

<h2>ステップアップ</h2>
<ol>
  <li>まず「〇時ちょうど」を読めるようにする</li>
  <li>「〇時30分」「〇時15分」など切りのいい時刻を覚える</li>
  <li>「〇時〇分」を分単位で読めるようにする</li>
</ol>
<div class="warn-box"><p>⚠️ 「11時55分」などは短針が12のすぐ手前にあり、12時と間違えやすい。短針が「11と12の間」にあれば11時です。</p></div>""",
    "faq": [
      {"q": "時計の読み方はいつ習いますか？", "a": "小学1年生で「〇時・〇時半」を習い、小学2年生で「〇時〇分」を習います。"},
      {"q": "子どもが時計を読めるようにするには？", "a": "まず「ちょうど」の時刻（3時、6時など）から始め、30分→15分→5分単位→1分単位と段階的に練習します。実物の時計を使った練習が最も効果的です。"},
      {"q": "デジタル時計と何が違いますか？", "a": "デジタルは数字をそのまま読むだけですが、アナログ時計は針の位置から時刻を読み取ります。アナログを読めると時間の流れ（経過）が視覚的に分かりやすくなります。"},
      {"q": "「午前・午後」は何年生で習いますか？", "a": "小学2年生で習います。1日＝24時間、午前12時間＋午後12時間の概念を学びます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/jikan-keisan.html",   "emoji": "⏱️", "text": "時間の計算"},
      {"href": "/jikan-henkan.html",   "emoji": "⏱️", "text": "時間の単位換算"},
      {"href": "/grade-1-matome.html", "emoji": "📚", "text": "1年生 全単元まとめ"},
      {"href": "/grade-2-matome.html", "emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },

  {
    "filename": "jikan-keisan.html",
    "title": "時間の計算プリント【無料】経過時間・終了時刻の求め方｜小学3年生",
    "description": "時間の計算（経過時間・終了時刻の求め方）を印刷不要・スマホで練習できる無料プリント。60進法の考え方をわかりやすく解説。小学3年生向け。",
    "h1": "時間の計算プリント【無料】小学3年生",
    "eyecatch": "⏱️ 時間の計算は「60進法」という特別なルールがあります。コツを覚えれば簡単に解けます！",
    "body_html": """\
<h2>時間の計算の特別ルール（60進法）</h2>
<p>時間の計算は「60になったら1繰り上げる」60進法を使います。</p>
<div class="formula-box"><p>60分 ＝ 1時間　／　60秒 ＝ 1分</p></div>

<h2>終了時刻を求める（たし算）</h2>
<div class="formula-box"><p>2時40分 ＋ 50分 ＝ 3時30分</p></div>
<ol>
  <li>分を足す：40＋50＝90分</li>
  <li>90分 ＝ 1時間30分 に変換</li>
  <li>時間に1を足す：2＋1＝3時間</li>
  <li>答え：3時30分</li>
</ol>

<h2>経過時間を求める（ひき算）</h2>
<div class="formula-box"><p>4時10分 ー 1時50分 ＝ 2時間20分</p></div>
<ol>
  <li>分を引く：10－50は引けない → 1時間（60分）借りる</li>
  <li>70分 ー 50分 ＝ 20分</li>
  <li>時間：（4－1）－1（借りた）＝ 2時間</li>
  <li>答え：2時間20分</li>
</ol>
<div class="tip-box"><p>💡 数直線（タイムライン）を書いて、きりのいい時刻を経由して計算するとミスが減ります。</p></div>
<div class="warn-box"><p>⚠️ 普通の計算と違い「60で繰り上げ・繰り下げ」することを忘れずに。50＋50＝100分ではなく1時間40分です。</p></div>""",
    "faq": [
      {"q": "時間の計算はいつ習いますか？", "a": "小学3年生で学習します。時刻の読み方（1〜2年生）の後に、時間の計算（足し算・引き算）を学びます。"},
      {"q": "時間の計算で繰り上がり・繰り下がりが難しい場合は？", "a": "数直線（タイムライン）を書く方法が効果的です。開始時刻から「ちょうどの時刻（○時ちょうど）」を経由して終了時刻まで足していく方法です。"},
      {"q": "「2時間30分＋1時間50分」はどう計算しますか？", "a": "まず分を足します：30＋50＝80分＝1時間20分。次に時間：2＋1＋1（繰り上がり）＝4時間。答えは4時間20分です。"},
      {"q": "秒の計算も同じですか？", "a": "はい、秒も60秒＝1分という60進法です。同じように60で繰り上げ・繰り下げをします。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/jikan-yomikata.html", "emoji": "🕐", "text": "時計の読み方"},
      {"href": "/jikan-henkan.html",   "emoji": "⏱️", "text": "時間の単位換算"},
      {"href": "/mondai-sokudo.html",  "emoji": "📝", "text": "速さの文章題"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "jikan-henkan.html",
    "title": "時間の単位換算プリント【無料】時間・分・秒の変換｜小学3年生",
    "description": "時間の単位換算（時間・分・秒）を印刷不要・スマホで練習できる無料プリント。60進法による換算方法をわかりやすく解説。小学3年生向け。",
    "h1": "時間の単位換算プリント【無料】小学3年生",
    "eyecatch": "⏱️ 時間の単位は「60進法」の特別なルール。1時間＝60分・1分＝60秒をしっかり覚えましょう！",
    "body_html": """\
<h2>時間の単位の関係</h2>
<div class="formula-box"><p>1時間 ＝ 60分　／　1分 ＝ 60秒　／　1時間 ＝ 3600秒</p></div>

<h2>時間→分への換算</h2>
<div class="formula-box"><p>2時間30分 ＝ 2×60＋30 ＝ 150分</p></div>
<ul>
  <li>時間 → 分：×60</li>
  <li>分 → 時間：÷60（あまりが「分」）</li>
</ul>

<h2>分→秒への換算</h2>
<div class="formula-box"><p>3分20秒 ＝ 3×60＋20 ＝ 200秒</p></div>
<ul>
  <li>分 → 秒：×60</li>
  <li>秒 → 分：÷60（あまりが「秒」）</li>
</ul>
<div class="tip-box"><p>💡 1時間半＝90分、2時間15分＝135分など、よく使う換算を暗記しておくと便利です。</p></div>

<h2>よく出る換算問題</h2>
<ul>
  <li>1時間30分 ＝ □分</li>
  <li>90分 ＝ □時間□分</li>
  <li>2分30秒 ＝ □秒</li>
  <li>150秒 ＝ □分□秒</li>
</ul>
<div class="warn-box"><p>⚠️ 時間の換算は10進法ではなく60進法。「1時間＝100分」などの間違いに注意！</p></div>""",
    "faq": [
      {"q": "時間の単位換算はいつ習いますか？", "a": "小学3年生で学習します。時計の読み方（1〜2年生）の後に習います。"},
      {"q": "なぜ時間は60進法なのですか？", "a": "古代バビロニアの60進数の数体系に由来します。60は2・3・4・5・6など多くの数で割り切れるため便利で、時間の単位として使われ続けています。"},
      {"q": "150分は何時間何分ですか？", "a": "150÷60＝2あまり30、なので2時間30分です。150÷60の計算は「60×2＝120、150－120＝30」と考えます。"},
      {"q": "速さの問題でも時間換算が必要ですか？", "a": "はい、速さの問題では「分速→時速」などの換算が必要になることがあります。時間の換算を確実に覚えておくと速さの問題も解きやすくなります。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/jikan-yomikata.html", "emoji": "🕐", "text": "時計の読み方"},
      {"href": "/jikan-keisan.html",   "emoji": "⏱️", "text": "時間の計算"},
      {"href": "/tani-nagasa.html",    "emoji": "📏", "text": "長さの単位換算"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },


  # ────────────────────────────────
  # 文章題
  # ────────────────────────────────
  {
    "filename": "mondai-hikizan.html",
    "title": "引き算の文章題プリント【無料】小学1〜2年生",
    "description": "引き算の文章題を印刷不要・スマホで練習できる無料プリント。求残・求差の2つのパターンをわかりやすく解説。小学1〜2年生向け。",
    "h1": "引き算の文章題プリント【無料】小学1〜2年生",
    "eyecatch": "➖ 引き算の文章題は「残りはいくつ？」「どちらが多い？」の2パターン。読み取り方を練習しましょう！",
    "body_html": """\
<h2>引き算文章題の2つのパターン</h2>
<h3>①残りを求める（求残）</h3>
<p>「8個あって3個食べた。残りは何個？」→ 8－3＝5</p>
<div class="tip-box"><p>💡 キーワード：「食べた」「なくなった」「使った」→引き算</p></div>
<h3>②違いを求める（求差）</h3>
<p>「Aさんは9個、Bさんは5個。何個多い？」→ 9－5＝4</p>
<div class="tip-box"><p>💡 キーワード：「何個多い？」「どちらが多い？」→引き算（大きい数－小さい数）</p></div>
<h2>文章題の解き方ステップ</h2>
<ol>
  <li>問題文を読んで「何を求めるか」確認</li>
  <li>数字を書き出す</li>
  <li>たし算か引き算かを判断</li>
  <li>式を書いて計算</li>
  <li>答えに単位を書く</li>
</ol>
<div class="warn-box"><p>⚠️ 答えには必ず単位（個・本・枚など）をつけましょう。</p></div>""",
    "faq": [
      {"q": "引き算の文章題が苦手な場合は？", "a": "絵や図を書いて場面を可視化することが効果的です。「取り去る」「比べる」どちらの場面かを確認しましょう。"},
      {"q": "たし算か引き算か迷う場合は？", "a": "「増える・合わせる」はたし算、「減る・残り・違い」は引き算が目安です。"},
      {"q": "2年生の引き算文章題はどう変わりますか？", "a": "2桁の数や繰り下がりのある計算が登場します。考え方は1年生と同じです。"},
      {"q": "単位を書き忘れたら減点されますか？", "a": "はい、小学校のテストでは単位の記載が必要です。習慣として式の後に単位を確認しましょう。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/mondai-tasizan.html", "emoji": "📝", "text": "足し算の文章題"},
      {"href": "/hikizan-kiso.html",   "emoji": "➖", "text": "引き算の基礎"},
      {"href": "/kongozan.html",       "emoji": "🔢", "text": "混合計算"},
      {"href": "/grade-1-matome.html", "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  {
    "filename": "mondai-jikan.html",
    "title": "時間の文章題プリント【無料】経過時間・時刻の計算｜小学3年生",
    "description": "時間の文章題（経過時間・終了時刻）を印刷不要・スマホで練習できる無料プリント。60進法の文章題をわかりやすく解説。小学3年生向け。",
    "h1": "時間の文章題プリント【無料】小学3年生",
    "eyecatch": "⏱️ 時間の文章題は「60進法」のルールが肝心。タイムラインを書いて確実に解きましょう！",
    "body_html": """\
<h2>よく出る時間の文章題パターン</h2>
<h3>①終了時刻を求める</h3>
<p>「10時30分から1時間20分後は何時？」</p>
<p>10時30分 ＋ 1時間20分 ＝ 11時50分</p>
<h3>②開始時刻を求める</h3>
<p>「3時15分の40分前は何時？」</p>
<p>3時15分 ー 40分 ＝ 2時35分</p>
<h3>③経過時間を求める</h3>
<p>「9時20分から11時10分まで何時間何分？」</p>
<p>9時20分 → 10時（40分）→ 11時10分（1時間10分）＝ 1時間50分</p>
<div class="tip-box"><p>💡 タイムラインを書いて「きりのいい時刻」を経由すると計算ミスが減ります。</p></div>
<h2>答えの確認</h2>
<ul>
  <li>時刻が0〜59分の範囲か確認</li>
  <li>「何時間何分」と「何分」の書き分けに注意</li>
</ul>""",
    "faq": [
      {"q": "時間の文章題でよくある間違いは？", "a": "分が60以上になっても「60で繰り上げる」を忘れるケースです。70分と書かず1時間10分に直しましょう。"},
      {"q": "「前」「後」の言葉の意味は？", "a": "「〇分後」はたし算、「〇分前」は引き算です。問題文のキーワードを確認しましょう。"},
      {"q": "経過時間の求め方で楽な方法は？", "a": "「きりのいい時刻（〇時ちょうど）」を経由して足していく方法が間違いが少なくておすすめです。"},
      {"q": "速さの問題と時間の計算は関係しますか？", "a": "はい、速さ・時間・距離の問題では時間の計算が必須です。時間の計算を確実にしておきましょう。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/jikan-keisan.html",   "emoji": "⏱️", "text": "時間の計算"},
      {"href": "/jikan-henkan.html",   "emoji": "⏱️", "text": "時間の単位換算"},
      {"href": "/mondai-sokudo.html",  "emoji": "📝", "text": "速さの文章題"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "mondai-menseki.html",
    "title": "面積の文章題プリント【無料】公式を使った応用問題｜小学4〜5年生",
    "description": "面積の文章題を印刷不要・スマホで練習できる無料プリント。長方形・三角形・円の面積を使った応用問題を解説。小学4〜5年生向け。",
    "h1": "面積の文章題プリント【無料】小学4〜5年生",
    "eyecatch": "📐 面積の文章題は「公式選び」がポイント。図を描いて形を確認してから解きましょう！",
    "body_html": """\
<h2>面積の公式まとめ</h2>
<ul>
  <li>長方形：たて × よこ</li>
  <li>正方形：一辺 × 一辺</li>
  <li>三角形：底辺 × 高さ ÷ 2</li>
  <li>平行四辺形：底辺 × 高さ</li>
  <li>円：半径 × 半径 × 3.14</li>
</ul>
<h2>文章題の解き方</h2>
<ol>
  <li>どんな形か図を描く</li>
  <li>与えられた数値を図に書き込む</li>
  <li>公式を選んで計算</li>
  <li>単位（cm²・m²）をつける</li>
</ol>
<div class="tip-box"><p>💡 複合図形は「大きい形から小さい形を引く」か「複数の形に分けて足す」の2通りで解けます。</p></div>
<h2>よく出る文章題パターン</h2>
<ul>
  <li>「畑の面積は何m²？」→長方形の公式</li>
  <li>「花壇を除いた庭の面積は？」→大きい長方形－小さい長方形</li>
  <li>「半円の面積は？」→円の面積÷2</li>
</ul>
<div class="warn-box"><p>⚠️ 単位に注意！cm×cmはcm²、m×mはm²。異なる単位が混在する場合は統一してから計算。</p></div>""",
    "faq": [
      {"q": "面積の文章題で間違いやすい点は？", "a": "単位の変換忘れと、複合図形で「引く」か「足す」かの判断ミスが多いです。必ず図を描いて確認しましょう。"},
      {"q": "単位をm²にするにはどうすれば？", "a": "問題の数値がcmで与えられている場合はcm²で計算し、必要に応じてm²に変換します（10000cm²＝1m²）。"},
      {"q": "複合図形はどうやって解きますか？", "a": "①知っている形に分けて合計する ②大きい形から余分な部分を引く、の2方法があります。図を描いてどちらが簡単か判断しましょう。"},
      {"q": "テストで図を描く必要がありますか？", "a": "必須ではありませんが、描くと間違いが減ります。特に複合図形や問題文だけでは分かりにくい場合は必ず描きましょう。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/menseki-sankakukei.html",     "emoji": "📐", "text": "三角形の面積"},
      {"href": "/menseki-heikoushikakkei.html","emoji": "📐", "text": "平行四辺形の面積"},
      {"href": "/menseki-enza.html",            "emoji": "📐", "text": "円の面積"},
      {"href": "/grade-5-matome.html",          "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "mondai-nagasa.html",
    "title": "長さの文章題プリント【無料】単位換算を使った計算｜小学3年生",
    "description": "長さの文章題（mm・cm・m・kmを使った計算）を印刷不要・スマホで練習できる無料プリント。単位をそろえる方法を解説。小学3年生向け。",
    "h1": "長さの文章題プリント【無料】小学3年生",
    "eyecatch": "📏 長さの文章題は「単位をそろえる」がポイント。バラバラな単位をそろえてから計算しましょう！",
    "body_html": """\
<h2>長さの文章題の基本ルール</h2>
<p>異なる単位が出てきたら、まず同じ単位にそろえてから計算します。</p>
<div class="formula-box"><p>10mm＝1cm　100cm＝1m　1000m＝1km</p></div>
<h2>よく出るパターン</h2>
<h3>①単位をそろえて足す・引く</h3>
<p>「2m30cmのテープと75cmのテープを合わせると何cm？」</p>
<p>2m30cm＝230cm　230＋75＝305cm</p>
<h3>②道のりの問題</h3>
<p>「学校から駅まで1.2km。そのうち600m歩いた。残りは何m？」</p>
<p>1.2km＝1200m　1200－600＝600m</p>
<div class="tip-box"><p>💡 先に単位を統一（どれか一つに合わせる）してから計算する習慣をつけましょう。</p></div>
<h2>間違いやすいポイント</h2>
<ul>
  <li>2m30cmを2.30mと書いて小数として扱うミス</li>
  <li>kmとmを混在させたまま計算する</li>
</ul>
<div class="warn-box"><p>⚠️ 単位換算を先に済ませることが正解への近道です。</p></div>""",
    "faq": [
      {"q": "長さの文章題はいつ習いますか？", "a": "小学3年生で本格的に学習します。mm・cm・m・kmを使った計算や単位換算が含まれます。"},
      {"q": "2m30cmを単一の単位に直すには？", "a": "cm単位なら：2×100＋30＝230cm。m単位なら：2.3m（小数）。どちらでも計算できますが、整数の方が間違いが少ないです。"},
      {"q": "kmを使った問題は何年生ですか？", "a": "小学3年生でkmを習います。「1km＝1000m」を使った換算問題が出てきます。"},
      {"q": "道のりと距離の違いは？", "a": "道のりは実際に歩いたルートの長さ、距離（直線距離）は2点間を直線で結んだ長さです。地図上の問題では区別が必要です。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/tani-nagasa.html",    "emoji": "📏", "text": "長さの単位換算"},
      {"href": "/mondai-tasizan.html", "emoji": "📝", "text": "足し算の文章題"},
      {"href": "/mondai-jikan.html",   "emoji": "📝", "text": "時間の文章題"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "mondai-bunsuu.html",
    "title": "分数の文章題プリント【無料】通分・計算を使った応用問題｜小学5年生",
    "description": "分数の文章題を印刷不要・スマホで練習できる無料プリント。通分・分数のたし算ひき算を使った文章題を解説。小学5年生向け。",
    "h1": "分数の文章題プリント【無料】小学5年生",
    "eyecatch": "½ 分数の文章題は「何を求めるか」を確認してから式を立てることが大切です！",
    "body_html": """\
<h2>よく出る分数文章題のパターン</h2>
<h3>①残り・合計を求める</h3>
<p>「ジュースが3/4L あって1/3L 飲んだ。残りは？」</p>
<p>3/4 ー 1/3 ＝ 9/12 ー 4/12 ＝ 5/12 L</p>
<h3>②「〇の何分の一」を求める</h3>
<p>「12個の2/3は何個？」</p>
<p>12 × 2/3 ＝ 8個</p>
<div class="tip-box"><p>💡 「〇の□分の1」はかけ算。「□分の1 が○個で全体は？」はわり算で解きます。</p></div>
<h2>文章題の手順</h2>
<ol>
  <li>単位（Lや個）を確認</li>
  <li>たし算・ひき算・かけ算・わり算どれかを判断</li>
  <li>通分が必要か確認</li>
  <li>答えを帯分数または整数に直す</li>
</ol>
<div class="warn-box"><p>⚠️ 答えの単位を必ず書きましょう。また仮分数のままにせず帯分数に直します。</p></div>""",
    "faq": [
      {"q": "分数の文章題が苦手な場合は？", "a": "まず分数の計算（通分・約分）を確実にしてから文章題に進みましょう。計算が不安定だと文章題は解けません。"},
      {"q": "「〇の何分の一」はかけ算ですか？", "a": "はい、「12の2/3」は12×2/3＝8です。「の」はかけ算を意味することが多いです。"},
      {"q": "答えが仮分数になったらどうしますか？", "a": "帯分数に直します（例：7/4→1と3/4）。整数になる場合（4/4→1）は整数で書きます。"},
      {"q": "分数と小数が混じった問題は？", "a": "どちらかに統一します。分数に直すか小数に直すかは問題によります。答えの形が指定されている場合は指定に従います。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-tasizan.html", "emoji": "½", "text": "分数のたし算"},
      {"href": "/bunsuu-tsuubun.html", "emoji": "½", "text": "通分のやり方"},
      {"href": "/mondai-sokudo.html",  "emoji": "📝", "text": "速さの文章題"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # 学年別 完全ガイド
  # ────────────────────────────────
  {
    "filename": "grade-1-tips.html",
    "title": "小学1年生の算数 完全ガイド｜つまずきポイントと勉強法",
    "description": "小学1年生の算数（数の概念・たし算・ひき算・時計・形）のつまずきポイントと効果的な勉強法を解説。保護者向けサポートガイド。",
    "h1": "小学1年生の算数 完全ガイド｜つまずきポイントと勉強法",
    "eyecatch": "🎒 1年生の算数は「算数が好き・嫌い」が決まる大切な時期。最初のつまずきを早めに解消しましょう！",
    "body_html": """\
<h2>1年生で学ぶ算数の全単元</h2>
<ul>
  <li>10までの数・20までの数</li>
  <li>たし算（繰り上がりなし・あり）</li>
  <li>ひき算（繰り下がりなし・あり）</li>
  <li>100までの数</li>
  <li>時計の読み方（〇時・〇時半）</li>
  <li>形（三角形・四角形・丸など）</li>
</ul>

<h2>1年生でつまずきやすい単元TOP3</h2>
<h3>1位：繰り上がりのたし算・繰り下がりのひき算</h3>
<p>「さくらんぼ計算」を使って10のまとまりを作る方法が理解できるかが鍵です。</p>
<h3>2位：数の大小比較</h3>
<p>「どちらが大きい？」「いくつ多い？」という問いへの答え方を練習します。</p>
<h3>3位：時計の読み方</h3>
<p>長針・短針の意味と「〇時半」の読み方を確実にしましょう。</p>

<h2>保護者ができるサポート</h2>
<ul>
  <li>毎日5〜10分の計算練習（継続が最重要）</li>
  <li>おはじき・ブロックなど具体物を使った学習</li>
  <li>日常生活で数を意識する（おやつの個数・時計を読む習慣）</li>
</ul>
<div class="tip-box"><p>💡 1年生の算数でつまずいたまま2年生になると九九が難しくなります。繰り上がり・繰り下がりは確実にマスターしましょう。</p></div>""",
    "faq": [
      {"q": "1年生算数で最も重要な単元は？", "a": "繰り上がりのたし算・繰り下がりのひき算です。これが2年生の九九・かけ算の基礎になります。"},
      {"q": "1年生で算数が苦手になったらどうする？", "a": "早めに対処が重要です。つまずきの原因（どの単元か）を特定して、その単元に戻って復習します。"},
      {"q": "計算カードは効果がありますか？", "a": "大変効果的です。繰り返しフラッシュカードをすることで、たし算・ひき算が自動化（反射的に答えられる）され、後の学習が楽になります。"},
      {"q": "1年生の算数はどこで練習できますか？", "a": "当サイトの無料ドリル（1年生ページ）でスマホから印刷不要で練習できます。毎回問題がランダムに変わるので繰り返し使えます。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/tasizan-kuriagari.html", "emoji": "➕", "text": "繰り上がりのたし算"},
      {"href": "/hikizan-kurisagari.html","emoji": "➖", "text": "繰り下がりのひき算"},
      {"href": "/jikan-yomikata.html",    "emoji": "🕐", "text": "時計の読み方"},
      {"href": "/grade-1-matome.html",   "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  {
    "filename": "grade-3-tips.html",
    "title": "小学3年生の算数 完全ガイド｜つまずきポイントと勉強法",
    "description": "小学3年生の算数（かけ算筆算・わり算・大きな数・時間・長さ・あまり）のつまずきポイントと勉強法を解説。保護者向けガイド。",
    "h1": "小学3年生の算数 完全ガイド｜つまずきポイントと勉強法",
    "eyecatch": "📚 3年生はわり算・大きな数・分数の入り口。九九が完璧かどうかが全てのカギになります！",
    "body_html": """\
<h2>3年生で学ぶ算数の全単元</h2>
<ul>
  <li>かけ算の筆算（2桁×1桁）</li>
  <li>わり算・あまりのあるわり算</li>
  <li>大きな数（万・億）</li>
  <li>時間と時刻の計算</li>
  <li>長さの単位（km）</li>
  <li>重さの単位（g・kg）</li>
  <li>分数の基礎</li>
  <li>三角形・角度の基礎</li>
  <li>棒グラフ</li>
</ul>

<h2>3年生でつまずきやすい単元TOP3</h2>
<h3>1位：わり算（特にあまりのあるわり算）</h3>
<p>九九の逆引きが不完全だとわり算でつまずきます。九九の完全習熟が前提です。</p>
<h3>2位：かけ算の筆算（繰り上がり）</h3>
<p>複数回の繰り上がりが重なると混乱しやすいです。</p>
<h3>3位：時間の計算（60進法）</h3>
<p>普通の計算と違うルールに戸惑う子が多いです。</p>

<h2>勉強法のポイント</h2>
<ul>
  <li>九九が怪しい場合は今すぐ復習（わり算の直前に）</li>
  <li>わり算の検算（割る数×商＋あまり）を習慣化</li>
  <li>時間の計算はタイムラインを書く</li>
</ul>
<div class="tip-box"><p>💡 3年生の九九の定着度が4年生以降の算数の土台になります。夏休みに総復習するのがおすすめです。</p></div>""",
    "faq": [
      {"q": "3年生算数で最も重要な単元は？", "a": "わり算です。九九の逆引きとして、割り算の概念をしっかり理解することが4年生の筆算につながります。"},
      {"q": "九九が不完全な状態でわり算を習い始めたら？", "a": "一時的にわり算の学習を止めて九九の完全習熟に集中することをおすすめします。九九なしのわり算学習は非効率です。"},
      {"q": "大きな数（万の位）が分からない場合は？", "a": "百の位・千の位まで確認してから万の位へ進みましょう。位取りの表を使って視覚的に確認するのが効果的です。"},
      {"q": "3年生から分数を習いますか？", "a": "はい、3年生で分数の基礎（1/2・1/3など）を学びます。同分母の簡単なたし算・ひき算まで学習します。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-kiso.html",   "emoji": "➗", "text": "わり算の基礎"},
      {"href": "/warizan-amari.html",  "emoji": "➗", "text": "あまりのあるわり算"},
      {"href": "/jikan-keisan.html",   "emoji": "⏱️", "text": "時間の計算"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "grade-4-tips.html",
    "title": "小学4年生の算数 完全ガイド｜つまずきポイントと勉強法",
    "description": "小学4年生の算数（わり算筆算・小数・分数・面積・角度・大きな数）のつまずきポイントと勉強法を解説。保護者向けガイド。",
    "h1": "小学4年生の算数 完全ガイド｜つまずきポイントと勉強法",
    "eyecatch": "📚 4年生は小数・分数・面積が同時に登場する「算数の分岐点」。早めの対策が5・6年生の差になります！",
    "body_html": """\
<h2>4年生で学ぶ算数の全単元</h2>
<ul>
  <li>大きな数（億・兆）</li>
  <li>わり算の筆算（2〜3桁÷1〜2桁）</li>
  <li>がい数（四捨五入）</li>
  <li>小数のたし算・ひき算</li>
  <li>分数（同分母のたし算・ひき算）</li>
  <li>面積（長方形・正方形）</li>
  <li>角度の測定・作図</li>
  <li>垂直・平行と四角形</li>
  <li>折れ線グラフ</li>
  <li>倍数・約数の基礎</li>
</ul>

<h2>4年生でつまずきやすい単元TOP3</h2>
<h3>1位：わり算の筆算（3桁÷2桁）</h3>
<p>商の見当づけが難しく、修正の繰り返しで嫌になりやすい単元です。</p>
<h3>2位：小数のたし算・ひき算</h3>
<p>小数点をそろえる手順を忘れるとミスが頻発します。</p>
<h3>3位：角度の問題</h3>
<p>分度器の使い方と「角度の合計は180°・360°」のルール理解が必要です。</p>

<h2>保護者ができるサポート</h2>
<ul>
  <li>わり算筆算は「たてる・かける・ひく・おろす」を声に出して練習</li>
  <li>小数の計算は「小数点をそろえる」チェックを習慣化</li>
  <li>角度は分度器を実際に使って練習</li>
</ul>
<div class="tip-box"><p>💡 4年生で「小数・分数・面積」の基礎を固めることが、5年生の難単元（割合・速さ）への準備になります。</p></div>""",
    "faq": [
      {"q": "4年生算数で最も重要な単元は？", "a": "小数と分数の基礎です。これが5年生の「割合」「速さ」の計算に直結します。"},
      {"q": "がい数（四捨五入）はなぜ難しいですか？", "a": "「以上・未満」や「上から○桁」など言葉が複雑なためです。どの桁を四捨五入するか問題文をよく読む練習が必要です。"},
      {"q": "角度の問題で分度器の使い方が分からない場合は？", "a": "まず0°と180°の目盛りの読み方を確認し、内側・外側どちらの目盛りを使うかを練習します。"},
      {"q": "倍数・約数は4年生で完璧にすべきですか？", "a": "基本は4年生で学びますが、通分・約分（5年生）で本格的に活用します。公倍数・公約数の概念を理解しておくと5年生が楽になります。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-hissan.html",  "emoji": "➗", "text": "わり算の筆算"},
      {"href": "/syousuu-tasizan.html", "emoji": "🔢", "text": "小数のたし算"},
      {"href": "/kakudo-guide.html",    "emoji": "📐", "text": "角度の学習ガイド"},
      {"href": "/grade-4-matome.html",  "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "grade-5-tips.html",
    "title": "小学5年生の算数 完全ガイド｜割合・速さのつまずき解消",
    "description": "小学5年生の算数（割合・速さ・分数・小数・体積・平均）のつまずきポイントと勉強法を解説。難しい5年生算数を乗り越えるガイド。",
    "h1": "小学5年生の算数 完全ガイド｜割合・速さのつまずき解消",
    "eyecatch": "📚 5年生は算数で最もつまずく子が多い学年。「割合」「速さ」を正しく理解することが最大の課題です！",
    "body_html": """\
<h2>5年生で学ぶ算数の全単元</h2>
<ul>
  <li>整数と小数（大きな数・小さな数）</li>
  <li>小数のかけ算・わり算</li>
  <li>分数の通分・約分</li>
  <li>分数のたし算・ひき算</li>
  <li>体積（直方体・立方体）</li>
  <li>割合・百分率・歩合</li>
  <li>速さ・時間・距離</li>
  <li>平均</li>
  <li>図形の合同</li>
  <li>三角形・平行四辺形の面積</li>
</ul>

<h2>5年生でつまずきやすい単元TOP3</h2>
<h3>1位：割合</h3>
<p>「もとにする量・比べる量・割合」の3者関係が概念的で難しい。「くもわ」の公式を図で理解することが重要。</p>
<h3>2位：速さ</h3>
<p>「速さ・時間・距離」の3者関係、単位換算（分速→時速）が重なって複雑になります。</p>
<h3>3位：分数の通分</h3>
<p>最小公倍数を正確に求める力が必要です。</p>

<h2>勉強法のポイント</h2>
<ul>
  <li>割合：「くもわ」の図（面積図）を使って視覚化</li>
  <li>速さ：「はじきの図」で3者関係を整理</li>
  <li>分数：最小公倍数の計算を確実にしてから通分へ</li>
</ul>
<div class="tip-box"><p>💡 5年生でつまずいたまま6年生になると中学数学にも影響します。夏休みに割合・速さを重点的に復習しましょう。</p></div>""",
    "faq": [
      {"q": "5年生算数で最も重要な単元は？", "a": "割合です。割合の概念は6年生の比・中学の方程式にもつながる最重要単元です。"},
      {"q": "割合が全く分からない場合はどうすれば？", "a": "「100人中60人が合格→合格率は0.6（60%）」など、具体的な例から理解しましょう。公式（比べる量÷もとにする量）に先に当てはめるのではなく、意味から理解することが大切です。"},
      {"q": "速さの「はじきの図」とは何ですか？", "a": "「は（速さ）・じ（時間）・き（距離）」を三角形の図で表したものです。求めたい部分を隠すと計算式が分かります。"},
      {"q": "小数のかけ算・わり算で小数点の位置を間違えます。", "a": "整数として計算した後、小数点の桁数を数えて移動させる手順を守ることが大切です。かける前に「桁数の合計」を先にメモしておく方法も効果的です。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/heikin-guide.html",     "emoji": "📊", "text": "平均の求め方"},
      {"href": "/mondai-sokudo.html",    "emoji": "📝", "text": "速さの文章題"},
      {"href": "/bunsuu-tsuubun.html",   "emoji": "½", "text": "通分のやり方"},
      {"href": "/grade-5-matome.html",   "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "grade-6-tips.html",
    "title": "小学6年生の算数 完全ガイド｜中学準備の総仕上げ",
    "description": "小学6年生の算数（分数計算・比・割合・円の面積・場合の数）のつまずきポイントと勉強法。中学数学につながる単元を解説。",
    "h1": "小学6年生の算数 完全ガイド｜中学準備の総仕上げ",
    "eyecatch": "📚 6年生の算数は小学校の集大成。分数計算・比・円を仕上げて中学数学へ万全の準備をしましょう！",
    "body_html": """\
<h2>6年生で学ぶ算数の全単元</h2>
<ul>
  <li>分数のかけ算・わり算</li>
  <li>比と比の値</li>
  <li>比例・反比例</li>
  <li>円の面積</li>
  <li>角柱・円柱の体積</li>
  <li>対称な図形（線対称・点対称）</li>
  <li>拡大図・縮図</li>
  <li>場合の数・並べ方</li>
  <li>データの活用（ドットプロット・ヒストグラム）</li>
  <li>文字と式（x・yの基礎）</li>
</ul>

<h2>6年生でつまずきやすい単元TOP3</h2>
<h3>1位：比例・反比例</h3>
<p>グラフと式の両方から理解する必要があり、抽象的な概念が難しいです。</p>
<h3>2位：分数のわり算（逆数）</h3>
<p>「逆数をかける」理由を理解せず、ルールだけ覚えて誤用するケースが多いです。</p>
<h3>3位：場合の数</h3>
<p>数え漏れ・重複なく数える方法（樹形図・表）の習得が必要です。</p>

<h2>中学準備として重要なこと</h2>
<ul>
  <li>比例・反比例の概念（中学数学の関数の基礎）</li>
  <li>文字式（x・yの使い方）の慣れ</li>
  <li>分数計算の完全習熟</li>
</ul>
<div class="tip-box"><p>💡 6年生の算数を仕上げることが中学1年生数学（方程式・関数）への最大の準備です。</p></div>""",
    "faq": [
      {"q": "6年生算数で最も重要な単元は？", "a": "比例・反比例です。中学1年生の「関数」の基礎になります。グラフと式を両方から理解しておきましょう。"},
      {"q": "分数のわり算が苦手な場合は？", "a": "「逆数をかける」というルールだけでなく、なぜそうなるかを具体例（絵や図）で確認しましょう。仕組みを理解すると忘れにくくなります。"},
      {"q": "場合の数で数え漏れを防ぐには？", "a": "樹形図や表を必ず書くことです。頭の中だけで数えると必ず漏れや重複が起きます。系統的に（一定のルールで）数える習慣をつけましょう。"},
      {"q": "6年生で文字（x・y）を使いますか？", "a": "算数では□や△を使うことが多いですが、6年生から文字式の準備として変数の概念に触れます。中学の方程式への助走になります。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/bunsuu-warizan.html",  "emoji": "½", "text": "分数のわり算"},
      {"href": "/hirei-hanpirei.html",  "emoji": "📊", "text": "比例と反比例"},
      {"href": "/menseki-enza.html",    "emoji": "📐", "text": "円の面積"},
      {"href": "/grade-6-matome.html",  "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # 学習記事
  # ────────────────────────────────
  {
    "filename": "keisan-hayaku.html",
    "title": "計算を速くする方法【10のコツ】小学生向け",
    "description": "計算を速くするための10のコツを解説。暗算・工夫・数の感覚を鍛える方法を小学生向けにわかりやすく紹介します。",
    "h1": "計算を速くする方法【10のコツ】小学生向け",
    "eyecatch": "⚡ 計算が速くなると算数のテストが楽になります。今日からできる10のコツを紹介します！",
    "body_html": """\
<h2>計算を速くする10のコツ</h2>
<h3>①数の補数を覚える</h3>
<p>「10の補数」（1と9、2と8…）、「100の補数」を瞬時に言えるようにする。</p>
<h3>②計算のきまりを使う</h3>
<p>99×□ ＝ 100×□ ー □（99に近い数はまとめて計算）</p>
<h3>③九九の完全習熟</h3>
<p>九九が自動化されるまで毎日練習。これが全計算の基礎。</p>
<h3>④計算の順番を変える（交換法則）</h3>
<p>3＋17＋13＋7 ＝ (3＋17)＋(13＋7) ＝ 20＋20 ＝ 40（きりのいい数にまとめる）</p>
<h3>⑤「倍」を使って計算</h3>
<p>15×4 ＝ 15×2×2 ＝ 30×2 ＝ 60（2回かけるより計算しやすい）</p>
<h3>⑥小数・分数を整数に直す</h3>
<p>途中で整数に換算してから計算するとミスが減る。</p>
<h3>⑦暗算の練習を毎日する</h3>
<p>5〜10分の暗算練習を習慣化。</p>
<h3>⑧検算の習慣をつける</h3>
<p>速さと正確さは両立できる。検算を習慣にすることでミスが減り、結果的に速くなる。</p>
<h3>⑨計算ミスのパターンを知る</h3>
<p>自分がよくするミス（繰り上がり忘れなど）を把握して意識的に注意。</p>
<h3>⑩数字に慣れる（数感覚）</h3>
<p>「125×8＝1000」など覚えておくと便利な計算を暗記する。</p>
<div class="tip-box"><p>💡 「速さ」より「正確さ」が先です。まず間違えずに解けるようになってから速さを追求しましょう。</p></div>""",
    "faq": [
      {"q": "計算を速くするのに一番効果的な方法は？", "a": "九九の完全習熟と補数の暗記です。この2つが自動化されるだけで計算速度は大幅にアップします。"},
      {"q": "暗算と筆算どちらを優先すべきですか？", "a": "まず筆算（手順の正確な習得）が先です。筆算が完璧になると暗算もできるようになります。暗算だけ練習しても筆算が不正確なままでは本末転倒です。"},
      {"q": "計算練習はどのくらいの頻度でするべきですか？", "a": "毎日5〜10分が最も効果的です。週に1回2時間するより毎日少しずつの方が記憶に定着します。"},
      {"q": "計算ミスをなくすにはどうすればいいですか？", "a": "①問題文を最後まで読む ②式を丁寧に書く ③答えの検算をする ④自分がよくするミスのパターンを把握する、この4つが基本です。"},
    ],
    "cta_href": "/",
    "cta_label": "ドリルで練習してみる",
    "related": [
      {"href": "/anzan-tips.html",      "emoji": "⚡", "text": "暗算のコツ"},
      {"href": "/mainichi-drill.html",  "emoji": "📅", "text": "毎日の計算練習法"},
      {"href": "/tesuto-100ten.html",   "emoji": "💯", "text": "テストで100点を取る方法"},
      {"href": "/keisan-machigai.html", "emoji": "❌", "text": "計算ミスをなくす方法"},
    ],
  },

  {
    "filename": "sansu-benkyou-houhou.html",
    "title": "算数の勉強方法【完全ガイド】小学生の効果的な学習法",
    "description": "小学生の算数を効果的に学ぶ勉強方法を解説。予習・復習・テスト対策まで、親子で取り組める学習法を紹介します。",
    "h1": "算数の勉強方法【完全ガイド】小学生向け",
    "eyecatch": "📖 「どう勉強すれば算数が得意になる？」その疑問に答えます。効果的な学習法をステップで解説！",
    "body_html": """\
<h2>算数が得意になる3つの鉄則</h2>
<h3>①基礎計算を「自動化」する</h3>
<p>たし算・ひき算・九九が頭を使わず瞬時に答えられる状態にすることが全ての基礎。</p>
<h3>②つまずいたらすぐ戻る</h3>
<p>算数は積み上げ教科。分からないまま進まず、必ずつまずいた単元に戻って解決する。</p>
<h3>③「なぜ？」を大切にする</h3>
<p>公式を丸暗記せず、なぜその式になるかを理解すると応用問題にも対応できる。</p>

<h2>毎日の学習ルーティン（おすすめ）</h2>
<ul>
  <li>計算練習：5〜10分（毎日継続）</li>
  <li>教科書の例題確認：10分</li>
  <li>ドリル・問題演習：15〜20分</li>
  <li>間違えた問題の見直し：5分</li>
</ul>
<div class="tip-box"><p>💡 合計30〜40分。長時間より毎日の短時間練習の方が効果的です。</p></div>

<h2>テスト前の対策</h2>
<ol>
  <li>教科書の例題と練習問題を全部解き直す</li>
  <li>間違えた問題をまとめた「ミスノート」を作る</li>
  <li>ドリルや過去問で時間を計って練習する</li>
</ol>

<h2>保護者のサポートポイント</h2>
<ul>
  <li>答えを教えるより「どこで詰まったか」を聞く</li>
  <li>正解より「なぜそう考えたか」のプロセスを大切にする</li>
  <li>勉強の習慣化（同じ時間・同じ場所でする）をサポート</li>
</ul>""",
    "faq": [
      {"q": "算数が苦手な子にはどんな教材がいいですか？", "a": "スモールステップで学べる教材が効果的です。学校の教科書に沿った問題集や、当サイトのような即時採点できるデジタルドリルがおすすめです。"},
      {"q": "予習と復習はどちらが大事ですか？", "a": "算数は復習が重要です。習ったことをその日のうちに復習し、週末に週の内容を振り返る習慣が定着の近道です。"},
      {"q": "塾に行くべきですか？", "a": "まず自宅学習で基礎を固めることが先です。つまずきが多い場合や、受験を考える場合に塾を検討しましょう。"},
      {"q": "計算ドリルは何種類やればいいですか？", "a": "多種類より一つの教材を繰り返す方が効果的です。当サイトのように問題がランダムに変わるドリルなら同じページを何度でも使えます。"},
    ],
    "cta_href": "/",
    "cta_label": "無料ドリルで練習する",
    "related": [
      {"href": "/keisan-hayaku.html",       "emoji": "⚡", "text": "計算を速くする方法"},
      {"href": "/mainichi-drill.html",      "emoji": "📅", "text": "毎日の計算練習法"},
      {"href": "/sansu-test-taisaku.html",  "emoji": "📝", "text": "算数テスト対策"},
      {"href": "/sansu-kirai.html",         "emoji": "😢", "text": "算数が嫌いな子への対処法"},
    ],
  },

  {
    "filename": "oyako-sansu.html",
    "title": "親子で楽しむ算数【日常生活で数学力を育てる方法】",
    "description": "日常生活の中で算数の力を自然に育てる方法を紹介。お買い物・料理・ゲームを使った親子学習のアイデア集。",
    "h1": "親子で楽しむ算数｜日常生活で数学力を育てる方法",
    "eyecatch": "👨‍👩‍👧 算数は机の上だけで学ぶものじゃない！日常生活に算数があふれています。親子で楽しみながら数学力を伸ばしましょう。",
    "body_html": """\
<h2>日常生活で算数を使う場面</h2>
<h3>🛒 お買い物</h3>
<ul>
  <li>「合計いくら？」→ 足し算・引き算</li>
  <li>「500円で何個買える？」→ わり算</li>
  <li>「20%引きはいくら？」→ 割合・百分率（高学年）</li>
</ul>
<h3>🍳 料理</h3>
<ul>
  <li>「4人分のレシピを2人分に」→ 分数・割合</li>
  <li>「小さじ3杯は何mL？」→ 単位換算</li>
  <li>「タイマー20分後は何時？」→ 時刻の計算</li>
</ul>
<h3>🎮 ゲーム・遊び</h3>
<ul>
  <li>トランプゲームで足し算・引き算</li>
  <li>サイコロゲームで確率感覚（高学年）</li>
  <li>ボードゲームで計算練習</li>
</ul>
<div class="tip-box"><p>💡 「これも算数なんだよ」と声に出すだけで、子どもが算数を日常のものとして意識するようになります。</p></div>

<h2>親が教える時のポイント</h2>
<ul>
  <li>「答えを教える前に考えさせる」</li>
  <li>間違えてもOK。「なぜそう思った？」と聞く</li>
  <li>できたら具体的にほめる（「計算が速くなったね！」）</li>
</ul>
<div class="warn-box"><p>⚠️ 「なんでわからないの？」という言葉は禁物。算数嫌いになる原因になります。</p></div>""",
    "faq": [
      {"q": "幼児期から算数の準備はできますか？", "a": "はい、日常生活の数え上げ（おもちゃの数を数える）、形の観察（三角・丸）、順序（1番、2番）などが算数の基礎になります。"},
      {"q": "勉強嫌いの子に算数を教えるコツは？", "a": "ゲーム感覚で取り組める活動（トランプ・カード・ボードゲーム）から始めると抵抗が少なくなります。"},
      {"q": "お買い物での算数学習はいつから？", "a": "小学1年生（10以内の足し算）から始められます。「あわせていくら？」という簡単な問いかけから始めましょう。"},
      {"q": "親自身が算数が苦手でも教えられますか？", "a": "はい。一緒に考える姿勢が大切です。「お母さんも考えてみよう」という姿勢は子どもにも良い影響を与えます。当サイトの解説ページも活用してください。"},
    ],
    "cta_href": "/",
    "cta_label": "無料ドリルで練習する",
    "related": [
      {"href": "/shukudai-oshiekata.html", "emoji": "📝", "text": "算数の宿題の教え方"},
      {"href": "/sansu-kirai.html",        "emoji": "😢", "text": "算数が嫌いな子への対処法"},
      {"href": "/sansu-benkyou-houhou.html","emoji": "📖", "text": "算数の効果的な勉強法"},
      {"href": "/mainichi-drill.html",     "emoji": "📅", "text": "毎日の計算練習法"},
    ],
  },


  # ────────────────────────────────
  # 比・割合・速さ
  # ────────────────────────────────
  {
    "filename": "wariai-guide.html",
    "title": "割合の求め方プリント【無料】くもわの公式と練習問題｜小学5年生",
    "description": "割合の求め方（くもわの公式）を印刷不要・スマホで練習できる無料プリント。百分率・歩合への変換も解説。小学5年生向け。",
    "h1": "割合の求め方プリント【無料】小学5年生",
    "eyecatch": "📊 割合は5年生最大の難関。「くもわ」の公式をマスターすれば百分率・歩合もスラスラ解けます！",
    "body_html": """\
<h2>割合の3つの量</h2>
<div class="formula-box"><p>割合 ＝ 比べる量 ÷ もとにする量</p></div>
<ul>
  <li><strong>もとにする量（も）：</strong>基準となる量（全体・元の量）</li>
  <li><strong>比べる量（く）：</strong>比較対象の量</li>
  <li><strong>割合（わ）：</strong>比べる量がもとにする量の何倍か</li>
</ul>
<div class="tip-box"><p>💡 「く＝も×わ」「も＝く÷わ」「わ＝く÷も」。求めたいものを隠すと式が出てきます。</p></div>

<h2>割合・百分率・歩合の変換</h2>
<ul>
  <li>割合0.25 ＝ 百分率25% ＝ 歩合2割5分</li>
  <li>割合→%：×100</li>
  <li>割合→歩合：×10（「割」の単位）</li>
</ul>

<h2>よく出る問題パターン</h2>
<ol>
  <li>「80人の40%は何人？」→ 比べる量＝80×0.4＝32人</li>
  <li>「60人が75%にあたる。全体は？」→ もとにする量＝60÷0.75＝80人</li>
  <li>「80人中60人。割合は？」→ 割合＝60÷80＝0.75＝75%</li>
</ol>
<div class="warn-box"><p>⚠️ 「もとにする量」の見極めが割合問題の肝。問題文の「〜の何割・何%」という表現で「〜」がもとにする量です。</p></div>""",
    "faq": [
      {"q": "割合はいつ習いますか？", "a": "小学5年生で学習します。百分率（%）・歩合（割・分・厘）も5年生で習います。"},
      {"q": "「くもわ」とは何ですか？", "a": "く（比べる量）・も（もとにする量）・わ（割合）の頭文字です。三角形の図に並べ、求めたい部分を隠すと計算式が分かります。"},
      {"q": "割合と比の違いは何ですか？", "a": "割合は「一方がもう一方の何倍か」を表す数。比は「2つの量の比べ方」で6年生で学習します。考え方は似ています。"},
      {"q": "百分率と歩合はどう使い分けますか？", "a": "百分率（%）は一般的な表現、歩合（割・分・厘）は主に野球の打率や商売の値引き表現で使います。小学校では両方学びます。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/mondai-wariai.html",  "emoji": "📝", "text": "割合の文章題"},
      {"href": "/hirei-hanpirei.html", "emoji": "📊", "text": "比例と反比例"},
      {"href": "/baai-no-kazu.html",   "emoji": "📊", "text": "場合の数"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "sokudo-guide.html",
    "title": "速さの求め方プリント【無料】はじきの公式と練習問題｜小学5年生",
    "description": "速さの求め方（はじきの公式）を印刷不要・スマホで練習できる無料プリント。速さ・時間・距離の3つの関係をわかりやすく解説。小学5年生向け。",
    "h1": "速さの求め方プリント【無料】小学5年生",
    "eyecatch": "🚀 速さの問題は「はじきの図」で解決！速さ・時間・距離の関係をマスターしましょう。",
    "body_html": """\
<h2>速さ・時間・距離の3つの関係</h2>
<div class="formula-box"><p>速さ ＝ 距離 ÷ 時間　距離 ＝ 速さ × 時間　時間 ＝ 距離 ÷ 速さ</p></div>
<div class="tip-box"><p>💡 「は（速さ）・じ（時間）・き（距離）」の三角形の図を使う。求めたい部分を隠すと式が出てきます。</p></div>

<h2>単位に注意</h2>
<ul>
  <li>時速（km/h）：1時間あたりのkm数</li>
  <li>分速（m/分）：1分あたりのm数</li>
  <li>秒速（m/秒）：1秒あたりのm数</li>
</ul>
<p>単位を変換する場合：時速60km ＝ 分速1000m（60000m÷60分）</p>

<h2>よく出る問題パターン</h2>
<ol>
  <li>「時速40kmで3時間走った。距離は？」→ 40×3＝120km</li>
  <li>「120kmを時速40kmで走ると何時間？」→ 120÷40＝3時間</li>
  <li>「120kmを3時間で走った。時速は？」→ 120÷3＝時速40km</li>
</ol>

<h2>時間の換算が必要な問題</h2>
<p>「分速60mで30分歩いた。距離は？」→ 60×30＝1800m</p>
<p>「時速72kmは分速何m？」→ 72000m÷60分＝分速1200m</p>
<div class="warn-box"><p>⚠️ 速さと時間の単位をそろえることが必須です。時間が「分」なら速さも「分速」に変換します。</p></div>""",
    "faq": [
      {"q": "速さはいつ習いますか？", "a": "小学5年生で学習します。割合と並んで5年生最難関の単元です。"},
      {"q": "「はじきの図」とは何ですか？", "a": "速さ（は）・時間（じ）・距離（き）を三角形の図に配置したものです。求めたい量を隠すと残りの計算式が見えます（き÷じ＝は、は×じ＝き、き÷は＝じ）。"},
      {"q": "時速と分速の変換方法は？", "a": "時速→分速：÷60（例：時速60km→分速1km＝1000m）。分速→秒速：÷60。逆は×60です。"},
      {"q": "速さの問題で一番多い間違いは？", "a": "単位の不一致です。速さが時速なのに時間が「分」で与えられている場合、時間を「時間」に変換（÷60）してから計算する必要があります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/mondai-sokudo.html",  "emoji": "📝", "text": "速さの文章題"},
      {"href": "/jikan-henkan.html",   "emoji": "⏱️", "text": "時間の単位換算"},
      {"href": "/wariai-guide.html",   "emoji": "📊", "text": "割合の求め方"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "hi-guide.html",
    "title": "比の求め方プリント【無料】比・比の値・比を簡単にする｜小学6年生",
    "description": "比の求め方（比の値・比を簡単にする・等しい比）を印刷不要・スマホで練習できる無料プリント。比の基礎から応用まで解説。小学6年生向け。",
    "h1": "比の求め方プリント【無料】小学6年生",
    "eyecatch": "📊 比は「2つの量の関係」を表す表現。割合との違いを理解して使いこなしましょう！",
    "body_html": """\
<h2>比とは？</h2>
<p>2つの量の関係を「a：b」（aコロンb）で表したものです。</p>
<div class="formula-box"><p>砂糖3：塩2 ＝ 砂糖が塩の1.5倍ある</p></div>

<h2>比の値</h2>
<p>a：b の比の値は a÷b です。</p>
<div class="formula-box"><p>6：4 の比の値 ＝ 6÷4 ＝ 1.5</p></div>

<h2>比を簡単にする（最大公約数で割る）</h2>
<div class="formula-box"><p>12：8 → 最大公約数4で割る → 3：2</p></div>
<div class="tip-box"><p>💡 比を簡単にするのは約分と同じ考え方。両方の数を同じ数で割ります。</p></div>

<h2>等しい比</h2>
<p>a：b に同じ数をかけても割っても等しい比になります。</p>
<div class="formula-box"><p>1：2 ＝ 3：6 ＝ 5：10（全て等しい比）</p></div>

<h2>比を使った計算</h2>
<p>「小麦粉と砂糖を3：1の比で混ぜる。小麦粉が150gなら砂糖は？」</p>
<p>3：1＝150：□ → □＝150÷3×1＝50g</p>
<div class="warn-box"><p>⚠️ 比は「等号（＝）」では結べません。「3：2」と「6：4」は等しい比ですが、数学的には「3：2＝6：4」と書けます（比例式）。</p></div>""",
    "faq": [
      {"q": "比はいつ習いますか？", "a": "小学6年生で学習します。割合（5年生）の発展として、比例・反比例とセットで学びます。"},
      {"q": "比と割合の違いは何ですか？", "a": "割合は「一方がもう一方の何倍か」を1つの数で表します（例：0.6倍）。比は2つの量の関係を「3：5」のように対で表します。"},
      {"q": "比を使った文章題のコツは？", "a": "「全体を何に分けるか」を先に決めることです。3：2なら全体を5に分け、3/5と2/5の部分に分けて考えます。"},
      {"q": "比例式（a：b＝c：d）の解き方は？", "a": "「内項の積＝外項の積」（b×c＝a×d）を使います。例：2：3＝4：□なら3×4÷2＝6となります。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/hirei-hanpirei.html",  "emoji": "📊", "text": "比例と反比例"},
      {"href": "/wariai-guide.html",    "emoji": "📊", "text": "割合の求め方"},
      {"href": "/kakudai-shukuzu.html", "emoji": "📐", "text": "拡大図・縮図"},
      {"href": "/grade-6-matome.html",  "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # 数・計算の基礎
  # ────────────────────────────────
  {
    "filename": "suji-kakikata.html",
    "title": "数字の書き方プリント【無料】1〜10の正しい書き方｜幼児・1年生",
    "description": "1〜10の数字の正しい書き方を練習できる無料プリント。書き順と形を丁寧に解説。幼稚園・保育園・小学1年生向け。",
    "h1": "数字の書き方プリント【無料】幼児・小学1年生",
    "eyecatch": "✏️ 正しい数字の書き方を最初に覚えることが大切。書き順と形をしっかり練習しましょう！",
    "body_html": """\
<h2>数字の書き方のポイント</h2>
<p>数字は形が似ているものがあり、最初に正しい書き方を覚えることが大切です。</p>

<h2>まちがえやすい数字</h2>
<ul>
  <li><strong>1 と 7：</strong> 1は縦棒のみ、7は横棒＋斜め線。しっかり区別する</li>
  <li><strong>6 と 9：</strong> 向きが逆になりやすい。6は丸が下、9は丸が上</li>
  <li><strong>2 と 5：</strong> 書き始めの向きを間違えやすい</li>
  <li><strong>3：</strong> 上と下の丸の大きさをそろえる</li>
</ul>
<div class="tip-box"><p>💡 マス目のノートに大きく書く練習から始めましょう。小さく書くのは上手に書けるようになってからです。</p></div>

<h2>練習の順番</h2>
<ol>
  <li>1〜5を練習</li>
  <li>6〜10を練習</li>
  <li>ランダムに書いて覚える</li>
  <li>速く・きれいに書く練習</li>
</ol>

<h2>大切なこと</h2>
<ul>
  <li>えんぴつの持ち方を正しく（人差し指・親指・中指の3点で支える）</li>
  <li>線の方向（上から下・左から右が基本）を意識する</li>
  <li>テスト用紙ではきれいに書かないと採点者が読めない場合も</li>
</ul>""",
    "faq": [
      {"q": "数字の書き方はいつ習いますか？", "a": "小学1年生の4月から習います。幼稚園・保育園で先取りして練習する子も多いです。"},
      {"q": "書き順は大切ですか？", "a": "厳密な書き順が決まっている漢字と違い、数字の書き順は複数あることも。ただし自然なバランスのとれた形で書くための順番を練習しましょう。"},
      {"q": "鉛筆の持ち方が悪い場合は？", "a": "正しい持ち方（3点持ち）を早めに矯正しましょう。補助具（三角鉛筆・鉛筆持ち方ガイド）を使うと自然に正しい持ち方が身につきます。"},
      {"q": "数字を反転して書いてしまう（鏡文字）場合は？", "a": "幼児期はよくあることです。6と9、2などは特に間違えやすいです。繰り返し練習することで自然に直ります。心配な場合は就学前相談を利用しましょう。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/youji-kazu.html",     "emoji": "🔢", "text": "幼児向け数の学習"},
      {"href": "/10made-no-kazu.html", "emoji": "🔢", "text": "10までの数"},
      {"href": "/nyuugaku-mae.html",   "emoji": "🎒", "text": "入学前の準備"},
      {"href": "/grade-1-matome.html", "emoji": "📚", "text": "1年生 全単元まとめ"},
    ],
  },

  {
    "filename": "anzan-practice.html",
    "title": "暗算練習プリント【無料】計算力を鍛える暗算トレーニング",
    "description": "暗算力を鍛える無料の計算練習プリント。1桁〜3桁の暗算トレーニング問題を解説付きで提供。スマホで即採点できます。",
    "h1": "暗算練習プリント【無料】計算力トレーニング",
    "eyecatch": "🧠 暗算は計算の最高峰。毎日少しずつ練習することで、頭の中で計算できる力が身につきます！",
    "body_html": """\
<h2>暗算力を高めるメリット</h2>
<ul>
  <li>テストで時間が余る</li>
  <li>日常生活（買い物・割り勘など）で役立つ</li>
  <li>頭のトレーニングになる</li>
  <li>複雑な計算の見通しが立てやすくなる</li>
</ul>

<h2>暗算のコツ①：補数を使う</h2>
<div class="formula-box"><p>98 ＋ 47 ＝ 100 ＋ 47 ー 2 ＝ 145</p></div>
<p>98を100とみて計算し、2を引く方法です。</p>

<h2>暗算のコツ②：分解して計算</h2>
<div class="formula-box"><p>37 ＋ 28 ＝ 37 ＋ 20 ＋ 8 ＝ 57 ＋ 8 ＝ 65</p></div>
<p>28を20と8に分けて、2段階で計算します。</p>

<h2>暗算のコツ③：九九の応用</h2>
<div class="formula-box"><p>15 × 4 ＝ 15 × 2 × 2 ＝ 30 × 2 ＝ 60</p></div>

<h2>暗算練習の進め方</h2>
<ol>
  <li>1桁の足し算・引き算を自動化</li>
  <li>2桁±1桁をすらすら言えるように</li>
  <li>2桁±2桁（繰り上がりなし→あり）へ</li>
  <li>かけ算・割り算の暗算へ</li>
</ol>
<div class="tip-box"><p>💡 毎日5分の暗算練習を2〜3か月続けると劇的に向上します。</p></div>""",
    "faq": [
      {"q": "暗算はいつから練習すべきですか？", "a": "1桁の足し算・引き算が確実にできる（小学1年生後半〜）から始めると効果的です。基礎計算が不安定なうちに暗算を急いでも定着しません。"},
      {"q": "暗算と筆算、どちらを優先すべきですか？", "a": "まず筆算で正確な計算手順を覚えることが先です。筆算が完璧になると暗算も自然と速くなります。"},
      {"q": "暗算が速い子と遅い子の違いは何ですか？", "a": "計算の自動化度合いの差です。速い子は「3＋7＝10」などが反射的に出てきます。繰り返しの練習量の違いが大きいです。"},
      {"q": "暗算練習に効果的なツールは？", "a": "フラッシュカード、計算アプリ、当サイトのようなデジタルドリルが効果的です。毎日少量継続が最重要です。"},
    ],
    "cta_href": "/",
    "cta_label": "計算ドリルで練習する",
    "related": [
      {"href": "/anzan-tips.html",      "emoji": "⚡", "text": "暗算のコツ"},
      {"href": "/keisan-hayaku.html",   "emoji": "⚡", "text": "計算を速くする方法"},
      {"href": "/mainichi-drill.html",  "emoji": "📅", "text": "毎日の計算練習法"},
      {"href": "/keisan-machigai.html", "emoji": "❌", "text": "計算ミスをなくす方法"},
    ],
  },

  {
    "filename": "tokei-yomikata.html",
    "title": "時計の読み方プリント【無料】幼児・保育園から始める時計学習",
    "description": "幼児・保育園向けの時計の読み方プリント。アナログ時計の針の読み方をスモールステップで練習できます。印刷不要・スマホ対応。",
    "h1": "時計の読み方プリント【無料】幼児から始める時計学習",
    "eyecatch": "🕐 「いま何時？」が読めると生活が変わります！幼児でも楽しく学べる時計の読み方ガイドです。",
    "body_html": """\
<h2>時計学習のステップ</h2>
<h3>ステップ1：針の名前を覚える</h3>
<ul>
  <li>みじかい針（時針）：「時」を示す</li>
  <li>ながい針（分針）：「分」を示す</li>
  <li>（秒針があれば）細い針：「秒」を示す</li>
</ul>

<h3>ステップ2：ちょうどの時刻を読む</h3>
<p>長い針が「12」を指しているとき → 「〇時ちょうど」</p>
<p>短い針が指す数字が「時」の数字です。</p>

<h3>ステップ3：30分を読む</h3>
<p>長い針が「6」を指しているとき → 「〇時半（30分）」</p>

<h3>ステップ4：5分刻みで読む</h3>
<p>1の目盛りが5分。長い針が「3」→15分、「9」→45分</p>

<h3>ステップ5：1分刻みで読む</h3>
<p>最終ゴール。目盛りを一つずつ数えて1分単位で読みます。</p>
<div class="tip-box"><p>💡 おもちゃの時計や本物の時計を動かしながら練習するのが最も効果的です。</p></div>
<div class="warn-box"><p>⚠️ 焦らずステップ1〜5を順番に。子どものペースに合わせましょう。</p></div>""",
    "faq": [
      {"q": "何歳から時計の読み方を教えますか？", "a": "「ちょうどの時刻」なら3〜4歳から始められます。本格的な分単位の読み方は小学1〜2年生が目安です。"},
      {"q": "デジタル時計とアナログ時計どちらを使うべきですか？", "a": "両方使えることが理想ですが、学習にはアナログ時計が向いています。時間の経過（針の動き）が視覚的に分かるためです。"},
      {"q": "時計の読み方をゲーム感覚で教えるには？", "a": "「今、針が何を指している？」「おやつの時間（3時）になったら教えて」などの声かけが効果的です。生活の中で自然に使う機会を作りましょう。"},
      {"q": "小学校でいつ習いますか？", "a": "1年生で「〇時・〇時半」、2年生で「〇時〇分」を習います。入学前に基礎を練習しておくと安心です。"},
    ],
    "cta_href": "/grade-1.html",
    "cta_label": "1年生のドリルをやってみる",
    "related": [
      {"href": "/jikan-yomikata.html", "emoji": "🕐", "text": "時計の読み方（小学生向け）"},
      {"href": "/jikan-keisan.html",   "emoji": "⏱️", "text": "時間の計算"},
      {"href": "/youji-kazu.html",     "emoji": "🔢", "text": "幼児向け数の学習"},
      {"href": "/nyuugaku-mae.html",   "emoji": "🎒", "text": "入学前の算数準備"},
    ],
  },

  {
    "filename": "kakezan-rensyu.html",
    "title": "かけ算練習プリント【無料】九九・2桁のかけ算総合問題",
    "description": "かけ算の総合練習プリント。九九から2桁×2桁まで印刷不要・スマホで練習できます。小学2〜4年生向け無料プリント。",
    "h1": "かけ算練習プリント【無料】小学2〜4年生",
    "eyecatch": "✖️ かけ算の基礎から応用まで総合練習！九九の復習から2桁の筆算まで幅広くカバーしています。",
    "body_html": """\
<h2>かけ算の学習ロードマップ</h2>
<ol>
  <li><strong>2年生：</strong>かけ算の意味・九九（1〜9の段）</li>
  <li><strong>3年生：</strong>かけ算の筆算（2桁×1桁）・0や1のかけ算</li>
  <li><strong>4年生：</strong>かけ算の筆算（2桁×2桁・3桁×2桁）</li>
</ol>

<h2>かけ算九九 確認テスト</h2>
<ul>
  <li>2の段：2×1〜2×9をすらすら言えますか？</li>
  <li>5の段・10の段：比較的覚えやすい段</li>
  <li>7の段・8の段：つまずきやすい難しい段</li>
  <li>逆から読む（9×□）も練習しましょう</li>
</ul>
<div class="tip-box"><p>💡 1日1段ずつ、声に出しながら練習するのが最も定着しやすい方法です。</p></div>

<h2>かけ算の性質（便利なルール）</h2>
<ul>
  <li>交換法則：3×4 ＝ 4×3</li>
  <li>結合法則：(2×3)×4 ＝ 2×(3×4)</li>
  <li>分配法則：5×(3＋2) ＝ 5×3 ＋ 5×2</li>
</ul>

<h2>よくある間違い</h2>
<ul>
  <li>九九の一部だけ覚えて残りを曖昧にする</li>
  <li>筆算で繰り上がりを忘れる</li>
  <li>0のかけ算（□×0＝0）を間違える</li>
</ul>
<div class="warn-box"><p>⚠️ 九九は全段・逆引きも含めて完璧にすることが目標です。部分的な習熟では後々困ります。</p></div>""",
    "faq": [
      {"q": "九九はどの段から覚えればいいですか？", "a": "2の段・5の段・10の段から始めるのが一般的です。これらは規則性が見えやすく覚えやすいです。"},
      {"q": "九九カードはどう使えばいいですか？", "a": "まず順番（2×1、2×2…）で答えを言えるようにし、次にランダムに引いても答えられるようにします。タイムを計って競争するのも効果的です。"},
      {"q": "7の段・8の段が覚えられません。", "a": "語呂合わせや歌が効果的です（例：7×8＝ごじゅうろく→「しちやごりょく」などの語呂）。また7×8＝8×7として8の段から覚えることも有効です。"},
      {"q": "かけ算の筆算でよく間違える原因は？", "a": "繰り上がりの書き忘れが最多です。繰り上がった数を問題の上に小さく書いてから計算する習慣をつけましょう。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/kuku-tips.html",      "emoji": "✖️", "text": "九九の覚え方ガイド"},
      {"href": "/kakizan-kiso.html",   "emoji": "✖️", "text": "かけ算の基礎"},
      {"href": "/kakizan-hissan.html", "emoji": "✖️", "text": "かけ算の筆算"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "warizan-rensyu.html",
    "title": "わり算練習プリント【無料】基礎から筆算まで総合問題",
    "description": "わり算の総合練習プリント。基礎のわり算からあまりのあるわり算・筆算まで印刷不要・スマホで練習できます。小学3〜4年生向け。",
    "h1": "わり算練習プリント【無料】小学3〜4年生",
    "eyecatch": "➗ わり算を総合的に練習！基礎から筆算まで段階的にステップアップできます。",
    "body_html": """\
<h2>わり算の学習ステップ</h2>
<ol>
  <li><strong>3年生前半：</strong>わり算の意味・九九を使ったわり算</li>
  <li><strong>3年生後半：</strong>あまりのあるわり算</li>
  <li><strong>4年生：</strong>わり算の筆算（2〜3桁÷1〜2桁）</li>
</ol>

<h2>わり算の確認テスト</h2>
<ul>
  <li>12÷4＝□ （九九の逆引き）</li>
  <li>15÷4＝□あまり□ （あまりあり）</li>
  <li>96÷3＝□ （筆算）</li>
  <li>126÷6＝□ （3桁÷1桁）</li>
</ul>
<div class="tip-box"><p>💡 検算（割る数×商＋あまり＝割られる数）を習慣化するとテストの点数が上がります。</p></div>

<h2>よくある間違いと対策</h2>
<ul>
  <li>商が0になる場合（例：306÷3）を間違える →「おろした数を割る数で割ると0」の処理</li>
  <li>あまりが割る数より大きくなる →「あまり＜割る数」を必ず確認</li>
  <li>筆算の「おろす」を忘れる →4ステップを必ず守る</li>
</ul>
<div class="warn-box"><p>⚠️ 「あまりは割る数より小さい」はわり算の鉄則。違う場合は商を修正しましょう。</p></div>""",
    "faq": [
      {"q": "わり算がなかなか速くなりません。", "a": "九九の習熟度が原因のことが多いです。わり算は九九の逆引きなので、九九を自動化することが先決です。"},
      {"q": "「0÷□」と「□÷0」の違いは？", "a": "0÷□＝0（0を何で割っても0）。□÷0は定義されていない（計算不可能）。この違いは重要です。"},
      {"q": "3桁÷2桁になると難しくなります。", "a": "商の見当づけが難しくなるためです。まず「2桁の上1桁÷割る数の上1桁」で大まかな見当をつけ、修正する練習をしましょう。"},
      {"q": "検算の習慣はいつから身につけるべきですか？", "a": "あまりのあるわり算を習うタイミング（小学3年生後半）から始めましょう。テストのミスを大幅に減らせます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-kiso.html",   "emoji": "➗", "text": "わり算の基礎"},
      {"href": "/warizan-amari.html",  "emoji": "➗", "text": "あまりのあるわり算"},
      {"href": "/warizan-hissan.html", "emoji": "➗", "text": "わり算の筆算"},
      {"href": "/grade-4-matome.html", "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "sansuu-ruuru.html",
    "title": "算数のルール・決まり【完全まとめ】小学生が知っておくべき公式",
    "description": "小学生が知っておくべき算数の公式・ルール・決まりをまとめた解説ページ。計算のきまりから図形公式まで一覧で確認できます。",
    "h1": "算数のルール・公式まとめ【小学生向け】",
    "eyecatch": "📋 算数には覚えておくべき大切なルールがたくさん！公式一覧で確認して苦手をなくしましょう。",
    "body_html": """\
<h2>計算のきまり</h2>
<ul>
  <li><strong>交換法則：</strong> a＋b＝b＋a、a×b＝b×a</li>
  <li><strong>結合法則：</strong> (a＋b)＋c＝a＋(b＋c)</li>
  <li><strong>分配法則：</strong> a×(b＋c)＝a×b＋a×c</li>
  <li><strong>計算の順序：</strong> ①（）の中 ②×÷ ③＋－ の順</li>
</ul>

<h2>面積の公式</h2>
<ul>
  <li>長方形：たて × よこ</li>
  <li>正方形：一辺 × 一辺</li>
  <li>三角形：底辺 × 高さ ÷ 2</li>
  <li>平行四辺形：底辺 × 高さ</li>
  <li>円：半径 × 半径 × 3.14</li>
</ul>

<h2>体積・単位</h2>
<ul>
  <li>直方体：たて × よこ × 高さ</li>
  <li>1L ＝ 1000cm³ ＝ 1000mL</li>
  <li>1km＝1000m、1kg＝1000g、1L＝1000mL</li>
</ul>

<h2>速さ・割合・比</h2>
<ul>
  <li>速さ＝距離÷時間</li>
  <li>距離＝速さ×時間</li>
  <li>割合＝比べる量÷もとにする量</li>
</ul>
<div class="tip-box"><p>💡 公式は丸暗記より「なぜそうなるか」を理解する方が長持ちします。</p></div>""",
    "faq": [
      {"q": "計算の順序（優先順位）のルールは？", "a": "①カッコの中を先に計算 ②×÷を先に計算 ③＋－を計算、の順です。「カッコ→掛け割り→足し引き」と覚えましょう。"},
      {"q": "分配法則はいつ使いますか？", "a": "計算を簡単にするとき（例：25×4＝25×2×2＝100）や、展開計算で使います。中学数学の多項式計算にもつながります。"},
      {"q": "算数の公式は全部覚えなければなりませんか？", "a": "よく使う公式は覚えると便利ですが、意味を理解していれば忘れても導き出せます。面積公式は図形の意味から理解することが大切です。"},
      {"q": "計算の順序を間違える場合の対策は？", "a": "問題を解く前に「×÷から」を意識してアンダーラインを引く習慣をつけましょう。慣れるまで手順を声に出すのも効果的です。"},
    ],
    "cta_href": "/",
    "cta_label": "ドリルで公式を練習する",
    "related": [
      {"href": "/keisan-hayaku.html",       "emoji": "⚡", "text": "計算を速くする方法"},
      {"href": "/menseki-sankakukei.html",  "emoji": "📐", "text": "三角形の面積"},
      {"href": "/wariai-guide.html",        "emoji": "📊", "text": "割合の求め方"},
      {"href": "/sokudo-guide.html",        "emoji": "🚀", "text": "速さの求め方"},
    ],
  },

  {
    "filename": "chuugaku-sansu-junbi.html",
    "title": "中学数学の準備【小学算数の総復習】入学前にやること",
    "description": "中学数学に向けて小学算数の何を復習すべきか解説。分数・割合・比例など中学数学の基礎になる単元を総まとめ。",
    "h1": "中学数学の準備｜小学算数の総復習ガイド",
    "eyecatch": "🎓 中学数学は小学算数の土台の上に成り立ちます。入学前に確認しておきたいポイントをまとめました！",
    "body_html": """\
<h2>中学数学に直結する小学算数の単元</h2>
<h3>①分数の計算（最重要）</h3>
<p>中学では分数を含む方程式・関数が頻出。通分・約分・分数の四則演算を完璧に。</p>
<h3>②比と割合</h3>
<p>中学の方程式・相似・確率の基礎。「比べる量÷もとにする量」の感覚を固める。</p>
<h3>③比例・反比例</h3>
<p>中学1年「関数」の直前の内容。グラフと式を結びつける練習をしておく。</p>
<h3>④速さ（距離・時間）</h3>
<p>中学数学の文章題で頻出。「はじき」の関係を確実に使えるようにする。</p>
<h3>⑤図形の性質</h3>
<p>三角形・平行四辺形・円の面積公式と合同・対称の性質を確認。</p>

<h2>入学前チェックリスト</h2>
<ul>
  <li>□ 分数の四則演算ができる</li>
  <li>□ 割合（%）の計算ができる</li>
  <li>□ 速さの公式を使える</li>
  <li>□ 面積の公式を全部言える</li>
  <li>□ 比の計算ができる</li>
  <li>□ 比例・反比例のグラフが読める</li>
</ul>
<div class="tip-box"><p>💡 小学6年生の2学期〜3学期が中学準備の最大のチャンスです。苦手単元を早めに解決しておきましょう。</p></div>""",
    "faq": [
      {"q": "中学数学で最初につまずく単元は？", "a": "「正負の数」と「文字式（方程式）」が最初の難関です。小学算数で分数・割合が得意な子はスムーズに進める傾向があります。"},
      {"q": "小学算数で特に重要な単元は何ですか？", "a": "分数の計算・割合・比例の3つが最重要です。これらが中学数学の文字式・方程式・関数の土台になります。"},
      {"q": "中学入学前に参考書・問題集は必要ですか？", "a": "小学算数の復習教材（特に5〜6年生の内容）は有効です。ただし無理な先取りより、小学内容の確実な習得を優先しましょう。"},
      {"q": "算数が苦手なまま中学に進んでも大丈夫ですか？", "a": "中学数学は小学算数の上に積み上がるため、苦手なまま進むと困難になります。特に分数計算が弱いと中学1年で大きくつまずきます。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルで総復習",
    "related": [
      {"href": "/chuugaku-junbi.html",  "emoji": "🎓", "text": "中学算数への準備ガイド"},
      {"href": "/grade-6-tips.html",    "emoji": "📚", "text": "6年生の算数 完全ガイド"},
      {"href": "/bunsuu-warizan.html",  "emoji": "½", "text": "分数のわり算"},
      {"href": "/wariai-guide.html",    "emoji": "📊", "text": "割合の求め方"},
    ],
  },


  # ────────────────────────────────
  # 図形
  # ────────────────────────────────
  {
    "filename": "sankakkei-shurui.html",
    "title": "三角形の種類プリント【無料】正三角形・二等辺三角形・直角三角形",
    "description": "三角形の種類（正三角形・二等辺三角形・直角三角形）を印刷不要・スマホで練習できる無料プリント。見分け方と性質を解説。小学3〜4年生向け。",
    "h1": "三角形の種類プリント【無料】小学3〜4年生",
    "eyecatch": "📐 三角形には3種類ある！辺の長さと角度の特徴を覚えて図形問題を得意にしましょう。",
    "body_html": """\
<h2>三角形の3つの種類</h2>
<h3>①正三角形</h3>
<p>3辺の長さがすべて等しい。3つの角もすべて60°。</p>
<div class="tip-box"><p>💡 正三角形は「正」がつく通り最も均整のとれた三角形です。</p></div>
<h3>②二等辺三角形</h3>
<p>2辺の長さが等しい三角形。等しい辺の間の角（底角）も等しい。</p>
<h3>③直角三角形</h3>
<p>1つの角が直角（90°）の三角形。直角の反対の辺を斜辺という。</p>
<h2>三角形の内角の和</h2>
<div class="formula-box"><p>三角形の3つの角の合計 ＝ 180°</p></div>
<p>どんな三角形でも3つの角を足すと必ず180°になります。</p>
<h2>見分け方のポイント</h2>
<ul>
  <li>コンパスで辺の長さを比べる</li>
  <li>分度器で角の大きさを測る</li>
  <li>直角の確認は三角定規を使う</li>
</ul>""",
    "faq": [
      {"q": "三角形の種類はいつ習いますか？", "a": "小学2〜3年生で習います。正三角形・二等辺三角形・直角三角形の3種類と、それぞれの性質を学びます。"},
      {"q": "内角の和が180°になる理由は？", "a": "三角形を切り取って3つの角を1か所に集めると直線（180°）になることで確認できます。"},
      {"q": "直角三角形に二等辺三角形はありますか？", "a": "はい、二等辺直角三角形（直角三角定規の形）があります。2つの鋭角がどちらも45°です。"},
      {"q": "正三角形は二等辺三角形ですか？", "a": "はい、正三角形は3辺すべてが等しいので、どの2辺を選んでも等しく、二等辺三角形の特別な形です。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/sankakkei-shikaku.html",  "emoji": "📐", "text": "三角形と四角形"},
      {"href": "/menseki-sankakukei.html", "emoji": "📐", "text": "三角形の面積"},
      {"href": "/kakudo-guide.html",       "emoji": "📐", "text": "角度の学習"},
      {"href": "/grade-3-matome.html",     "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "shikakkei-seishitsu.html",
    "title": "四角形の種類と性質プリント【無料】正方形・長方形・平行四辺形",
    "description": "四角形の種類（正方形・長方形・平行四辺形・ひし形・台形）と性質を印刷不要・スマホで練習できる無料プリント。小学4年生向け。",
    "h1": "四角形の種類と性質プリント【無料】小学4年生",
    "eyecatch": "📐 四角形にはたくさんの種類がある！それぞれの特徴と関係を整理して覚えましょう。",
    "body_html": """\
<h2>四角形の種類</h2>
<ul>
  <li><strong>正方形：</strong>4辺等しく、4角すべて90°</li>
  <li><strong>長方形：</strong>4角すべて90°（向かい合う辺が等しい）</li>
  <li><strong>平行四辺形：</strong>向かい合う辺が平行かつ等しい</li>
  <li><strong>ひし形：</strong>4辺がすべて等しい（角は90°でなくてよい）</li>
  <li><strong>台形：</strong>1組の向かい合う辺だけが平行</li>
</ul>
<div class="formula-box"><p>四角形の内角の和 ＝ 360°</p></div>
<div class="tip-box"><p>💡 正方形は「長方形でもあり、ひし形でもある」特別な四角形です。</p></div>
<h2>見分け方のポイント</h2>
<ul>
  <li>向かい合う辺が平行か → 平行四辺形・長方形・正方形・ひし形</li>
  <li>すべての辺が等しいか → 正方形・ひし形</li>
  <li>すべての角が直角か → 正方形・長方形</li>
</ul>
<h2>対角線の性質</h2>
<ul>
  <li>長方形・正方形：対角線が等しく、互いに2等分する</li>
  <li>ひし形：対角線が垂直に交わり、互いに2等分する</li>
  <li>正方形：どちらの性質もある</li>
</ul>""",
    "faq": [
      {"q": "四角形の種類はいつ習いますか？", "a": "正方形・長方形は小学2年生、平行四辺形・ひし形・台形は小学4年生で学習します。"},
      {"q": "正方形は長方形の特別な形ですか？", "a": "はい、正方形はすべての角が直角という長方形の条件を満たしています。正方形⊂長方形の関係です。"},
      {"q": "台形の面積公式は？", "a": "（上底＋下底）×高さ÷2です。上底と下底が平行な2辺です。小学4〜5年生で学びます。"},
      {"q": "四角形の内角の和が360°になる理由は？", "a": "四角形は対角線で2つの三角形に分けられます。三角形の内角の和180°×2＝360°です。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/suichoku-heiko.html",         "emoji": "📐", "text": "垂直・平行と四角形"},
      {"href": "/menseki-heikoushikakkei.html","emoji": "📐", "text": "平行四辺形の面積"},
      {"href": "/sankakkei-shurui.html",       "emoji": "📐", "text": "三角形の種類"},
      {"href": "/grade-4-matome.html",         "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "en-chokukei.html",
    "title": "円と直径の関係プリント【無料】円周・直径・半径の計算｜小学3〜6年生",
    "description": "円の円周・直径・半径の関係を印刷不要・スマホで練習できる無料プリント。円周率3.14の使い方から面積まで解説。",
    "h1": "円と直径の関係プリント【無料】小学3〜6年生",
    "eyecatch": "⭕ 円は算数で何度も登場する図形。直径・半径・円周の関係をしっかりマスターしましょう！",
    "body_html": """\
<h2>円の各部分の名前</h2>
<ul>
  <li><strong>中心：</strong>円の真ん中の点</li>
  <li><strong>半径：</strong>中心から円周上の点までの距離（半径＝直径÷2）</li>
  <li><strong>直径：</strong>円の中心を通る最も長い弦（直径＝半径×2）</li>
  <li><strong>円周：</strong>円の周りの長さ</li>
</ul>
<div class="formula-box"><p>円周 ＝ 直径 × 3.14（π）</p></div>
<div class="tip-box"><p>💡 直径と半径の関係：直径＝半径×2、半径＝直径÷2。問題文で与えられるのが直径か半径かを必ず確認。</p></div>
<h2>円周率3.14</h2>
<p>円周率（π）は3.14159…の無限に続く数。小学校では3.14を使います。</p>
<ul>
  <li>直径10cmの円の円周：10×3.14＝31.4cm</li>
  <li>半径5cmの円の円周：5×2×3.14＝31.4cm</li>
</ul>
<h2>円の面積</h2>
<div class="formula-box"><p>円の面積 ＝ 半径 × 半径 × 3.14</p></div>
<div class="warn-box"><p>⚠️ 円周は「直径×3.14」、面積は「半径×半径×3.14」。使う長さが違います。</p></div>""",
    "faq": [
      {"q": "円の学習はいつ習いますか？", "a": "円の基礎（直径・半径・中心）は小学3年生、円周と円周率は小学5年生、円の面積は小学6年生で学習します。"},
      {"q": "円周率が3.14の理由は？", "a": "どんな大きさの円でも「円周÷直径＝約3.14159…」になります。この一定の比率が円周率（π）で、小学校では3.14で近似します。"},
      {"q": "3.14の計算でよく使う数を教えてください。", "a": "3.14×2＝6.28、×3＝9.42、×4＝12.56、×5＝15.7、×10＝31.4。これらを覚えておくと計算が速くなります。"},
      {"q": "おうぎ形の円周（弧の長さ）は？", "a": "弧の長さ＝円周×（中心角÷360°）。中心角90°の場合は円周×1/4です。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/menseki-enza.html",   "emoji": "📐", "text": "円の面積"},
      {"href": "/kakudo-guide.html",   "emoji": "📐", "text": "角度の学習"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # 数の性質
  # ────────────────────────────────
  {
    "filename": "gusuu-kisuu.html",
    "title": "偶数と奇数プリント【無料】見分け方と性質｜小学5年生",
    "description": "偶数・奇数の見分け方と性質を印刷不要・スマホで練習できる無料プリント。計算での活用まで解説。小学5年生向け。",
    "h1": "偶数と奇数プリント【無料】小学5年生",
    "eyecatch": "🔢 偶数と奇数の区別は数の性質の基本。「2で割り切れるか」という判断が様々な場面で役立ちます！",
    "body_html": """\
<h2>偶数・奇数の定義</h2>
<div class="formula-box"><p>偶数：2で割り切れる整数（0, 2, 4, 6, 8, 10, …）<br>奇数：2で割り切れない整数（1, 3, 5, 7, 9, 11, …）</p></div>
<div class="tip-box"><p>💡 一の位が0・2・4・6・8なら偶数、1・3・5・7・9なら奇数。一の位だけ見れば分かります。</p></div>
<h2>偶数・奇数の計算での性質</h2>
<ul>
  <li>偶数＋偶数＝偶数、奇数＋奇数＝偶数</li>
  <li>偶数＋奇数＝奇数</li>
  <li>偶数×偶数＝偶数、偶数×奇数＝偶数、奇数×奇数＝奇数</li>
</ul>
<h2>0は偶数？奇数？</h2>
<p>0は偶数です。0÷2＝0で割り切れるため偶数に分類されます。</p>
<h2>よく出る問題</h2>
<ul>
  <li>「1から20までの偶数をすべて書く」</li>
  <li>「奇数と偶数どちらが多いか」</li>
  <li>「2つの数の和が偶数か奇数か」</li>
</ul>""",
    "faq": [
      {"q": "偶数・奇数はいつ習いますか？", "a": "小学5年生で正式に学習します。ただし2年生の九九のころから「2の倍数」として偶数の概念に触れています。"},
      {"q": "負の数（−2, −3など）にも偶数・奇数はありますか？", "a": "数学的には負の数にも偶数・奇数の概念があります（−2は偶数、−3は奇数）。ただし小学校では正の整数の範囲で学びます。"},
      {"q": "0は偶数ですか？", "a": "0は偶数です。0÷2＝0でwhoあまりがないため偶数に分類されます。"},
      {"q": "偶数×奇数の結果はなぜ偶数ですか？", "a": "偶数は「2×整数」と表せるため、何をかけても2の倍数（偶数）になります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/baisuu-yakusuu.html", "emoji": "🔢", "text": "倍数と約数"},
      {"href": "/ookina-kazu.html",    "emoji": "🔢", "text": "大きな数"},
      {"href": "/gaisuu-guide.html",   "emoji": "🔢", "text": "がい数（四捨五入）"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "sosuu-guide.html",
    "title": "素数とは何か【わかりやすく解説】小学〜中学準備",
    "description": "素数（2・3・5・7・11…）の定義と求め方をわかりやすく解説。エラトステネスのふるいも紹介。小学高学年〜中学準備向け。",
    "h1": "素数とは何か？わかりやすく解説",
    "eyecatch": "🔢 素数は数の世界の「基本的な構成要素」。算数・数学の世界で大切な概念を理解しましょう！",
    "body_html": """\
<h2>素数の定義</h2>
<p>素数とは「1とその数自身以外に約数を持たない2以上の整数」のことです。</p>
<div class="formula-box"><p>素数：2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47 …</p></div>
<div class="tip-box"><p>💡 1は素数ではありません。素数は2から始まります。2は唯一の偶数の素数です。</p></div>
<h2>素数の判定方法</h2>
<p>2・3・5・7で割り切れなければ、50以下の数は素数です。</p>
<ul>
  <li>2で割り切れる → 偶数（2以外は素数でない）</li>
  <li>各位の和が3の倍数 → 3で割り切れる</li>
  <li>一の位が0か5 → 5で割り切れる</li>
</ul>
<h2>エラトステネスのふるい（素数を全部見つける方法）</h2>
<ol>
  <li>2以上の数を並べる</li>
  <li>2を残して2の倍数（4,6,8…）を消す</li>
  <li>3を残して3の倍数（6,9,12…）を消す</li>
  <li>5→7の順で繰り返す</li>
  <li>残った数がすべて素数</li>
</ol>
<h2>素因数分解</h2>
<p>どんな整数も素数の積に分解できます。例：12＝2×2×3＝2²×3</p>""",
    "faq": [
      {"q": "素数は小学校で習いますか？", "a": "正式には中学以降ですが、約数・倍数（小学5年生）の発展として小学高学年で紹介されることがあります。"},
      {"q": "1が素数でない理由は？", "a": "素数の定義「1とその数自身の2つの約数を持つ」に対し、1の約数は1つだけ（1のみ）なので除外されます。"},
      {"q": "2が唯一の偶数の素数なのはなぜ？", "a": "2以外の偶数はすべて2で割り切れるため、2という約数を持ちます。つまり2以外の偶数は「1・2・その数」の3つ以上の約数を持ち素数ではありません。"},
      {"q": "素数は無限にありますか？", "a": "はい、素数は無限に存在します。古代ギリシャのユークリッドがこれを証明しました。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/baisuu-yakusuu.html", "emoji": "🔢", "text": "倍数と約数"},
      {"href": "/gusuu-kisuu.html",    "emoji": "🔢", "text": "偶数と奇数"},
      {"href": "/chuugaku-junbi.html", "emoji": "🎓", "text": "中学数学への準備"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  {
    "filename": "saishou-koubaisu.html",
    "title": "最小公倍数の求め方プリント【無料】LCMの計算方法｜小学5年生",
    "description": "最小公倍数（LCM）の求め方を印刷不要・スマホで練習できる無料プリント。2数・3数の最小公倍数を丁寧に解説。小学5年生向け。",
    "h1": "最小公倍数の求め方プリント【無料】小学5年生",
    "eyecatch": "🔢 最小公倍数は通分に欠かせない概念！確実に求める方法を覚えましょう。",
    "body_html": """\
<h2>最小公倍数（LCM）とは</h2>
<p>2つ以上の整数に共通する倍数のうち、最も小さいものです。</p>
<h2>求め方①：倍数を列挙する方法</h2>
<div class="formula-box"><p>4の倍数：4,8,12,16,20,24…<br>6の倍数：6,12,18,24,30…<br>最小公倍数 ＝ 12</p></div>
<h2>求め方②：連除法（素因数分解）</h2>
<p>2数を同じ素数で割り続けて求める方法。数が大きい場合に便利です。</p>
<div class="formula-box"><p>4と6の最小公倍数：4＝2²、6＝2×3 → LCM＝2²×3＝12</p></div>
<div class="tip-box"><p>💡 通分するときは分母の最小公倍数を使うと計算が最もシンプルになります。</p></div>
<h2>3つの数の最小公倍数</h2>
<p>3つの数でも同じ方法で求められます。2つずつ求めてから最終的な公倍数を出す方法も有効です。</p>
<h2>最大公約数との関係</h2>
<div class="formula-box"><p>LCM(a,b) × GCD(a,b) ＝ a × b</p></div>""",
    "faq": [
      {"q": "最小公倍数はいつ習いますか？", "a": "小学4〜5年生で学習します。分数の通分（5年生）で必須の知識になります。"},
      {"q": "最小公倍数と最大公約数の違いは？", "a": "最小公倍数（LCM）は共通する倍数の最小値、最大公約数（GCD）は共通する約数の最大値です。通分にLCM、約分にGCDを使います。"},
      {"q": "3・4・6の最小公倍数は？", "a": "3の倍数：3,6,9,12… 4の倍数：4,8,12… 6の倍数：6,12… 最初に3つ全部の倍数になるのは12です。"},
      {"q": "最小公倍数の使い道は？", "a": "分数の通分（異分母を合わせる）で使います。また公倍数を求める文章題（「○日おきに重なる日はいつ？」など）でも使います。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/saidai-kouyakusuu.html","emoji": "🔢", "text": "最大公約数の求め方"},
      {"href": "/baisuu-yakusuu.html",   "emoji": "🔢", "text": "倍数と約数"},
      {"href": "/bunsuu-tsuubun.html",   "emoji": "½", "text": "通分のやり方"},
      {"href": "/grade-5-matome.html",   "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "saidai-kouyakusuu.html",
    "title": "最大公約数の求め方プリント【無料】GCDの計算方法｜小学5年生",
    "description": "最大公約数（GCD）の求め方を印刷不要・スマホで練習できる無料プリント。2数の最大公約数をユークリッド互除法まで解説。小学5年生向け。",
    "h1": "最大公約数の求め方プリント【無料】小学5年生",
    "eyecatch": "🔢 最大公約数は約分の核心！確実な求め方を覚えて分数計算をスムーズにしましょう。",
    "body_html": """\
<h2>最大公約数（GCD）とは</h2>
<p>2つ以上の整数に共通する約数のうち、最も大きいものです。</p>
<h2>求め方①：約数を全部書き出す</h2>
<div class="formula-box"><p>12の約数：1,2,3,4,6,12<br>18の約数：1,2,3,6,9,18<br>最大公約数 ＝ 6</p></div>
<h2>求め方②：連除法</h2>
<p>共通する素因数で割り続け、商の積を求める方法。</p>
<div class="formula-box"><p>12と18を2で割る→6と9、次に3で割る→2と3（公約数なし）<br>GCD ＝ 2×3 ＝ 6</p></div>
<div class="tip-box"><p>💡 約分するとき、分子・分母の最大公約数で割ると一回で最も簡単な形になります。</p></div>
<h2>互いに素（GCD＝1）</h2>
<p>最大公約数が1の2つの整数を「互いに素」といいます。例：3と5、7と8など。</p>""",
    "faq": [
      {"q": "最大公約数はいつ習いますか？", "a": "小学5年生で学習します。分数の約分や通分で必須の知識です。"},
      {"q": "大きい数の最大公約数はどう求めますか？", "a": "連除法（共通の素因数で割る）か、ユークリッド互除法（大きい方を小さい方で割りあまりで繰り返す）が効率的です。"},
      {"q": "最大公約数が1の場合は？", "a": "「互いに素」といいます。この場合、その2数を持つ分数はすでに最も簡単な形（既約分数）です。"},
      {"q": "3つの数の最大公約数は？", "a": "2つずつ求めてから最終的なGCDを出す方法が分かりやすいです。例：GCD(12,18,24)→GCD(12,18)＝6、GCD(6,24)＝6。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/saishou-koubaisu.html","emoji": "🔢", "text": "最小公倍数の求め方"},
      {"href": "/baisuu-yakusuu.html",  "emoji": "🔢", "text": "倍数と約数"},
      {"href": "/bunsuu-yakubun.html",  "emoji": "½", "text": "約分のやり方"},
      {"href": "/grade-5-matome.html",  "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  # ────────────────────────────────
  # テスト・学習サポート記事
  # ────────────────────────────────
  {
    "filename": "tesuto-naoshi.html",
    "title": "テストの直し方【完全ガイド】点数を上げる見直し方法",
    "description": "算数テストの効果的な直し方を解説。ただ答えを写すだけではなく、理解につながるテスト直しの方法を紹介します。",
    "h1": "算数テストの直し方【点数を上げる方法】",
    "eyecatch": "📝 テスト直しは「正しい方法」でやれば最強の学習ツール。ただ答えを写すだけでは意味がありません！",
    "body_html": """\
<h2>NG なテスト直し</h2>
<ul>
  <li>❌ 答えだけ赤で写す</li>
  <li>❌ なぜ間違えたか考えない</li>
  <li>❌ 直しをそのままにして見直さない</li>
</ul>
<h2>正しいテスト直しの5ステップ</h2>
<ol>
  <li><strong>間違いを分類する：</strong>計算ミス・理解不足・問題読み違い のどれか</li>
  <li><strong>解説を読む：</strong>なぜその答えになるかを確認する</li>
  <li><strong>自分で解き直す：</strong>解説を見ずに自分で解き直す</li>
  <li><strong>ミスノートに記録：</strong>間違えた問題と「なぜ間違えたか」を書く</li>
  <li><strong>1週間後に再チャレンジ：</strong>ミスノートを見て再度解く</li>
</ol>
<div class="tip-box"><p>💡 「計算ミス」と「理解不足」では対策が違います。計算ミスは練習量、理解不足は概念の再学習が必要です。</p></div>
<h2>ミスノートの作り方</h2>
<ul>
  <li>問題・自分の答え・正しい答え・理由を書く</li>
  <li>1冊のノートにまとめる（科目ごとでもOK）</li>
  <li>テスト前に読み返す習慣をつける</li>
</ul>
<div class="warn-box"><p>⚠️ テスト直しをしない子は同じミスを繰り返します。直しは面倒でも最強の復習になります。</p></div>""",
    "faq": [
      {"q": "テスト直しはいつするのがベストですか？", "a": "返却されたその日（遅くても翌日）が最適です。問題を解いた記憶が残っているうちに直すと効果が上がります。"},
      {"q": "ミスノートは本当に効果がありますか？", "a": "効果的です。自分がよくするミスのパターンが可視化され、テスト前に確認することで同じミスを防げます。"},
      {"q": "計算ミスと理解不足の見分け方は？", "a": "同じ問題をもう一度解いて正解できれば計算ミス、再度間違えたり解き方が分からなければ理解不足です。"},
      {"q": "テスト直しに何分くらいかければいいですか？", "a": "テスト全体を通じて30〜45分を目安に。間違えた問題数によりますが、1問あたり5〜10分かけてしっかり理解することが大切です。"},
    ],
    "cta_href": "/sansu-test-taisaku.html",
    "cta_label": "テスト対策をはじめる",
    "related": [
      {"href": "/sansu-test-taisaku.html", "emoji": "📝", "text": "算数テスト対策"},
      {"href": "/tesuto-100ten.html",       "emoji": "💯", "text": "テストで100点を取る方法"},
      {"href": "/keisan-machigai.html",     "emoji": "❌", "text": "計算ミスをなくす方法"},
      {"href": "/mainichi-drill.html",      "emoji": "📅", "text": "毎日の計算練習法"},
    ],
  },

  {
    "filename": "note-torikumi.html",
    "title": "算数のノートの取り方【コツと書き方】成績が上がるノート術",
    "description": "算数のノートを効果的に使う方法を解説。きれいに書くコツ・計算の書き方・見直しやすいノートの作り方を紹介します。",
    "h1": "算数のノートの取り方【成績が上がるノート術】",
    "eyecatch": "📓 ノートの使い方を変えるだけで算数の理解が深まります。シンプルだけど効果的な方法を紹介！",
    "body_html": """\
<h2>算数ノートの基本ルール</h2>
<ul>
  <li>1つの問題に十分なスペースを取る（詰め込まない）</li>
  <li>必ず式を書いてから計算する</li>
  <li>答えは必ず単位をつける</li>
  <li>間違えた場合は消さずに×をつけて下に正しい解答を書く</li>
</ul>
<div class="tip-box"><p>💡 方眼ノートを使うと位がそろいやすく、筆算の間違いが減ります。</p></div>
<h2>計算の書き方のコツ</h2>
<ul>
  <li>筆算は位をそろえて書く（方眼を活用）</li>
  <li>繰り上がり・繰り下がりは必ず書く</li>
  <li>文章題は「式→計算→答え」の形式で書く</li>
  <li>大きく、はっきりと書く（小さい字は採点ミスの原因に）</li>
</ul>
<h2>復習しやすいノートの工夫</h2>
<ul>
  <li>日付・ページ・単元名を必ず書く</li>
  <li>重要な公式や間違えた問題に付箋・マーカーをつける</li>
  <li>余白に「なぜ？」メモを書く（公式の理由など）</li>
</ul>
<h2>NGなノートの書き方</h2>
<ul>
  <li>❌ 式を書かず計算だけ書く</li>
  <li>❌ 消しゴムで全部消してしまう（間違いの記録が消える）</li>
  <li>❌ 小さすぎて読めない字で書く</li>
</ul>""",
    "faq": [
      {"q": "算数ノートは方眼と罫線どちらがいいですか？", "a": "算数は方眼ノートがおすすめです。数字の位がそろいやすく、筆算や図形のスケッチにも便利です。"},
      {"q": "間違えた問題は消すべきですか？", "a": "消さないほうが良いです。×印をつけて残しておき、その下に正しい解答を書く方が後で見直せます。"},
      {"q": "ノートを見やすくするために何が大切ですか？", "a": "1問1スペース（詰め込まない）、日付・単元名の記入、式→答えの流れを統一することが見やすさの基本です。"},
      {"q": "計算ミスが多い子はノートの書き方に問題がありますか？", "a": "関係することが多いです。位がずれた筆算、小さすぎる数字、繰り上がりを書かないなどが計算ミスの原因になります。"},
    ],
    "cta_href": "/keisan-machigai.html",
    "cta_label": "計算ミスをなくす方法",
    "related": [
      {"href": "/keisan-machigai.html",     "emoji": "❌", "text": "計算ミスをなくす方法"},
      {"href": "/tesuto-naoshi.html",        "emoji": "📝", "text": "テストの直し方"},
      {"href": "/sansu-benkyou-houhou.html", "emoji": "📖", "text": "算数の効果的な勉強法"},
      {"href": "/mainichi-drill.html",       "emoji": "📅", "text": "毎日の計算練習法"},
    ],
  },

  {
    "filename": "shukudai-kanri.html",
    "title": "算数の宿題を効率よくこなす方法【保護者向けガイド】",
    "description": "算数の宿題を効率よくこなす方法を解説。計画の立て方・集中する環境の作り方・子どもへの声かけのコツを紹介。保護者向けガイド。",
    "h1": "算数の宿題を効率よくこなす方法【保護者向け】",
    "eyecatch": "📋 宿題を効率よく終わらせて、理解も深める方法があります。保護者ができるサポートを紹介！",
    "body_html": """\
<h2>宿題を効率よく終わらせる3つのコツ</h2>
<h3>①時間と場所を決める</h3>
<p>「帰ったら30分」「ダイニングテーブルで」など習慣化が最重要。毎日同じ時間・場所にすると自然に取り組めるようになります。</p>
<h3>②難しい問題から始めない</h3>
<p>得意な問題・簡単な問題から始めてエンジンをかけてから、難しい問題に取り組みます。</p>
<h3>③見守りと適切なサポート</h3>
<p>すぐ答えを教えず「どこが分からない？」「何の問題だったっけ？」と問いかけて考えさせましょう。</p>
<div class="tip-box"><p>💡 「できた！」という達成感を毎日積み重ねることが算数好きへの近道です。</p></div>
<h2>よくある宿題トラブルと対策</h2>
<ul>
  <li><strong>「算数の宿題だけ時間がかかる」：</strong>つまずき単元を特定して重点復習</li>
  <li><strong>「宿題をやらない」：</strong>小さな目標（3問だけ）から始める</li>
  <li><strong>「写してしまう」：</strong>解いた後に口頭で説明させる</li>
</ul>
<h2>保護者がしてはいけないこと</h2>
<ul>
  <li>怒りながら教える（算数嫌いの原因に）</li>
  <li>全問題を一緒にやってしまう</li>
  <li>「なんでこれが分からないの」という言葉</li>
</ul>""",
    "faq": [
      {"q": "宿題に何時間もかかる場合はどうすれば？", "a": "全問解こうとせず、まず苦手な問題の見極めを。理解できていない単元に戻って学習し直す必要があります。宿題時間が長すぎる場合は先生に相談しましょう。"},
      {"q": "子どもが宿題中にスマホを触ってしまいます。", "a": "宿題中はスマホをリビングに置く、または見えない場所に片付けるなど物理的な対策が最も効果的です。"},
      {"q": "保護者が算数が苦手な場合の教え方は？", "a": "「一緒に考えよう」というスタンスが大切です。教科書や当サイトの解説を一緒に読んで考える姿勢は子どもにも良い影響を与えます。"},
      {"q": "宿題をやらせるより塾に行かせた方がいいですか？", "a": "まず自宅での学習習慣を作ることが先決です。宿題をこなす習慣が塾でも活きます。塾は補助的な手段として考えましょう。"},
    ],
    "cta_href": "/shukudai-oshiekata.html",
    "cta_label": "算数の教え方ガイド",
    "related": [
      {"href": "/shukudai-oshiekata.html", "emoji": "📝", "text": "算数の宿題の教え方"},
      {"href": "/oyako-sansu.html",        "emoji": "👨‍👩‍👧", "text": "親子で楽しむ算数"},
      {"href": "/sansu-benkyou-houhou.html","emoji": "📖", "text": "算数の効果的な勉強法"},
      {"href": "/mainichi-drill.html",     "emoji": "📅", "text": "毎日の計算練習法"},
    ],
  },

  {
    "filename": "nyuusi-sansu.html",
    "title": "中学受験の算数対策【小学生向け基礎固めガイド】",
    "description": "中学受験を目指す小学生向けに、算数の基礎固めの方法と受験頻出単元を解説。無料ドリルを活用した対策法を紹介。",
    "h1": "中学受験の算数対策｜小学生の基礎固めガイド",
    "eyecatch": "🎯 中学受験の算数は「基礎の完璧な習熟」が土台。まず教科書レベルを完璧にすることから始めましょう！",
    "body_html": """\
<h2>中学受験算数の特徴</h2>
<ul>
  <li>小学校の全単元から出題（広い範囲）</li>
  <li>応用問題・文章題が中心</li>
  <li>時間配分のスキルも必要</li>
  <li>計算力・論理的思考力・図形センスが問われる</li>
</ul>
<h2>基礎固めで最重要な単元</h2>
<h3>計算系</h3>
<ul>
  <li>四則演算（特に分数・小数を含む計算）</li>
  <li>計算のきまり（交換・結合・分配法則）</li>
</ul>
<h3>文章題系</h3>
<ul>
  <li>割合・比・速さ（3大頻出単元）</li>
  <li>面積・体積の応用</li>
  <li>場合の数・確率</li>
</ul>
<h3>図形系</h3>
<ul>
  <li>面積・体積の公式と応用</li>
  <li>角度の計算</li>
  <li>相似・拡大縮小</li>
</ul>
<div class="tip-box"><p>💡 受験勉強を始める前に「学校の算数を完璧に」することが最優先。教科書レベルが不完全では受験問題は解けません。</p></div>
<h2>効果的な学習の流れ</h2>
<ol>
  <li>教科書レベルの完全習得（5年生まで）</li>
  <li>苦手単元の集中攻略</li>
  <li>応用問題・過去問演習</li>
</ol>""",
    "faq": [
      {"q": "中学受験算数はいつから準備すべきですか？", "a": "本格的な受験勉強は小学3〜4年生からが一般的です。ただし「学校の算数の完全習得」はそれ以前から意識しましょう。"},
      {"q": "受験算数と学校算数は何が違いますか？", "a": "学校算数は基礎概念の習得が目的、受験算数は応用・発展問題の解法習得が目的です。受験算数は学校算数の完璧な習得なしには取り組めません。"},
      {"q": "受験算数で最も差がつく単元は？", "a": "割合・速さ・比の3単元です。これらは概念が難しく、対策できているかどうかで大きく差がつきます。"},
      {"q": "塾なしで中学受験に臨めますか？", "a": "可能ですが、難関校ほど専門的な指導が有効です。まず基礎を当サイトのようなドリルで固め、上位校を目指す場合は専門機関の利用を検討しましょう。"},
    ],
    "cta_href": "/sansu-test-taisaku.html",
    "cta_label": "テスト対策を始める",
    "related": [
      {"href": "/chuugaku-junbi.html",     "emoji": "🎓", "text": "中学数学への準備"},
      {"href": "/wariai-guide.html",       "emoji": "📊", "text": "割合の求め方"},
      {"href": "/sokudo-guide.html",       "emoji": "🚀", "text": "速さの求め方"},
      {"href": "/sansu-benkyou-houhou.html","emoji": "📖", "text": "算数の効果的な勉強法"},
    ],
  },

  {
    "filename": "fuyu-benkyou.html",
    "title": "冬休みの算数勉強計画【学年別おすすめ復習法】",
    "description": "冬休みの算数勉強計画を学年別に紹介。2学期の復習と3学期の予習をバランスよく進める方法をまとめました。",
    "h1": "冬休みの算数勉強計画【学年別おすすめ復習法】",
    "eyecatch": "❄️ 冬休みは2学期の総復習と3学期の準備ができる大切な時期。計画的に学習して3学期を有利に始めましょう！",
    "body_html": """\
<h2>冬休みの算数学習の優先順位</h2>
<ol>
  <li><strong>2学期の苦手単元の復習（最優先）：</strong>定着していない単元は冬休みに固める</li>
  <li><strong>計算の基礎練習（毎日）：</strong>短時間でも毎日継続</li>
  <li><strong>3学期の予習（余裕があれば）：</strong>教科書の次の単元を先読み</li>
</ol>
<h2>学年別 冬休みの重点単元</h2>
<h3>1〜2年生</h3>
<p>繰り上がり・繰り下がりの計算、九九（2年生）の完全習熟</p>
<h3>3〜4年生</h3>
<p>わり算の筆算、小数・分数の基礎、角度の計算</p>
<h3>5〜6年生</h3>
<p>割合・速さ・比の復習（3学期・受験に備えて）</p>
<div class="tip-box"><p>💡 冬休みの学習時間は1日30〜45分が目安。お正月も含めて毎日続けることが重要です。</p></div>
<h2>冬休みの学習スケジュール例（小学4年生）</h2>
<ul>
  <li>12月下旬：わり算の筆算の復習（5日間）</li>
  <li>12月〜1月：小数のたし算・ひき算（3日間）</li>
  <li>1月上旬：角度の問題（3日間）</li>
  <li>毎日：計算ドリル（基礎10問）</li>
</ul>""",
    "faq": [
      {"q": "冬休みの算数学習は何時間すべきですか？", "a": "1日30〜45分が適切です。長時間より毎日継続することが重要で、お正月も短時間でも続けましょう。"},
      {"q": "何から始めれば良いですか？", "a": "まず2学期のテストや宿題を見返して、間違いが多かった単元を確認します。その単元から復習を始めましょう。"},
      {"q": "遊びも大事では？", "a": "はい、冬休みは学習だけでなく休息も大切です。午前中に勉強して午後は遊ぶなど、めりはりをつけましょう。"},
      {"q": "市販の冬休み用ドリルは必要ですか？", "a": "当サイトのような無料オンラインドリルを活用すれば追加購入不要です。苦手単元を集中的に練習できます。"},
    ],
    "cta_href": "/",
    "cta_label": "冬休みの練習を始める",
    "related": [
      {"href": "/fuyu-sansu.html",          "emoji": "❄️", "text": "冬の算数問題"},
      {"href": "/sansu-benkyou-houhou.html", "emoji": "📖", "text": "算数の効果的な勉強法"},
      {"href": "/keisan-machigai.html",      "emoji": "❌", "text": "計算ミスをなくす方法"},
      {"href": "/mainichi-drill.html",       "emoji": "📅", "text": "毎日の計算練習法"},
    ],
  },

  {
    "filename": "natsu-benkyou.html",
    "title": "夏休みの算数勉強計画【学年別おすすめ復習法】",
    "description": "夏休みの算数勉強計画を学年別に紹介。1学期の復習と2学期の予習をバランスよく進める方法をまとめました。",
    "h1": "夏休みの算数勉強計画【学年別おすすめ復習法】",
    "eyecatch": "☀️ 夏休みは算数の遅れを取り戻すまたとないチャンス！計画を立てて実力アップを目指しましょう。",
    "body_html": """\
<h2>夏休みに算数を頑張るべき理由</h2>
<ul>
  <li>まとまった時間が取れる（学期中より集中できる）</li>
  <li>1学期の苦手を解消するラストチャンス</li>
  <li>2学期は内容がさらに難しくなるため</li>
  <li>九九や計算の基礎を固めるのに最適</li>
</ul>
<h2>学年別 夏休みの重点単元</h2>
<h3>1年生</h3>
<p>たし算・ひき算の計算（繰り上がり・繰り下がりの完全習熟）</p>
<h3>2年生</h3>
<p>九九の完全習熟（これが最重要！）</p>
<h3>3年生</h3>
<p>かけ算の筆算、わり算の基礎</p>
<h3>4年生</h3>
<p>わり算の筆算（特に3桁÷2桁）、小数の計算</p>
<h3>5年生</h3>
<p>分数の通分・約分・計算、割合の基礎</p>
<h3>6年生</h3>
<p>分数の四則計算、比・比例の総復習</p>
<div class="tip-box"><p>💡 夏休みの学習は「午前中に集中」が基本。涼しいうちに算数を終わらせて午後は自由に過ごしましょう。</p></div>
<h2>40日間の学習計画（目安）</h2>
<ul>
  <li>1〜2週目：1学期の苦手単元を集中復習</li>
  <li>3週目：総合練習・ランダム問題で定着確認</li>
  <li>4週目〜：余裕があれば2学期の予習</li>
</ul>""",
    "faq": [
      {"q": "夏休みに何ページのドリルをすればいいですか？", "a": "量より質が重要です。1日10〜20問を正確に解くことを継続する方が、大量にこなすより効果的です。"},
      {"q": "2年生の九九はいつまでに完璧にすべきですか？", "a": "3年生のわり算が始まる前（9月まで）に全段完璧にすることが目標です。夏休みは最大のチャンスです。"},
      {"q": "夏休みにゲームや遊びと勉強のバランスは？", "a": "午前中に勉強、午後は遊び、というリズムが最もうまくいくパターンです。最初に勉強を終わらせると「あとは自由」という達成感があります。"},
      {"q": "苦手単元が多すぎて何から手をつければ？", "a": "最も古い（下の学年の）苦手単元から始めましょう。算数は積み上げ教科なので、基礎から積み直すことが最短コースです。"},
    ],
    "cta_href": "/natsu-sansu.html",
    "cta_label": "夏の算数問題を解いてみる",
    "related": [
      {"href": "/natsu-sansu.html",         "emoji": "☀️", "text": "夏の算数問題"},
      {"href": "/sansu-benkyou-houhou.html", "emoji": "📖", "text": "算数の効果的な勉強法"},
      {"href": "/mainichi-drill.html",       "emoji": "📅", "text": "毎日の計算練習法"},
      {"href": "/kuku-tips.html",            "emoji": "✖️", "text": "九九の覚え方"},
    ],
  },

  {
    "filename": "haru-benkyou.html",
    "title": "春休みの算数勉強計画【進級前に基礎を固める方法】",
    "description": "春休みの算数勉強計画を紹介。進級・入学前の算数の基礎固めと次の学年への準備をする方法をまとめました。",
    "h1": "春休みの算数勉強計画【進級前に基礎を固める】",
    "eyecatch": "🌸 春休みは「1年間の総復習」と「新学年への準備」の2つを進める絶好の機会です！",
    "body_html": """\
<h2>春休みにやるべき2つのこと</h2>
<h3>①この1年間の総復習</h3>
<p>3学期の内容を含めた全体の復習。苦手だった単元を最終確認します。</p>
<h3>②次の学年の準備</h3>
<p>新学年で最初に習う単元の先取り（少しだけ）。4月のスタートが楽になります。</p>
<h2>学年別 春休みの重点確認事項</h2>
<h3>1年→2年生</h3>
<p>繰り上がり・繰り下がりの計算の完全習熟（2年生の九九の前提）</p>
<h3>2年→3年生</h3>
<p>九九の全段確認（3年生のわり算・かけ算筆算の前提）</p>
<h3>3年→4年生</h3>
<p>わり算・あまりのある計算の確認（4年生の筆算の前提）</p>
<h3>4年→5年生</h3>
<p>分数の基礎・小数の計算確認（5年生の通分・割合の前提）</p>
<h3>5年→6年生</h3>
<p>割合・比の概念確認（6年生の比例・縮尺の前提）</p>
<div class="tip-box"><p>💡 春休みは短い（2週間程度）ので1〜2つの単元に絞って徹底的に練習しましょう。</p></div>""",
    "faq": [
      {"q": "春休みは何日間くらい勉強すればいいですか？", "a": "毎日少しずつ（1日20〜30分）が基本です。春休みは約2週間なので、苦手単元を1〜2つ絞って集中練習しましょう。"},
      {"q": "新学年の教科書は春休みに読んでいいですか？", "a": "はい、大まかに眺めておくと4月の学習がスムーズに始められます。ただし深く先取りするより前の学年の復習を優先しましょう。"},
      {"q": "入学前（年長→1年生）は何を準備すれば？", "a": "数字の読み書き・1〜20の数の概念・簡単な足し算（指を使ってOK）を練習しておくと安心です。"},
      {"q": "春休みに市販のドリルは必要ですか？", "a": "当サイトで無料で練習できます。学年を超えた単元も練習できるので、苦手単元の復習に活用してください。"},
    ],
    "cta_href": "/haru-sansu.html",
    "cta_label": "春の算数問題を解く",
    "related": [
      {"href": "/haru-sansu.html",          "emoji": "🌸", "text": "春の算数問題"},
      {"href": "/sansu-benkyou-houhou.html", "emoji": "📖", "text": "算数の効果的な勉強法"},
      {"href": "/nyuugaku-mae.html",         "emoji": "🎒", "text": "入学前の算数準備"},
      {"href": "/mainichi-drill.html",       "emoji": "📅", "text": "毎日の計算練習法"},
    ],
  },


  # ────────────────────────────────
  # 計算・数の応用
  # ────────────────────────────────
  {
    "filename": "kakko-keisan.html",
    "title": "かっこを使った計算プリント【無料】計算の順序｜小学3年生",
    "description": "かっこを使った計算（計算の順序）を印刷不要・スマホで練習できる無料プリント。計算の優先順位をわかりやすく解説。小学3年生向け。",
    "h1": "かっこを使った計算プリント【無料】小学3年生",
    "eyecatch": "🔢 かっこを使った計算は「かっこの中を先に」がルール。計算の順序を正しく覚えましょう！",
    "body_html": """\
<h2>計算の順序のルール</h2>
<div class="formula-box"><p>①かっこの中 ②×÷ ③＋－ の順に計算する</p></div>
<h2>かっこありとなしの違い</h2>
<ul>
  <li>かっこなし：10 ー 3 ＋ 2 ＝ 7 ＋ 2 ＝ 9（左から順）</li>
  <li>かっこあり：10 ー (3 ＋ 2) ＝ 10 ー 5 ＝ 5（かっこの中を先）</li>
</ul>
<div class="tip-box"><p>💡 かっこは「先に計算する」合図。かっこを見つけたら最初に計算します。</p></div>
<h2>×÷が＋－より先のルール</h2>
<ul>
  <li>3 ＋ 4 × 2 ＝ 3 ＋ 8 ＝ 11（×を先に）</li>
  <li>(3 ＋ 4) × 2 ＝ 7 × 2 ＝ 14（かっこで先の順を変える）</li>
</ul>
<div class="warn-box"><p>⚠️ かっこがなければ「×÷を先に」が絶対ルール。左から順に計算してしまうミスに注意！</p></div>""",
    "faq": [
      {"q": "かっこの計算はいつ習いますか？", "a": "小学3年生で学習します。かけ算・わり算の後に習う「計算のきまり」の一つです。"},
      {"q": "かっこが複数ある場合はどう計算しますか？", "a": "内側のかっこから順に計算します。二重かっこ（中括弧）がある場合は内側から外側へ。"},
      {"q": "なぜ×÷が＋－より先なのですか？", "a": "数学的な約束（定義）によるものです。この順序のルールがあることで式の書き方が統一され、誰が読んでも同じ意味になります。"},
      {"q": "かっこの計算でよく使われる問題パターンは？", "a": "文章題で「〇個ずつ入った袋が△袋あって、□個取り出したら残りは？」のような状況式でかっこが使われます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/sansuu-ruuru.html",   "emoji": "📋", "text": "算数の公式・ルールまとめ"},
      {"href": "/kongozan.html",       "emoji": "🔢", "text": "混合計算"},
      {"href": "/keisan-hayaku.html",  "emoji": "⚡", "text": "計算を速くする方法"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "suuji-4keta.html",
    "title": "4桁の数プリント【無料】千・万の位の計算｜小学3年生",
    "description": "4桁の数（千・万の位）の読み書きと計算を印刷不要・スマホで練習できる無料プリント。位の仕組みをわかりやすく解説。小学3年生向け。",
    "h1": "4桁の数プリント【無料】小学3年生",
    "eyecatch": "🔢 4桁の数は「千の位」が加わります。位の仕組みを理解すれば大きな数も怖くない！",
    "body_html": """\
<h2>4桁の数の位取り</h2>
<div class="formula-box"><p>千の位 ｜ 百の位 ｜ 十の位 ｜ 一の位</p></div>
<p>例：3456 ＝ 千の位3、百の位4、十の位5、一の位6</p>
<h2>数の読み方</h2>
<ul>
  <li>1000：千（せん）</li>
  <li>2000：二千（にせん）</li>
  <li>9999：九千九百九十九（きゅうせんきゅうひゃくきゅうじゅうきゅう）</li>
  <li>10000：一万（いちまん）← 5桁</li>
</ul>
<div class="tip-box"><p>💡 「千・百・十・一」を繰り返し声に出して、位の順番を覚えましょう。</p></div>
<h2>4桁の数の大小比較</h2>
<p>千の位から順に比べる。千の位が同じなら百の位を比べる。</p>
<ul>
  <li>3456 と 3298 → 千の位が同じ3、百の位 4＞2 なので 3456 ＞ 3298</li>
</ul>
<h2>4桁の足し算・引き算</h2>
<p>手順は2桁・3桁と同じ。位をそろえて一の位から計算します。</p>""",
    "faq": [
      {"q": "4桁の数はいつ習いますか？", "a": "小学3年生で学習します。4桁の数の読み書き、大小比較、たし算・ひき算を学びます。"},
      {"q": "9999の次の数は？", "a": "10000（一万）です。9999に1を足すと桁が増えて5桁になります。"},
      {"q": "4桁の数の足し算で繰り上がりが何回もある場合は？", "a": "各位で繰り上がりを確認しながら一の位から順に計算します。方眼ノートに位をそろえて書くと間違いが減ります。"},
      {"q": "「0」が含まれる数（1003など）の読み方は？", "a": "0の位は読みません。1003は「千三（せんさん）」と読みます。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/ookina-kazu.html",    "emoji": "🔢", "text": "大きな数（万・億）"},
      {"href": "/1000made-no-kazu.html","emoji": "🔢", "text": "1000までの数"},
      {"href": "/gaisuu-guide.html",   "emoji": "🔢", "text": "がい数（四捨五入）"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "shosu-to-bunsuu.html",
    "title": "小数と分数の変換プリント【無料】相互変換の方法｜小学5年生",
    "description": "小数と分数の相互変換を印刷不要・スマホで練習できる無料プリント。0.5＝1/2 などの変換方法をわかりやすく解説。小学5年生向け。",
    "h1": "小数と分数の変換プリント【無料】小学5年生",
    "eyecatch": "🔢 小数と分数は同じ量を別の形で表したもの。スムーズに変換できると計算が楽になります！",
    "body_html": """\
<h2>小数→分数への変換</h2>
<div class="formula-box"><p>0.1 ＝ 1/10　0.01 ＝ 1/100　0.25 ＝ 25/100 ＝ 1/4</p></div>
<ol>
  <li>小数を分数で書く（0.25なら25/100）</li>
  <li>約分する（25/100 ÷ 25 ＝ 1/4）</li>
</ol>
<h2>分数→小数への変換</h2>
<div class="formula-box"><p>1/4 ＝ 1÷4 ＝ 0.25　1/3 ＝ 1÷3 ＝ 0.333…</p></div>
<p>分子÷分母を計算します。割り切れない場合は循環小数になります。</p>
<div class="tip-box"><p>💡 よく使う変換を暗記：1/2＝0.5、1/4＝0.25、1/5＝0.2、3/4＝0.75</p></div>
<h2>計算での使い分け</h2>
<ul>
  <li>たし算・ひき算：同じ形（分数か小数）にそろえてから計算</li>
  <li>かけ算：どちらの形でもOK（計算しやすい方を選ぶ）</li>
</ul>
<div class="warn-box"><p>⚠️ 1/3＝0.333…は割り切れません。分数と小数が混在する問題では分数に統一するのがおすすめです。</p></div>""",
    "faq": [
      {"q": "小数と分数の変換はいつ習いますか？", "a": "小学5年生で学習します。分数の通分・約分と合わせて学ぶことが多いです。"},
      {"q": "1/3は小数でいくつですか？", "a": "1÷3＝0.333…（0.3の循環小数）です。割り切れないため、正確に表すには分数を使います。"},
      {"q": "小数と分数が混じった計算はどうしますか？", "a": "どちらかに統一してから計算します。割り切れる小数は分数に直す方が正確です。"},
      {"q": "0.125は何分の何ですか？", "a": "0.125＝125/1000＝1/8です。125÷1000をして約分（GCDは125）すると1/8になります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/syousuu-kiso.html",   "emoji": "🔢", "text": "小数の基礎"},
      {"href": "/bunsuu-kiso.html",    "emoji": "½", "text": "分数の基礎"},
      {"href": "/bunsuu-yakubun.html", "emoji": "½", "text": "約分のやり方"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "menseki-fukuzatsu.html",
    "title": "複合図形の面積プリント【無料】L字・凹字形の求め方｜小学5年生",
    "description": "複合図形（L字・凹字・半円を含む形）の面積を印刷不要・スマホで練習できる無料プリント。図形を分ける考え方を解説。小学5年生向け。",
    "h1": "複合図形の面積プリント【無料】小学5年生",
    "eyecatch": "📐 複合図形は「分けるか引くか」がポイント。2つの方法をマスターして応用問題に強くなろう！",
    "body_html": """\
<h2>複合図形の解き方2パターン</h2>
<h3>①足す：図形をいくつかに分けて合計</h3>
<p>L字形 → 2つの長方形に分けてそれぞれの面積を足す</p>
<div class="tip-box"><p>💡 どこで分けるか迷ったら「直線で2つの長方形にする」方法を試してみましょう。</p></div>
<h3>②引く：大きい図形から余分を引く</h3>
<p>凹字形 → 全体の大きい長方形から欠けた部分を引く</p>
<h2>複合図形の解き方ステップ</h2>
<ol>
  <li>図を見て「分ける」か「引く」か判断</li>
  <li>足りない辺の長さを計算する</li>
  <li>各部分の面積を計算</li>
  <li>合計または差を計算</li>
</ol>
<h2>よく出る複合図形</h2>
<ul>
  <li>L字形（長方形2つに分割）</li>
  <li>凹字形（大長方形から小長方形を引く）</li>
  <li>正方形から四分の一円を引く形</li>
  <li>三角形と長方形の組み合わせ</li>
</ul>
<div class="warn-box"><p>⚠️ 複合図形では「使わない辺の長さ」を誤って使ってしまうミスが多い。図に情報を書き込んで整理しましょう。</p></div>""",
    "faq": [
      {"q": "複合図形の面積はいつ習いますか？", "a": "小学5年生で習います。三角形・平行四辺形の面積を学んだ後に複合図形の問題が登場します。"},
      {"q": "足りない辺の長さはどう求めますか？", "a": "向かい合う辺の長さが等しいという性質を使います。全体の幅から分かっている部分を引くことで求められます。"},
      {"q": "「分ける」か「引く」かはどう判断しますか？", "a": "どちらでも正解ですが、計算が少ない方を選びましょう。凹字形は「引く」の方が計算ステップが少ないことが多いです。"},
      {"q": "円を含む複合図形はどう解きますか？", "a": "正方形から半円・四分の一円を引く、または足す計算になります。円の面積＝半径×半径×3.14を使います。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/menseki-sankakukei.html",     "emoji": "📐", "text": "三角形の面積"},
      {"href": "/menseki-heikoushikakkei.html","emoji": "📐", "text": "平行四辺形の面積"},
      {"href": "/menseki-enza.html",            "emoji": "📐", "text": "円の面積"},
      {"href": "/grade-5-matome.html",          "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "kakudo-mondai.html",
    "title": "角度の計算問題プリント【無料】三角形・四角形の角度｜小学4年生",
    "description": "角度の計算問題（三角形・四角形・直線の角度）を印刷不要・スマホで練習できる無料プリント。角度の性質を使った問題を解説。小学4年生向け。",
    "h1": "角度の計算問題プリント【無料】小学4年生",
    "eyecatch": "📐 角度の問題は「内角の和」と「直線の角度」のルールを覚えれば解ける！練習を積み重ねましょう。",
    "body_html": """\
<h2>覚えておくべき角度のルール</h2>
<ul>
  <li>直線の角度：180°</li>
  <li>1周の角度：360°</li>
  <li>三角形の内角の和：180°</li>
  <li>四角形の内角の和：360°</li>
  <li>直角：90°</li>
</ul>
<div class="formula-box"><p>三角形の残りの角 ＝ 180° ー （他の2つの角の和）</p></div>
<h2>よく出る問題パターン</h2>
<h3>①三角形の1つの角を求める</h3>
<p>2つの角が40°と70°の三角形。残りの角は？</p>
<p>180 ー (40 ＋ 70) ＝ 180 ー 110 ＝ 70°</p>
<h3>②直線の角度を使う</h3>
<p>直線上の角度は合計180°。片方が120°なら残りは60°。</p>
<h3>③折れ線の角度</h3>
<p>外角＝内角の2つの非隣辺の角の和（中学で詳しく学ぶ）</p>
<div class="tip-box"><p>💡 「a°と b°が直線上にある → a＋b＝180°」を繰り返し使います。</p></div>""",
    "faq": [
      {"q": "角度の計算はいつ習いますか？", "a": "小学4年生で角度（°）・直角・分度器の使い方を習い、三角形・四角形の内角の和も学びます。"},
      {"q": "分度器の使い方が苦手です。", "a": "まず0°と180°の目盛りの位置を確認します。次に角の頂点を分度器の中心に合わせ、一方の辺を0°に合わせて読みます。内側か外側どちらを読むかも確認しましょう。"},
      {"q": "三角形の外角はどうやって求めますか？", "a": "三角形の外角＝隣り合わない2つの内角の和です（例：50°と70°の三角形の外角は120°）。"},
      {"q": "四角形の内角の和が360°になる理由は？", "a": "四角形は対角線で2つの三角形に分けられ、三角形の内角の和180°×2＝360°になります。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/kakudo-guide.html",       "emoji": "📐", "text": "角度の学習ガイド"},
      {"href": "/sankakkei-shurui.html",   "emoji": "📐", "text": "三角形の種類"},
      {"href": "/shikakkei-seishitsu.html","emoji": "📐", "text": "四角形の種類と性質"},
      {"href": "/grade-4-matome.html",     "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "boubou-graph.html",
    "title": "棒グラフの読み方と書き方プリント【無料】｜小学3年生",
    "description": "棒グラフの読み方・書き方を印刷不要・スマホで練習できる無料プリント。目盛りの読み方から棒グラフの作成まで解説。小学3年生向け。",
    "h1": "棒グラフの読み方と書き方プリント【無料】小学3年生",
    "eyecatch": "📊 棒グラフは「比べる」ためのグラフ。正しい読み方と書き方をマスターしましょう！",
    "body_html": """\
<h2>棒グラフとは？</h2>
<p>棒の長さで量の大きさを表すグラフです。複数のものを比較するのに適しています。</p>
<h2>棒グラフの読み方</h2>
<ol>
  <li>グラフのタイトルを確認（何を表しているか）</li>
  <li>縦軸の単位と目盛りを確認</li>
  <li>棒の先端が目盛りのどこを指すか読む</li>
  <li>目盛りの間の場合は比例配分で読む</li>
</ol>
<div class="tip-box"><p>💡 目盛りを読む時は棒の先端から水平に線を引いて縦軸の数字を読むと正確です。</p></div>
<h2>棒グラフの書き方</h2>
<ol>
  <li>適切な目盛りの幅を決める（最大値が入るように）</li>
  <li>縦軸に目盛りをつける（単位も忘れずに）</li>
  <li>横軸に項目名を書く</li>
  <li>それぞれの値に合わせて棒を書く</li>
  <li>タイトルを書く</li>
</ol>
<div class="warn-box"><p>⚠️ 目盛りは等間隔に書くことが大切。不等間隔では正確なグラフになりません。</p></div>""",
    "faq": [
      {"q": "棒グラフはいつ習いますか？", "a": "小学3年生で学習します。2年生で簡単なグラフを習い、3年生で棒グラフを本格的に学びます。"},
      {"q": "棒グラフと折れ線グラフの違いは？", "a": "棒グラフは「量の大きさを比較」するのに適し、折れ線グラフは「量の変化（時間経過）」を表すのに適しています。"},
      {"q": "目盛りの幅はどう決めますか？", "a": "最大値が収まるように決めます。例えば最大値が85ならば10刻みの目盛りで100まで取ります。"},
      {"q": "棒グラフで最も大きい・小さい項目をすぐ分かる方法は？", "a": "棒の長さを見れば一目瞭然です。これが棒グラフの最大のメリットです。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/graph-boubou.html",  "emoji": "📊", "text": "棒グラフドリル"},
      {"href": "/graph-oretsu.html",  "emoji": "📊", "text": "折れ線グラフドリル"},
      {"href": "/graph-circle.html",  "emoji": "📊", "text": "円グラフドリル"},
      {"href": "/grade-3-matome.html","emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "oretsu-graph.html",
    "title": "折れ線グラフの読み方と書き方プリント【無料】｜小学4年生",
    "description": "折れ線グラフの読み方・書き方を印刷不要・スマホで練習できる無料プリント。変化の傾向の読み取り方まで解説。小学4年生向け。",
    "h1": "折れ線グラフの読み方と書き方プリント【無料】小学4年生",
    "eyecatch": "📊 折れ線グラフは「変化」を見るためのグラフ。傾きの読み取りまでマスターしましょう！",
    "body_html": """\
<h2>折れ線グラフとは？</h2>
<p>点を線でつないだグラフで、時間の変化や推移を表すのに適しています。</p>
<h2>折れ線グラフの読み方のポイント</h2>
<ul>
  <li><strong>上がり傾向：</strong>線が右上がり → 増えている</li>
  <li><strong>下がり傾向：</strong>線が右下がり → 減っている</li>
  <li><strong>水平：</strong>変化なし</li>
  <li><strong>急な傾き：</strong>変化が大きい</li>
  <li><strong>緩やかな傾き：</strong>変化が小さい</li>
</ul>
<div class="tip-box"><p>💡 「一番急に上がっているのはどこ？」という問題は、線の傾きが最も急な区間を選びます。</p></div>
<h2>折れ線グラフの書き方</h2>
<ol>
  <li>縦軸・横軸の目盛りを書く</li>
  <li>各データの点を打つ</li>
  <li>点を直線で順番につなぐ</li>
  <li>タイトルを書く</li>
</ol>
<div class="warn-box"><p>⚠️ 点と点はきれいな直線でつなぎます。曲線にならないように注意！</p></div>""",
    "faq": [
      {"q": "折れ線グラフはいつ習いますか？", "a": "小学4年生で学習します。3年生の棒グラフに続いて学ぶグラフです。"},
      {"q": "折れ線グラフはどんな場面で使いますか？", "a": "気温の変化（日ごと・月ごと）、身長・体重の変化、売上の推移など、時間変化を見たい場合に使います。"},
      {"q": "「変化が最も大きい区間」はどう見つけますか？", "a": "線の傾きが最も急な区間です。数値的には「後の値から前の値を引いた差が最も大きい区間」です。"},
      {"q": "棒グラフと折れ線グラフを重ねることはできますか？", "a": "はい、複合グラフといいます。例えば気温（折れ線）と雨量（棒グラフ）を一つのグラフに表す方法が小学校でも紹介されます。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/graph-oretsu.html",  "emoji": "📊", "text": "折れ線グラフドリル"},
      {"href": "/boubou-graph.html",  "emoji": "📊", "text": "棒グラフの読み方"},
      {"href": "/graph-circle.html",  "emoji": "📊", "text": "円グラフドリル"},
      {"href": "/grade-4-matome.html","emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "douten-graph.html",
    "title": "ドットプロット・ヒストグラムプリント【無料】データの活用｜小学6年生",
    "description": "ドットプロット・ヒストグラムの読み方・書き方を印刷不要・スマホで練習できる無料プリント。データの分布の読み取り方を解説。小学6年生向け。",
    "h1": "ドットプロット・ヒストグラムプリント【無料】小学6年生",
    "eyecatch": "📊 ドットプロットとヒストグラムはデータの分布を視覚化するグラフ。6年生で学ぶデータ活用の基礎です！",
    "body_html": """\
<h2>ドットプロットとは？</h2>
<p>数直線上にデータを点（ドット）で表したグラフです。少ないデータの分布を見るのに適しています。</p>
<ul>
  <li>同じ値が複数ある場合は点を縦に重ねる</li>
  <li>データの分布（かたまり・散らばり）が一目で分かる</li>
</ul>
<h2>ヒストグラムとは？</h2>
<p>データを区間（階級）ごとに集計して棒で表したグラフです。</p>
<ul>
  <li>棒と棒の間にすき間がない（棒グラフとの違い）</li>
  <li>どの範囲にデータが集中しているかが分かる</li>
</ul>
<div class="tip-box"><p>💡 ヒストグラムは「度数分布表」をグラフにしたものです。表とグラフを対応させて読みましょう。</p></div>
<h2>度数分布表の作り方</h2>
<ol>
  <li>データの最小値・最大値を確認</li>
  <li>適切な階級幅を決める（例：5点刻み）</li>
  <li>各階級に含まれるデータ数（度数）を数える</li>
  <li>表を完成させる</li>
</ol>""",
    "faq": [
      {"q": "ドットプロットとヒストグラムはいつ習いますか？", "a": "小学6年生で学習します。データの活用（統計）単元の一部として学びます。"},
      {"q": "ヒストグラムと棒グラフの違いは何ですか？", "a": "棒グラフは項目ごとの比較、ヒストグラムは連続データの度数分布を表します。ヒストグラムは棒の間にすき間がないことも特徴です。"},
      {"q": "度数分布表とは何ですか？", "a": "データを階級（例：60〜70点）ごとに分けて、各階級の個数（度数）をまとめた表です。ヒストグラムの元になります。"},
      {"q": "代表値（平均・中央値・最頻値）とデータ活用の関係は？", "a": "ドットプロットやヒストグラムからデータの分布を見て、適切な代表値を選ぶことを学びます。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/heikin-guide.html",   "emoji": "📊", "text": "平均の求め方"},
      {"href": "/graph-circle.html",   "emoji": "📊", "text": "円グラフドリル"},
      {"href": "/baai-no-kazu.html",   "emoji": "📊", "text": "場合の数"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  {
    "filename": "taiseki-rittai.html",
    "title": "角柱・円柱の体積プリント【無料】底面積×高さの計算｜小学6年生",
    "description": "角柱・円柱の体積（底面積×高さ）を印刷不要・スマホで練習できる無料プリント。三角柱・四角柱・円柱の体積を解説。小学6年生向け。",
    "h1": "角柱・円柱の体積プリント【無料】小学6年生",
    "eyecatch": "📦 柱体の体積は「底面積×高さ」の公式一つ！どんな形の柱でも同じ考え方です。",
    "body_html": """\
<h2>柱体の体積の公式</h2>
<div class="formula-box"><p>柱体の体積 ＝ 底面積 × 高さ</p></div>
<p>角柱（三角柱・四角柱など）も円柱も同じ公式です。底面の形によって底面積の求め方が変わります。</p>
<h2>各柱体の体積の求め方</h2>
<h3>三角柱</h3>
<div class="formula-box"><p>底面積 ＝ 底辺×高さ÷2（三角形） → 体積 ＝ 底面積×柱の高さ</p></div>
<h3>四角柱（直方体）</h3>
<div class="formula-box"><p>底面積 ＝ たて×よこ → 体積 ＝ 底面積×高さ</p></div>
<h3>円柱</h3>
<div class="formula-box"><p>底面積 ＝ 半径×半径×3.14 → 体積 ＝ 底面積×高さ</p></div>
<div class="tip-box"><p>💡 底面の形を特定してから底面積を求め、そこに高さをかける手順を守りましょう。</p></div>
<h2>よくある間違い</h2>
<ul>
  <li>底面の「高さ」と柱全体の「高さ」を混同する（三角柱）</li>
  <li>円柱で直径を半径と間違える</li>
  <li>単位をcm³と書かずcm²と書く</li>
</ul>""",
    "faq": [
      {"q": "角柱・円柱の体積はいつ習いますか？", "a": "小学6年生で学習します。5年生の直方体・立方体の体積の発展として学びます。"},
      {"q": "三角柱の体積の計算方法を教えてください。", "a": "底面（三角形）の面積を求めて、それに柱の高さをかけます。例：底辺4cm・高さ3cmの三角形が底面で、柱の高さが5cmなら：(4×3÷2)×5＝30cm³。"},
      {"q": "円柱の体積での「高さ」はどこですか？", "a": "円柱の2つの円形の底面の間の距離（柱の側面の長さ）が高さです。円の半径と混同しないようにしましょう。"},
      {"q": "体積と容積の違いは？", "a": "体積は立体が占める空間の量、容積は容器に入る液体の量です。容器の厚みがない場合、体積と容積は等しくなります。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/taiseki-kiso.html",   "emoji": "📦", "text": "体積の基礎"},
      {"href": "/menseki-enza.html",   "emoji": "📐", "text": "円の面積"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
      {"href": "/tani-kaseki.html",    "emoji": "🧪", "text": "かさの単位換算"},
    ],
  },

  {
    "filename": "moji-shiki.html",
    "title": "文字と式プリント【無料】□・△を使った式｜小学4〜6年生",
    "description": "□や△を使った式（文字と式の基礎）を印刷不要・スマホで練習できる無料プリント。中学数学への橋渡しになる単元を解説。小学4〜6年生向け。",
    "h1": "文字と式プリント【無料】小学4〜6年生",
    "eyecatch": "🔢 □や△を使った式は中学数学の方程式への第一歩。考え方をしっかり身につけましょう！",
    "body_html": """\
<h2>□を使った式とは？</h2>
<p>分からない数を□や△で表した式です。</p>
<div class="formula-box"><p>□ ＋ 3 ＝ 8　→ □ ＝ 5</p></div>
<h2>□を求める解き方</h2>
<ul>
  <li>□ ＋ 3 ＝ 8 → □ ＝ 8 ー 3 ＝ 5（逆算）</li>
  <li>□ × 4 ＝ 20 → □ ＝ 20 ÷ 4 ＝ 5（逆算）</li>
  <li>6 ー □ ＝ 4 → □ ＝ 6 ー 4 ＝ 2（逆算）</li>
</ul>
<div class="tip-box"><p>💡 「逆算」のコツ：＋の逆はー、×の逆は÷。□の反対側の操作をすれば求められます。</p></div>
<h2>変わり方（関係式）</h2>
<p>「□が変わると△がどう変わるか」を式で表す学習です。</p>
<div class="formula-box"><p>□の2倍が△ → □ × 2 ＝ △</p></div>
<h2>中学数学への準備</h2>
<p>□や△は中学数学でxやyに変わります。考え方は全く同じです。</p>
<div class="warn-box"><p>⚠️ 「□が2つある式」（□＋□＝10など）は中学の方程式で扱います。小学では1つの□に1つの答えを求める問題が基本です。</p></div>""",
    "faq": [
      {"q": "□を使った式はいつ習いますか？", "a": "小学3年生から少しずつ登場し、6年生では文字（□・△）と式として体系的に学習します。"},
      {"q": "中学のxとyと何が違いますか？", "a": "記号が違うだけで考え方は同じです。□＋3＝8はx＋3＝8と同じです。"},
      {"q": "□×□のような問題は出ますか？", "a": "小学校では「同じ□」として扱うことがありますが、基本的には1つの□に1つの値を求める問題です。"},
      {"q": "逆算の方法を覚えられません。", "a": "「＋をしたら逆は－」「×をしたら逆は÷」と対応を覚えましょう。それぞれ「逆の操作」で□が求まります。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/sansuu-ruuru.html",    "emoji": "📋", "text": "算数の公式まとめ"},
      {"href": "/hirei-hanpirei.html",  "emoji": "📊", "text": "比例と反比例"},
      {"href": "/chuugaku-junbi.html",  "emoji": "🎓", "text": "中学数学への準備"},
      {"href": "/grade-6-matome.html",  "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  {
    "filename": "baai-keisan.html",
    "title": "場合の数・並べ方プリント【無料】樹形図の使い方｜小学6年生",
    "description": "場合の数（並べ方・組み合わせ）を印刷不要・スマホで練習できる無料プリント。樹形図と表の使い方をわかりやすく解説。小学6年生向け。",
    "h1": "場合の数・並べ方プリント【無料】小学6年生",
    "eyecatch": "🎲 場合の数は「もれなく・重複なく」数えることが大切。樹形図をマスターすれば確実に数えられます！",
    "body_html": """\
<h2>場合の数を数えるツール</h2>
<h3>①樹形図（じゅけいず）</h3>
<p>木の枝のように分岐させてすべての場合を書き出す方法です。</p>
<div class="tip-box"><p>💡 樹形図は「もれなく・重複なく」数えるための最強ツール。まず必ず書いてみましょう。</p></div>
<h3>②表</h3>
<p>2つのものの組み合わせを表で整理する方法です。</p>
<h2>並べ方（順列）の例</h2>
<p>A・B・C 3枚のカードを1列に並べると何通り？</p>
<ul>
  <li>1枚目：3通り</li>
  <li>2枚目：2通り（残りから）</li>
  <li>3枚目：1通り</li>
  <li>合計：3×2×1＝6通り</li>
</ul>
<h2>組み合わせ（順番が関係ない場合）の例</h2>
<p>A・B・C・Dから2枚選ぶと何通り？</p>
<p>樹形図で書き出すと：AB・AC・AD・BC・BD・CD ＝ 6通り</p>
<div class="warn-box"><p>⚠️ 並べ方と組み合わせは違います。「AB」と「BA」を別々に数えるか同じとみるかで答えが変わります。</p></div>""",
    "faq": [
      {"q": "場合の数はいつ習いますか？", "a": "小学6年生で学習します。並べ方・組み合わせの基礎と樹形図・表の使い方を学びます。"},
      {"q": "樹形図を書かずに暗算で数えると間違えます。", "a": "必ず樹形図か表を書きましょう。場合の数は暗算で数えるとほぼ必ずミスが起きます。"},
      {"q": "順列と組み合わせの違いは？", "a": "順列は並び順が違えば別のもの（ABとBA）。組み合わせは並び順を無視します（ABとBAは同じ）。問題文で「並べ方」か「選び方」かを確認しましょう。"},
      {"q": "「何通り」と「確率」の違いは？", "a": "場合の数は「何通りあるか」の個数。確率は「ある事柄が起きる割合」。確率＝求める場合の数÷全部の場合の数です。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/baai-no-kazu.html",   "emoji": "📊", "text": "場合の数ドリル"},
      {"href": "/heikin-guide.html",   "emoji": "📊", "text": "平均の求め方"},
      {"href": "/douten-graph.html",   "emoji": "📊", "text": "データの活用"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  {
    "filename": "taiseki-mizu.html",
    "title": "水の体積・容積プリント【無料】水そうの問題｜小学5〜6年生",
    "description": "水の体積・容積（水そうに入る水の量）を印刷不要・スマホで練習できる無料プリント。体積とLの換算を解説。小学5〜6年生向け。",
    "h1": "水の体積・容積プリント【無料】小学5〜6年生",
    "eyecatch": "💧 水そうの体積問題は「cm³とLの換算」がポイント。1L＝1000cm³の関係を使いこなしましょう！",
    "body_html": """\
<h2>体積と容積の単位換算</h2>
<div class="formula-box"><p>1L ＝ 1000cm³ ＝ 1000mL<br>1m³ ＝ 1000000cm³ ＝ 1000L</p></div>
<h2>水そう問題の解き方</h2>
<h3>①水そうの容積を求める</h3>
<p>直方体の水そう：たて×よこ×高さ（cm³）→ ÷1000でL</p>
<h3>②水の深さから体積を求める</h3>
<p>水が深さhまで入っている水そう：たて×よこ×h（水位）</p>
<h3>③水を入れたときの深さを求める</h3>
<p>□L入れたとき：体積＝□×1000（cm³）→ 深さ＝体積÷（たて×よこ）</p>
<div class="tip-box"><p>💡 LとmLとcm³の換算を確実に。1L＝1000mL＝1000cm³が基本です。</p></div>
<h2>よく出る応用問題</h2>
<ul>
  <li>「何分で満杯になるか？」→ 容積÷1分あたりの水量</li>
  <li>「石を入れたときの水位上昇」→ 石の体積÷底面積</li>
</ul>""",
    "faq": [
      {"q": "1L は何cm³ ですか？", "a": "1L＝1000cm³です。1辺10cmの立方体（10×10×10）の体積が1Lになります。"},
      {"q": "水そう問題でよくある間違いは？", "a": "単位の換算忘れ（cm³のままLに直さない）と、水位×底面積で体積を求めることを忘れるケースが多いです。"},
      {"q": "円柱形の水そうの容積は？", "a": "底面積（半径×半径×3.14）×高さ（cm³）→÷1000でLに換算します。"},
      {"q": "水を入れている途中の水位はどう求めますか？", "a": "入れた水の体積（cm³）÷底面積（cm²）＝水位（cm）です。単位に注意して計算しましょう。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/taiseki-kiso.html",   "emoji": "📦", "text": "体積の基礎"},
      {"href": "/taiseki-rittai.html", "emoji": "📦", "text": "角柱・円柱の体積"},
      {"href": "/mizu-no-kasa.html",   "emoji": "🧪", "text": "水のかさの単位"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "mondai-warisan.html",
    "title": "わり算の文章題プリント【無料】等分・包含の2パターン｜小学3年生",
    "description": "わり算の文章題（等分除・包含除）を印刷不要・スマホで練習できる無料プリント。2つのパターンを見分ける方法を解説。小学3年生向け。",
    "h1": "わり算の文章題プリント【無料】小学3年生",
    "eyecatch": "➗ わり算文章題は「等しく分ける」と「何個分」の2パターン。読み取り方をマスターしましょう！",
    "body_html": """\
<h2>わり算文章題の2パターン</h2>
<h3>①等分除（等しく分ける）</h3>
<p>「24個を6人に等しく分けると1人何個？」→ 24÷6＝4個</p>
<div class="tip-box"><p>💡 キーワード：「等しく分ける」「一人分は？」「一つ分は？」</p></div>
<h3>②包含除（何グループに分けられるか）</h3>
<p>「24個を1袋4個ずつに分けると何袋できる？」→ 24÷4＝6袋</p>
<div class="tip-box"><p>💡 キーワード：「何袋？」「何箱？」「何人分？」（1袋・1箱の量が分かっている）</p></div>
<h2>文章題の解き方ステップ</h2>
<ol>
  <li>「何を求めるか」を確認</li>
  <li>全体の数・分ける数（または1まとまりの数）を確認</li>
  <li>どちらのパターンか判断</li>
  <li>式を立てて計算</li>
  <li>単位をつけて答える</li>
</ol>
<div class="warn-box"><p>⚠️ あまりが出る問題は「あまりをどうするか」まで答えに含めましょう。</p></div>""",
    "faq": [
      {"q": "等分除と包含除の区別が難しい場合は？", "a": "どちらも式は「全体÷1グループの数または人数」です。「何を÷何」するかを図で整理してみましょう。"},
      {"q": "あまりのあるわり算の文章題のコツは？", "a": "「あまりを切り捨て」か「切り上げ」かを問題文から読み取ることが大切です。「最低何袋いるか」は切り上げ、「何袋できるか」は切り捨てです。"},
      {"q": "わり算文章題でよく使われる言葉は？", "a": "「等しく分ける」「一つ分」「何人分」「何袋」などです。数量の場面を図に書いて整理すると式が立てやすくなります。"},
      {"q": "文章題が苦手な場合はどうすれば？", "a": "まず問題を読んで図・絵を書く習慣をつけましょう。数字と場面を対応させることが文章題攻略の基本です。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/warizan-kiso.html",   "emoji": "➗", "text": "わり算の基礎"},
      {"href": "/warizan-amari.html",  "emoji": "➗", "text": "あまりのあるわり算"},
      {"href": "/mondai-tasizan.html", "emoji": "📝", "text": "足し算の文章題"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "mondai-kakizan.html",
    "title": "かけ算の文章題プリント【無料】1あたりの数を使った問題｜小学2〜3年生",
    "description": "かけ算の文章題（1あたりの数×いくつ分）を印刷不要・スマホで練習できる無料プリント。場面の読み取り方を解説。小学2〜3年生向け。",
    "h1": "かけ算の文章題プリント【無料】小学2〜3年生",
    "eyecatch": "✖️ かけ算文章題は「1つ分の数×いくつ分」がポイント。式の意味を理解して確実に解きましょう！",
    "body_html": """\
<h2>かけ算文章題の公式</h2>
<div class="formula-box"><p>1つ分の数 × いくつ分 ＝ 全部の数</p></div>
<h2>よく出るパターン</h2>
<h3>①「〇個ずつ入った袋が△袋」</h3>
<p>「1袋4個のりんごが5袋。全部で何個？」→ 4×5＝20個</p>
<h3>②「1人〇個、△人分」</h3>
<p>「1人3本のえんぴつ、6人分。全部で何本？」→ 3×6＝18本</p>
<h3>③倍の問題</h3>
<p>「Aの3倍はB。AとBはそれぞれ？」→ 3倍＝×3</p>
<div class="tip-box"><p>💡 「〇つ分」や「〇倍」はかけ算のサイン。まず何が1つ分かを確認しましょう。</p></div>
<h2>かけ算文章題の注意点</h2>
<ul>
  <li>「式の順番」：2×3と3×2は答えが同じでも意味が違う（1つ分が先）</li>
  <li>単位の確認（個・本・枚など必ず書く）</li>
</ul>""",
    "faq": [
      {"q": "かけ算文章題はいつから難しくなりますか？", "a": "3年生から2桁の数を使った問題や倍の問題が登場し、難易度が上がります。"},
      {"q": "式の順番（被乗数と乗数）は重要ですか？", "a": "小学校では「1つ分×いくつ分」の順に式を書くことが教えられます。答えは同じでも式の意味として正しい順番を書く習慣をつけましょう。"},
      {"q": "「〇の△倍」の問題はどう解きますか？", "a": "「〇の△倍」は〇×△と式を立てます。例：「5の3倍は？」→5×3＝15。"},
      {"q": "文章題で何を掛け合わせるか迷う場合は？", "a": "「1つ分（1袋・1人分・1回分）はいくつか」と「いくつ分（何袋・何人・何回）あるか」を整理してから式を立てましょう。"},
    ],
    "cta_href": "/grade-2.html",
    "cta_label": "2年生のドリルをやってみる",
    "related": [
      {"href": "/kakizan-kiso.html",   "emoji": "✖️", "text": "かけ算の基礎"},
      {"href": "/mondai-warisan.html", "emoji": "📝", "text": "わり算の文章題"},
      {"href": "/kuku-tips.html",      "emoji": "✖️", "text": "九九の覚え方"},
      {"href": "/grade-2-matome.html", "emoji": "📚", "text": "2年生 全単元まとめ"},
    ],
  },


  # ────────────────────────────────
  # 追加ページ群
  # ────────────────────────────────
  {
    "filename": "kakezan-bunpai.html",
    "title": "かけ算の分配法則プリント【無料】計算を簡単にするコツ｜小学3年生",
    "description": "分配法則（a×(b+c)＝a×b＋a×c）を使った計算の工夫を練習できる無料プリント。計算を速くするコツを解説。小学3年生向け。",
    "h1": "かけ算の分配法則プリント【無料】小学3年生",
    "eyecatch": "✖️ 分配法則を使うと難しいかけ算が簡単に！計算の工夫を学んでスピードアップしましょう。",
    "body_html": """\
<h2>分配法則とは</h2>
<div class="formula-box"><p>a × (b ＋ c) ＝ a × b ＋ a × c</p></div>
<h2>使い方の例</h2>
<ul>
  <li>12 × 9 ＝ 12 × (10 ー 1) ＝ 120 ー 12 ＝ 108</li>
  <li>7 × 13 ＝ 7 × (10 ＋ 3) ＝ 70 ＋ 21 ＝ 91</li>
</ul>
<div class="tip-box"><p>💡 九九の範囲を超えたかけ算も「10に近い数」に分解すると計算しやすくなります。</p></div>
<h2>逆方向の利用（まとめる）</h2>
<p>5 × 7 ＋ 5 × 3 ＝ 5 × (7 ＋ 3) ＝ 5 × 10 ＝ 50</p>
<p>共通因数（5）でまとめると計算が速くなります。</p>""",
    "faq": [
      {"q": "分配法則はいつ習いますか？", "a": "小学3年生の「かけ算のきまり」として学習します。正式な名前は中学数学で学びます。"},
      {"q": "分配法則の日常での使い道は？", "a": "暗算を速くするのに役立ちます。例えば99×5を(100-1)×5として計算するなど。"},
      {"q": "引き算でも使えますか？", "a": "はい。a×(b-c)＝a×b-a×cも成立します。"},
      {"q": "なぜ分配法則が成り立つのですか？", "a": "面積図で考えると分かりやすいです。長さaで幅(b+c)の長方形はa×bとa×cの長方形2つを合わせた形です。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/kakizan-kiso.html",   "emoji": "✖️", "text": "かけ算の基礎"},
      {"href": "/keisan-hayaku.html",  "emoji": "⚡", "text": "計算を速くする方法"},
      {"href": "/sansuu-ruuru.html",   "emoji": "📋", "text": "算数の公式まとめ"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "tsuriawase.html",
    "title": "つり合いと天秤プリント【無料】重さの比較と等式｜小学3年生",
    "description": "天秤・つり合いを使った重さの比較問題を印刷不要・スマホで練習できる無料プリント。等式の基礎概念を解説。小学3年生向け。",
    "h1": "つり合いと天秤プリント【無料】小学3年生",
    "eyecatch": "⚖️ 天秤の問題は「つり合い＝等しい」の感覚が大切。等式の基礎をゲーム感覚で学びましょう！",
    "body_html": """\
<h2>天秤のつり合いのルール</h2>
<p>天秤が水平（つり合っている）＝両側の重さが等しい</p>
<div class="formula-box"><p>左の重さ ＝ 右の重さ</p></div>
<h2>天秤を使った問題パターン</h2>
<h3>①重さを比べる</h3>
<p>AとBどちらが重い？→ 天秤が下がった側が重い</p>
<h3>②未知の重さを求める</h3>
<p>片方が200g、もう片方が□g＋50g のとき□は？</p>
<p>200 ＝ □ ＋ 50 → □ ＝ 200 ー 50 ＝ 150g</p>
<div class="tip-box"><p>💡 天秤問題は「等号（＝）」の感覚を自然に身につけられる良い教材です。</p></div>
<h2>いくつのりんごで何gか問題</h2>
<p>りんご3個＝300g → りんご1個＝100g</p>
<p>式：3 × □ ＝ 300 → □ ＝ 100</p>""",
    "faq": [
      {"q": "天秤の問題はいつ習いますか？", "a": "小学3年生の重さの単元で学習します。g・kgの単位と合わせて学びます。"},
      {"q": "天秤問題が中学数学とどうつながりますか？", "a": "天秤のつり合い（両辺が等しい）は方程式の基礎概念です。「つり合いを保ったまま両辺に同じ操作をする」が方程式の解き方と同じです。"},
      {"q": "天秤が不等式になる問題はありますか？", "a": "小学校では主に等しい場合を扱いますが、「どちらが重い？」という不等式の概念にも触れます。"},
      {"q": "実際に天秤を使って練習するのは効果的ですか？", "a": "はい、実物の天秤やオモリを使った実験は理解を深めます。身近な食品をg単位で量ってみることも学習になります。"},
    ],
    "cta_href": "/grade-3.html",
    "cta_label": "3年生のドリルをやってみる",
    "related": [
      {"href": "/tani-omosa.html",     "emoji": "⚖️", "text": "重さの単位換算"},
      {"href": "/moji-shiki.html",     "emoji": "🔢", "text": "文字と式"},
      {"href": "/mondai-tasizan.html", "emoji": "📝", "text": "文章題"},
      {"href": "/grade-3-matome.html", "emoji": "📚", "text": "3年生 全単元まとめ"},
    ],
  },

  {
    "filename": "gaisuu-shishagoonyuu.html",
    "title": "四捨五入プリント【無料】がい数の求め方｜小学4年生",
    "description": "四捨五入（がい数）を印刷不要・スマホで練習できる無料プリント。上から〇桁・〇の位まで四捨五入する方法を解説。小学4年生向け。",
    "h1": "四捨五入プリント【無料】小学4年生",
    "eyecatch": "🔢 四捨五入はニュースや日常でよく使われる重要スキル。「上から〇桁」と「〇の位まで」の2通りを覚えよう！",
    "body_html": """\
<h2>四捨五入のルール</h2>
<div class="formula-box"><p>0〜4 → 切り捨て（その桁を0にする）<br>5〜9 → 切り上げ（1つ上の桁に1加える）</p></div>
<h2>「〇の位まで」の四捨五入</h2>
<p>「百の位まで」→ 十の位を四捨五入</p>
<ul>
  <li>3456 → 十の位5 → 切り上げ → 3500</li>
  <li>3450 → 十の位5 → 切り上げ → 3500</li>
  <li>3444 → 十の位4 → 切り捨て → 3400</li>
</ul>
<div class="tip-box"><p>💡 「〇の位まで」の四捨五入は、その1つ下の位を四捨五入します。</p></div>
<h2>「上から〇桁」の四捨五入</h2>
<p>「上から2桁」→ 3桁目（上から3桁目）を四捨五入</p>
<ul>
  <li>3456 → 上から3桁目＝4 → 切り捨て → 3500（上から2桁）</li>
  <li>3756 → 上から3桁目＝5 → 切り上げ → 3800（上から2桁）</li>
</ul>
<div class="warn-box"><p>⚠️ 「以上・以下・未満」の言葉も確認。5以上は切り上げ、4以下は切り捨てです。</p></div>""",
    "faq": [
      {"q": "四捨五入はいつ習いますか？", "a": "小学4年生で「がい数」として学習します。"},
      {"q": "「〇の位まで」と「上から〇桁」の違いは？", "a": "「〇の位まで」は位名で指定（百の位まで、十の位まで）。「上から〇桁」は左から数えた桁数で指定します。どちらも1つ下の位を四捨五入します。"},
      {"q": "5は切り上げ・切り捨てどちらですか？", "a": "5は「切り上げ」です。0〜4が切り捨て、5〜9が切り上げというルールです。"},
      {"q": "がい数を使う場面は？", "a": "人口（「約〇万人」）、距離（「約〇km」）など正確な数字が必要でない場面で使います。「おおよその数」「見当をつける」計算にも使います。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/gaisuu-guide.html",   "emoji": "🔢", "text": "がい数ガイド"},
      {"href": "/ookina-kazu.html",    "emoji": "🔢", "text": "大きな数"},
      {"href": "/suuji-4keta.html",    "emoji": "🔢", "text": "4桁の数"},
      {"href": "/grade-4-matome.html", "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "wahiku-kongo.html",
    "title": "たし算・ひき算・かけ算・わり算 混合計算プリント【無料】",
    "description": "四則演算（たし算・ひき算・かけ算・わり算）の混合計算を印刷不要・スマホで練習できる無料プリント。計算の順序を意識した練習。小学3〜4年生向け。",
    "h1": "四則混合計算プリント【無料】小学3〜4年生",
    "eyecatch": "🔢 四則混合計算は計算の順序が命。×÷を先に、かっこがあれば最初に！ルールを守って正確に解こう。",
    "body_html": """\
<h2>計算の順序（復習）</h2>
<div class="formula-box"><p>① かっこの中 → ② × ÷ → ③ ＋ ー</p></div>
<h2>問題パターン別の解き方</h2>
<h3>例①：足し算・かけ算の混合</h3>
<p>3 ＋ 4 × 2 ＝ 3 ＋ 8 ＝ 11（×を先に）</p>
<h3>例②：かっこあり</h3>
<p>(3 ＋ 4) × 2 ＝ 7 × 2 ＝ 14（かっこを先に）</p>
<h3>例③：÷と＋の混合</h3>
<p>20 ÷ 4 ＋ 3 ＝ 5 ＋ 3 ＝ 8（÷を先に）</p>
<h3>例④：複合かっこ</h3>
<p>2 × (8 ー (3 ＋ 1)) ＝ 2 × (8 ー 4) ＝ 2 × 4 ＝ 8（内側から）</p>
<div class="tip-box"><p>💡 混合計算は「どこから計算するか」の計画を立ててから数字を動かしましょう。</p></div>
<div class="warn-box"><p>⚠️ 「左から順番に」計算するのは＋ーだけのとき。×÷が入ったら計算順序に注意！</p></div>""",
    "faq": [
      {"q": "四則混合計算はいつ習いますか？", "a": "小学3〜4年生で学習します。かっこを使った計算（3年生）→四則混合（4年生）と段階的に学びます。"},
      {"q": "かっこが多い問題の解き方は？", "a": "内側のかっこから解きます。一番内側の計算を終えたら次のかっこへ、と外側に向かって計算します。"},
      {"q": "分数や小数が入った混合計算は？", "a": "基本的なルール（かっこ→×÷→＋ー）は同じです。分数・小数が入っても計算順序は変わりません。"},
      {"q": "検算の方法は？", "a": "計算結果を別の方法（逆算）で確認するか、一から計算し直す方法があります。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/kakko-keisan.html",   "emoji": "🔢", "text": "かっこを使った計算"},
      {"href": "/kongozan.html",       "emoji": "🔢", "text": "混合計算ドリル"},
      {"href": "/sansuu-ruuru.html",   "emoji": "📋", "text": "算数の公式まとめ"},
      {"href": "/grade-4-matome.html", "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "furigana-kazu.html",
    "title": "数の読み方・書き方プリント【無料】大きな数の読み方｜小学4年生",
    "description": "大きな数（万・億・兆）の読み方と書き方を印刷不要・スマホで練習できる無料プリント。位取りの仕組みをわかりやすく解説。小学4年生向け。",
    "h1": "大きな数の読み方・書き方プリント【無料】小学4年生",
    "eyecatch": "🔢 億・兆など大きな数の読み方をマスターしよう！数字の位取りの仕組みが理解の鍵です。",
    "body_html": """\
<h2>大きな数の位取り</h2>
<div class="formula-box"><p>兆 ｜ 億 ｜ 万 ｜ 一（の位）<br>各単位ごとに「千百十一」の4桁</p></div>
<h2>数の読み方</h2>
<ul>
  <li>10000 ＝ 一万（いちまん）</li>
  <li>1000000 ＝ 百万（ひゃくまん）</li>
  <li>100000000 ＝ 一億（いちおく）</li>
  <li>1000000000000 ＝ 一兆（いちちょう）</li>
</ul>
<div class="tip-box"><p>💡 「一・十・百・千」の4桁ごとに「万・億・兆」の単位が変わります。右から4桁ずつ区切ると読みやすくなります。</p></div>
<h2>桁数の多い数の書き方</h2>
<p>「三億四千五百六十七万八千九百」→ 345678900</p>
<ol>
  <li>億の桁：3（3億）</li>
  <li>千万〜万の桁：4567（4567万）</li>
  <li>千〜一の桁：8900</li>
  <li>並べる：345678900</li>
</ol>""",
    "faq": [
      {"q": "億・兆はいつ習いますか？", "a": "万は小学3年生、億は小学4年生、兆は小学5〜6年生で習います。"},
      {"q": "右から4桁で区切る方法を教えてください。", "a": "例：123456789 → 1|2345|6789。右から4桁ずつ「一・万・億」の順に読みます。"},
      {"q": "0が多い数の読み方は？", "a": "0がある桁は読みません。100030000（一億三万）のように飛ばして読みます。"},
      {"q": "日本語と英語の大きな数の単位は違いますか？", "a": "はい。日本語は4桁ごと（万・億・兆）、英語は3桁ごと（thousand・million・billion）に区切ります。"},
    ],
    "cta_href": "/grade-4.html",
    "cta_label": "4年生のドリルをやってみる",
    "related": [
      {"href": "/ookina-kazu.html",    "emoji": "🔢", "text": "大きな数ドリル"},
      {"href": "/gaisuu-guide.html",   "emoji": "🔢", "text": "がい数（四捨五入）"},
      {"href": "/suuji-4keta.html",    "emoji": "🔢", "text": "4桁の数"},
      {"href": "/grade-4-matome.html", "emoji": "📚", "text": "4年生 全単元まとめ"},
    ],
  },

  {
    "filename": "hiritu-guide.html",
    "title": "比率・歩合・百分率プリント【無料】変換の方法｜小学5年生",
    "description": "比率・歩合（割・分・厘）・百分率（%）の変換を印刷不要・スマホで練習できる無料プリント。三者の関係をわかりやすく解説。小学5年生向け。",
    "h1": "比率・歩合・百分率の変換プリント【無料】小学5年生",
    "eyecatch": "📊 割合の3つの表し方をマスター！0.75＝75%＝7割5分、この変換が自由にできるようになろう。",
    "body_html": """\
<h2>3つの表し方の関係</h2>
<div class="formula-box"><p>比率 0.75 ＝ 百分率 75% ＝ 歩合 7割5分</p></div>
<h2>変換方法</h2>
<ul>
  <li>比率 → %：× 100</li>
  <li>% → 比率：÷ 100</li>
  <li>比率 → 歩合：× 10（一の位が「割」）</li>
  <li>歩合 → 比率：÷ 10</li>
</ul>
<h2>よく使う変換の暗記</h2>
<ul>
  <li>1割 ＝ 0.1 ＝ 10%</li>
  <li>5割 ＝ 0.5 ＝ 50%</li>
  <li>3割5分 ＝ 0.35 ＝ 35%</li>
  <li>2割引 ＝ 定価の0.8倍 ＝ 80%</li>
</ul>
<div class="tip-box"><p>💡 スポーツの打率や商品の値引きで歩合・百分率は日常的に使われます。実例と結びつけて覚えましょう。</p></div>
<div class="warn-box"><p>⚠️ 「3割引」は「3割の値段」ではなく「3割分安い」＝7割の値段。紛らわしいので注意！</p></div>""",
    "faq": [
      {"q": "歩合・百分率はいつ習いますか？", "a": "小学5年生で割合の学習として習います。"},
      {"q": "「2割引」の計算方法を教えてください。", "a": "定価×(1-0.2)＝定価×0.8です。定価が1000円なら1000×0.8＝800円。"},
      {"q": "野球の打率（3割2分1厘）の計算方法は？", "a": "打率＝安打数÷打数です。0.321＝3割2分1厘（321厘＝32.1分＝3.21割）。"},
      {"q": "消費税（10%）の計算は？", "a": "税込価格＝本体価格×1.1（0.1が10%分）。本体1000円なら1100円になります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/wariai-guide.html",   "emoji": "📊", "text": "割合の求め方"},
      {"href": "/mondai-wariai.html",  "emoji": "📝", "text": "割合の文章題"},
      {"href": "/hi-guide.html",       "emoji": "📊", "text": "比の求め方"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "taishitsu-keisan.html",
    "title": "対称な図形の作図プリント【無料】線対称・点対称｜小学6年生",
    "description": "線対称・点対称な図形の見分け方と作図を印刷不要・スマホで練習できる無料プリント。対称の軸と中心の求め方を解説。小学6年生向け。",
    "h1": "対称な図形の作図プリント【無料】小学6年生",
    "eyecatch": "🔷 線対称・点対称は図形の美しさに関わる概念。見分け方と作図を確実にマスターしましょう！",
    "body_html": """\
<h2>線対称とは</h2>
<p>1本の直線で折り返すと完全に重なる図形です。その直線を「対称の軸」といいます。</p>
<ul>
  <li>線対称の例：正三角形（3本の軸）、長方形（2本の軸）、円（無数の軸）</li>
  <li>対称の軸は1本とは限りません</li>
</ul>
<h2>点対称とは</h2>
<p>1つの点を中心に180°回転すると重なる図形です。その点を「対称の中心」といいます。</p>
<ul>
  <li>点対称の例：正方形、平行四辺形、円</li>
  <li>対称の中心の求め方：対角線の交点</li>
</ul>
<div class="tip-box"><p>💡 線対称でも点対称でも図形の美しさが生まれます。自然界（雪の結晶・葉の形）にも多く見られます。</p></div>
<h2>作図の手順（線対称）</h2>
<ol>
  <li>各頂点から対称の軸に垂線を引く</li>
  <li>軸の反対側に同じ距離で点を打つ</li>
  <li>対応する頂点を直線でつなぐ</li>
</ol>""",
    "faq": [
      {"q": "対称な図形はいつ習いますか？", "a": "小学6年生で学習します。線対称・点対称の概念と作図を学びます。"},
      {"q": "線対称と点対称の両方の性質を持つ図形は？", "a": "正方形・長方形・ひし形・正三角形（点対称ではない）などがあります。円は両方の性質を持ちます。"},
      {"q": "正三角形は点対称ですか？", "a": "いいえ、正三角形は線対称（3本の軸）ですが点対称ではありません。180°回転しても重なりません。"},
      {"q": "線対称の軸が何本あるかはどう求めますか？", "a": "図形を実際に折り返してみる（または想像する）か、辺・角の数と性質から判断します。正n角形はn本の対称軸を持ちます。"},
    ],
    "cta_href": "/grade-6.html",
    "cta_label": "6年生のドリルをやってみる",
    "related": [
      {"href": "/taishou-figure.html", "emoji": "🔷", "text": "対称な図形ドリル"},
      {"href": "/goudo-figure.html",   "emoji": "🔷", "text": "図形の合同"},
      {"href": "/kakudai-shukuzu.html","emoji": "📐", "text": "拡大図・縮図"},
      {"href": "/grade-6-matome.html", "emoji": "📚", "text": "6年生 全単元まとめ"},
    ],
  },

  {
    "filename": "oyako-machigai.html",
    "title": "子どもの算数ミスが減らない？保護者向け原因と対策ガイド",
    "description": "子どもの算数ミスが減らない原因と効果的な対策を保護者向けに解説。計算ミス・理解不足・不注意の見分け方と改善方法を紹介。",
    "h1": "子どもの算数ミスが減らない？原因と対策ガイド",
    "eyecatch": "🔍 「何度言っても同じミスをする」には理由があります。ミスの種類に合った対策を取ることが改善の近道です！",
    "body_html": """\
<h2>算数ミスの3つの種類</h2>
<h3>①計算ミス（うっかりミス）</h3>
<p>分かっているのに計算間違いをする。繰り上がり忘れ・筆算ずれなど。</p>
<p>→ 対策：見直しの習慣化、丁寧に書く練習</p>
<h3>②理解不足</h3>
<p>概念が理解できていないため間違える。</p>
<p>→ 対策：その単元まで戻って理解し直す</p>
<h3>③不注意・読み違い</h3>
<p>問題文を最後まで読まない、単位を書き忘れるなど。</p>
<p>→ 対策：問題文に印をつけながら読む習慣</p>
<div class="tip-box"><p>💡 「どの種類のミスか」を把握することが改善の第一歩。全部同じ対策では解決しません。</p></div>
<h2>ミスが多い子の保護者ができること</h2>
<ul>
  <li>「なぜ間違えたか」を一緒に分析する</li>
  <li>間違えた問題の「やり直し」を確認する</li>
  <li>テスト返却後のミスの種類を分類する習慣をつける</li>
</ul>
<div class="warn-box"><p>⚠️ 「また間違えた！」と叱るだけでは改善しません。ミスの原因を一緒に考えることが大切です。</p></div>""",
    "faq": [
      {"q": "計算ミスと理解不足の見分け方は？", "a": "同じ問題をもう一度解いて正解できれば計算ミス、再度間違えたり手が止まれば理解不足です。"},
      {"q": "何度言っても同じミスをするのはなぜですか？", "a": "ミスの種類に合った対策が取れていないか、直す機会が少ないためです。ミスノートを作って同じミスのパターンを可視化しましょう。"},
      {"q": "見直しの習慣がなかなかつきません。", "a": "「時間が余ったら見直す」ではなく「必ず最後の2分を見直し時間にする」と決めると習慣化しやすいです。"},
      {"q": "算数ミスは成長とともに自然に減りますか？", "a": "意識的な改善なしには減りにくいです。ミスのパターンを把握して対策を取ることで着実に減っていきます。"},
    ],
    "cta_href": "/keisan-machigai.html",
    "cta_label": "計算ミスをなくす方法",
    "related": [
      {"href": "/keisan-machigai.html",  "emoji": "❌", "text": "計算ミスをなくす方法"},
      {"href": "/tesuto-naoshi.html",    "emoji": "📝", "text": "テストの直し方"},
      {"href": "/note-torikumi.html",    "emoji": "📓", "text": "ノートの取り方"},
      {"href": "/shukudai-oshiekata.html","emoji": "📝", "text": "宿題の教え方"},
    ],
  },

  {
    "filename": "sangaku-chishiki.html",
    "title": "算数に関する豆知識【子どもが喜ぶ数のふしぎ】",
    "description": "算数・数学の面白い豆知識を紹介。フィボナッチ数列・円周率・特別な数など、子どもが「算数って面白い！」と思えるトリビア集。",
    "h1": "算数の豆知識【数のふしぎ・おもしろ話】",
    "eyecatch": "🤩 算数って実はとっても面白い！知っておくと自慢できる数の不思議をまとめました。",
    "body_html": """\
<h2>数の不思議①：1÷7のひみつ</h2>
<p>1÷7＝0.142857142857…と同じ数字が繰り返します（循環小数）。</p>
<p>しかもこの6桁「142857」は不思議な性質を持っています：142857×2＝285714（同じ数字！）</p>

<h2>数の不思議②：フィボナッチ数列</h2>
<p>1, 1, 2, 3, 5, 8, 13, 21, 34, 55…（前2つを足したもの）</p>
<p>ひまわりの種・貝殻の形・植物の葉の付き方にこの数列が現れます。</p>

<h2>数の不思議③：ぞろ目の計算</h2>
<p>1×1＝1、11×11＝121、111×111＝12321…</p>
<p>計算すると山型の数字になります！</p>

<h2>数の不思議④：3の倍数チェック</h2>
<p>各桁の数字の和が3の倍数なら、その数も3の倍数です。</p>
<p>例：123 → 1＋2＋3＝6（3の倍数）→ 123÷3＝41 ✓</p>
<div class="tip-box"><p>💡 9の倍数チェックも同じ方法です。各桁の和が9の倍数なら9で割り切れます。</p></div>

<h2>数の不思議⑤：円周率π</h2>
<p>3.14159265358979…と無限に続く不思議な数。どこにも繰り返しがありません。</p>
<p>円周率を100桁以上暗記する人もいます（現記録は数万桁！）。</p>""",
    "faq": [
      {"q": "フィボナッチ数列はなぜ自然界に現れるのですか？", "a": "植物が効率よく成長するために葉や種を配置する数学的な法則と関係しています。「黄金比」にも関連する不思議な数列です。"},
      {"q": "3の倍数チェックはなぜ成り立つのですか？", "a": "10を3で割ると余り1（10≡1 mod 3）になるため、各桁の数字をそのまま足した余りが元の数の余りと等しくなります。"},
      {"q": "円周率を暗記しても意味がありますか？", "a": "実用上は3.14で十分ですが、暗記挑戦は集中力や記憶力のトレーニングになります。"},
      {"q": "小学生に算数の面白さを伝えるには？", "a": "こうした豆知識や日常の謎（なぜ時計は60分？）を一緒に考えることが効果的です。「なぜ？」という好奇心が算数学習の原動力になります。"},
    ],
    "cta_href": "/",
    "cta_label": "算数ドリルで練習する",
    "related": [
      {"href": "/sosuu-guide.html",        "emoji": "🔢", "text": "素数の話"},
      {"href": "/en-chokukei.html",        "emoji": "⭕", "text": "円と円周率"},
      {"href": "/sansu-kirai.html",        "emoji": "😢", "text": "算数が嫌いな子へ"},
      {"href": "/oyako-sansu.html",        "emoji": "👨‍👩‍👧", "text": "親子で楽しむ算数"},
    ],
  },

  {
    "filename": "device-free-sansu.html",
    "title": "スマホ・タブレットなしで算数練習する方法【アナログ学習法】",
    "description": "デジタルデバイスなしで算数力を伸ばすアナログ学習法を紹介。計算カード・ノート・ゲームを使った練習方法をまとめました。",
    "h1": "デバイスなしで算数練習する方法【アナログ学習法】",
    "eyecatch": "📝 スマホなしでも算数は十分練習できます！計算カードやノートを使ったアナログ学習法を紹介します。",
    "body_html": """\
<h2>アナログ学習のメリット</h2>
<ul>
  <li>目が疲れない</li>
  <li>書く力・集中力が身につく</li>
  <li>親子のコミュニケーションになる</li>
  <li>どこでもできる（電源不要）</li>
</ul>

<h2>計算カード（フラッシュカード）の使い方</h2>
<ol>
  <li>市販の計算カードまたは手作りカードを用意</li>
  <li>問題を出して答えを言わせる</li>
  <li>正解・不正解に分けて、不正解カードを繰り返す</li>
  <li>タイムを計って速さを競う</li>
</ol>
<div class="tip-box"><p>💡 手作りカードは子どもに書かせると学習効果が2倍！書く行為自体が記憶を強化します。</p></div>

<h2>ノートを使った練習法</h2>
<ul>
  <li>毎日10問を方眼ノートに解く習慣</li>
  <li>答え合わせは親が行う（子どもが採点すると楽をしてしまいがち）</li>
  <li>間違えた問題に★をつけて翌日再挑戦</li>
</ul>

<h2>ゲームで楽しく練習</h2>
<ul>
  <li><strong>トランプ：</strong>数字の足し算・引き算・大小比較</li>
  <li><strong>サイコロ：</strong>出た目の合計・かけ算</li>
  <li><strong>お買い物ごっこ：</strong>足し算・お釣りの計算</li>
</ul>""",
    "faq": [
      {"q": "計算カードは市販と手作りどちらがいいですか？", "a": "どちらでも効果的です。手作りの場合は書く練習にもなります。市販品はサイズや印刷品質が揃っています。"},
      {"q": "アナログ学習にかける時間の目安は？", "a": "1回5〜15分が集中できる目安です。短時間でも毎日継続することが最重要です。"},
      {"q": "デジタルとアナログはどちらが効果的ですか？", "a": "組み合わせるのが最も効果的です。デジタルは即時フィードバック、アナログは書く力・集中力の育成に強みがあります。"},
      {"q": "トランプゲームで算数練習する方法を教えてください。", "a": "絵札を除いて数字カードだけを使い、2枚引いて足す（引く）ゲームが定番です。「21ゲーム」もかけ算・引き算の練習になります。"},
    ],
    "cta_href": "/",
    "cta_label": "オンラインドリルも試してみる",
    "related": [
      {"href": "/mainichi-drill.html",      "emoji": "📅", "text": "毎日の計算練習法"},
      {"href": "/oyako-sansu.html",         "emoji": "👨‍👩‍👧", "text": "親子で楽しむ算数"},
      {"href": "/sansu-benkyou-houhou.html","emoji": "📖", "text": "算数の効果的な勉強法"},
      {"href": "/anzan-practice.html",      "emoji": "🧠", "text": "暗算練習"},
    ],
  },

  {
    "filename": "mondai-sokudo2.html",
    "title": "速さの文章題プリント（応用）【無料】旅人算・流水算｜小学5〜6年生",
    "description": "速さの応用文章題（旅人算・流水算）を印刷不要・スマホで練習できる無料プリント。向かい合いや追いかけの問題を解説。小学5〜6年生向け。",
    "h1": "速さの文章題（応用）プリント【無料】小学5〜6年生",
    "eyecatch": "🚀 速さの応用問題に挑戦！向かい合いや追いかけのパターンをマスターしよう。",
    "body_html": """\
<h2>旅人算の基本パターン</h2>
<h3>①向かい合って出発（出会う問題）</h3>
<p>2人が向かい合って歩く → 合わせた速さで近づく</p>
<div class="formula-box"><p>出会うまでの時間 ＝ 距離 ÷ (速さA ＋ 速さB)</p></div>
<p>例：2km離れた2人が分速80mと分速70mで向かい合って歩く。何分後に会う？</p>
<p>2000 ÷ (80＋70) ＝ 2000 ÷ 150 ≈ 13分</p>

<h3>②同じ方向で追いかける問題</h3>
<div class="formula-box"><p>追いつくまでの時間 ＝ 距離の差 ÷ (速さA ー 速さB)</p></div>

<h2>ポイント</h2>
<ul>
  <li>向かい合い：速さを足す（近づく速さ）</li>
  <li>追いかけ：速さを引く（縮まる速さ）</li>
  <li>単位を統一してから計算</li>
</ul>
<div class="tip-box"><p>💡 図（数直線）を描いて位置関係を整理することが旅人算を解くコツです。</p></div>""",
    "faq": [
      {"q": "旅人算はいつ習いますか？", "a": "小学5〜6年生の速さの応用として習います。中学受験でも頻出の単元です。"},
      {"q": "なぜ向かい合いは速さを足すのですか？", "a": "2人が同時に近づいているため、1秒当たりに縮まる距離は2人の速さの合計になります。"},
      {"q": "流水算とは何ですか？", "a": "川の流れを考慮した速さの問題です。上り（流れに逆らう）は速さを引き、下り（流れに乗る）は速さを足します。"},
      {"q": "追いつく問題と出会う問題の違いは？", "a": "出会う問題は2人が向かい合って進む（速さを足す）、追いつく問題は同じ方向に進む（速さの差を使う）点が違います。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/sokudo-guide.html",   "emoji": "🚀", "text": "速さの基本"},
      {"href": "/mondai-sokudo.html",  "emoji": "📝", "text": "速さの文章題（基礎）"},
      {"href": "/jikan-henkan.html",   "emoji": "⏱️", "text": "時間の単位換算"},
      {"href": "/grade-5-matome.html", "emoji": "📚", "text": "5年生 全単元まとめ"},
    ],
  },

  {
    "filename": "tokubetsu-suji.html",
    "title": "特別な数・整数の性質まとめ【小学生向け】倍数・約数・素数",
    "description": "整数の性質（倍数・約数・素数・偶数・奇数）を一覧でまとめた解説ページ。テスト前の確認・まとめ学習に最適。",
    "h1": "整数の性質まとめ【小学生向け】",
    "eyecatch": "🔢 倍数・約数・素数・偶数・奇数を一気に整理！数の性質をマスターして算数を得意にしましょう。",
    "body_html": """\
<h2>整数の性質まとめ</h2>
<h3>偶数・奇数</h3>
<ul>
  <li>偶数：2で割り切れる（0,2,4,6,8…）</li>
  <li>奇数：2で割り切れない（1,3,5,7,9…）</li>
</ul>
<h3>倍数・約数</h3>
<ul>
  <li>倍数：ある数を整数倍した数（6の倍数：6,12,18…）</li>
  <li>約数：ある数を割り切れる整数（12の約数：1,2,3,4,6,12）</li>
  <li>公倍数・公約数：2つ以上の数に共通の倍数・約数</li>
</ul>
<h3>最大公約数・最小公倍数</h3>
<div class="formula-box"><p>GCD(最大公約数)：公約数の最大値 → 約分に使う<br>LCM(最小公倍数)：公倍数の最小値 → 通分に使う</p></div>
<h3>素数</h3>
<p>1とその数自身以外に約数を持たない数（2,3,5,7,11,13…）</p>
<div class="tip-box"><p>💡 どの整数も素数の積として表せます（素因数分解）。12＝2²×3など。</p></div>
<h2>割り算のチェック法</h2>
<ul>
  <li>2の倍数：一の位が0,2,4,6,8</li>
  <li>3の倍数：各桁の和が3の倍数</li>
  <li>5の倍数：一の位が0か5</li>
  <li>9の倍数：各桁の和が9の倍数</li>
</ul>""",
    "faq": [
      {"q": "倍数と公倍数の違いは？", "a": "倍数は1つの数の倍（3の倍数：3,6,9…）。公倍数は2つ以上の数に共通する倍数（3と4の公倍数：12,24…）。"},
      {"q": "なぜ3の倍数チェックは各桁の和でできるのですか？", "a": "10≡1（mod 3）なので、各桁の数字×10の累乗を足した数（元の数）の3で割った余りは、各桁の和の3で割った余りと等しくなります。"},
      {"q": "素因数分解を使うとどんなことができますか？", "a": "最大公約数・最小公倍数を効率よく求めたり、分数の約分を一度で終わらせたりすることができます。"},
      {"q": "整数の性質は小学校でどこまで学びますか？", "a": "倍数・約数・公倍数・公約数は小学5年生で学びます。素数・素因数分解は中学で詳しく学びますが、概念として小学高学年で触れることがあります。"},
    ],
    "cta_href": "/grade-5.html",
    "cta_label": "5年生のドリルをやってみる",
    "related": [
      {"href": "/baisuu-yakusuu.html",   "emoji": "🔢", "text": "倍数と約数"},
      {"href": "/gusuu-kisuu.html",      "emoji": "🔢", "text": "偶数と奇数"},
      {"href": "/sosuu-guide.html",      "emoji": "🔢", "text": "素数の話"},
      {"href": "/saishou-koubaisu.html", "emoji": "🔢", "text": "最小公倍数"},
    ],
  },

  {
    "filename": "nyuugaku-sansu2.html",
    "title": "入学前に覚えたい算数【年長さん向け数の準備】",
    "description": "小学校入学前（年長・5〜6歳）に覚えておきたい算数の基礎を解説。数の読み書き・数え方・形の名前など入学準備ガイド。",
    "h1": "入学前に覚えたい算数【年長さん向け】",
    "eyecatch": "🌟 小学校入学前に算数の土台を作りましょう！焦らずゆっくり、楽しみながら準備できます。",
    "body_html": """\
<h2>入学前に覚えておきたいこと</h2>
<h3>①数の読み書き（1〜20）</h3>
<ul>
  <li>1〜10を声に出して数えられる</li>
  <li>1〜10の数字を読み書きできる</li>
  <li>10までの数の大小が分かる</li>
</ul>
<h3>②数え方</h3>
<ul>
  <li>物を1つずつ指さして数える</li>
  <li>「全部でいくつ？」を数えられる</li>
</ul>
<h3>③簡単な足し算・引き算の感覚</h3>
<p>「3個と2個合わせると5個」という感覚（指を使ってOK）</p>
<h3>④時計の読み方（ちょうど）</h3>
<p>「3時ちょうど」「6時ちょうど」が読める程度でOK</p>
<h3>⑤形の名前</h3>
<p>丸・三角・四角の区別ができる</p>
<div class="tip-box"><p>💡 「できる」より「楽しめる」が大事。算数は難しいものではなく面白いものだという感覚を入学前に作ることが最大の準備です。</p></div>
<div class="warn-box"><p>⚠️ 無理な先取り（難しいかけ算など）は逆効果になることも。基礎の「楽しさ」を大切に。</p></div>""",
    "faq": [
      {"q": "入学前にどこまで算数を教えるべきですか？", "a": "1〜10の読み書き・数え方・簡単な数の大小比較ができれば十分です。先取り学習より「数が面白い」と感じる経験を大切にしましょう。"},
      {"q": "数字の書き方は入学前に練習すべきですか？", "a": "練習しておくと安心ですが必須ではありません。入学後に学校で習います。ただし鉛筆の持ち方と線の書き方（縦線・横線・曲線）の練習は有効です。"},
      {"q": "数への興味がない子にはどう働きかけますか？", "a": "日常生活の中で自然に（おやつの数を数える・カルタや絵本）取り入れることが効果的です。無理に「勉強」としてやらせると逆効果です。"},
      {"q": "入学後すぐに苦労しないための準備は？", "a": "1〜10の数の読み書きと「いくつといくつ」（5は3と2など）の感覚を持っていると1年生の最初がスムーズです。"},
    ],
    "cta_href": "/nyuugaku-mae.html",
    "cta_label": "入学準備ページへ",
    "related": [
      {"href": "/nyuugaku-mae.html",  "emoji": "🎒", "text": "入学前の算数準備"},
      {"href": "/youji-kazu.html",    "emoji": "🔢", "text": "幼児向け数の学習"},
      {"href": "/suji-kakikata.html", "emoji": "✏️", "text": "数字の書き方"},
      {"href": "/tokei-yomikata.html","emoji": "🕐", "text": "時計の読み方（幼児向け）"},
    ],
  },

  # ===== Batch 8 =====
  {
    "filename": "heikin-guide.html",
    "title": "平均の求め方｜算数ドリル",
    "description": "平均の計算方法をわかりやすく解説。合計÷個数の基本から文章題まで練習しましょう。",
    "h1": "平均の求め方",
    "eyecatch": "📊",
    "body_html": """\
<h2>平均とは？</h2>
<p>いくつかの数をならして同じ大きさにしたものが<strong>平均</strong>です。</p>
<div class="formula-box"><p>平均 ＝ 合計 ÷ 個数</p></div>
<h3>例題</h3>
<p>テストの点数が 80, 90, 70, 60 のとき平均は？</p>
<p>合計 = 80+90+70+60 = 300　　300 ÷ 4 = <strong>75点</strong></p>
<div class="tip-box"><p>💡 平均を使うと「全体の傾向」がわかります。</p></div>""",
    "faq": [
      {"q": "平均が整数にならない場合は？", "a": "割り切れない場合は小数で答えます。例：合計7÷3個＝約2.33。"},
      {"q": "0が含まれる場合も個数に数える？", "a": "はい、0も個数に含めます。"},
    ],
    "cta_href": "/mondai-hikizan.html",
    "cta_label": "文章題を練習する",
    "related": [
      {"href": "/warizan-kiso.html",   "emoji": "➗", "text": "わり算の基本"},
      {"href": "/syousuu-warizan.html","emoji": "🔢", "text": "小数のわり算"},
    ],
  },
  {
    "filename": "kakudo-kiso.html",
    "title": "角度の基本｜算数ドリル",
    "description": "角度の読み方・書き方・直角・鋭角・鈍角を解説。分度器の使い方も紹介します。",
    "h1": "角度の基本と分度器の使い方",
    "eyecatch": "📐",
    "body_html": """\
<h2>角度とは？</h2>
<p>2本の直線が交わる「開き具合」を角度といい、<strong>度（°）</strong>で表します。</p>
<h3>角度の種類</h3>
<ul>
<li><strong>直角</strong>：90°</li>
<li><strong>鋭角</strong>：90°より小さい</li>
<li><strong>鈍角</strong>：90°より大きく180°より小さい</li>
<li><strong>平角</strong>：180°（一直線）</li>
</ul>
<div class="formula-box"><p>三角形の内角の和 ＝ 180°</p></div>
<div class="tip-box"><p>💡 分度器は中心を頂点に合わせ、0°の線を一辺に合わせて測ります。</p></div>""",
    "faq": [
      {"q": "直角三角形は何度？", "a": "1つの角が必ず90°の三角形です。残り2角の合計は90°です。"},
      {"q": "360°を超える角度はある？", "a": "算数では基本的に0°〜360°で考えます。"},
    ],
    "cta_href": "/sankakkei-shurui.html",
    "cta_label": "三角形の種類を復習",
    "related": [
      {"href": "/sankakkei-shurui.html","emoji": "🔺", "text": "三角形の種類"},
      {"href": "/menseki-sankakukei.html","emoji": "📐", "text": "三角形の面積"},
    ],
  },
  {
    "filename": "harizan-guide.html",
    "title": "植木算の解き方｜算数ドリル",
    "description": "植木算（間隔と本数の関係）の基本から応用まで丁寧に解説します。",
    "h1": "植木算の解き方",
    "eyecatch": "🌳",
    "body_html": """\
<h2>植木算とは？</h2>
<p>木を一定間隔で並べるとき、木の本数と間の数の関係を求める問題です。</p>
<div class="formula-box">
<p>両端に植える：本数 ＝ 間の数 ＋ 1</p>
<p>一方だけ植える：本数 ＝ 間の数</p>
<p>円形に植える：本数 ＝ 間の数</p>
</div>
<h3>例題</h3>
<p>100mの道に10m間隔で両端を含めて木を植えると？</p>
<p>間の数 = 100÷10 = 10　　本数 = 10＋1 = <strong>11本</strong></p>
<div class="tip-box"><p>💡 「両端あり・なし・円形」の3パターンを整理しましょう。</p></div>""",
    "faq": [
      {"q": "円形の場合はなぜ本数=間の数？", "a": "円形は端がないため、間の数と本数が同じになります。"},
      {"q": "中学受験でも出ますか？", "a": "はい、中学受験の頻出問題です。"},
    ],
    "cta_href": "/grade-5-tips.html",
    "cta_label": "5年生のコツを見る",
    "related": [
      {"href": "/sokudo-guide.html","emoji": "🏃", "text": "速さの基本"},
      {"href": "/mondai-menseki.html","emoji": "📐", "text": "面積の文章題"},
    ],
  },
  {
    "filename": "ruikei-keisan.html",
    "title": "累計・合計の計算｜算数ドリル",
    "description": "累計（るいけい）の意味と計算方法を解説。グラフや表の読み取りにも役立ちます。",
    "h1": "累計・合計の計算",
    "eyecatch": "📈",
    "body_html": """\
<h2>累計とは？</h2>
<p>数を順番に足し合わせていったものを<strong>累計</strong>といいます。</p>
<h3>例：売上の累計</h3>
<table border="1" style="border-collapse:collapse;padding:4px">
<tr><th>月</th><th>売上</th><th>累計</th></tr>
<tr><td>1月</td><td>100</td><td>100</td></tr>
<tr><td>2月</td><td>150</td><td>250</td></tr>
<tr><td>3月</td><td>120</td><td>370</td></tr>
</table>
<div class="tip-box"><p>💡 折れ線グラフや棒グラフで「累計」が出たら、前の値と今の値を足すだけです。</p></div>""",
    "faq": [
      {"q": "累計と合計の違いは？", "a": "合計は全部を足した最終結果、累計は途中途中の足し算の結果をすべて示したものです。"},
    ],
    "cta_href": "/boubou-graph.html",
    "cta_label": "グラフの読み方を練習",
    "related": [
      {"href": "/boubou-graph.html","emoji": "📊", "text": "棒グラフの読み方"},
      {"href": "/oretsu-graph.html","emoji": "📈", "text": "折れ線グラフ"},
    ],
  },
  {
    "filename": "mahouujin-guide.html",
    "title": "魔方陣の解き方｜算数ドリル",
    "description": "3×3魔方陣の解き方を解説。縦・横・斜めの合計が同じになる数の配置を練習しましょう。",
    "h1": "魔方陣の解き方",
    "eyecatch": "🔮",
    "body_html": """\
<h2>魔方陣とは？</h2>
<p>縦・横・斜めのどの列も合計が同じになるように数を並べたマス目です。</p>
<h3>3×3魔方陣（1〜9を使う場合）</h3>
<div class="formula-box"><p>1〜9の合計 = 45　　1列の合計 = 45÷3 = 15</p></div>
<p>中心には必ず5が入ります。</p>
<pre style="background:#f5f5f5;padding:8px">
2 | 7 | 6
9 | 5 | 1
4 | 3 | 8
</pre>
<div class="tip-box"><p>💡 4隅と中心から埋めていくと解きやすいです。</p></div>""",
    "faq": [
      {"q": "4×4魔方陣も算数で出ますか？", "a": "中学受験の難問として出ることがあります。基本は3×3から習得しましょう。"},
    ],
    "cta_href": "/sangaku-chishiki.html",
    "cta_label": "算数の豆知識を見る",
    "related": [
      {"href": "/sangaku-chishiki.html","emoji": "🧮", "text": "算数の豆知識"},
      {"href": "/sosuu-guide.html","emoji": "🔢", "text": "素数一覧"},
    ],
  },
  {
    "filename": "taisaku-3nen.html",
    "title": "3年生の算数まとめ・弱点対策｜算数ドリル",
    "description": "小学3年生の算数で躓きやすいポイントを総まとめ。かけ算・わり算・大きな数・時間の単位を復習。",
    "h1": "3年生の算数まとめ・弱点対策",
    "eyecatch": "📝",
    "body_html": """\
<h2>3年生で学ぶ主な内容</h2>
<ul>
<li>かけ算九九の完成・かけ算の筆算</li>
<li>わり算の基本（あまりなし・あまりあり）</li>
<li>大きな数（千・万）</li>
<li>時間・長さ・重さの単位換算</li>
<li>分数の基本</li>
<li>三角形・四角形</li>
</ul>
<div class="warn-box"><p>⚠️ 特に<strong>かけ算九九の暗記</strong>は4年生以降の全単元に影響します。確実に定着させましょう。</p></div>
<div class="tip-box"><p>💡 苦手な九九だけ集中して練習するのが効率的です。</p></div>""",
    "faq": [
      {"q": "3年生でわり算がわからない場合は？", "a": "かけ算九九をもとにわり算を考えます。まず九九の定着を確認しましょう。"},
      {"q": "単位換算が苦手です", "a": "1km=1000m、1kg=1000gなど「1000倍」の関係を表にして覚えると整理しやすいです。"},
    ],
    "cta_href": "/grade-3-tips.html",
    "cta_label": "3年生の勉強のコツを見る",
    "related": [
      {"href": "/grade-3-tips.html","emoji": "📚", "text": "3年生の勉強法"},
      {"href": "/kakezan-rensyu.html","emoji": "✖️", "text": "かけ算練習"},
      {"href": "/warizan-kiso.html","emoji": "➗", "text": "わり算の基本"},
    ],
  },
  {
    "filename": "taisaku-4nen.html",
    "title": "4年生の算数まとめ・弱点対策｜算数ドリル",
    "description": "小学4年生の算数で躓きやすいポイントを総まとめ。割り算の筆算・小数・面積・角度を復習。",
    "h1": "4年生の算数まとめ・弱点対策",
    "eyecatch": "📝",
    "body_html": """\
<h2>4年生で学ぶ主な内容</h2>
<ul>
<li>大きな数（億・兆）</li>
<li>割り算の筆算</li>
<li>小数のたし算・ひき算</li>
<li>角度・三角形の内角</li>
<li>面積（長方形・正方形）</li>
<li>折れ線グラフ・棒グラフ</li>
</ul>
<div class="warn-box"><p>⚠️ <strong>割り算の筆算</strong>は桁が増えるにつれて複雑になります。商の見当のつけ方を練習しましょう。</p></div>
<div class="tip-box"><p>💡 小数は「0.1が何個」と考えると計算しやすいです。</p></div>""",
    "faq": [
      {"q": "小数の計算でミスが多いです", "a": "小数点の位置に注意しましょう。筆算では小数点を縦に揃えて書くのが基本です。"},
      {"q": "面積の単位（cm²・m²）が混乱します", "a": "面積は「縦×横」で求め、単位も2乗になります。単位だけ分けて考えると整理しやすいです。"},
    ],
    "cta_href": "/grade-4-tips.html",
    "cta_label": "4年生の勉強のコツを見る",
    "related": [
      {"href": "/grade-4-tips.html","emoji": "📚", "text": "4年生の勉強法"},
      {"href": "/warizan-hissan.html","emoji": "➗", "text": "わり算の筆算"},
      {"href": "/menseki-heikoushikakkei.html","emoji": "📐", "text": "長方形の面積"},
    ],
  },
  {
    "filename": "taisaku-5nen.html",
    "title": "5年生の算数まとめ・弱点対策｜算数ドリル",
    "description": "小学5年生の算数で躓きやすいポイントを総まとめ。分数・割合・速さ・図形を復習。",
    "h1": "5年生の算数まとめ・弱点対策",
    "eyecatch": "📝",
    "body_html": """\
<h2>5年生で学ぶ主な内容</h2>
<ul>
<li>整数・小数・分数の四則計算</li>
<li>公約数・公倍数</li>
<li>割合（百分率・歩合）</li>
<li>速さ（距離・時間・速さの関係）</li>
<li>面積（三角形・平行四辺形・ひし形・台形）</li>
<li>立体（直方体・立方体の体積）</li>
</ul>
<div class="warn-box"><p>⚠️ <strong>割合</strong>と<strong>速さ</strong>は多くの子が躓く最重要単元。図（線分図・面積図）を使った解き方を身につけましょう。</p></div>""",
    "faq": [
      {"q": "割合がどうしてもわかりません", "a": "「割合＝比べる量÷もとにする量」と覚えましょう。図を描いて整理することが大切です。"},
      {"q": "速さの3公式が混乱します", "a": "「はじき」（速さ・距離・時間）の三角形で覚えると便利です。"},
    ],
    "cta_href": "/grade-5-tips.html",
    "cta_label": "5年生の勉強のコツを見る",
    "related": [
      {"href": "/grade-5-tips.html","emoji": "📚", "text": "5年生の勉強法"},
      {"href": "/sokudo-guide.html","emoji": "🏃", "text": "速さの基本"},
      {"href": "/wariai-guide.html","emoji": "📊", "text": "割合の基本"},
    ],
  },
  {
    "filename": "taisaku-6nen.html",
    "title": "6年生の算数まとめ・弱点対策｜算数ドリル",
    "description": "小学6年生の算数で躓きやすいポイントを総まとめ。比・文字式・比例・反比例・資料の活用。",
    "h1": "6年生の算数まとめ・弱点対策",
    "eyecatch": "📝",
    "body_html": """\
<h2>6年生で学ぶ主な内容</h2>
<ul>
<li>分数÷分数</li>
<li>比と比例式</li>
<li>文字を使った式</li>
<li>比例・反比例</li>
<li>円の面積・円柱・円錐の体積</li>
<li>資料の活用（平均・最頻値・中央値）</li>
</ul>
<div class="warn-box"><p>⚠️ <strong>分数÷分数</strong>は中学数学の基礎。「÷は逆数をかける」を確実に理解しましょう。</p></div>
<div class="tip-box"><p>💡 6年生の内容は中学1年生の内容と深く繋がっています。理解重視の学習を心がけましょう。</p></div>""",
    "faq": [
      {"q": "分数÷分数がいつも間違えます", "a": "「÷b/c = ×c/b（逆数）」と覚えて、必ず逆数に直してからかけ算してください。"},
      {"q": "比と割合の違いは？", "a": "割合は2量の比較を1つの数で表し、比は「3:2」のように2量の関係を表します。"},
    ],
    "cta_href": "/grade-6-tips.html",
    "cta_label": "6年生の勉強のコツを見る",
    "related": [
      {"href": "/grade-6-tips.html","emoji": "📚", "text": "6年生の勉強法"},
      {"href": "/bunsuu-warizan.html","emoji": "➗", "text": "分数のわり算"},
      {"href": "/hi-guide.html","emoji": "📊", "text": "比の基本"},
    ],
  },
  {
    "filename": "mondai-waribiki.html",
    "title": "割引・売買の文章題｜算数ドリル",
    "description": "定価・売価・割引・利益の計算問題を練習。割合を使った売買算の解き方を解説します。",
    "h1": "割引・売買の文章題",
    "eyecatch": "🛒",
    "body_html": """\
<h2>売買算の基本用語</h2>
<ul>
<li><strong>仕入れ値</strong>：買ってくる値段</li>
<li><strong>定価</strong>：普通に売る値段（仕入れ値＋利益）</li>
<li><strong>売価</strong>：実際に売る値段（割引後など）</li>
<li><strong>利益</strong>：売価－仕入れ値</li>
</ul>
<div class="formula-box">
<p>定価 ＝ 仕入れ値 × (1 ＋ 利益率)</p>
<p>売価 ＝ 定価 × (1 － 割引率)</p>
</div>
<h3>例題</h3>
<p>仕入れ値500円の商品に2割の利益を乗せ、さらに1割引きで売ると？</p>
<p>定価 = 500×1.2 = 600円　　売価 = 600×0.9 = <strong>540円</strong>　　利益 = 540-500 = <strong>40円</strong></p>""",
    "faq": [
      {"q": "「2割引き」と「8掛け」は同じですか？", "a": "はい、同じです。2割引き＝定価×0.8です。"},
      {"q": "「原価の3割増し」の計算は？", "a": "原価×1.3です。"},
    ],
    "cta_href": "/wariai-guide.html",
    "cta_label": "割合の基本を復習",
    "related": [
      {"href": "/wariai-guide.html","emoji": "📊", "text": "割合の基本"},
      {"href": "/hiritu-guide.html","emoji": "🔢", "text": "比率・百分率"},
      {"href": "/mondai-sokudo2.html","emoji": "🏃", "text": "速さの応用"},
    ],
  },
  {
    "filename": "mondai-nenrei.html",
    "title": "年齢算の解き方｜算数ドリル",
    "description": "年齢算（現在・過去・未来の年齢差の問題）の解き方を解説。線分図で整理する方法を紹介します。",
    "h1": "年齢算の解き方",
    "eyecatch": "👨‍👩‍👧",
    "body_html": """\
<h2>年齢算とは？</h2>
<p>2人以上の人の年齢の関係を使って解く問題です。</p>
<h3>ポイント</h3>
<ul>
<li>年齢差は何年経っても変わらない</li>
<li>何年後・何年前でも差は一定</li>
</ul>
<div class="formula-box"><p>年齢差 ＝ 一定（変わらない）</p></div>
<h3>例題</h3>
<p>現在、父40歳・子10歳。父の年齢が子の2倍になるのは何年後？</p>
<p>差 = 30歳（変わらない）　何年後かをxとすると：(40+x) = 2×(10+x)　→ x = 20</p>
<p>答え：<strong>20年後</strong></p>
<div class="tip-box"><p>💡 線分図で現在と未来の年齢を並べると整理しやすいです。</p></div>""",
    "faq": [
      {"q": "年齢差がいつも変わらないのはなぜ？", "a": "2人とも毎年1歳ずつ増えるので、差は変わりません。"},
    ],
    "cta_href": "/mondai-sokudo2.html",
    "cta_label": "速さの応用問題を練習",
    "related": [
      {"href": "/mondai-waribiki.html","emoji": "🛒", "text": "割引・売買の問題"},
      {"href": "/mondai-bunsuu.html","emoji": "½", "text": "分数の文章題"},
    ],
  },
  {
    "filename": "mondai-menseki2.html",
    "title": "複合図形の面積｜算数ドリル",
    "description": "L字・コの字・円の一部など複合図形の面積の求め方を解説。分割・補完法で解きましょう。",
    "h1": "複合図形の面積",
    "eyecatch": "🔷",
    "body_html": """\
<h2>複合図形とは？</h2>
<p>いくつかの図形を組み合わせたり、一部を切り取った形です。</p>
<h3>基本の解き方</h3>
<ul>
<li><strong>分割法</strong>：図形をいくつかの基本図形に分けて面積を足す</li>
<li><strong>補完法</strong>：大きな図形から余分な部分を引く</li>
</ul>
<h3>例：L字型</h3>
<p>縦10cm・横8cmの長方形から縦4cm・横3cmを切り取った形</p>
<p>全体 = 10×8 = 80　　切り取り = 4×3 = 12　　面積 = <strong>68cm²</strong></p>
<div class="tip-box"><p>💡 補助線を引いて基本図形に分けるのがコツです。</p></div>""",
    "faq": [
      {"q": "円の一部（扇形）の面積は？", "a": "扇形の面積 = 円の面積 × （中心角÷360）です。"},
      {"q": "コの字型の求め方は？", "a": "大きな長方形から内側の長方形を引く補完法が簡単です。"},
    ],
    "cta_href": "/menseki-fukuzatsu.html",
    "cta_label": "複雑な面積問題へ",
    "related": [
      {"href": "/menseki-fukuzatsu.html","emoji": "🔷", "text": "複雑な面積"},
      {"href": "/menseki-enza.html","emoji": "⭕", "text": "円の面積"},
      {"href": "/menseki-sankakukei.html","emoji": "📐", "text": "三角形の面積"},
    ],
  },
  {
    "filename": "tanihenkan-guide.html",
    "title": "単位換算まとめ｜算数ドリル",
    "description": "長さ・重さ・面積・体積・時間の単位換算をまとめて解説。換算表と練習問題付きです。",
    "h1": "単位換算まとめ",
    "eyecatch": "📏",
    "body_html": """\
<h2>よく使う単位換算</h2>
<h3>長さ</h3>
<p>1km＝1000m　1m＝100cm　1cm＝10mm</p>
<h3>重さ</h3>
<p>1t＝1000kg　1kg＝1000g</p>
<h3>面積</h3>
<p>1km²＝1000000m²　1m²＝10000cm²　1a＝100m²　1ha＝10000m²</p>
<h3>体積・容積</h3>
<p>1L＝1000mL　1dL＝100mL　1m³＝1000000cm³</p>
<h3>時間</h3>
<p>1時間＝60分　1分＝60秒　1日＝24時間</p>
<div class="tip-box"><p>💡 「大きい単位→小さい単位」は×、「小さい単位→大きい単位」は÷です。</p></div>""",
    "faq": [
      {"q": "dL（デシリットル）はどんな場面で使いますか？", "a": "主に小学校低学年の算数で登場します。日常生活ではあまり使いません。"},
      {"q": "面積の単位「a（アール）」「ha（ヘクタール）」は？", "a": "農地や土地の広さを表すのに使います。1ha＝10000m²と覚えましょう。"},
    ],
    "cta_href": "/jikan-henkan.html",
    "cta_label": "時間の換算を練習",
    "related": [
      {"href": "/jikan-henkan.html","emoji": "🕐", "text": "時間の換算"},
      {"href": "/jikan-keisan.html","emoji": "⏱", "text": "時間の計算"},
      {"href": "/taiseki-kiso.html","emoji": "📦", "text": "体積の基本"},
    ],
  },
  {
    "filename": "rounding-guide.html",
    "title": "切り捨て・切り上げ・四捨五入の違い｜算数ドリル",
    "description": "切り捨て・切り上げ・四捨五入の3種類の概数の作り方と使い分けを解説します。",
    "h1": "切り捨て・切り上げ・四捨五入の違い",
    "eyecatch": "🔢",
    "body_html": """\
<h2>3種類の概数</h2>
<div class="formula-box">
<p><strong>切り捨て</strong>：求める位の下の桁を0にする（数が小さくなる）</p>
<p><strong>切り上げ</strong>：求める位の下の桁が1以上なら1加える（数が大きくなる）</p>
<p><strong>四捨五入</strong>：下の桁が4以下なら切り捨て、5以上なら切り上げ</p>
</div>
<h3>例：2364を百の位で概数に</h3>
<ul>
<li>切り捨て：2300</li>
<li>切り上げ：2400</li>
<li>四捨五入：2400（64→百の位で6≥5なので切り上げ）</li>
</ul>
<div class="tip-box"><p>💡 「何の位で」という指示をよく読みましょう。「百の位で四捨五入」は十の位の数字で判断します。</p></div>""",
    "faq": [
      {"q": "「上から2桁の概数」の意味は？", "a": "上から数えて2桁目までを有効数字として残し、それ以下を処理します。例：3456→上から2桁で四捨五入＝3500。"},
    ],
    "cta_href": "/gaisuu-shishagoonyuu.html",
    "cta_label": "四捨五入の練習",
    "related": [
      {"href": "/gaisuu-shishagoonyuu.html","emoji": "🔢", "text": "四捨五入の基本"},
      {"href": "/syousuu-tasizan.html","emoji": "🔢", "text": "小数のたし算"},
    ],
  },
  {
    "filename": "suugaku-yogo.html",
    "title": "算数・数学の用語まとめ｜算数ドリル",
    "description": "算数でよく使う用語（商・余り・因数・倍数など）をわかりやすくまとめました。",
    "h1": "算数・数学の用語まとめ",
    "eyecatch": "📖",
    "body_html": """\
<h2>よく使う算数用語</h2>
<h3>計算</h3>
<ul>
<li><strong>和</strong>：足し算の答え</li>
<li><strong>差</strong>：引き算の答え</li>
<li><strong>積</strong>：かけ算の答え</li>
<li><strong>商</strong>：わり算の答え</li>
<li><strong>余り</strong>：わり算で割り切れない分</li>
</ul>
<h3>数の性質</h3>
<ul>
<li><strong>倍数</strong>：ある数の整数倍（3の倍数：3,6,9…）</li>
<li><strong>約数</strong>：ある数を割り切れる数（12の約数：1,2,3,4,6,12）</li>
<li><strong>素数</strong>：1と自分自身しか約数がない数（2,3,5,7,11…）</li>
</ul>
<h3>図形</h3>
<ul>
<li><strong>周長</strong>：図形の周りの長さ</li>
<li><strong>面積</strong>：平面の広さ</li>
<li><strong>体積</strong>：立体の大きさ</li>
</ul>
<div class="tip-box"><p>💡 用語を正しく理解すると問題文が読みやすくなります。</p></div>""",
    "faq": [
      {"q": "「商」と「余り」を問われたらどう答える？", "a": "「○○÷△△＝□あまり×」の形で答えます。"},
    ],
    "cta_href": "/sosuu-guide.html",
    "cta_label": "素数の一覧を見る",
    "related": [
      {"href": "/sosuu-guide.html","emoji": "🔢", "text": "素数ガイド"},
      {"href": "/saishou-koubaisu.html","emoji": "🔢", "text": "最小公倍数"},
      {"href": "/saidai-kouyakusuu.html","emoji": "🔢", "text": "最大公約数"},
    ],
  },

  # ===== Batch 9 =====
  {
    "filename": "mondai-tokeisan.html",
    "title": "時計算の文章題｜算数ドリル",
    "description": "時計の長針と短針が作る角度や重なる時刻を求める時計算の解き方を解説します。",
    "h1": "時計算の文章題",
    "eyecatch": "🕐",
    "body_html": """\
<h2>時計算の基本</h2>
<p>長針は1分で6°、短針は1分で0.5°進みます。</p>
<div class="formula-box">
<p>長針の速さ：6°/分　　短針の速さ：0.5°/分</p>
<p>長針と短針の差：5.5°/分</p>
</div>
<h3>例題：3時ちょうどから長針と短針が重なるのは何分後？</h3>
<p>3時ちょうど：短針は90°位置。長針が追いつくまで90÷5.5 ≒ 16.36分</p>
<p>答え：<strong>約16分22秒後</strong>（3時16分22秒）</p>
<div class="tip-box"><p>💡 長針は短針より毎分5.5°速く進みます。</p></div>""",
    "faq": [
      {"q": "1日に長針と短針が重なるのは何回？", "a": "12時間で11回（12時ちょうども含む）、1日で22回です。"},
    ],
    "cta_href": "/jikan-keisan.html",
    "cta_label": "時間の計算を練習",
    "related": [
      {"href": "/jikan-keisan.html","emoji": "⏱", "text": "時間の計算"},
      {"href": "/kakudo-kiso.html","emoji": "📐", "text": "角度の基本"},
    ],
  },
  {
    "filename": "mondai-ryoushin.html",
    "title": "両数算・和差算の解き方｜算数ドリル",
    "description": "2つの数の和と差から元の数を求める和差算の解き方を図解で解説します。",
    "h1": "和差算の解き方",
    "eyecatch": "➕",
    "body_html": """\
<h2>和差算とは？</h2>
<p>2つの数の<strong>和（合計）</strong>と<strong>差</strong>がわかっているとき、それぞれの数を求めます。</p>
<div class="formula-box">
<p>大きい数 ＝ (和 ＋ 差) ÷ 2</p>
<p>小さい数 ＝ (和 － 差) ÷ 2</p>
</div>
<h3>例題</h3>
<p>2つの数の和は28、差は8のとき、それぞれの数は？</p>
<p>大きい数 = (28+8)÷2 = 18　　小さい数 = (28-8)÷2 = 10</p>
<div class="tip-box"><p>💡 線分図を描くと和・差の関係がわかりやすくなります。</p></div>""",
    "faq": [
      {"q": "和差算と過不足算の違いは？", "a": "和差算は2数の和と差を使い、過不足算は配りすぎ・不足の条件から元の数を求めます。"},
    ],
    "cta_href": "/mondai-nenrei.html",
    "cta_label": "年齢算を練習",
    "related": [
      {"href": "/mondai-nenrei.html","emoji": "👨‍👩‍👧", "text": "年齢算"},
      {"href": "/mondai-waribiki.html","emoji": "🛒", "text": "割引の問題"},
    ],
  },
  {
    "filename": "mondai-tsurukami.html",
    "title": "つるかめ算の解き方｜算数ドリル",
    "description": "つるとかめの合計と足の数から数を求めるつるかめ算の解き方を解説します。",
    "h1": "つるかめ算の解き方",
    "eyecatch": "🐢",
    "body_html": """\
<h2>つるかめ算とは？</h2>
<p>2種類のものの個数の合計と、ある量の合計から、それぞれの個数を求める問題です。</p>
<div class="formula-box">
<p>仮定法：全部を片方と仮定→差を利用して求める</p>
</div>
<h3>例題</h3>
<p>つる（足2本）とかめ（足4本）合わせて10匹、足は32本。それぞれ何匹？</p>
<p>全部つると仮定：10×2=20本　実際より12本少ない</p>
<p>かめ1匹でつる1匹を置き換えると2本増える→かめ = 12÷2 = 6匹、つる = 4匹</p>
<div class="tip-box"><p>💡 仮定して差を調整する考え方は他の問題にも応用できます。</p></div>""",
    "faq": [
      {"q": "方程式を使えば解けますか？", "a": "はい、連立方程式でも解けますが、小学算数では仮定法（面積図）が基本です。"},
    ],
    "cta_href": "/mondai-ryoushin.html",
    "cta_label": "和差算を練習",
    "related": [
      {"href": "/mondai-ryoushin.html","emoji": "➕", "text": "和差算"},
      {"href": "/grade-5-tips.html","emoji": "📚", "text": "5年生の勉強法"},
    ],
  },
  {
    "filename": "mondai-suitou.html",
    "title": "水槽の問題（体積・容積）｜算数ドリル",
    "description": "水槽に水を入れる・排水する問題を解説。体積と容積の違いもわかりやすく説明します。",
    "h1": "水槽の問題（体積・容積）",
    "eyecatch": "💧",
    "body_html": """\
<h2>体積と容積</h2>
<ul>
<li><strong>体積</strong>：立体が占める空間の大きさ（cm³）</li>
<li><strong>容積</strong>：容器の中に入る量（mL・L・cm³）</li>
</ul>
<div class="formula-box"><p>直方体の体積 ＝ 縦 × 横 × 高さ</p></div>
<h3>例題</h3>
<p>縦20cm・横30cm・高さ40cmの水槽に毎分2Lで注水。満水になるまで何分？</p>
<p>容積 = 20×30×40 = 24000cm³ = 24L　　時間 = 24÷2 = <strong>12分</strong></p>
<div class="tip-box"><p>💡 1cm³ = 1mL = 0.001L の換算を覚えましょう。</p></div>""",
    "faq": [
      {"q": "1L = 何cm³？", "a": "1L = 1000cm³です。1dL = 100cm³です。"},
    ],
    "cta_href": "/taiseki-kiso.html",
    "cta_label": "体積の基本を復習",
    "related": [
      {"href": "/taiseki-kiso.html","emoji": "📦", "text": "体積の基本"},
      {"href": "/taiseki-mizu.html","emoji": "💧", "text": "水の体積問題"},
    ],
  },
  {
    "filename": "mondai-kakizan2.html",
    "title": "かけ算の文章題｜算数ドリル",
    "description": "かけ算を使う文章題の種類と解き方を練習。何倍・何セット・単価×個数の問題を解説します。",
    "h1": "かけ算の文章題",
    "eyecatch": "✖️",
    "body_html": """\
<h2>かけ算が使える場面</h2>
<ul>
<li>同じ数が何組かある（単価×個数）</li>
<li>何倍かを求める・何倍かの量を求める</li>
<li>縦×横（面積・配列）</li>
</ul>
<h3>例題1：単価×個数</h3>
<p>1個80円のりんごを12個買うと？　80×12 = <strong>960円</strong></p>
<h3>例題2：何倍</h3>
<p>赤が15個、青はその3倍。青は何個？　15×3 = <strong>45個</strong></p>
<div class="tip-box"><p>💡 文章題では「何×何」かを読み取ることが大切です。単位を確認しましょう。</p></div>""",
    "faq": [
      {"q": "かけ算とたし算を間違えます", "a": "「同じ数がいくつかある」のがかけ算の目印です。「3個が5セット」→3×5です。"},
    ],
    "cta_href": "/kakizan-kiso.html",
    "cta_label": "かけ算の基本を復習",
    "related": [
      {"href": "/kakizan-kiso.html","emoji": "✖️", "text": "かけ算の基本"},
      {"href": "/kakezan-rensyu.html","emoji": "✖️", "text": "かけ算の練習"},
    ],
  },
  {
    "filename": "mondai-warizan2.html",
    "title": "わり算の文章題｜算数ドリル",
    "description": "わり算を使う文章題の種類と解き方を練習。等分・包含除の違いも解説します。",
    "h1": "わり算の文章題",
    "eyecatch": "➗",
    "body_html": """\
<h2>わり算の2種類</h2>
<ul>
<li><strong>等分除</strong>：同じ数に分ける（24個を6人で分けると1人何個？）</li>
<li><strong>包含除</strong>：何個分かを求める（24個を6個ずつ分けると何人分？）</li>
</ul>
<h3>例題1：等分除</h3>
<p>42本の鉛筆を7人で等分。1人何本？　42÷7 = <strong>6本</strong></p>
<h3>例題2：包含除</h3>
<p>48枚のカードを8枚ずつ配ると何人に配れる？　48÷8 = <strong>6人</strong></p>
<div class="tip-box"><p>💡 どちらも式は同じ「÷」ですが、意味が違います。答えの単位に注目しましょう。</p></div>""",
    "faq": [
      {"q": "余りが出るわり算の文章題は？", "a": "問題によって「余りを切り捨て」か「1つ多く必要」かが変わります。文脈をよく読みましょう。"},
    ],
    "cta_href": "/warizan-kiso.html",
    "cta_label": "わり算の基本を復習",
    "related": [
      {"href": "/warizan-kiso.html","emoji": "➗", "text": "わり算の基本"},
      {"href": "/warizan-rensyu.html","emoji": "➗", "text": "わり算の練習"},
    ],
  },
  {
    "filename": "mondai-tasizan2.html",
    "title": "たし算の文章題｜算数ドリル",
    "description": "たし算を使う文章題の種類と解き方を練習。合わせて・全部で・増えての場面を解説します。",
    "h1": "たし算の文章題",
    "eyecatch": "➕",
    "body_html": """\
<h2>たし算が使える場面</h2>
<ul>
<li>「合わせて」「全部で」「増えて」</li>
<li>2つ以上のものをまとめる</li>
</ul>
<h3>例題1</h3>
<p>赤い花が15本、白い花が23本。合わせて何本？　15+23 = <strong>38本</strong></p>
<h3>例題2</h3>
<p>昨日32ページ、今日18ページ読んだ。全部で何ページ？　32+18 = <strong>50ページ</strong></p>
<div class="tip-box"><p>💡 「合わせて」「全部で」「増えて」というキーワードがたし算のサインです。</p></div>""",
    "faq": [
      {"q": "3つ以上の数を足すときは？", "a": "順番に足してOKです。計算しやすい組み合わせを先に足す工夫もできます。"},
    ],
    "cta_href": "/tasizan-kiso.html",
    "cta_label": "たし算の基本を復習",
    "related": [
      {"href": "/tasizan-kiso.html","emoji": "➕", "text": "たし算の基本"},
      {"href": "/tasizan-kuriagari.html","emoji": "➕", "text": "くり上がりのたし算"},
    ],
  },
  {
    "filename": "mondai-hikizan2.html",
    "title": "ひき算の文章題（応用）｜算数ドリル",
    "description": "ひき算を使う文章題のパターンを整理。「残り・差・減る」の場面を練習します。",
    "h1": "ひき算の文章題（応用）",
    "eyecatch": "➖",
    "body_html": """\
<h2>ひき算が使える場面</h2>
<ul>
<li>「残り」：持っていた数から使った数を引く</li>
<li>「差・違い」：2量の差を求める</li>
<li>「減る・もらった逆」：元の数を求める</li>
</ul>
<h3>例題1</h3>
<p>50枚の折り紙から17枚使った。残りは？　50-17 = <strong>33枚</strong></p>
<h3>例題2</h3>
<p>兄75cm・弟62cm。身長差は？　75-62 = <strong>13cm</strong></p>
<div class="tip-box"><p>💡 「どちらが多い（大きい）か」を先に確認してから引く順を決めましょう。</p></div>""",
    "faq": [
      {"q": "「あと何個必要？」もひき算？", "a": "はい、目標数から今の数を引きます。例：100個必要で63個ある→100-63=37個。"},
    ],
    "cta_href": "/mondai-hikizan.html",
    "cta_label": "ひき算文章題を練習",
    "related": [
      {"href": "/mondai-hikizan.html","emoji": "➖", "text": "ひき算の文章題"},
      {"href": "/hikizan-kiso.html","emoji": "➖", "text": "ひき算の基本"},
    ],
  },
  {
    "filename": "drill-1nen.html",
    "title": "1年生の算数ドリル問題集｜算数ドリル",
    "description": "小学1年生向けの算数ドリルまとめ。たし算・ひき算・数の読み書き・時計の問題を練習できます。",
    "h1": "1年生の算数ドリル問題集",
    "eyecatch": "1️⃣",
    "body_html": """\
<h2>1年生で練習する内容</h2>
<ul>
<li>1〜100の数の読み書き</li>
<li>たし算（くり上がりなし・あり）</li>
<li>ひき算（くり下がりなし・あり）</li>
<li>時計（何時・何時半）</li>
<li>形（丸・三角・四角）</li>
</ul>
<h3>練習のポイント</h3>
<div class="tip-box"><p>💡 毎日5〜10分の短い練習が効果的。できた問題に○をつけて「できた！」の実感を大切に。</p></div>
<div class="warn-box"><p>⚠️ くり上がり・くり下がりが弱い場合はブロックや指を使って「イメージ」から始めましょう。</p></div>""",
    "faq": [
      {"q": "1年生でくり上がりがわかりません", "a": "「10のまとまり」の感覚が重要です。ブロックや数カードで10を作る練習をしましょう。"},
    ],
    "cta_href": "/tasizan-kuriagari.html",
    "cta_label": "くり上がりたし算を練習",
    "related": [
      {"href": "/tasizan-kiso.html","emoji": "➕", "text": "たし算の基本"},
      {"href": "/hikizan-kurisagari.html","emoji": "➖", "text": "くり下がりひき算"},
      {"href": "/tokei-yomikata.html","emoji": "🕐", "text": "時計の読み方"},
    ],
  },
  {
    "filename": "drill-2nen.html",
    "title": "2年生の算数ドリル問題集｜算数ドリル",
    "description": "小学2年生向けの算数ドリルまとめ。かけ算九九・大きな数・長さ・時間の問題を練習できます。",
    "h1": "2年生の算数ドリル問題集",
    "eyecatch": "2️⃣",
    "body_html": """\
<h2>2年生で練習する内容</h2>
<ul>
<li>かけ算九九（1〜9の段）</li>
<li>1000までの数</li>
<li>長さ（cm・mm）</li>
<li>時刻と時間</li>
<li>三角形・四角形</li>
</ul>
<h3>最重要：かけ算九九</h3>
<div class="warn-box"><p>⚠️ 九九は3年生以降のすべての計算の基礎。2年生中に完全に覚えましょう。</p></div>
<div class="tip-box"><p>💡 苦手な段だけ集中練習。お風呂や車の中でも声に出して練習しましょう。</p></div>""",
    "faq": [
      {"q": "九九が覚えられません", "a": "7の段・8の段が特に難しいです。毎日3分間、その段だけを繰り返し唱える練習が効果的です。"},
    ],
    "cta_href": "/kakezan-rensyu.html",
    "cta_label": "かけ算練習をする",
    "related": [
      {"href": "/kakezan-rensyu.html","emoji": "✖️", "text": "かけ算の練習"},
      {"href": "/jikan-keisan.html","emoji": "⏱", "text": "時間の計算"},
    ],
  },
  {
    "filename": "drill-3nen.html",
    "title": "3年生の算数ドリル問題集｜算数ドリル",
    "description": "小学3年生向けの算数ドリルまとめ。かけ算筆算・わり算・分数・時間単位の問題を練習できます。",
    "h1": "3年生の算数ドリル問題集",
    "eyecatch": "3️⃣",
    "body_html": """\
<h2>3年生で練習する内容</h2>
<ul>
<li>2・3桁のかけ算（筆算）</li>
<li>わり算（九九を使う）</li>
<li>大きな数（万・億）</li>
<li>分数（2分の1など）</li>
<li>時間・長さ・重さの単位換算</li>
</ul>
<div class="warn-box"><p>⚠️ わり算は九九が定着していないと進めません。九九を確認してから進みましょう。</p></div>
<div class="tip-box"><p>💡 筆算は丁寧に書く習慣が正解率UPのカギです。</p></div>""",
    "faq": [
      {"q": "わり算の余りの計算が間違えます", "a": "商が合っているか九九で確認してから余りを計算しましょう。余りは割る数より小さくなります。"},
    ],
    "cta_href": "/taisaku-3nen.html",
    "cta_label": "3年生の弱点対策を見る",
    "related": [
      {"href": "/taisaku-3nen.html","emoji": "📝", "text": "3年生弱点対策"},
      {"href": "/warizan-kiso.html","emoji": "➗", "text": "わり算の基本"},
      {"href": "/kakizan-hissan.html","emoji": "✖️", "text": "かけ算の筆算"},
    ],
  },
  {
    "filename": "drill-4nen.html",
    "title": "4年生の算数ドリル問題集｜算数ドリル",
    "description": "小学4年生向けの算数ドリルまとめ。わり算筆算・小数・角度・面積の問題を練習できます。",
    "h1": "4年生の算数ドリル問題集",
    "eyecatch": "4️⃣",
    "body_html": """\
<h2>4年生で練習する内容</h2>
<ul>
<li>わり算の筆算（2桁÷2桁）</li>
<li>小数のたし算・ひき算</li>
<li>角度（分度器の使い方）</li>
<li>面積（長方形・正方形）</li>
<li>折れ線グラフ・棒グラフ</li>
</ul>
<div class="warn-box"><p>⚠️ わり算筆算の「商の見当」が難しいポイント。何十で割る練習を重ねましょう。</p></div>
<div class="tip-box"><p>💡 小数の計算は小数点の位置に注目。筆算で小数点を揃えて書く習慣をつけましょう。</p></div>""",
    "faq": [
      {"q": "角度の問題が苦手です", "a": "三角形の内角の和180°、四角形の内角の和360°を覚えましょう。これだけで多くの問題が解けます。"},
    ],
    "cta_href": "/taisaku-4nen.html",
    "cta_label": "4年生の弱点対策を見る",
    "related": [
      {"href": "/taisaku-4nen.html","emoji": "📝", "text": "4年生弱点対策"},
      {"href": "/warizan-hissan.html","emoji": "➗", "text": "わり算の筆算"},
      {"href": "/kakudo-kiso.html","emoji": "📐", "text": "角度の基本"},
    ],
  },
  {
    "filename": "drill-5nen.html",
    "title": "5年生の算数ドリル問題集｜算数ドリル",
    "description": "小学5年生向けの算数ドリルまとめ。分数・割合・速さ・面積（多角形）の問題を練習できます。",
    "h1": "5年生の算数ドリル問題集",
    "eyecatch": "5️⃣",
    "body_html": """\
<h2>5年生で練習する内容</h2>
<ul>
<li>分数の四則計算</li>
<li>最大公約数・最小公倍数</li>
<li>割合（百分率・歩合）</li>
<li>速さ（距離・時間・速さ）</li>
<li>多角形の面積（三角形・台形・ひし形）</li>
<li>立体の体積（直方体・立方体）</li>
</ul>
<div class="warn-box"><p>⚠️ 割合と速さは6年生・中学でも使う最重要単元。時間をかけて理解を深めましょう。</p></div>""",
    "faq": [
      {"q": "分数の計算で通分がうまくできません", "a": "最小公倍数を使って通分します。まず最小公倍数を求める練習をしましょう。"},
    ],
    "cta_href": "/taisaku-5nen.html",
    "cta_label": "5年生の弱点対策を見る",
    "related": [
      {"href": "/taisaku-5nen.html","emoji": "📝", "text": "5年生弱点対策"},
      {"href": "/sokudo-guide.html","emoji": "🏃", "text": "速さの基本"},
      {"href": "/wariai-guide.html","emoji": "📊", "text": "割合の基本"},
    ],
  },
  {
    "filename": "drill-6nen.html",
    "title": "6年生の算数ドリル問題集｜算数ドリル",
    "description": "小学6年生向けの算数ドリルまとめ。分数÷分数・比・文字式・比例・反比例の問題を練習できます。",
    "h1": "6年生の算数ドリル問題集",
    "eyecatch": "6️⃣",
    "body_html": """\
<h2>6年生で練習する内容</h2>
<ul>
<li>分数÷分数</li>
<li>比・比例式</li>
<li>文字を使った式（xを使う）</li>
<li>比例・反比例</li>
<li>円の面積・円柱の体積</li>
<li>資料の調べ方（平均・最頻値・中央値）</li>
</ul>
<div class="warn-box"><p>⚠️ 6年生の内容は中学数学の直接の準備。確実に理解しておきましょう。</p></div>
<div class="tip-box"><p>💡 比例・反比例はグラフと表を使って関係を視覚的に理解することが大切です。</p></div>""",
    "faq": [
      {"q": "比の問題で比の値がわかりません", "a": "比の値＝前の数÷後の数です。2:3なら比の値は2÷3=2/3です。"},
    ],
    "cta_href": "/taisaku-6nen.html",
    "cta_label": "6年生の弱点対策を見る",
    "related": [
      {"href": "/taisaku-6nen.html","emoji": "📝", "text": "6年生弱点対策"},
      {"href": "/bunsuu-warizan.html","emoji": "➗", "text": "分数のわり算"},
      {"href": "/hi-guide.html","emoji": "📊", "text": "比の基本"},
    ],
  },
  {
    "filename": "benkyou-jikan.html",
    "title": "算数の勉強時間の目安｜算数ドリル",
    "description": "学年別・目的別の算数勉強時間の目安を解説。効率よく成績を上げるための時間配分を紹介。",
    "h1": "算数の勉強時間の目安",
    "eyecatch": "⏰",
    "body_html": """\
<h2>学年別・推奨勉強時間</h2>
<table border="1" style="border-collapse:collapse;padding:4px">
<tr><th>学年</th><th>平日</th><th>休日</th></tr>
<tr><td>1〜2年</td><td>10〜15分</td><td>20〜30分</td></tr>
<tr><td>3〜4年</td><td>20〜30分</td><td>30〜60分</td></tr>
<tr><td>5〜6年</td><td>30〜45分</td><td>60〜90分</td></tr>
</table>
<h3>効率アップのコツ</h3>
<ul>
<li>毎日同じ時間帯に勉強（習慣化）</li>
<li>1回の勉強は25分以内（集中力が続く範囲）</li>
<li>間違えた問題だけを翌日に復習</li>
</ul>
<div class="tip-box"><p>💡 量より質。短くても集中した勉強の方が効果があります。</p></div>""",
    "faq": [
      {"q": "テスト前はどのくらい勉強すればいい？", "a": "テスト3〜4日前から1日30〜60分の復習をするのが理想です。前日の詰め込みは効果が薄いです。"},
    ],
    "cta_href": "/sansu-benkyou-houhou.html",
    "cta_label": "算数の勉強法を見る",
    "related": [
      {"href": "/sansu-benkyou-houhou.html","emoji": "📚", "text": "算数の勉強法"},
      {"href": "/tesuto-naoshi.html","emoji": "📝", "text": "テストの見直し法"},
    ],
  },
  {
    "filename": "keisanki-tukaikata.html",
    "title": "電卓・計算機の正しい使い方｜算数ドリル",
    "description": "電卓の基本的な使い方と、算数学習における計算機との上手な付き合い方を解説します。",
    "h1": "電卓・計算機の正しい使い方",
    "eyecatch": "🔢",
    "body_html": """\
<h2>電卓の基本操作</h2>
<ul>
<li><strong>AC/C</strong>：全消去・1つ消去</li>
<li><strong>÷ × − +</strong>：四則演算</li>
<li><strong>%</strong>：パーセント計算（例：100の20%→100×20%）</li>
</ul>
<h3>算数学習での注意点</h3>
<div class="warn-box"><p>⚠️ 小学算数では原則として電卓を使わずに手計算で練習することが大切です。計算力は中学数学の基礎になります。</p></div>
<div class="tip-box"><p>💡 電卓は「答え合わせ」や「桁が多い実生活の計算」に使いましょう。</p></div>
<h3>上手な使い分け</h3>
<p>練習中：手で計算→答え合わせに電卓　実生活：積極的に活用OK</p>""",
    "faq": [
      {"q": "スマートフォンの電卓で答え合わせはOK？", "a": "はい。ただし数字の打ち間違いに注意しましょう。"},
    ],
    "cta_href": "/anzan-practice.html",
    "cta_label": "暗算練習をする",
    "related": [
      {"href": "/anzan-practice.html","emoji": "🧠", "text": "暗算の練習"},
      {"href": "/keisan-hayaku.html","emoji": "⚡", "text": "計算を速くするコツ"},
    ],
  },

  # ===== Batch 10 =====
  {
    "filename": "sansu-juku-erabi.html",
    "title": "算数塾の選び方｜算数ドリル",
    "description": "子どもに合った算数塾の選び方を解説。集団・個別・オンラインの違いと選ぶポイントを紹介します。",
    "h1": "算数塾の選び方",
    "eyecatch": "🏫",
    "body_html": """\
<h2>塾の種類と特徴</h2>
<ul>
<li><strong>集団塾</strong>：授業形式。競争意識が持てる。料金は比較的安い</li>
<li><strong>個別指導塾</strong>：1対1〜2。弱点に集中できる。料金は高め</li>
<li><strong>オンライン塾</strong>：場所を選ばない。費用も比較的安い</li>
</ul>
<h3>選ぶときのポイント</h3>
<ol>
<li>お子さんの性格（競争が好き？個別が好き？）</li>
<li>弱点科目への対応力</li>
<li>月謝・送迎の負担</li>
<li>体験授業で実際に確認</li>
</ol>
<div class="tip-box"><p>💡 まず体験授業を2〜3か所受けてから決めると失敗が少ないです。</p></div>""",
    "faq": [
      {"q": "何年生から塾に行くべきですか？", "a": "算数の場合、3〜4年生から始める家庭が多いです。弱点が出始めたタイミングが目安です。"},
    ],
    "cta_href": "/sansu-benkyou-houhou.html",
    "cta_label": "算数の勉強法を見る",
    "related": [
      {"href": "/sansu-benkyou-houhou.html","emoji": "📚", "text": "算数の勉強法"},
      {"href": "/oyako-sansu.html","emoji": "👨‍👩‍👧", "text": "親子で算数"},
    ],
  },
  {
    "filename": "mondai-kakuritsu.html",
    "title": "確率の基本｜算数ドリル",
    "description": "コインやさいころを使った確率の基本をわかりやすく解説。起こりやすさを数で表す方法を学びます。",
    "h1": "確率の基本",
    "eyecatch": "🎲",
    "body_html": """\
<h2>確率とは？</h2>
<p>あることが起こる<strong>可能性の大きさ</strong>を0〜1の数で表したものです。</p>
<div class="formula-box"><p>確率 ＝ 求める場合の数 ÷ 全体の場合の数</p></div>
<h3>例：コインを1回投げて表が出る確率</h3>
<p>全体＝2通り（表・裏）　求める＝1通り（表）　確率 = 1÷2 = <strong>1/2</strong></p>
<h3>例：さいころで3が出る確率</h3>
<p>全体＝6通り　求める＝1通り　確率 = 1÷6 = <strong>1/6</strong></p>
<div class="tip-box"><p>💡 確率0は「絶対に起きない」、確率1は「必ず起きる」です。</p></div>""",
    "faq": [
      {"q": "「確率が高い」とはどういう意味？", "a": "1に近いほど起こりやすい（確率が高い）、0に近いほど起こりにくい（確率が低い）です。"},
    ],
    "cta_href": "/grade-6-tips.html",
    "cta_label": "6年生の学習法を見る",
    "related": [
      {"href": "/sosuu-guide.html","emoji": "🔢", "text": "素数ガイド"},
      {"href": "/sangaku-chishiki.html","emoji": "🧮", "text": "算数の豆知識"},
    ],
  },
  {
    "filename": "mondai-heikin2.html",
    "title": "平均の応用問題｜算数ドリル",
    "description": "平均を使った応用問題（平均から合計を求める・一部が不明な場合など）を解説します。",
    "h1": "平均の応用問題",
    "eyecatch": "📊",
    "body_html": """\
<h2>平均から合計を求める</h2>
<div class="formula-box"><p>合計 ＝ 平均 × 個数</p></div>
<h3>例題1：合計を求める</h3>
<p>5人のテストの平均が72点。5人の合計点は？　72×5 = <strong>360点</strong></p>
<h3>例題2：1つが不明な場合</h3>
<p>4回のテストの平均を80点にしたい。3回の合計が232点のとき4回目は？</p>
<p>目標合計 = 80×4 = 320　　4回目 = 320-232 = <strong>88点</strong></p>
<div class="tip-box"><p>💡 「平均×個数＝合計」の逆算が応用問題の核心です。</p></div>""",
    "faq": [
      {"q": "加重平均とは？", "a": "個数・比重が異なるデータの平均です。「A組の平均とB組の平均が違う場合の全体平均」などで使います。"},
    ],
    "cta_href": "/heikin-guide.html",
    "cta_label": "平均の基本を復習",
    "related": [
      {"href": "/heikin-guide.html","emoji": "📊", "text": "平均の基本"},
      {"href": "/mondai-waribiki.html","emoji": "🛒", "text": "割引の問題"},
    ],
  },
  {
    "filename": "mondai-menseki3.html",
    "title": "等積変形の問題｜算数ドリル",
    "description": "形を変えても面積が変わらない等積変形を解説。三角形・平行四辺形への変形問題を練習します。",
    "h1": "等積変形の問題",
    "eyecatch": "🔷",
    "body_html": """\
<h2>等積変形とは？</h2>
<p>図形の面積を変えずに形を変えることです。</p>
<h3>基本の考え方</h3>
<p>底辺と高さが同じなら、三角形の面積は等しい。</p>
<div class="formula-box"><p>同じ底辺・同じ高さ → 面積が等しい</p></div>
<h3>よく使う変形</h3>
<ul>
<li>三角形 ↔ 平行四辺形（底辺・高さが同じ）</li>
<li>底辺を平行に移動しても面積不変</li>
</ul>
<div class="tip-box"><p>💡 「どこに補助線を引くか」が等積変形のポイントです。</p></div>""",
    "faq": [
      {"q": "等積変形はどの学年で習いますか？", "a": "小学5〜6年生の発展問題・中学受験で登場します。"},
    ],
    "cta_href": "/mondai-menseki2.html",
    "cta_label": "複合図形の面積を練習",
    "related": [
      {"href": "/mondai-menseki2.html","emoji": "🔷", "text": "複合図形の面積"},
      {"href": "/menseki-sankakukei.html","emoji": "📐", "text": "三角形の面積"},
    ],
  },
  {
    "filename": "mondai-ryoutan.html",
    "title": "両端問題・等間隔の問題｜算数ドリル",
    "description": "等間隔に並ぶ物の数と間隔の関係を解く問題を解説。植木算との関連も確認しましょう。",
    "h1": "両端問題・等間隔の問題",
    "eyecatch": "📏",
    "body_html": """\
<h2>等間隔問題のパターン</h2>
<div class="formula-box">
<p>両端あり：個数 ＝ 間の数 ＋ 1</p>
<p>片端あり：個数 ＝ 間の数</p>
<p>円形：個数 ＝ 間の数</p>
</div>
<h3>例題：直線上に5m間隔でポールを立てる</h3>
<p>長さ60m、両端を含む場合：間の数 = 60÷5 = 12　個数 = 12+1 = <strong>13本</strong></p>
<h3>階段の問題</h3>
<p>1段上がるたびに1踏む。10段の階段を上るには何回踏む？ → <strong>10回</strong>（端を考えない）</p>
<div class="tip-box"><p>💡 「両端を数えるか」を問題文で確認することが最重要です。</p></div>""",
    "faq": [
      {"q": "植木算と同じですか？", "a": "同じ考え方です。植木算の応用として電柱・ポール・街灯の問題が出ます。"},
    ],
    "cta_href": "/harizan-guide.html",
    "cta_label": "植木算の解き方を見る",
    "related": [
      {"href": "/harizan-guide.html","emoji": "🌳", "text": "植木算"},
      {"href": "/mondai-nagasa.html","emoji": "📏", "text": "長さの文章題"},
    ],
  },
  {
    "filename": "syougaku-sansu-map.html",
    "title": "小学算数の学習マップ｜算数ドリル",
    "description": "小学1〜6年生の算数の学習内容を一覧で確認。どの単元がどの学年で習うか一目でわかります。",
    "h1": "小学算数の学習マップ",
    "eyecatch": "🗺️",
    "body_html": """\
<h2>学年別・単元マップ</h2>
<h3>1年生</h3>
<p>数の読み書き、たし算・ひき算（20まで）、時計（ちょうど・半）、形</p>
<h3>2年生</h3>
<p>たし算・ひき算（筆算）、かけ算九九、長さ・かさ・重さ、時刻と時間</p>
<h3>3年生</h3>
<p>かけ算筆算、わり算、大きな数、分数、円・球</p>
<h3>4年生</h3>
<p>わり算筆算、小数の計算、角度、面積（長方形）、折れ線グラフ</p>
<h3>5年生</h3>
<p>分数の計算、割合、速さ、多角形の面積、立体の体積</p>
<h3>6年生</h3>
<p>分数÷分数、比、文字式、比例・反比例、円の面積、資料の活用</p>
<div class="tip-box"><p>💡 前の学年の内容が次の学年の基礎になります。弱点は早めに補強しましょう。</p></div>""",
    "faq": [
      {"q": "どの単元が最も重要ですか？", "a": "かけ算九九（2年）、割合（5年）、速さ（5年）、分数の計算（5〜6年）が特に重要です。"},
    ],
    "cta_href": "/grade-1-tips.html",
    "cta_label": "学年別勉強法を見る",
    "related": [
      {"href": "/drill-1nen.html","emoji": "1️⃣", "text": "1年生ドリル"},
      {"href": "/drill-3nen.html","emoji": "3️⃣", "text": "3年生ドリル"},
      {"href": "/drill-5nen.html","emoji": "5️⃣", "text": "5年生ドリル"},
    ],
  },
  {
    "filename": "keisan-training.html",
    "title": "計算トレーニングの方法｜算数ドリル",
    "description": "計算力を上げるためのトレーニング方法を解説。百マス計算・フラッシュ暗算・時間制限練習を紹介。",
    "h1": "計算トレーニングの方法",
    "eyecatch": "💪",
    "body_html": """\
<h2>計算力を上げる練習法</h2>
<h3>①百マス計算</h3>
<p>縦・横各10個の数字で100マスを埋める計算練習。毎日記録して成長を実感。</p>
<h3>②時間制限練習</h3>
<p>同じ問題を「昨日より速く」を目標に繰り返す。ストップウォッチで計測。</p>
<h3>③フラッシュ暗算</h3>
<p>数字を素早く暗算する練習。そろばんに近い効果。</p>
<h3>④間違えた問題専用ノート</h3>
<p>ミスした問題だけをまとめて繰り返し練習。</p>
<div class="tip-box"><p>💡 毎日10〜15分の継続が最も効果的です。</p></div>""",
    "faq": [
      {"q": "百マス計算は毎日やるべき？", "a": "毎日同じ時間にやると習慣化しやすく、タイムが縮まっていく楽しさがあります。"},
    ],
    "cta_href": "/keisan-hayaku.html",
    "cta_label": "計算を速くするコツ",
    "related": [
      {"href": "/keisan-hayaku.html","emoji": "⚡", "text": "計算を速くするコツ"},
      {"href": "/anzan-practice.html","emoji": "🧠", "text": "暗算の練習"},
    ],
  },
  {
    "filename": "mondai-step1.html",
    "title": "算数ステップ1：基本の四則計算｜算数ドリル",
    "description": "算数の基礎固め。たし算・ひき算・かけ算・わり算を段階的に練習するステップ1の問題集です。",
    "h1": "算数ステップ1：基本の四則計算",
    "eyecatch": "🔰",
    "body_html": """\
<h2>ステップ1で練習すること</h2>
<p>算数の基本である四則計算を確実にマスターします。</p>
<h3>練習内容</h3>
<ol>
<li>1桁+1桁のたし算（例：7+8=15）</li>
<li>2桁-1桁のひき算（例：15-8=7）</li>
<li>1桁×1桁のかけ算（九九）</li>
<li>1桁÷1桁のわり算（余りなし）</li>
</ol>
<div class="tip-box"><p>💡 すべてを暗算で素早く答えられるようになることが目標です。</p></div>
<div class="warn-box"><p>⚠️ ステップ1が確実でないと上のステップが崩れます。焦らず定着させましょう。</p></div>""",
    "faq": [
      {"q": "ステップ1はどの学年対象ですか？", "a": "主に1〜2年生向けですが、上の学年でも基礎の確認に使えます。"},
    ],
    "cta_href": "/drill-1nen.html",
    "cta_label": "1年生ドリルへ",
    "related": [
      {"href": "/drill-1nen.html","emoji": "1️⃣", "text": "1年生ドリル"},
      {"href": "/tasizan-kiso.html","emoji": "➕", "text": "たし算の基本"},
      {"href": "/kakezan-rensyu.html","emoji": "✖️", "text": "かけ算練習"},
    ],
  },
  {
    "filename": "mondai-step2.html",
    "title": "算数ステップ2：筆算と単位計算｜算数ドリル",
    "description": "算数の応用ステップ2。かけ算・わり算の筆算と長さ・重さ・時間の単位計算を練習します。",
    "h1": "算数ステップ2：筆算と単位計算",
    "eyecatch": "📝",
    "body_html": """\
<h2>ステップ2で練習すること</h2>
<ol>
<li>2〜3桁のかけ算筆算</li>
<li>2桁÷1桁のわり算筆算</li>
<li>長さの単位換算（km・m・cm・mm）</li>
<li>時間の計算（何時間何分後）</li>
</ol>
<div class="tip-box"><p>💡 筆算は「丁寧に書く」ことがミスを減らす最大の対策です。</p></div>
<h3>よくあるミス</h3>
<ul>
<li>くり上がりを忘れる</li>
<li>位をそろえて書かない</li>
<li>余りの確認を忘れる</li>
</ul>""",
    "faq": [
      {"q": "筆算を速く正確にするコツは？", "a": "まず正確さを優先して、慣れてきたら速さを意識しましょう。急ぐとミスが増えます。"},
    ],
    "cta_href": "/kakizan-hissan.html",
    "cta_label": "かけ算筆算を練習",
    "related": [
      {"href": "/kakizan-hissan.html","emoji": "✖️", "text": "かけ算筆算"},
      {"href": "/warizan-hissan.html","emoji": "➗", "text": "わり算筆算"},
      {"href": "/tanihenkan-guide.html","emoji": "📏", "text": "単位換算まとめ"},
    ],
  },
  {
    "filename": "mondai-step3.html",
    "title": "算数ステップ3：分数・小数・割合｜算数ドリル",
    "description": "算数の発展ステップ3。分数・小数の計算と割合の問題を段階的に練習します。",
    "h1": "算数ステップ3：分数・小数・割合",
    "eyecatch": "🎯",
    "body_html": """\
<h2>ステップ3で練習すること</h2>
<ol>
<li>分数のたし算・ひき算（通分）</li>
<li>分数のかけ算・わり算</li>
<li>小数の四則計算</li>
<li>割合（百分率・歩合）の計算</li>
</ol>
<div class="warn-box"><p>⚠️ ステップ3は多くの子が躓くポイント。特に割合は時間をかけて理解しましょう。</p></div>
<div class="tip-box"><p>💡 分数と小数の変換（1/2=0.5など）を覚えておくと計算しやすくなります。</p></div>""",
    "faq": [
      {"q": "分数のわり算でどうして逆数をかけるの？", "a": "÷b/cは「b/cがいくつ分あるか」を求めるため、逆数（c/b）をかける操作になります。"},
    ],
    "cta_href": "/bunsuu-tasizan.html",
    "cta_label": "分数のたし算を練習",
    "related": [
      {"href": "/bunsuu-tasizan.html","emoji": "½", "text": "分数のたし算"},
      {"href": "/wariai-guide.html","emoji": "📊", "text": "割合の基本"},
      {"href": "/syousuu-tasizan.html","emoji": "🔢", "text": "小数のたし算"},
    ],
  },
  {
    "filename": "sansuu-douwa.html",
    "title": "算数が楽しくなる話・エピソード｜算数ドリル",
    "description": "算数にまつわる面白い話やエピソードを紹介。数の不思議や数学者の逸話で算数が好きになるかも。",
    "h1": "算数が楽しくなる話・エピソード",
    "eyecatch": "✨",
    "body_html": """\
<h2>数の不思議な話</h2>
<h3>①1から100の合計を一瞬で求めた少年</h3>
<p>数学者ガウスは小学生のとき1+2+...+100を瞬時に5050と答えたといわれています。<br>コツは (1+100)×100÷2 = 5050 という工夫です。</p>
<h3>②9のかけ算の指を使ったトリック</h3>
<p>両手を広げて左から数えてn番目の指を折ると、左に(n-1)本・右に(10-n)本残り、それが9×nの答えになります。</p>
<h3>③数の回文（パリンドローム）</h3>
<p>11×11=121、111×111=12321…対称な数が続きます。</p>
<div class="tip-box"><p>💡 算数は「答えを出す」だけでなく「不思議を楽しむ」学問でもあります。</p></div>""",
    "faq": [
      {"q": "算数と数学の違いは？", "a": "算数は小学校で学ぶ実用的な計算・図形。数学は中学以降で学ぶより抽象的な体系です。"},
    ],
    "cta_href": "/sangaku-chishiki.html",
    "cta_label": "算数の豆知識を見る",
    "related": [
      {"href": "/sangaku-chishiki.html","emoji": "🧮", "text": "算数の豆知識"},
      {"href": "/mahouujin-guide.html","emoji": "🔮", "text": "魔方陣の解き方"},
    ],
  },
  {
    "filename": "mondai-bunrui.html",
    "title": "算数文章題の種類・分類一覧｜算数ドリル",
    "description": "算数の文章題を種類別（速さ・割合・年齢算・植木算など）に分類。問題の種類の見分け方も解説します。",
    "h1": "算数文章題の種類・分類一覧",
    "eyecatch": "📋",
    "body_html": """\
<h2>文章題の種類別分類</h2>
<h3>1. 計算型</h3>
<p>たし算・ひき算・かけ算・わり算の場面設定の問題</p>
<h3>2. 数量関係型</h3>
<p>和差算、つるかめ算、過不足算、植木算</p>
<h3>3. 速さ・時間・距離型</h3>
<p>速さの3公式を使う問題（旅人算・通過算を含む）</p>
<h3>4. 割合・比型</h3>
<p>割合・百分率・歩合・比・比例の問題</p>
<h3>5. 図形型</h3>
<p>面積・体積・周囲の長さを求める問題</p>
<h3>6. 年齢・消去算型</h3>
<p>年齢算・方程式的な考え方が必要な問題</p>
<div class="tip-box"><p>💡 問題を読んだらまず「何型の問題か」を判断することが解法への第一歩です。</p></div>""",
    "faq": [
      {"q": "どの種類が一番難しいですか？", "a": "速さ・割合・つるかめ算が特に難しいとされています。"},
    ],
    "cta_href": "/mondai-sokudo2.html",
    "cta_label": "速さの文章題を練習",
    "related": [
      {"href": "/mondai-sokudo2.html","emoji": "🏃", "text": "速さの応用"},
      {"href": "/mondai-tsurukami.html","emoji": "🐢", "text": "つるかめ算"},
      {"href": "/mondai-nenrei.html","emoji": "👨‍👩‍👧", "text": "年齢算"},
    ],
  },
  {
    "filename": "yoichi-sansu.html",
    "title": "幼児向け算数の入門｜算数ドリル",
    "description": "幼児（3〜6歳）が算数を楽しく学ぶための方法を紹介。数え方・数字の読み書き・形の認識を解説します。",
    "h1": "幼児向け算数の入門",
    "eyecatch": "🧒",
    "body_html": """\
<h2>幼児算数の基本ステップ</h2>
<h3>ステップ1（3歳〜）：数を数える</h3>
<p>おもちゃ・おやつを1個ずつ指差しして「1・2・3…」と数える</p>
<h3>ステップ2（4歳〜）：数字を認識する</h3>
<p>1〜10の数字カードを見て読める・書けるようにする</p>
<h3>ステップ3（5歳〜）：簡単な足し算</h3>
<p>「3個と2個で何個？」をブロックや指で考える</p>
<h3>ステップ4（6歳〜）：数の大小比較</h3>
<p>「5と8どちらが大きい？」「10まで数えて一番大きい数は？」</p>
<div class="tip-box"><p>💡 幼児期は「楽しさ」が最優先。ゲームや歌を通じて自然に学ばせましょう。</p></div>""",
    "faq": [
      {"q": "何歳から算数を教え始めればいい？", "a": "3歳頃から日常生活の中で数を数える習慣から始めると自然です。"},
    ],
    "cta_href": "/nyuugaku-sansu2.html",
    "cta_label": "入学前の準備を確認",
    "related": [
      {"href": "/nyuugaku-sansu2.html","emoji": "🎒", "text": "入学前準備"},
      {"href": "/suji-kakikata.html","emoji": "✏️", "text": "数字の書き方"},
      {"href": "/drill-1nen.html","emoji": "1️⃣", "text": "1年生ドリル"},
    ],
  },
  {
    "filename": "tokui-nigete.html",
    "title": "算数が得意な子の特徴と育て方｜算数ドリル",
    "description": "算数が得意な子の共通点と、算数力を伸ばす環境・習慣の作り方を保護者向けに解説します。",
    "h1": "算数が得意な子の特徴と育て方",
    "eyecatch": "⭐",
    "body_html": """\
<h2>算数が得意な子の共通点</h2>
<ul>
<li>「なぜ？」と考える習慣がある</li>
<li>計算ミスを丁寧に見直す</li>
<li>図や絵を使って考える</li>
<li>間違えることを恐れない</li>
</ul>
<h3>得意を育てる習慣</h3>
<ol>
<li>日常生活でお金の計算をさせる</li>
<li>なぜその答えになるか説明させる</li>
<li>間違えた問題を「チャンス」として扱う</li>
<li>算数パズルやゲームで楽しみながら考える力を養う</li>
</ol>
<div class="tip-box"><p>💡 「できた！」の小さな成功体験を積み重ねることが自信につながります。</p></div>""",
    "faq": [
      {"q": "算数が得意になると他の教科にも影響しますか？", "a": "はい。論理的思考力・集中力が鍛えられ、理科・国語（文章読解）にも良い影響があります。"},
    ],
    "cta_href": "/oyako-sansu.html",
    "cta_label": "親子で算数を学ぶ方法",
    "related": [
      {"href": "/oyako-sansu.html","emoji": "👨‍👩‍👧", "text": "親子で算数"},
      {"href": "/sansu-benkyou-houhou.html","emoji": "📚", "text": "算数の勉強法"},
    ],
  },
  {
    "filename": "tougou-review.html",
    "title": "小学算数 総合復習テスト｜算数ドリル",
    "description": "小学算数の全範囲を網羅した総合復習テスト形式のページ。各単元のポイントを確認できます。",
    "h1": "小学算数 総合復習テスト",
    "eyecatch": "📋",
    "body_html": """\
<h2>総合復習の流れ</h2>
<p>全学年の重要単元を確認します。できない問題があった単元に戻って復習しましょう。</p>
<h3>確認項目リスト</h3>
<ul>
<li>☐ くり上がりたし算・くり下がりひき算</li>
<li>☐ かけ算九九の全段</li>
<li>☐ わり算（あまりあり）</li>
<li>☐ 小数・分数の四則計算</li>
<li>☐ 割合（百分率・歩合）</li>
<li>☐ 速さの3公式</li>
<li>☐ 面積・体積の公式</li>
<li>☐ 単位換算（長さ・重さ・時間）</li>
</ul>
<div class="warn-box"><p>⚠️ 1つでもチェックできない項目があれば、そのページで集中復習しましょう。</p></div>""",
    "faq": [
      {"q": "中学に向けて特に重要な単元は？", "a": "分数の計算・割合・速さ・比・文字式が中学数学の直接の基礎になります。"},
    ],
    "cta_href": "/syougaku-sansu-map.html",
    "cta_label": "学習マップを確認",
    "related": [
      {"href": "/syougaku-sansu-map.html","emoji": "🗺️", "text": "学習マップ"},
      {"href": "/chuugaku-sansu-junbi.html","emoji": "📚", "text": "中学数学の準備"},
    ],
  },
  {
    "filename": "grade-2-tips.html",
    "title": "2年生の算数：勉強のコツと攻略法｜算数ドリル",
    "description": "小学2年生の算数（かけ算九九・長さ・時間・大きな数）の勉強のコツと攻略法を解説します。",
    "h1": "2年生の算数：勉強のコツと攻略法",
    "eyecatch": "2️⃣",
    "body_html": """\
<h2>2年生の最重要テーマ</h2>
<h3>かけ算九九</h3>
<p>2年生最大のテーマ。1〜9の段をすべて暗記します。</p>
<div class="warn-box"><p>⚠️ 九九は3年生以降のすべての単元の基礎。2年生のうちに完全定着させましょう。</p></div>
<h3>覚えにくい段の攻略</h3>
<ul>
<li>7の段：7,14,21,28,35,42,49,56,63</li>
<li>8の段：8,16,24,32,40,48,56,64,72</li>
<li>6と7、7と8で間違えやすいので特に練習</li>
</ul>
<h3>長さ・かさ・重さ</h3>
<p>cm・mm・mL・L・g・kgの単位と換算を確認しましょう。</p>
<div class="tip-box"><p>💡 九九は毎日お風呂で唱えるだけで驚くほど定着します。</p></div>""",
    "faq": [
      {"q": "九九の覚え順は？", "a": "1の段から順番でもOKですが、2・5・10の段から始めると簡単なものから自信がつきます。"},
    ],
    "cta_href": "/kakezan-rensyu.html",
    "cta_label": "かけ算練習をする",
    "related": [
      {"href": "/kakezan-rensyu.html","emoji": "✖️", "text": "かけ算練習"},
      {"href": "/drill-2nen.html","emoji": "2️⃣", "text": "2年生ドリル"},
    ],
  },

  # ===== Batch 11 (Final) =====
  {
    "filename": "sansu-quiz1.html",
    "title": "算数クイズ①｜小学算数ドリル",
    "description": "算数の知識を試すクイズ問題集。四則計算・単位・図形の基本クイズで楽しく復習しましょう。",
    "h1": "算数クイズ①",
    "eyecatch": "❓",
    "body_html": """\
<h2>クイズで算数を復習しよう</h2>
<h3>Q1：7×8＝？</h3>
<p>答え：<strong>56</strong></p>
<h3>Q2：1km＝何m？</h3>
<p>答え：<strong>1000m</strong></p>
<h3>Q3：三角形の内角の和は？</h3>
<p>答え：<strong>180°</strong></p>
<h3>Q4：1/2＋1/3＝？</h3>
<p>答え：3/6+2/6＝<strong>5/6</strong></p>
<h3>Q5：速さ60km/hで2時間走ると何km？</h3>
<p>答え：60×2＝<strong>120km</strong></p>
<div class="tip-box"><p>💡 全問正解できたら次のクイズに挑戦してみましょう！</p></div>""",
    "faq": [
      {"q": "クイズで間違えた問題はどうすれば？", "a": "該当するページに戻って基本から確認しましょう。"},
    ],
    "cta_href": "/tougou-review.html",
    "cta_label": "総合復習テストへ",
    "related": [
      {"href": "/tougou-review.html","emoji": "📋", "text": "総合復習テスト"},
      {"href": "/keisan-training.html","emoji": "💪", "text": "計算トレーニング"},
    ],
  },
  {
    "filename": "sansu-quiz2.html",
    "title": "算数クイズ②（応用編）｜小学算数ドリル",
    "description": "少し難しい算数クイズ。割合・速さ・面積・文章題など応用問題で実力を試しましょう。",
    "h1": "算数クイズ②（応用編）",
    "eyecatch": "🧠",
    "body_html": """\
<h2>応用クイズに挑戦</h2>
<h3>Q1：定価1000円の商品を2割引きで買うと？</h3>
<p>答え：1000×0.8＝<strong>800円</strong></p>
<h3>Q2：時速80kmで90分走ると何km？</h3>
<p>答え：90分＝1.5時間　80×1.5＝<strong>120km</strong></p>
<h3>Q3：底辺6cm・高さ4cmの三角形の面積は？</h3>
<p>答え：6×4÷2＝<strong>12cm²</strong></p>
<h3>Q4：つると亀が合わせて8匹、足が22本。亀は何匹？</h3>
<p>全部つるなら8×2=16本、差6本÷2=<strong>3匹</strong>がかめ</p>
<div class="tip-box"><p>💡 応用問題も基本の組み合わせです。焦らず1ステップずつ解きましょう。</p></div>""",
    "faq": [
      {"q": "応用問題でつまずく原因は？", "a": "基本の公式を理解せず丸暗記している場合が多いです。なぜその式になるかを理解しましょう。"},
    ],
    "cta_href": "/mondai-bunrui.html",
    "cta_label": "文章題の種類を確認",
    "related": [
      {"href": "/mondai-bunrui.html","emoji": "📋", "text": "文章題の分類"},
      {"href": "/mondai-tsurukami.html","emoji": "🐢", "text": "つるかめ算"},
    ],
  },
  {
    "filename": "hito-keta-warizan.html",
    "title": "1桁のわり算完全マスター｜算数ドリル",
    "description": "1桁÷1桁のわり算を完全マスター。九九を使ったわり算の考え方と練習問題を解説します。",
    "h1": "1桁のわり算完全マスター",
    "eyecatch": "➗",
    "body_html": """\
<h2>わり算の考え方</h2>
<p>わり算はかけ算の逆です。九九を使って答えを求めます。</p>
<div class="formula-box"><p>□ ÷ ○ ＝ △ → ○ × △ ＝ □ (九九で確認)</p></div>
<h3>練習問題</h3>
<ul>
<li>18÷3＝<strong>6</strong>（3×6=18）</li>
<li>35÷7＝<strong>5</strong>（7×5=35）</li>
<li>48÷8＝<strong>6</strong>（8×6=48）</li>
<li>63÷9＝<strong>7</strong>（9×7=63）</li>
</ul>
<div class="tip-box"><p>💡 わり算で迷ったら「○の段で□になる数を探す」と考えましょう。</p></div>""",
    "faq": [
      {"q": "0÷○と○÷0はどうなる？", "a": "0÷○=0です。○÷0は計算できません（割ってはいけない）。"},
    ],
    "cta_href": "/warizan-kiso.html",
    "cta_label": "わり算の基本へ",
    "related": [
      {"href": "/warizan-kiso.html","emoji": "➗", "text": "わり算の基本"},
      {"href": "/warizan-rensyu.html","emoji": "➗", "text": "わり算の練習"},
    ],
  },
  {
    "filename": "kakezan-kujira.html",
    "title": "かけ算の工夫（交換・結合法則）｜算数ドリル",
    "description": "かけ算の交換法則・結合法則を使った計算の工夫を解説。計算を楽にするテクニックを練習しましょう。",
    "h1": "かけ算の工夫（交換・結合法則）",
    "eyecatch": "✖️",
    "body_html": """\
<h2>かけ算の基本法則</h2>
<div class="formula-box">
<p>交換法則：a×b ＝ b×a（順番を入れ替えても同じ）</p>
<p>結合法則：(a×b)×c ＝ a×(b×c)</p>
<p>分配法則：a×(b+c) ＝ a×b ＋ a×c</p>
</div>
<h3>計算の工夫例</h3>
<p>25×4×7 → (25×4)×7 = 100×7 = <strong>700</strong></p>
<p>99×8 → (100-1)×8 = 800-8 = <strong>792</strong></p>
<div class="tip-box"><p>💡 「×100になる組み合わせを先に計算」が工夫のコツです。</p></div>""",
    "faq": [
      {"q": "分配法則はいつ使う？", "a": "99×□や101×□など、100に近い数のかけ算に使うと便利です。"},
    ],
    "cta_href": "/kakezan-bunpai.html",
    "cta_label": "分配法則を練習",
    "related": [
      {"href": "/kakezan-bunpai.html","emoji": "✖️", "text": "分配法則"},
      {"href": "/kakizan-kiso.html","emoji": "✖️", "text": "かけ算の基本"},
    ],
  },
  {
    "filename": "mondai-nenkan.html",
    "title": "年間カレンダーと日数計算｜算数ドリル",
    "description": "月の日数・うるう年・○日後の計算など、カレンダーを使った日数計算の解き方を解説します。",
    "h1": "年間カレンダーと日数計算",
    "eyecatch": "📅",
    "body_html": """\
<h2>月の日数を覚えよう</h2>
<p>「30日ある月」：4・6・9・11月　「31日ある月」：1・3・5・7・8・10・12月　「2月」：28日（うるう年は29日）</p>
<div class="formula-box"><p>うるう年：4で割り切れる年（ただし100で割り切れても400で割り切れない年は除く）</p></div>
<h3>日数計算の例</h3>
<p>3月15日から45日後は何月何日？<br>3月残り：31-15=16日　4月：30日　45-16-30=△　5月の△日→<strong>4月30日+(-1)=4月29日</strong></p>
<p>→ 16+29=45日なので<strong>4月29日</strong></p>
<div class="tip-box"><p>💡 月をまたぐ計算は「その月の残り日数」から順に引いていくのがコツです。</p></div>""",
    "faq": [
      {"q": "うるう年は何年ごとですか？", "a": "おおよそ4年ごとです。ただし100年ごとに1回は飛び、400年ごとに1回は戻ります。"},
    ],
    "cta_href": "/jikan-keisan.html",
    "cta_label": "時間の計算を練習",
    "related": [
      {"href": "/jikan-keisan.html","emoji": "⏱", "text": "時間の計算"},
      {"href": "/jikan-henkan.html","emoji": "🕐", "text": "時間の換算"},
    ],
  },
  {
    "filename": "sansu-matome.html",
    "title": "算数の公式・定理まとめ集｜算数ドリル",
    "description": "小学算数で使う主要な公式・定理を一覧にまとめました。テスト前の最終確認に活用してください。",
    "h1": "算数の公式・定理まとめ集",
    "eyecatch": "📚",
    "body_html": """\
<h2>面積の公式</h2>
<ul>
<li>長方形：縦×横</li>
<li>正方形：一辺×一辺</li>
<li>三角形：底辺×高さ÷2</li>
<li>平行四辺形：底辺×高さ</li>
<li>台形：(上底+下底)×高さ÷2</li>
<li>ひし形：対角線×対角線÷2</li>
<li>円：半径×半径×3.14</li>
</ul>
<h2>体積の公式</h2>
<ul>
<li>直方体：縦×横×高さ</li>
<li>立方体：一辺×一辺×一辺</li>
<li>円柱：底面積×高さ</li>
</ul>
<h2>速さの公式</h2>
<div class="formula-box">
<p>速さ＝距離÷時間　距離＝速さ×時間　時間＝距離÷速さ</p>
</div>
<div class="tip-box"><p>💡 このページをブックマークしてテスト直前の確認に使いましょう。</p></div>""",
    "faq": [
      {"q": "円周の公式は？", "a": "円周＝直径×3.14（または半径×2×3.14）です。"},
    ],
    "cta_href": "/tougou-review.html",
    "cta_label": "総合復習テストへ",
    "related": [
      {"href": "/tougou-review.html","emoji": "📋", "text": "総合復習テスト"},
      {"href": "/suugaku-yogo.html","emoji": "📖", "text": "算数用語まとめ"},
      {"href": "/syougaku-sansu-map.html","emoji": "🗺️", "text": "学習マップ"},
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
