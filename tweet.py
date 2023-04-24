import tweet_stream
import twitter_api

class TweetMetrics:
    def __init__(self, retweet_count:int, reply_count:int, like_count:int, quote_count:int)-> None:
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.quote_count = quote_count

    def from_json(metrics:dict):
        return TweetMetrics(
            retweet_count=int(metrics["retweet_count"]),
            reply_count=int(metrics["reply_count"]),
            like_count=int(metrics["like_count"]),
            quote_count=int(metrics["quote_count"])
        )

class Tweet:
    def __init__(self, id:int, text:str, author_id:int, conversation_id:int, is_reply:bool, metrics:TweetMetrics) -> None:
        self.id = id
        self.text = text
        self.author_id = author_id
        self.conversation_id = conversation_id
        self.is_reply = is_reply
        self.metrics = metrics
    
    def from_json(tweet:dict, constant_information:dict={}):
        tweet_dict = tweet | constant_information
        try:
            is_reply = bool(tweet_dict["is_reply"])
        except KeyError:
            try:
                tweet_dict["in_reply_to_user_id"]
                is_reply = True
            except KeyError:
                is_reply = False
            
        return Tweet(id=int(tweet_dict["id"]),
        text=tweet_dict["text"],
        author_id=int(tweet_dict["author_id"]),
        conversation_id=int(tweet_dict['conversation_id']),
        is_reply=is_reply,
        metrics=TweetMetrics.from_json(tweet_dict["public_metrics"]))
    
    def get_response_stream(self, api:twitter_api.TwitterAPI):
        response_getter = tweet_stream.GetTweetResponses(self.conversation_id, api)
        return tweet_stream.TweetStream(response_getter)

    def get_dict(self, api, max_replies:int):
        response_stream = self.get_response_stream(api)
        replies = []
        for response in response_stream:
            if len(replies) >= max_replies:
                break
            else:
                replies.append(response)

        dict_resp = {"id": self.id, "author_id":self.author_id, "content": self.text,
        "likes": self.metrics.like_count, "retweets": self.metrics.retweet_count, 
        "quote_count":self.metrics.quote_count, "replies":self.metrics.reply_count}

        if len(replies) <= 0:
            return dict_resp
        else:
            dict_resp["responses"] = [resp.get_dict(api, 0) for resp in replies]
            return dict_resp