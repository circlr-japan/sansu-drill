#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL インデックス申請スクリプト

使い方:
  python3 url_inspection.py --sitemap      # サイトマップ再送信（無制限）
  python3 url_inspection.py --inspect      # 新記事のURL検査（10件/日）
  python3 url_inspection.py --all          # 両方実行

認証:
  token.json が必要。なければ search_console_auth.py を先に実行。
  ※ webmasters スコープ（read/write）が必要。token.jsonを削除して再認証が必要な場合あり。
"""

import os
import json
import argparse
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
LOG_FILE = os.path.join(BASE_DIR, "reports/inspection_log.json")

SITE_URL = "sc-domain:nijumaru-drill.com"
SITE_BASE = "https://www.nijumaru-drill.com"
SITEMAP_URL = f"{SITE_BASE}/sitemap.xml"

# webmasters スコープ（readonlyではなくwrite込み）
SCOPES = ["https://www.googleapis.com/auth/webmasters"]

# インデックス申請優先URL（バッチ管理）
# バッチ1（2026-05-22 実施済み）: 5/22公開の10記事
BATCH_1 = [
    "/parent-support.html",
    "/tablet-learning.html",
    "/review-method.html",
    "/notebook-method.html",
    "/math-game.html",
    "/unit-conversion.html",
    "/prime-numbers.html",
    "/speed-distance.html",
    "/ratio-guide.html",
    "/large-numbers.html",
]

# バッチ2（次回実施用）: 5/18〜5/21公開の4記事 + 主要記事6件
BATCH_2 = [
    "/addition-guide.html",
    "/subtraction-guide.html",
    "/multiplication-guide.html",
    "/time-calculation.html",
    "/geometry-guide.html",
    "/kuku-tips.html",
    "/percentage-guide.html",
    "/fractions-guide.html",
    "/word-problems.html",
    "/mental-math.html",
]

# バッチ3（2026-05-23 実施予定）: addition-guide再申請 + 難易度別ページ先行9件
BATCH_3 = [
    "/addition-guide.html",
    "/tasizan-kuriagari-nashi.html",
    "/tasizan-kuriagari-ari.html",
    "/tasizan-2keta.html",
    "/tasizan-hissan.html",
    "/hikizan-kurisagari-nashi.html",
    "/hikizan-kurisagari-ari.html",
    "/hikizan-2keta.html",
    "/hikizan-hissan.html",
]

# バッチ4（2026-05-24 実施予定）: 九九段別
BATCH_4 = [
    "/kuku-1dan.html",
    "/kuku-2dan.html",
    "/kuku-3dan.html",
    "/kuku-4dan.html",
    "/kuku-5dan.html",
    "/kuku-6dan.html",
    "/kuku-7dan.html",
    "/kuku-8dan.html",
    "/kuku-9dan.html",
]

# バッチ5（2026-05-25 実施予定）: わり算・かけ算難易度別
BATCH_5 = [
    "/warizan-kantan.html",
    "/warizan-amari.html",
    "/warizan-2keta.html",
    "/warizan-hissan-kantan.html",
    "/warizan-hissan-2keta.html",
    "/kakizan-2keta-1keta.html",
    "/kakizan-hissan-kantan.html",
    "/kakizan-hissan-2keta.html",
    "/suken-guide.html",
]

# バッチ6（2026-05-26 実施予定）: 分数・小数難易度別
BATCH_6 = [
    "/bunsuu-doubunmo.html",
    "/bunsuu-ibunmo.html",
    "/bunsuu-taisuu.html",
    "/bunsuu-kakizan.html",
    "/bunsuu-warizan.html",
    "/syousuu-tasizan.html",
    "/syousuu-kakizan.html",
    "/syousuu-warizan.html",
    "/grade-6-tips.html",
]

# 現在のバッチ（切り替えて使用）
PRIORITY_URLS = BATCH_3


def get_credentials():
    """認証情報を取得（token.jsonがあれば再利用、なければ新規認証）"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"❌ {CREDENTIALS_FILE} が見つかりません")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def submit_sitemap(service):
    """サイトマップを再送信してGoogleに再クロールを促す"""
    print("\n📋 サイトマップ再送信中...")
    print(f"  URL: {SITEMAP_URL}")
    try:
        service.sitemaps().submit(siteUrl=SITE_URL, feedpath=SITEMAP_URL).execute()
        print(f"  ✅ 送信成功！Googleがクロールを開始します")
        return True
    except HttpError as e:
        if e.resp.status == 403:
            print(f"  ⚠️ 権限エラー: webmasters スコープが必要です。token.json を削除して再認証してください")
        else:
            print(f"  ❌ エラー: {e}")
        return False


def inspect_urls(service, urls):
    """URLを個別に検査してインデックス状況を確認"""
    print(f"\n🔍 URL検査開始（{len(urls)}件）...")

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    log = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            log = json.load(f)

    results = []
    for url in urls:
        full_url = SITE_BASE + url
        print(f"\n  チェック中: {full_url}")
        try:
            result = service.urlInspection().index().inspect(
                body={
                    "inspectionUrl": full_url,
                    "siteUrl": SITE_URL
                }
            ).execute()

            inspection = result.get("inspectionResult", {})
            index_status = inspection.get("indexStatusResult", {})
            coverage_state = index_status.get("coverageState", "不明")
            verdict = index_status.get("verdict", "不明")
            last_crawl = index_status.get("lastCrawlTime", "未クロール")

            # 日付のみ表示
            if "T" in str(last_crawl):
                last_crawl = last_crawl[:10]

            status_icon = "✅" if verdict == "PASS" else "⏳"
            print(f"    {status_icon} 状態: {coverage_state} | 最終クロール: {last_crawl}")

            log[full_url] = {
                "checked": str(datetime.date.today()),
                "verdict": verdict,
                "coverage_state": coverage_state,
                "last_crawl": last_crawl
            }
            results.append({"url": url, "verdict": verdict, "coverage_state": coverage_state})

        except HttpError as e:
            if e.resp.status == 429:
                print(f"    ⚠️ クォータ超過（10件/日）。明日また実行してください")
                break
            elif "URL_NOT_ON_PROPERTY" in str(e):
                print(f"    ❌ プロパティ外のURL")
            else:
                print(f"    ❌ エラー: {e}")

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    # サマリー
    passed = sum(1 for r in results if r["verdict"] == "PASS")
    print(f"\n📊 結果サマリー: {passed}/{len(results)} インデックス済み")
    if passed < len(results):
        not_indexed = [r["url"] for r in results if r["verdict"] != "PASS"]
        print("  未インデックス:")
        for u in not_indexed:
            print(f"    - {u}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sitemap", action="store_true", help="サイトマップ再送信")
    parser.add_argument("--inspect", action="store_true", help="URL個別検査（10件/日）")
    parser.add_argument("--all", action="store_true", help="サイトマップ再送信＋URL検査")
    args = parser.parse_args()

    if not any([args.sitemap, args.inspect, args.all]):
        parser.print_help()
        return

    creds = get_credentials()
    if not creds:
        return

    service = build("searchconsole", "v1", credentials=creds)

    if args.sitemap or args.all:
        submit_sitemap(service)

    if args.inspect or args.all:
        inspect_urls(service, PRIORITY_URLS)


if __name__ == "__main__":
    main()
