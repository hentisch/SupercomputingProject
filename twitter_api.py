import requests

class TwitterAPI:

    def get_field_string(fields:dict):
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

    def __init__(self, bearer_token:str) -> None:
        self.bearer_token = bearer_token
        self.auth_header = {"Authorization": f"Bearer {self.bearer_token}"}

    def get_tweet(self, tweet_id:int):
        return requests.get(headers=self.auth_header,
        url=f"https://api.twitter.com/labs/2/tweets/{tweet_id}?expansions=attachments.media_keys&tweet.fields=created_at,author_id,lang,source,public_metrics,context_annotations,entities")

    def get_user_tweets(self, user_id:int):
        return requests.get(headers=self.auth_header,
        url=f"https://api.twitter.com/2/users/{user_id}/tweets?tweet.fields=public_metrics")
    
    def get_user_id(self, username:str):
        response = requests.get(headers=self.auth_header,
        url=f"https://api.twitter.com/2/users/by/username/{username}")

        return int(response.json()["data"]["id"])