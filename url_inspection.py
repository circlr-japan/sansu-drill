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

# インデックス申請優先URL（新しい記事順）
PRIORITY_URLS = [
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
