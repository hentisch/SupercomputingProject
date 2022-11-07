import requests

class TwitterAPI:

    def get_field_string(fields:dict):
        if len(list(fields)) > 0:
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

    def get_user_tweets(self, user_id:int, extra_fields = {}):
        fields = {"tweet.fields": "public_metrics", "max_results": '100', "tweet.fields": "public_metrics"} | extra_fields
        return requests.get(headers=self.auth_header,
        url=f"https://api.twitter.com/2/users/{user_id}/tweets" + TwitterAPI.get_field_string(fields))
    
    def get_user_id(self, username:str, extra_fields = {}):
        response = requests.get(headers=self.auth_header,
        url=f"https://api.twitter.com/2/users/by/username/{username}" + TwitterAPI.get_field_string(extra_fields))

        return int(response.json()["data"]["id"])
