import requests
import time

class TwitterAPI:

    api_link = "https://api.twitter.com/2/" 
    tweet_fields = ["public_metrics", "conversation_id", "in_reply_to_user_id", "author_id"]

    def get_field_string(fields:dict):
        """ A specially formatted string of fields to append to a Twitter API endpoint 
        
        Paramaters 
        ----------
        fields : dict
            A dictonary representing each field to be formatted

        Returns
        -------
        str
            A formatted string of fields
        """
        
        if len(list(fields)) == 0:
            return ''
        
        field_str = "?"
        
        for i, field in enumerate(fields):
            field_str += field + "="

            field_value = fields[field]

            if type(field_value) == str:
                field_str += field_value
            else:
                field_str += ','.join(field_value)
            
            if i < len(fields)-1:
                field_str += '&'
        
        return field_str
    
    def get_url(self, endpoint:str, fields:dict):
        field_str = TwitterAPI.get_field_string(fields)
        return f"{self.api_link}{endpoint}{field_str}"

    def __init__(self, bearer_token:str) -> None:
        self.bearer_token = bearer_token
        self.auth_header = {"Authorization": f"Bearer {self.bearer_token}"}
        # self.get_user_tweet_limit = RateLimit(1500-30)
        # self.get_user_id_limit = RateLimit(300-30)
        # self.get_responses_limit = RateLimit(300-30)

    def get_user_tweets(self, user_id:int, extra_fields = {}) -> requests.Response:
        """ The tweet history of a particular user in the raw form returned by the Twitter API
        
        Paramaters
        ----------
        user_id : int
            The user_id of the specified user
        extra_fields : dict, optional
            Any extra fields to be added to the URL of the reuqest. Fields in this will override the methods default fields.

        Returns
        -------
        requests.Response
            The raw response from the Twitter API
        """
        # print("user tweets")
        fields = {"tweet.fields": self.tweet_fields, "max_results": '100'} | extra_fields
        while True:
            response = requests.get(headers=self.auth_header,
            url=self.get_url(f"users/{user_id}/tweets", fields))
            if response.status_code != 429:
                return response
            else:
                time.sleep(60)
    
    def get_user_id(self, username:str, extra_fields = {}) -> requests.Response:
        """ The user id of the Twitter user with the specified username
        
        Paramaters
        ----------
        username : str
            Twitter Username of the specified user
        extra_fields : dict
            Any extra fields to be added to the URL of the reuqest. Fields in this will override the methods default fields.

        Returns
        -------
        requests.Response
            The raw response from the Twitter API    
        """
        while True:
            response = requests.get(headers=self.auth_header,
            url=self.get_url(f"users/by/username/{username}", extra_fields))
            if response.status_code != 429:
                return int(response.json()["data"]["id"])
            else:
                time.sleep(60)


    def get_tweet_responses(self, conversation_id:int, extra_fields = {}):
        """ The responses of a particular tweet
        
        Paramaters 
        ----------
        conversation_id : int
            The converation ID of the Tweet to retrive the responses of
        extra_fields : dict
            Any extra fields to tbe added to the URL of the request. Fields in this will override the methods default fields. 
            
        Returns
        -------
        requests.Response
            The raw response from the Twitter API """
    
        fields = {"query": f"conversation_id:{conversation_id}", "tweet.fields": self.tweet_fields}
        while True:
            response = requests.get(headers=self.auth_header, url=self.get_url("tweets/search/recent", fields))
            if response.status_code != 429:
                return response
            else:
                time.sleep(60)