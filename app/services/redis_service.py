from __future__ import annotations

import json
from typing import Any, Optional

import redis
from redis.exceptions import RedisError

from app.config import settings


class RedisService:
    def __init__(self) -> None:
        self.client = redis.Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except RedisError:
            return False

    def set_value(self, key: str, value: str) -> bool:
        try:
            return bool(self.client.set(key, value))
        except RedisError:
            return False

    def get_value(self, key: str) -> Optional[str]:
        try:
            return self.client.get(key)
        except RedisError:
            return None

    def set_json(self, key: str, value: dict[str, Any]) -> bool:
        try:
            return bool(self.client.set(key, json.dumps(value)))
        except RedisError:
            return False

    def get_json(self, key: str) -> Optional[dict[str, Any]]:
        try:
            raw = self.client.get(key)
            return json.loads(raw) if raw else None
        except (RedisError, json.JSONDecodeError):
            return None
        
    def push_event(self, stream_name: str, data: dict[str, Any]) -> Optional[str]:
        try:
            return self.client.xadd(stream_name, data)
        except RedisError:
            return None 


redis_service = RedisService()
