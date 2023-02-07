import time

class RateLimit:
    def __init__(self, num_requests:int) -> None:
        self.num_requests = num_requests
        self.current_window = time.time() // 60*15
        self.current_requests = 0
    
    def make_request(self):
        current_window = time.time() // 60*15
        if current_window > self.current_window:
            self.current_window = current_window
            self.current_requests = 0
        self.current_requests += 1
        if self.current_requests < self.num_requests:
            return
        else:
            next_window_time = (current_window+1)*60*15
            time.sleep(time.time()-next_window_time)