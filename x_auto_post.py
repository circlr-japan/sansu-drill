#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) 自動投稿スクリプト
新規記事公開時・定期的な算数Tips投稿を自動化

使い方:
  python3 x_auto_post.py --type tips        # 算数Tipsをランダム投稿
  python3 x_auto_post.py --type article     # 最新記事を投稿
  python3 x_auto_post.py --type test        # テスト投稿（実際には投稿しない）

設定:
  x_config.json に API キーを記載してください
"""

import os
import json
import random
import argparse
import datetime
import tweepy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "x_config.json")
POST_LOG_FILE = os.path.join(BASE_DIR, "x_post_log.json")

# ===== 投稿テンプレート =====

TIPS_POSTS = [
    """📐 図形が苦手な小学生へ

「面積」は頭で考えるより、方眼紙に書いてみるのが一番！
1マス＝1㎠で実際に数えると、公式の意味が自然とわかります。

#算数 #小学生 #図形 #にじゅうまるドリル
https://www.nijumaru-drill.com/geometry-guide.html""",

    """✖️ 九九が覚えられない子に効果的な方法

「歌で覚える」より「使って覚える」が定着します。
毎日の買い物で「3個×4袋=?」と声に出すだけでOK！

#算数 #九九 #小学生 #にじゅうまるドリル
https://www.nijumaru-drill.com/kuku-tips.html""",

    """📝 文章題が解けない本当の理由

計算力の問題ではなく「何を求めるか」が読めていないケースが多いです。
問題文に線を引いて「求めるもの」を丸で囲む習慣をつけましょう。

#算数 #文章題 #小学生 #にじゅうまるドリル
https://www.nijumaru-drill.com/word-problems.html""",

    """💡 算数嫌いになる一番の原因

「わからないまま次に進んでしまうこと」です。
小学校の算数は完全に積み上げ式。
1つでもつまずきを放置すると連鎖します。

#算数 #小学生 #勉強法 #にじゅうまるドリル
https://www.nijumaru-drill.com/math-anxiety.html""",

    """🧠 暗算が速くなる練習法

計算問題をただ解くより「10の補数」を体に染み込ませると激変。
8+?=10 → 2、7+?=10 → 3、これを瞬時に言えるまで練習！

#算数 #暗算 #計算力 #にじゅうまるドリル
https://www.nijumaru-drill.com/mental-math.html""",

    """✅ 計算ミスを減らす3つの習慣

1. 答えを書いたら必ず見直す（1問ずつ）
2. 筆算は丁寧に大きく書く
3. 繰り上がり・繰り下がりを小さく書いておく

これだけで正答率が大きく変わります！

#算数 #計算ミス #小学生 #にじゅうまるドリル
https://www.nijumaru-drill.com/no-mistakes.html""",

    """📊 割合が苦手な子へ

「もとにする量」「比べる量」「割合」の3つを
表に整理するだけで急に解けるようになります。

公式を丸暗記するより関係性を理解するのが近道！

#算数 #割合 #小学5年生 #にじゅうまるドリル
https://www.nijumaru-drill.com/percentage-guide.html""",

    """📅 算数が得意な子の共通点

毎日10分でもドリルをやっていること。
週1回2時間より毎日10分の方が圧倒的に定着します。

「習慣化」こそが算数上達の最短ルートです。

#算数 #勉強習慣 #小学生 #にじゅうまるドリル
https://www.nijumaru-drill.com/study-habits.html""",

    """➗ 割り算をわかりやすく教えるコツ

「12÷3」を「12個のお菓子を3人で分けると何個ずつ？」
に変換するだけで子どもの理解が一気に深まります。

具体的な場面に結びつけることが大切！

#算数 #割り算 #小学生 #にじゅうまるドリル
https://www.nijumaru-drill.com/division-guide.html""",

    """🔢 小数の計算でよくあるミス

小数点の位置を間違えるのが一番多いです。
0.3×4＝1.2 を 0.3×4＝12 にしてしまうケース。

「0.1がいくつ分か」で考えると間違えにくくなります！

#算数 #小数 #小学生 #にじゅうまるドリル
https://www.nijumaru-drill.com/decimal-fraction-guide.html""",
]

ARTICLE_POST_TEMPLATE = """📚 新記事を公開しました！

{title}

{description}

無料で使える算数ドリルはこちら👇
{url}

#算数 #小学生 #無料ドリル #にじゅうまるドリル"""

