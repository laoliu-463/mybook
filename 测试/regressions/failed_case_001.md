# Redis 分布式锁代码片段

下面记录一个带正则反向引用的 Redis 分布式锁示例，用于回归验证代码块格式化不会再次触发替换异常。

```python
import re
import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=True)
LOCK_PATTERN = r"(lock:)(\\w+)\\2"

def acquire_lock(resource_id: str) -> bool:
    lock_key = f"lock:{resource_id}"
    if re.match(LOCK_PATTERN, lock_key):
        return bool(client.set(lock_key, "1", nx=True, ex=30))
    return False
```

- 需要人工检查分布式锁续期、时钟漂移与异常释放问题。
- 这类笔记应走代码类子代理，不应因为 `\\2` 触发失败。
