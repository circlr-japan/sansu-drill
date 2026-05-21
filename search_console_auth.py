#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Search Console API 認証スクリプト
初回実行でブラウザが開き、Googleアカウントで認可します。
token.json が生成されたら次回以降は自動認証されます。

使い方:
  python3 search_console_auth.py
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Search Console の読み取り権限
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

def get_credentials():
    creds = None

    # 既存トークンを読み込む
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # トークンが無効 or 期限切れの場合は再認証
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("✅ トークンを更新しました")
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"❌ {CREDENTIALS_FILE} が見つかりません")
                print("Google Cloud Console から OAuth クライアント ID の JSON をダウンロードしてください")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            print("✅ 認証成功！")

        # トークンを保存
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"✅ トークンを保存: {TOKEN_FILE}")

    return creds

if __name__ == "__main__":
    print("🔑 Google Search Console API 認証を開始します...")
    creds = get_credentials()
    if creds:
        print("\n✅ 認証完了！search_console_analysis.py を実行できます")
    else:
        print("\n❌ 認証に失敗しました")
