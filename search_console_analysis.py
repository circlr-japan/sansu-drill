#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search Console キーワード自動分析スクリプト
- 過去28日間のクエリデータを取得
- 表示回数が多いのにクリック率が低いクエリを抽出
- 対応記事がないキーワードを検出
- レポートをMarkdownで出力

使い方:
  python3 search_console_analysis.py
"""

import os
import json
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# ===== 設定 =====
SITE_URL = "sc-domain:nijumaru-drill.com"  # Search Console のプロパティURL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# 既存ページのキーワードマッピング（ページが対応しているトピック）
EXISTING_TOPICS = {
    "たし算", "ひき算", "かけ算", "わり算", "九九", "分数", "小数", "百分率", "割合",
    "図形", "面積", "体積", "角度", "円周", "文章題", "暗算", "計算ミス", "ケアレスミス",
    "算数嫌い", "テスト対策", "夏休み", "先取り学習", "学習ルーティン", "勉強習慣",
    "1年生", "2年生", "3年生", "4年生", "5年生", "6年生",
    "足し算", "引き算", "掛け算", "割り算",
}

def get_service():
    """Search Console API サービスを取得"""
    if not os.path.exists(TOKEN_FILE):
        print("❌ token.json が見つかりません。先に search_console_auth.py を実行してください")
        return None

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("searchconsole", "v1", credentials=creds)

def fetch_queries(service, days=28, row_limit=500):
    """過去N日間のクエリデータを取得"""
    end_date = datetime.date.today() - datetime.timedelta(days=3)  # 3日前まで（最新データの遅延考慮）
    start_date = end_date - datetime.timedelta(days=days)

    print(f"📅 データ取得期間: {start_date} ～ {end_date}")

    request_body = {
        "startDate": str(start_date),
        "endDate": str(end_date),
        "dimensions": ["query"],
        "rowLimit": row_limit,
        "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}]
    }

    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request_body
    ).execute()

    rows = response.get("rows", [])
    print(f"✅ {len(rows)} クエリを取得")
    return rows

def fetch_pages(service, days=28, row_limit=100):
    """ページ別パフォーマンスデータを取得"""
    end_date = datetime.date.today() - datetime.timedelta(days=3)
    start_date = end_date - datetime.timedelta(days=days)

    request_body = {
        "startDate": str(start_date),
        "endDate": str(end_date),
        "dimensions": ["page"],
        "rowLimit": row_limit,
        "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}]
    }

    response = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body=request_body
    ).execute()

    return response.get("rows", [])

def analyze_opportunities(rows):
    """SEO改善機会を分析"""
    # CTRが低いのに表示回数が多いクエリ（タイトル改善候補）
    low_ctr = [r for r in rows
               if r.get("impressions", 0) >= 10
               and r.get("ctr", 1) < 0.05
               and r.get("position", 99) <= 20]
    low_ctr.sort(key=lambda x: x.get("impressions", 0), reverse=True)

    # 順位11-20位（2ページ目）で表示回数が多い（1ページ目に上げやすい）
    page2 = [r for r in rows
             if 11 <= r.get("position", 99) <= 20
             and r.get("impressions", 0) >= 5]
    page2.sort(key=lambda x: x.get("impressions", 0), reverse=True)

    # 対応記事がないと思われるキーワード（新規記事候補）
    def has_existing_page(query):
        return any(topic in query for topic in EXISTING_TOPICS)

    new_article_candidates = [r for r in rows
                               if r.get("impressions", 0) >= 5
                               and not has_existing_page(r["keys"][0])]
    new_article_candidates.sort(key=lambda x: x.get("impressions", 0), reverse=True)

    return {
        "low_ctr": low_ctr[:20],
        "page2": page2[:20],
        "new_article_candidates": new_article_candidates[:20],
    }

def generate_report(rows, pages, opportunities):
    """Markdownレポートを生成"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    total_impressions = sum(r.get("impressions", 0) for r in rows)
    total_clicks = sum(r.get("clicks", 0) for r in rows)
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_position = (sum(r.get("position", 0) * r.get("impressions", 0) for r in rows) / total_impressions) if total_impressions > 0 else 0

    report = f"""# Search Console 分析レポート
生成日: {today}

## 📊 サマリー（過去28日間）
| 指標 | 値 |
|------|-----|
| 総表示回数 | {total_impressions:,} |
| 総クリック数 | {total_clicks:,} |
| 平均CTR | {avg_ctr:.1f}% |
| 平均掲載順位 | {avg_position:.1f}位 |
| クエリ数 | {len(rows):,} |

## 🏆 上位クエリ TOP20
| クエリ | 表示回数 | クリック | CTR | 順位 |
|--------|----------|----------|-----|------|
"""
    for r in rows[:20]:
        q = r["keys"][0]
        imp = int(r.get("impressions", 0))
        clk = int(r.get("clicks", 0))
        ctr = r.get("ctr", 0) * 100
        pos = r.get("position", 0)
        report += f"| {q} | {imp:,} | {clk} | {ctr:.1f}% | {pos:.1f} |\n"

    report += f"""
## ⚠️ CTR改善候補（表示回数多いのにCTR低い）
タイトル・ディスクリプションの改善で大幅クリック増が見込める

| クエリ | 表示回数 | CTR | 順位 |
|--------|----------|-----|------|
"""
    for r in opportunities["low_ctr"][:10]:
        q = r["keys"][0]
        imp = int(r.get("impressions", 0))
        ctr = r.get("ctr", 0) * 100
        pos = r.get("position", 0)
        report += f"| {q} | {imp:,} | {ctr:.1f}% | {pos:.1f} |\n"

    report += f"""
## 📈 2ページ目キーワード（1ページ目に上げやすい）
内部リンク強化・コンテンツ追記で順位アップ可能

| クエリ | 表示回数 | クリック | 順位 |
|--------|----------|----------|------|
"""
    for r in opportunities["page2"][:10]:
        q = r["keys"][0]
        imp = int(r.get("impressions", 0))
        clk = int(r.get("clicks", 0))
        pos = r.get("position", 0)
        report += f"| {q} | {imp:,} | {clk} | {pos:.1f} |\n"

    report += f"""
## 📝 新規記事候補キーワード（対応ページなし）
これらのクエリに特化した記事を作成することで新規流入が見込める

| クエリ | 表示回数 | 順位 |
|--------|----------|------|
"""
    for r in opportunities["new_article_candidates"][:15]:
        q = r["keys"][0]
        imp = int(r.get("impressions", 0))
        pos = r.get("position", 0)
        report += f"| {q} | {imp:,} | {pos:.1f} |\n"

    report += f"""
## 📄 上位ページ TOP10
| ページ | 表示回数 | クリック | CTR | 順位 |
|--------|----------|----------|-----|------|
"""
    for r in pages[:10]:
        url = r["keys"][0].replace("https://www.nijumaru-drill.com", "")
        imp = int(r.get("impressions", 0))
        clk = int(r.get("clicks", 0))
        ctr = r.get("ctr", 0) * 100
        pos = r.get("position", 0)
        report += f"| {url} | {imp:,} | {clk} | {ctr:.1f}% | {pos:.1f} |\n"

    report += "\n---\n*Generated by search_console_analysis.py*\n"
    return report

