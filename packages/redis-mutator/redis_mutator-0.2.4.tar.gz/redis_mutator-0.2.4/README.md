# Redis Mutator
[GitHub](https://github.com/Llyme/redis-mutator)

Inject another Redis connection to your Redis connection!

# Installation
```sh
pip install redis-mutator
```

# Uses
1. Separate read-only functions to another Redis connection.
2. Log functions as you use them.

# How to Use
```py
from redis_mutator import mutate, READ_METHOD_NAMES
from redis import Redis

redis = Redis(...)
read_only_redis = Redis(...)
mutate(redis, READ_METHOD_NAMES).use(read_only_redis)

redis.sadd("hello", "world!") # Uses `redis`.
redis.smembers("hello") # Uses `read_only_redis`.
```

## Specify Method Names
```py
from redis_mutator import mutate
from redis import Redis

redis = Redis(...)
my_other_redis = Redis(...)
mutate(redis, "sadd", "spop").use(my_other_redis)

redis.sadd("hello", "world!") # Uses `my_other_redis`.
redis.spop("hello", 1) # Uses `my_other_redis`.

redis.hset("hello", "world", "hi") # Uses `redis`.
redis.hget("hello", "world") # Uses `redis`.
```

## Prefix & Postfix Hooks
```py
from redis_mutator import mutate
from redis import Redis

redis = Redis(...)
my_other_redis = Redis(...)

def prefix(*args, **kwargs):
    print('Prefix called.')

def postfix(value):
    print('Postfix called.')

mutate(redis, "sadd", "spop").prefix(prefix)
mutate(redis, "sadd", "spop").postfix(postfix)

redis.sadd("hello", "world!")
# Prefix called.
# `redis.sadd(...)`
# Postfix called.
```

## Override Methods
```py
from redis_mutator import mutate
from redis import Redis

redis = Redis(...)
my_other_redis = Redis(...)

def prefix(*args, **kwargs):
    print('Hi-jacked!')

    return False # Return `False` to stop the process.

mutate(redis, "sadd", "spop").prefix(prefix)

redis.sadd("hello", "world!") # Hi-jacked!
```