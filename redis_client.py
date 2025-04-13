import os
import redis

# Should use the environment variables provided in docker-compose.yaml
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

# Create Redis client
redis_client = redis.Redis(host=redis_host, port=redis_port)