def main():
    print("🔍 Search Console キーワード分析を開始します...")

    service = get_service()
    if not service:
        return

    # データ取得
    rows = fetch_queries(service)
    pages = fetch_pages(service)

    if not rows:
        print("❌ データが取得できませんでした")
        return

    # 分析
    opportunities = analyze_opportunities(rows)

    # レポート生成
    report = generate_report(rows, pages, opportunities)

    # 保存
    os.makedirs(REPORT_DIR, exist_ok=True)
    today = datetime.date.today().strftime("%Y-%m-%d")
    report_path = os.path.join(REPORT_DIR, f"seo_report_{today}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ レポートを保存: {report_path}")

    # コンソールにサマリー表示
    print("\n" + "="*50)
    print("📊 クイックサマリー")
    print("="*50)
    print(f"上位クエリ: {rows[0]['keys'][0]} ({int(rows[0].get('impressions',0))}回表示)" if rows else "")
    print(f"\n⚠️ CTR改善候補 上位3件:")
    for r in opportunities["low_ctr"][:3]:
        print(f"  - {r['keys'][0]}: {int(r.get('impressions',0))}回表示, CTR {r.get('ctr',0)*100:.1f}%")
    print(f"\n📝 新規記事候補 上位3件:")
    for r in opportunities["new_article_candidates"][:3]:
        print(f"  - {r['keys'][0]}: {int(r.get('impressions',0))}回表示, {r.get('position',0):.1f}位")

if __name__ == "__main__":
    main()
