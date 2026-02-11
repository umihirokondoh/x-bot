import os
import sqlite3
import requests
import tweepy
import random
import re

# 設定
DB_PATH = "posted.db"

def get_clients():
    """API v1.1(画像用)とv2(投稿用)の両方のクライアントを返す"""
    auth = tweepy.OAuth1UserHandler(
        os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_SECRET"]
    )
    api_v1 = tweepy.API(auth)
    
    client_v2 = tweepy.Client(
        bearer_token=os.environ["X_BEARER_TOKEN"],
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_SECRET"]
    )
    return api_v1, client_v2

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS posted_tweets (tweet_id TEXT PRIMARY KEY)")
    conn.commit()
    conn.close()

def is_already_posted(tweet_id):
    conn = sqlite3.connect(DB_PATH)
    res = conn.execute("SELECT 1 FROM posted_tweets WHERE tweet_id = ?", (tweet_id,)).fetchone()
    conn.close()
    return res is not None

def mark_as_posted(tweet_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO posted_tweets (tweet_id) VALUES (?)", (tweet_id,))
    conn.commit()
    conn.close()

def main():
    api_v1, client_v2 = get_clients()
    user_id = os.environ["X_USER_ID"]
    init_db()

    # 1. 過去のツイートを取得
    response = client_v2.get_users_tweets(
        id=user_id,
        max_results=50,
        expansions=["attachments.media_keys"],
        media_fields=["url", "type"],
        tweet_fields=["text", "created_at"]
    )

    if not response or not response.data:
        print("ツイートが見つかりませんでした。")
        return

    # メディア情報のマッピング
    media_map = {m.media_key: m for m in response.includes.get("media", [])} if response.includes else {}

    # 2. 画像付き かつ 未投稿 のツイートを抽出
    candidates = []
    for t in response.data:
