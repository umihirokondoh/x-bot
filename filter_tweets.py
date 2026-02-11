def filter_image_tweets(tweets, includes):
    image_tweets = []

    # メディア情報がそもそも含まれていない場合は空リストを返す
    if not includes or "media" not in includes:
        return []

    # メディア情報の中から「画像(photo)」の media_key だけをリスト化する
    photo_keys = [
        m.media_key for m in includes["media"] 
        if getattr(m, 'type', None) == "photo"
    ]

    for t in tweets:
        # ツイートに添付ファイル(attachments)があるか確認
        attachments = getattr(t, 'attachments', None)
        if not attachments or "media_keys" not in attachments:
            continue

        # ツイートの media_keys の中に、画像(photo)の key が含まれているか判定
        tweet_media_keys = attachments["media_keys"]
        for mk in tweet_media_keys:
            if mk in photo_keys:
                image_tweets.append(t)
                break

    return image_tweets
