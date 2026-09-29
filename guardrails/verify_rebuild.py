#!/usr/bin/env python3
"""AdSense再構築（家庭学習の一次情報＋独自教材）done_when の機械判定。

引数なしで実行。すべて合格なら exit 0、1件でも落ちれば exit 1。
verify_adsense_ready.py と両方 exit 0 で完了とする。

  python3 guardrails/verify_rebuild.py
"""
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


def text_of(src):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", src))


ALL_HTML = sorted(os.path.basename(p) for p in glob(os.path.join(ROOT, "*.html")))
INDEXABLE = [p for p in ALL_HTML
             if "noindex" not in read(p) and p != "google4da7168775a54d86.html"]
sm = read("sitemap.xml")
SITEMAP = {("index.html" if u == "" else u)
           for u in re.findall(rf"<loc>{re.escape(SITE)}([^<]*)</loc>", sm)}


# ── R1. 主要15ページ：図解3・例題5・誤答例3・家庭実践メモ・ドリル導線・一次資料 ──
KEY15 = (["index.html", "grade-guide.html"]
         + [f"grade-{i}-tips.html" for i in range(1, 7)]
         + ["addition-guide.html", "subtraction-guide.html", "multiplication-guide.html",
            "division-guide.html", "fractions-guide.html", "percentage-guide.html",
            "bunshoudai-guide.html"])


def figures(src):
    """<figure class="fig..."> のうち中に <svg> を持つもの（自作図解）の数。"""
    n = 0
    for m in re.finditer(r'<figure class="fig[^"]*"[^>]*>(.*?)</figure>', src, re.S):
        body = m.group(1)
        if "<svg" in body and "<figcaption" in body:
            n += 1
    return n


total_fig = 0
for p in KEY15:
    src = read(p)
    f = figures(src)
    total_fig += f
    check("R1 図解3点以上", f >= 3, f"{p} の図解 {f}点")
    q = len(re.findall(r'<li class="q"', src))
    check("R1 独自例題5問以上", q >= 5, f"{p} の例題 {q}問")
    e = len(re.findall(r'class="err-case"', src))
    check("R1 誤答例3パターン以上", e >= 3, f"{p} の誤答例 {e}件")
    check("R1 家庭実践メモ", 'class="memo-box"' in src, f"{p} に memo-box が無い")
    check("R1 ドリル導線", re.search(r'href="/(drill|daily)\.html', src) is not None,
          f"{p} に drill/daily への導線が無い")
    if p != "index.html":
        check("R1 一次資料", 'class="ref-box"' in src, f"{p} に ref-box が無い")
    # 例題には解答が付いていること（<details> で折りたたみ）
    qs = re.findall(r'<li class="q".*?</li>', src, re.S)
    no_ans = [i for i, b in enumerate(qs, 1) if "<details" not in b]
    check("R1 例題に解答", not no_ans, f"{p} の例題 {no_ans} に解答が無い")

check("R1 図解の総数（主要15ページ）", total_fig >= 45, f"合計 {total_fig}点（45点以上）")


# ── R2. 統合：旧URLは移転スタブ（GitHub Pages では301不可のため meta refresh＋canonical＋noindex） ──
MERGED = {
    "parent-support.html": "math-anxiety.html",
    "teaching-tips.html": "math-anxiety.html",
    "benkyou-gohoubi.html": "study-habits.html",
    "tasizan-kuriagari.html": "addition-guide.html",
}
for old, new in MERGED.items():
    src = read(old)
    check("R2 stub noindex", 'content="noindex,follow"' in src, f"{old} が noindex,follow でない")
    check("R2 stub refresh", f'url=/{new}"' in src, f"{old} の meta refresh 先が {new} でない")
    check("R2 stub canonical", f'rel="canonical" href="{SITE}{new}"' in src,
          f"{old} の canonical が {new} でない")
    check("R2 stub 本文なし", len(text_of(src[src.find("<body"):])) < 200, f"{old} に本文が残っている")
    check("R2 sitemap除外", old not in SITEMAP, f"{old} が sitemap に残っている")
    check("R2 受け皿がsitemap", new in SITEMAP, f"{new} が sitemap に無い")
    for p in ALL_HTML:
        if p == old:
            continue
        check("R2 被リンク解消", f'href="/{old}' not in read(p), f"{p} が {old} を参照")

# 統合先に統合元の中身が実際に入っていること（削除だけで済ませていない証拠）
MERGE_EVIDENCE = {
    "math-anxiety.html": ["具体物", "ヒントは3段階", "先生ではない", "1回15分", "一緒に調べよう"],
    "study-habits.html": ["ごほうび", "体験型"],
    "addition-guide.html": ["36", "さくらんぼ"],
}
for p, keys in MERGE_EVIDENCE.items():
    txt = text_of(read(p))
    for k in keys:
        check("R2 統合の実体", k in txt, f"{p} に「{k}」が無い")


