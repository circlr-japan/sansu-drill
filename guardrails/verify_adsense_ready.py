#!/usr/bin/env python3
"""AdSense再申請 優先度S チェック（改修指示書 §31 / §34 の機械判定版）

引数なしで実行。すべて合格なら exit 0、1件でも落ちれば exit 1。
判定はこのスクリプトのみが行う。目視やエージェントの主観は根拠にしない。

  python3 guardrails/verify_adsense_ready.py
"""
import json
import os
import re
import sys
from glob import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.nijumaru-drill.com/"

failures = []
checks = 0


def check(name, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        failures.append(f"{name}: {detail}")
    return ok


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def visible_html(src):
    """初期HTMLとして描画される部分（<template> と <script> を除いた body）。"""
    body = src[src.find("<body"):]
    body = re.sub(r"<template\b.*?</template>", "", body, flags=re.S)
    body = re.sub(r"<script\b.*?</script>", "", body, flags=re.S)
    return body


def text_of(src):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", src))


ALL_HTML = sorted(os.path.basename(p) for p in glob(os.path.join(ROOT, "*.html")))
# 別サイトの移転スタブ・Google認証ファイルは対象外
EXCLUDE = {"google4da7168775a54d86.html", "tokusho-uranai.html"}
PAGES = [p for p in ALL_HTML if p not in EXCLUDE]


# ── S1. /index.html への内部リンクが残っていない（トップは / に一本化） ──
for p in PAGES:
    hits = re.findall(r'href="/?index\.html"', read(p))
    check("S1 index.html内部リンク", not hits, f"{p} に {len(hits)}件")
check("S1 トップcanonical", f'rel="canonical" href="{SITE}"' in read("index.html"),
      "index.html の canonical が / になっていない")


# ── S2. drill のcanonicalが /drill.html に固定（パラメータURLも同一HTML） ──
check("S2 drill canonical",
      f'rel="canonical" href="{SITE}drill.html"' in read("drill.html"),
      "drill.html の canonical が /drill.html でない")


# ── S3/S28. sitemap の健全性 ──
sm = read("sitemap.xml")
locs = re.findall(rf"<loc>{re.escape(SITE)}([^<]*)</loc>", sm)
check("S3 sitemapにパラメータURLなし",
      not [u for u in locs if "?" in u], str([u for u in locs if "?" in u]))
check("S3 sitemapにindex.htmlなし", "index.html" not in locs, "index.html が掲載されている")
for u in locs:
    fname = "index.html" if u == "" else u
    if not check("S3 sitemap実在", os.path.exists(os.path.join(ROOT, fname)), f"{u} のファイルが無い"):
        continue
    src = read(fname)
    check("S3 sitemapにnoindexなし", "noindex" not in src, f"{u} は noindex")
    m = re.search(rf'rel="canonical" href="{re.escape(SITE)}([^"]*)"', src)
    check("S3 canonical自己参照", m is not None and m.group(1) == u,
          f"{u} の canonical が {m.group(1) if m else 'なし'}")


# ── S4. index対象ページに「近日」「準備中」等が無い ──
INCOMPLETE = ["近日", "準備中", "coming soon", "Coming Soon", "実装予定", "追加予定"]
for p in PAGES:
    src = read(p)
    if "noindex" in src:
        continue
    txt = text_of(visible_html(src))
    for w in INCOMPLETE:
        check("S4 未完成表示", w not in txt, f"{p} に「{w}」")


# ── S5/S27. 検索対象外にすべきページの noindex ──
for p in ["premium-pdf.html", "thanks.html", "404.html", "no-mistakes.html"]:
    src = read(p)
    check("S5 noindex", re.search(r'<meta name="robots" content="noindex', src) is not None,
          f"{p} に noindex が無い")


# ── S7/S29/S30. 広告を置かないページ ──
NO_AD = ["premium.html", "premium-pdf.html", "thanks.html", "drill.html",
         "daily.html", "404.html", "no-mistakes.html"]
for p in NO_AD:
    check("S7 広告なし", "adsbygoogle" not in read(p), f"{p} に AdSense がある")


# ── S6. privacy に必須の記載がある ──
priv = read("privacy.html")
for key in ["Stripe", "カード番号", "パーソナライズ", "取得する場合があります", "Cookie"]:
    check("S6 privacy記載", key in priv, f"privacy.html に「{key}」が無い")
check("S6 privacy断定回避",
      "当サイトは氏名・住所・電話番号などの個人を特定できる情報を収集しません。" not in priv,
      "「収集しません」の断定が残っている")


# ── S8. no-mistakes が reduce-mistakes に統合済み ──
nm = read("no-mistakes.html")
check("S8 統合リダイレクト", "url=/reduce-mistakes.html" in nm, "no-mistakes に meta refresh が無い")
check("S8 統合canonical", f'href="{SITE}reduce-mistakes.html"' in nm, "no-mistakes の canonical が違う")
for p in PAGES:
    if p == "no-mistakes.html":
        continue
    check("S8 被リンク解消", "no-mistakes.html" not in read(p), f"{p} が no-mistakes を参照")
rm = read("reduce-mistakes.html")
check("S8 中心コンテンツ", "1週間ミス記録表" in rm, "reduce-mistakes に1週間ミス記録表が無い")


# ── S9/S10. drill / daily の初期HTMLに結果画面が出ない ──
# 結果表示の文言（説明文ではなく画面そのもの）
STATE_WORDS = ["解答一覧", "パーフェクト", "今日のドリル完了", "使い切りました",
               "点 / 100点", "0/40", "0/25"]
# 操作後にだけ存在すべき画面の要素ID
STATE_IDS = {
    "drill.html": ["resultPage", "quizPage", "taResultPage", "countdownPage",
                   "scoreNum", "resultTitle", "reviewList", "rankingEntrySection",
                   "shareSection", "statScore"],
    "daily.html": ["drillPage", "resultPage", "drillProgress"],
}
for p in ["drill.html", "daily.html"]:
    vis = visible_html(read(p))
    txt = text_of(vis)
    for w in STATE_WORDS:
        check("S9/S10 初期HTML", w not in txt, f"{p} の初期HTMLに「{w}」")
    for eid in STATE_IDS[p]:
        check("S9/S10 初期HTML要素", f'id="{eid}"' not in vis,
              f"{p} の初期HTMLに #{eid} がある")
# 初期HTMLに必要な要素は残っていること
drill_txt = text_of(visible_html(read("drill.html")))
for w in ["学年", "難易度", "使い方"]:
    check("S9 初期HTML必須", w in drill_txt, f"drill.html の初期HTMLに「{w}」が無い")
daily_txt = text_of(visible_html(read("daily.html")))
for w in ["今日のドリルとは", "毎日続けるメリット", "学年", "難易度"]:
    check("S10 初期HTML必須", w in daily_txt, f"daily.html の初期HTMLに「{w}」が無い")
# template が実在し、展開コードがあること
for p in ["drill.html", "daily.html"]:
    src = read(p)
    check("S9/S10 template", 'id="tpl-appStates"' in src, f"{p} に tpl-appStates が無い")
    check("S9/S10 展開コード", "materializeAppStates" in src, f"{p} に展開処理が無い")


# ── S11. 根拠のない断定表現（§21） ──
BANNED = ["絶対", "最強", "鉄則", "治療", "定着率", "多くの子ども", "ほぼ全部", "正解です"]
BANNED_RE = [r"\d+点以下", r"\d+分以上", r"効果が\d+倍"]
for p in PAGES:
    src = read(p)
    if "noindex" in src:
        continue
    txt = text_of(src)  # JSON-LD も含めて検査
    for w in BANNED:
        n = txt.count(w)
        # math-anxiety の「ほぼ全部が合うレベル」は程度表現なので許容
        if w == "ほぼ全部" and "ほぼ全部が合うレベル" in txt:
            n -= txt.count("ほぼ全部が合うレベル")
        check("S11 断定表現", n <= 0, f"{p} に「{w}」x{n}")
    for rx in BANNED_RE:
        hit = re.findall(rx, txt)
        check("S11 数値断定", not hit, f"{p} に {hit}")


# ── 想定外の文字種が混入していない（日本語サイトなので） ──
STRAY = re.compile(r"[Ѐ-ӿԀ-ԯ가-힯฀-๿]")
for p in PAGES:
    hit = STRAY.findall(read(p))
    check("文字種", not hit, f"{p} にキリル文字/ハングル/タイ文字 {hit[:5]}")


# ── 404リンクなし（サイト内リンクの実在確認） ──
for p in PAGES:
    src = read(p)
    for href in set(re.findall(r'href="/([A-Za-z0-9_\-]+\.html)"', src)):
        check("内部リンク実在", os.path.exists(os.path.join(ROOT, href)), f"{p} → /{href} が無い")


# ── JSON-LD が壊れていない ──
for p in PAGES:
    for m in re.finditer(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', read(p), re.S):
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            check("JSON-LD", False, f"{p}: {e}")
        else:
            check("JSON-LD", True)


# ── 結果 ──
if failures:
    print(f"NG {len(failures)} / {checks} checks failed\n")
    for f in failures:
        print("  ✗ " + f)
    sys.exit(1)

print(f"OK  {checks} checks passed")
sys.exit(0)
