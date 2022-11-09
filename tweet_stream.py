import collections
import twitter_api

class GetAuthorTweet:
    def __init__(self, author_id:int, api:twitter_api.TwitterAPI) -> None:
        self.author_id = author_id
        self.api = api
    
    def get_tweets(self, fields:dict):
        return self.api.get_user_tweets(self.author_id, extra_fields=fields)

class TweetStream:
    def __init__(self, tweet_get:object) -> None:
        self.tweet_get = tweet_get
        self.posts = collections.deque()
        self.pagination_token = None

        self.more_pagination = True
    
    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.posts.popleft()
        except IndexError:
            if not self.more_pagination:
                raise StopIteration
            
            if self.pagination_token == None:
                fields = {"max_results": "5"}
            else:
                fields = {"pagination_token": self.pagination_token, "max_results": "5"}
            
            api_response = self.tweet_get.get_tweets(fields)
            
            try:
                posts = api_response.json()['data']
            except KeyError:
                raise StopIteration

            try:
                self.pagination_token = api_response.json()['meta']['next_token']
            except KeyError:
                self.more_pagination = False

            self.posts.extend(posts)

            return self.posts.popleft()