# ── R3. トップ：家庭で学ぶ → 練習する → 保護者向け の順 ──
top = read("index.html")
pos = [top.find(k) for k in ['id="learn"', 'id="practice"', 'id="parents"']]
check("R3 トップ3区分", all(x >= 0 for x in pos), f"区分idが無い {pos}")
check("R3 トップ区分の順序", pos == sorted(pos), f"順序が違う {pos}")
check("R3 キャッチ", "わかる→できる" in text_of(top), "キャッチコピーに「わかる→できる」が無い")
for k in ["運営者", "文部科学省", "検算"]:
    check("R3 既存の良い要素", k in text_of(top), f"トップから「{k}」が消えている")


# ── R4. 実践研究室：実データの無いページは公開しない ──
LAB = [p for p in ALL_HTML if p.startswith("lab-")]
for p in LAB:
    src = read(p)
    recorded = 'data-status="recorded"' in src
    if not recorded:
        check("R4 未記録は非公開", "noindex" in src, f"{p} は記録なしなのに index")
        check("R4 未記録はsitemap外", p not in SITEMAP, f"{p} は記録なしなのに sitemap")
check("R4 記録コンポーネント", os.path.exists(os.path.join(ROOT, "record-kit.js")),
      "record-kit.js が無い")


# ── R5. 根拠のない断定表現（§15）：index対象ページ全体 ──
BANNED = ["最高", "最短", "最強", "唯一", "半分は", "多くの子", "大半", "一番険しい",
          "最も生まれる", "最難関", "最重要",
          # 独立検証（2026-09-27）で見つかった言い回し
          "最大の原因", "最大の山場", "最大の難所", "最大の混乱", "最大の準備", "最大のテーマ",
          "劇的", "準拠", "試したかぎり", "一番の対策", "最も多い", "最も効率", "子が多い"]
for p in INDEXABLE:
    txt = text_of(read(p))  # JSON-LD も対象
    for w in BANNED:
        check("R5 断定表現", w not in txt, f"{p} に「{w}」x{txt.count(w)}")


# ── R6. 文字化け・誤字（簡体字の混入） ──
# 日本語と同じ符号位置の字（会・来 など）は入れない。簡体字にしか無い字だけを検出する。
SIMPLIFIED = re.compile(r"[题为这们对说时过发经问给还样]")
for p in ALL_HTML:
    hit = SIMPLIFIED.findall(text_of(read(p)))
    check("R6 簡体字", not hit, f"{p} に {hit[:5]}")


# ── R7. index対象ページの h1 / title / description 重複なし ──
for tagname, rx in [("title", r"<title>(.*?)</title>"),
                    ("description", r'<meta name="description" content="(.*?)"'),
                    ("h1", r"<h1[^>]*>(.*?)</h1>")]:
    seen = {}
    for p in INDEXABLE:
        m = re.search(rx, read(p), re.S)
        if not m:
            check(f"R7 {tagname}あり", tagname == "description", f"{p} に {tagname} が無い")
            continue
        v = text_of(m.group(1)).strip()
        if v in seen:
            check(f"R7 {tagname}重複", False, f"{p} と {seen[v]}")
        seen[v] = p


# ── R8. 画像 alt ──
for p in INDEXABLE:
    for img in re.findall(r"<img\b[^>]*>", read(p)):
        check("R8 img alt", "alt=" in img, f"{p}: {img[:60]}")


# ── R9. SVG 図解にアクセシブルな名前 ──
for p in KEY15:
    for m in re.finditer(r'<figure class="fig[^"]*"[^>]*>(.*?)</figure>', read(p), re.S):
        svg = re.search(r"<svg\b[^>]*>", m.group(1))
        if svg:
            check("R9 svg role/label", 'role="img"' in svg.group(0) and "aria-label" in svg.group(0),
                  f"{p}: {svg.group(0)[:70]}")


# ── R10. FAQ構造化データは画面に表示している質問だけ（Googleのガイドライン） ──
import json as _json
for p in INDEXABLE:
    src = read(p)
    vis = text_of(re.sub(r'<script\b.*?</script>', ' ', src[src.find("<body"):], flags=re.S))
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        data = _json.loads(m.group(1))
        if data.get("@type") != "FAQPage":
            continue
        for q in data.get("mainEntity", []):
            name = re.sub(r"\s+", " ", q["name"]).strip()
            check("R10 FAQ構造化データが画面にある", name in vis, f"{p}: 「{name[:30]}」が画面に無い")


# ── R11. sitemap の lastmod と、記事に表示している最終更新日が一致 ──
for line in sm.splitlines():
    m = re.search(rf"<loc>{re.escape(SITE)}([^<]*)</loc><lastmod>(\d+)-(\d+)-(\d+)</lastmod>", line)
    if not m:
        continue
    p = m.group(1) or "index.html"
    shown = re.search(r"最終更新: (\d+)年(\d+)月(\d+)日", read(p))
    if shown:
        want = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
        got = tuple(int(x) for x in shown.groups())
        check("R11 最終更新日", got == want, f"{p}: 表示 {got} / sitemap {want}")


