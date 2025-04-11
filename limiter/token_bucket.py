from .base import BaseRateLimiter
from redis_client import redis_client
import  time

class TokenBucketLimiter(BaseRateLimiter):
    def __init__(self,tokens,refill_rate):
        self.tokens = tokens
        self.refill_rate = refill_rate
        
    
    def is_allowed(self, client_id):
        key = f"key:tb:{client_id}"
        now = time.time()
        data = redis_client.hgetall(key)
        tokens = int(data['tokens'])
        last_refill = float(data['last_refill'])

        now = time.time()
        elapsed = now - last_refill
        new_tokens = int(elapsed // self.refill_rate)
        tokens = min(self.tokens, tokens + new_tokens)

        if tokens > 0:
            tokens -= 1
            redis_client.hmset(key, {'tokens': tokens, 'last_refill': now})
            return True
        else:
            return False