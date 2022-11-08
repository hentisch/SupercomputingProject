import collections
import twitter_api

class TweetStream:
    def __init__(self, api:twitter_api.TwitterAPI, user_id) -> None:
        self.api = api
        
        self.user_id = user_id
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
            
            api_response = self.api.get_user_tweets(self.user_id, extra_fields=fields)
            
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