# ── R12. 例題の答えと考え方に、数え方の誤り（1日n問×日数）が無い ──
for p in KEY15:
    for m in re.finditer(r"1日(\d+)問ずつなら、?(\d+)日で(\d+)問", text_of(read(p))):
        a, d, total = map(int, m.groups())
        check("R12 日数×問数", a * d >= total, f"{p}: {a}×{d}＜{total}")


# ── R13. ドリルの出題が平成29年告示の学習指導要領の学年配当に合う（速さは第5学年） ──
SPEED = re.compile(r"分速は|道のりは|何時間")
for p in ["drill.html", "daily.html", "premium-pdf.html"]:
    src = read(p)
    s5, s6 = src.index("5:{label:'小学5年生'"), src.index("6:{label:'小学6年生'")
    e6 = src.index("}}", src.index("hard:[", s6))
    check("R13 速さは5年で出題", len(SPEED.findall(src[s5:s6])) >= 3, f"{p}: 5年に速さの問題が無い")
    check("R13 6年で速さを出題しない", not SPEED.findall(src[s6:e6]), f"{p}: 6年に速さの問題がある")


# ── R14. Amazonアソシエイト：必須の表記と、リンクの rel="sponsored" ──
AMZ_STATEMENT = "Amazonのアソシエイトとして、にじゅうまる。算数ドリルは適格販売により収入を得ています。"
check("R14 privacy に Amazon の表記", AMZ_STATEMENT in text_of(read("privacy.html")),
      "privacy.html に Amazon アソシエイトの表記が無い")
for p in ALL_HTML:
    src = read(p)
    links = re.findall(r'<a\b[^>]*href=["\']https?://(?:amzn\.to|amzn\.asia|a\.co|(?:www\.)?amazon\.co\.jp)/[^"\']*["\'][^>]*>', src)
    if not links:
        continue
    check("R14 Amazonリンクのあるページに表記", AMZ_STATEMENT in text_of(src),
          f"{p} に Amazon アソシエイトの表記が無い")
    for a in links:
        rel = re.search(r'rel="([^"]*)"', a)
        check("R14 Amazonリンクは sponsored", rel is not None and "sponsored" in rel.group(1).split(),
              f"{p}: {a[:70]}")


# ── R15. アフィリエイトは比較記事1ページだけ（AdSense審査中の方針）＋クリック計測 ──
AFF_PAGE = "tablet-sansu-kyozai-hikaku.html"
AFF_MARK = re.compile(r"px\.a8\.net|rakuten_affiliateId|hb\.afl\.rakuten|amzn\.to|amzn\.asia|amazon\.co\.jp/[^\"']*tag=")
for p in ALL_HTML:
    if p != AFF_PAGE:
        check("R15 アフィリエイトは1ページだけ", not AFF_MARK.search(read(p)), f"{p} にアフィリエイトがある")
aff = read(AFF_PAGE)
aff_links = re.findall(r'<a\b[^>]*href="https://(?:px\.a8\.net|amzn\.to)/[^"]*"[^>]*>', aff)
check("R15 アフィリエイトリンクがある", len(aff_links) >= 5, f"{len(aff_links)}本")
for a in aff_links:
    check("R15 計測属性", bool(re.search(r'data-aff="[a-z]+"', a) and re.search(r'data-pos="[a-z]+"', a)),
          f"data-aff / data-pos が無い: {a[:70]}")
    rel = re.search(r'rel="([^"]*)"', a)
    check("R15 sponsored", rel is not None and "sponsored" in rel.group(1).split(),
          f"rel に sponsored が無い: {a[:70]}")
check("R15 クリック計測スクリプト", '"affiliate_click"' in aff and 'closest("a[data-aff]")' in aff,
      "affiliate_click の送信が無い")
check("R15 本文に Amazon Kids+ の節", '<h2 id="amazon-kids">' in aff
      and 'data-aff="amazon" data-pos="body"' in aff, "Amazon Kids+ の節か本文リンクが無い")
check("R15 比較記事への内部リンク",
      any(f'href="/{AFF_PAGE}' in read(p) for p in INDEXABLE if p != AFF_PAGE),
      "比較記事がどこからもリンクされていない")


if failures:
    print(f"NG {len(failures)} / {checks} checks failed\n")
    for f in failures[:120]:
        print("  ✗ " + f)
    if len(failures) > 120:
        print(f"  … ほか {len(failures) - 120} 件")
    sys.exit(1)

print(f"OK  {checks} checks passed  (主要15ページの図解 合計 {total_fig}点)")
sys.exit(0)
