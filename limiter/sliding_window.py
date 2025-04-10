from .base import BaseRateLimiter 
import time 
from redis_client import redis_client



class SlidingWindow(BaseRateLimiter):
    def __init__(self , limit: int,window_seconds:int):
        self.limit = limit
        self.window_seconds = window_seconds
    def is_allowed(self, client_id):
        key = f"rate:sw:{client_id}"
        now = time.time()
        window_start = now - self.window_seconds
        redis_client.zremrangebyscore(key, 0, window_start)
        count = redis_client.zcard(key)
        if count>= self.limit:
            return False
                
        redis_client.zadd(key, {str(now): now})
        redis_client.expire(key, self.window_seconds)
        return True