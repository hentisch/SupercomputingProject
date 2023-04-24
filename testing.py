import tweet
import twitter_api
import tweet_stream

if __name__ == "__main__":
    api = twitter_api.TwitterAPI("AAAAAAAAAAAAAAAAAAAAANmniwEAAAAA6E06JzvYoT%2F%2Fx8jI8Upe8Ckeq60%3DCp09FHixy8myxTq3ISh6npgVwKgc0T8vrhH7ofqCwMeiqjxbqe")
    id = api.get_user_id("elonmusk")
    tweets = tweet_stream.GetAuthorTweet.get_stream(id, api)
    for t in tweets:
        print(t.text)
        print(t.get_dict(api, 1))
        