# 最新記事情報（GitHub Actionsで記事公開時に更新）
LATEST_ARTICLES = [
    {
        "title": "たし算の完全ガイド【小学1年生〜3年生】",
        "description": "繰り上がりのあるたし算を図解でわかりやすく解説。つまずきポイントと克服法も紹介。",
        "url": "https://www.nijumaru-drill.com/addition-guide.html"
    },
    {
        "title": "円周の求め方【小学6年生】面積・体積・角度も完全攻略",
        "description": "円周＝直径×3.14の意味から図形全般まで。苦手な子向けの攻略法を解説。",
        "url": "https://www.nijumaru-drill.com/geometry-guide.html"
    },
]


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ {CONFIG_FILE} が見つかりません")
        print("x_config.json を作成してAPIキーを設定してください")
        return None
    with open(CONFIG_FILE) as f:
        return json.load(f)


def load_post_log():
    if os.path.exists(POST_LOG_FILE):
        with open(POST_LOG_FILE) as f:
            return json.load(f)
    return {"posted_tips": [], "last_article_post": None}


def save_post_log(log):
    with open(POST_LOG_FILE, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def post_tweet(text, config):
    """X API v2 でツイートを投稿 (tweepy使用)"""
    client = tweepy.Client(
        consumer_key=config["api_key"],
        consumer_secret=config["api_secret"],
        access_token=config["access_token"],
        access_token_secret=config["access_token_secret"]
    )
    try:
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        print(f"✅ 投稿成功！ https://x.com/i/web/status/{tweet_id}")
        return tweet_id
    except tweepy.TweepyException as e:
        print(f"❌ 投稿失敗: {e}")
        return None


def post_tips(config, dry_run=False):
    """算数TipsをランダムにX投稿"""
    log = load_post_log()
    posted = set(log.get("posted_tips", []))

    # まだ投稿していないTipsから選ぶ
    unposted = [i for i in range(len(TIPS_POSTS)) if i not in posted]
    if not unposted:
        # 全部投稿済みならリセット
        print("🔄 全Tips投稿済み。リセットして最初から")
        posted = set()
        unposted = list(range(len(TIPS_POSTS)))
        log["posted_tips"] = []

    idx = random.choice(unposted)
    text = TIPS_POSTS[idx]

    print(f"📝 投稿予定 (Tips #{idx+1}/{len(TIPS_POSTS)}):")
    print("-" * 40)
    print(text)
    print("-" * 40)

    if dry_run:
        print("🧪 テストモード: 実際には投稿しません")
        return

    tweet_id = post_tweet(text, config)
    if tweet_id:
        log["posted_tips"].append(idx)
        log["last_post_date"] = str(datetime.date.today())
        save_post_log(log)


def post_article(config, dry_run=False):
    """最新記事をX投稿"""
    log = load_post_log()
    last = log.get("last_article_post")

    # 直近7日以内に記事投稿済みならスキップ
    if last:
        days_since = (datetime.date.today() - datetime.date.fromisoformat(last)).days
        if days_since < 7:
            print(f"⏭️ 前回の記事投稿から{days_since}日。スキップします")
            # 代わりにTipsを投稿
            post_tips(config, dry_run)
            return

    article = random.choice(LATEST_ARTICLES)
    text = ARTICLE_POST_TEMPLATE.format(
        title=article["title"],
        description=article["description"],
        url=article["url"]
    )

    print(f"📚 記事投稿予定:")
    print("-" * 40)
    print(text)
    print("-" * 40)

    if dry_run:
        print("🧪 テストモード: 実際には投稿しません")
        return

    tweet_id = post_tweet(text, config)
    if tweet_id:
        log["last_article_post"] = str(datetime.date.today())
        save_post_log(log)


def main():
    parser = argparse.ArgumentParser(description="X 自動投稿スクリプト")
    parser.add_argument("--type", choices=["tips", "article", "test"], default="tips",
                        help="投稿タイプ: tips(算数Tips), article(記事紹介), test(テスト)")
    args = parser.parse_args()

    if args.type == "test":
        print("🧪 テストモード")
        post_tips(config=None, dry_run=True)
        return

    config = load_config()
    if not config:
        return

    if args.type == "article":
        post_article(config)
    else:
        post_tips(config)


def generate_buffer_posts():
    """Buffer用に今週の投稿テキストを一括生成"""
    log = load_post_log()
    posted = set(log.get("posted_tips", []))
    unposted = [i for i in range(len(TIPS_POSTS)) if i not in posted]
    if not unposted:
        posted = set()
        unposted = list(range(len(TIPS_POSTS)))

    print("=" * 50)
    print("📋 Buffer用 投稿テキスト（コピーして貼り付け）")
    print("=" * 50)
    # 今週分2件を出力
    for i, idx in enumerate(unposted[:2]):
        print(f"\n【投稿{i+1}】")
        print("-" * 40)
        print(TIPS_POSTS[idx])
        print("-" * 40)

    print("\n✅ buffer.com でスケジュール設定してください")
    print("推奨時間: 火曜・金曜 20:00〜21:00")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--buffer":
        generate_buffer_posts()
    else:
        main()
