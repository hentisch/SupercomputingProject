class TweetMetrics:
    def __init__(self, retweet_count:int, reply_count:int, like_count:int, quote_count:int)-> None:
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.quote_count = quote_count

class Tweet:
    def __init__(self, id:int, text:str, author_id:int, conversation_id:str, metrics:TweetMetrics) -> None:
        self.id = id
        self.text = text
        self.author_id = author_id
        self.conversation_id = conversation_id
        self.metrics = metrics