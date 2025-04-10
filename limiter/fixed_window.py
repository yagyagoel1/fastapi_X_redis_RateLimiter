
import time 
from .base import  BaseRateLimiter
from redis_client import redis_client

class FixedWindow(BaseRateLimiter):
    def __init__(self , limit: int,window_seconds:int):
        self.limit = limit
        self.window_seconds = window_seconds
    
    def is_allowed(self,client_id:str)-> bool:
        current_window=int(time.time()// self.window_seconds)
        key= f"rate:{client_id}:{current_window}"
        count  = redis_client.incr(key)
        if count == 1:
            redis_client.expire(key,self.window_seconds)
        return self.limit>=count
            