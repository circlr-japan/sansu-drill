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
