from fetch_tweets import fetch_my_tweets
from filter_tweets import filter_image_tweets
from select_tweet import select_random
from post_tweet import post
from db import init_db, already_posted, mark_posted

def main():
    init_db()

    tweets = fetch_my_tweets(max_results=100)
    image_tweets = filter_image_tweets(tweets)

    candidate = select_random(image_tweets)

    if not candidate:
        print("対象ツイートなし")
        return

    if already_posted(candidate["id"]):
        print("すでに投稿済み:", candidate["id"])
        return

    post(candidate["text"])
    mark_posted(candidate["id"])
    print("投稿完了:", candidate["id"])

if __name__ == "__main__":
    main()
