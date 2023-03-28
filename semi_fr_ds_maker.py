import twitter_api
import tweet_stream
import json
from tqdm import tqdm

users = [
    "BarackObama",
    "elonmusk",
    "justinbieber",
    "katyperry",
    "rihanna",
    "Cristiano",
    "taylorswift13",
    "realDonaldTrump",
    "narendramodi",
    "ladygaga"
]

api = twitter_api.TwitterAPI("AAAAAAAAAAAAAAAAAAAAANmniwEAAAAA6E06JzvYoT%2F%2Fx8jI8Upe8Ckeq60%3DCp09FHixy8myxTq3ISh6npgVwKgc0T8vrhH7ofqCwMeiqjxbqe")
tweets = []

for user in tqdm(users):
    id = api.get_user_id(user)
    user_tweets = tweet_stream.GetAuthorTweet.get_stream(id, api)
    for tweet in user_tweets:
        tweet_dict = tweet.get_dict(api, 0)
        tweets.append(tweet_dict)
    with open("dataset.json", "w") as f:
        f.write(json.dumps(tweets))

with open("dataset.json", "w") as f:
    f.write(json.dumps(tweets))
