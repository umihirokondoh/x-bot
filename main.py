import os
import tweepy
from filter_tweets import filter_image_tweets

def main():
    bearer_token = os.environ["X_BEARER_TOKEN"]
    api_key = os.environ["X_API_KEY"]
    api_secret = os.environ["X_API_SECRET"]
    access_token = os.environ["X_ACCESS_TOKEN"]
    access_token_secret = os.environ["X_ACCESS_SECRET"]
    user_id = os.environ["X_USER_ID"]

    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # 修正ポイント: expansions と media_fields を追加して画像データを取得可能にする
    response = client.get_users_tweets(
        id=user_id, 
        max_results=10,
        expansions=["attachments.media_keys"],
        media_fields=["type"]
    )

    tweets = response.data
    includes = response.includes

    if not tweets:
        print("ツイートが見つかりませんでした。")
        return

    # 修正ポイント: メディア詳細情報(includes)も一緒に渡す
    image_tweets = filter_image_tweets(tweets, includes)

    if not image_tweets:
        print("画像付きツイートはありませんでした。")
        return

    for t in image_tweets:
        try:
            client.retweet(t.id)
            print(f"Retweeted tweet ID: {t.id}")
        except Exception as e:
            print(f"Error retweeting {t.id}: {e}")

if __name__ == "__main__":
    main()
