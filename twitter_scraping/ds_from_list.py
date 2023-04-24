import twitter_api
import tweet_stream
import json
from tqdm import tqdm
import sys

with open(sys.argv[1], "r") as f:
    users = [user.strip() for user in f.readlines()]

api = twitter_api.TwitterAPI("AAAAAAAAAAAAAAAAAAAAANmniwEAAAAA6E06JzvYoT%2F%2Fx8jI8Upe8Ckeq60%3DCp09FHixy8myxTq3ISh6npgVwKgc0T8vrhH7ofqCwMeiqjxbqe")

try:
    with open("dataset.json", "r") as f:
    	tweets = json.load(f)
    	print("old tweets found and successfully loaded")
except FileNotFoundError:
    tweets = []
    

user_ids = set()
for tweet in tweets:
    user_ids.add(tweet["author_id"])

for user in tqdm(users):
    id = api.get_user_id(user)
    if id in user_ids:
    	continue
    user_tweets = tweet_stream.GetAuthorTweet.get_stream(id, api)
    for tweet in user_tweets:
        tweet_dict = tweet.get_dict(api, 0)
        tweets.append(tweet_dict)
    with open("dataset.json", "w") as f:
        f.write(json.dumps(tweets))

with open("dataset.json", "w") as f:
    f.write(json.dumps(tweets))
