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
