import collections

import twitter_api
import tweet

class GetAuthorTweet:
    def __init__(self, author_id:int, api:twitter_api.TwitterAPI) -> None:
        self.author_id = author_id
        self.api = api
    
    def get_tweets(self, pagination_token:str=None, other_fields:dict={}):
        if pagination_token == None:
            fields = other_fields
        else:
            fields = {"pagination_token": pagination_token} | other_fields
        
        return self.api.get_user_tweets(self.author_id, extra_fields=fields)

    def get_stream(author_id:int, api:twitter_api.TwitterAPI) -> None:
        return TweetStream(GetAuthorTweet(author_id, api))

class GetTweetResponses:
    def __init__(self, conversation_id:int, api:twitter_api.TwitterAPI) -> None:
        self.conversation_id = conversation_id
        self.api = api

    def get_tweets(self, pagination_token:str=None, other_fields:dict = {}):
        if pagination_token == None:
            fields = other_fields
        else:
            fields = {"next_token": pagination_token} | other_fields
        
        return self.api.get_tweet_responses(self.conversation_id, extra_fields=fields)
    
    def get_stream(conversation_id:int, api:twitter_api.TwitterAPI) -> None:
        return TweetStream(GetTweetResponses(conversation_id, api))

class TweetStream:
    def __init__(self, tweet_get:object) -> None:
        self.tweet_get = tweet_get
        self.posts = collections.deque()
        self.pagination_token = None

        self.more_pagination = True
    
    def __iter__(self):
        return self

    def _get_tweet_object(self):
        return tweet.Tweet.from_json(self.posts.popleft())

    def __next__(self):
        try:
            return self._get_tweet_object()
        except IndexError:
            if not self.more_pagination:
                raise StopIteration
            
            api_response = self.tweet_get.get_tweets(pagination_token=self.pagination_token, other_fields={"max_results": "100"})
            
            try:
                posts = api_response.json()['data']
            except KeyError:
                raise StopIteration

            try:
                self.pagination_token = api_response.json()['meta']['next_token']
            except KeyError:
                self.more_pagination = False

            self.posts.extend(posts)

            return self._get_tweet_object()