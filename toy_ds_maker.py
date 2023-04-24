import twitter_api
import tweet_stream
import json
from tqdm import tqdm

users = [
    "BarackObama",
    "elonmusk",
    "justinbieber",
    "katyperry",
    "rihanna"
]

api = twitter_api.TwitterAPI("AAAAAAAAAAAAAAAAAAAAANmniwEAAAAA6E06JzvYoT%2F%2Fx8jI8Upe8Ckeq60%3DCp09FHixy8myxTq3ISh6npgVwKgc0T8vrhH7ofqCwMeiqjxbqe")
tweets = []
tweets_per_user = 20
for user in users:
    id = api.get_user_id(user)
    user_tweets = tweet_stream.GetAuthorTweet.get_stream(id, api)

    n_tweets = 0
    pbar = tqdm(total=tweets_per_user)
    for tweet in user_tweets:
        if n_tweets < tweets_per_user:
            tweet_dict = tweet.get_dict(api, 100)
            tweets.append(tweet_dict)
            n_tweets += 1
            pbar.update(1)
        if n_tweets >= tweets_per_user:
            pbar.close()
            break
    
    with open("dataset.json", "w") as f:
        f.write(json.dumps(tweets))
