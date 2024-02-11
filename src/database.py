import redis

from src.config import settings

redis_object = redis.Redis(host=settings.redis_host, port=settings.redis_port)
