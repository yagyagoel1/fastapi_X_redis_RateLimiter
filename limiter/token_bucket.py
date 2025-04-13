from .base import BaseRateLimiter
from redis_client import redis_client
import time

class TokenBucketLimiter(BaseRateLimiter):
    def __init__(self, tokens, refill_rate):
        self.tokens = tokens
        self.refill_rate = refill_rate
        
    def is_allowed(self, client_id):
        key = f"key:tb:{client_id}"
        now = time.time()
        data = redis_client.hgetall(key)
        
        if not data:
            redis_client.hset(key, mapping={"tokens": int(self.tokens), "last_refill": now})
            return True
        
        if isinstance(next(iter(data.keys()), ''), bytes):
            data = {k.decode('utf-8'): v.decode('utf-8') if isinstance(v, bytes) else v 
                   for k, v in data.items()}
            
        try:
            tokens = int(data['tokens'])
            last_refill = float(data['last_refill'])
        except (KeyError, ValueError):
            redis_client.hset(key, mapping={"tokens": int(self.tokens), "last_refill": now})
            return True

        elapsed = now - last_refill
        new_tokens = int(elapsed // self.refill_rate)
        tokens = min(self.tokens, tokens + new_tokens)

        if tokens > 0:
            tokens -= 1
            redis_client.hset(key, mapping={'tokens': tokens, 'last_refill': now})
            return True
        else:
            return False