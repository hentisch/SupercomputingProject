import requests

class TwitterAPI:

    api_link = "https://api.twitter.com/2/" 

    def get_field_string(fields:dict):
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

    def get_user_tweets(self, user_id:int, extra_fields = {}):
        fields = {"tweet.fields": ["public_metrics", "conversation_id", "in_reply_to_user_id", "author_id"], "max_results": '100'} | extra_fields
        return requests.get(headers=self.auth_header,
        url=self.get_url(f"users/{user_id}/tweets", fields))
    
    def get_user_id(self, username:str, extra_fields = {}):
        response = requests.get(headers=self.auth_header,
        url=self.get_url(f"users/by/username/{username}", extra_fields))
        return int(response.json()["data"]["id"])

    def get_tweet_responses(self, conversation_id:int, extra_fields = {}):
        fields = {"query": f"conversation_id:{conversation_id}"}
        return requests.get(headers=self.auth_header, url=self.get_url("/2/tweets/search/recent", fields))