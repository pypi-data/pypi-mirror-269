from typing import List, Union
from redis import Redis
from .redis_mutator import RedisMutator


BASE_KEY = "!redis_mutator_"
WRAPPED_KEY = f"{BASE_KEY}wrapped"
MUTATIONS_KEY = f"{BASE_KEY}mutations"
PREFIXES_KEY = f"{BASE_KEY}prefixes"
POSTFIXES_KEY = f"{BASE_KEY}postfixes"


def mutate(
    redis: Redis,
    *names: Union[str, List[str]],
):
    """
    Mutate the given method names.
    """
    if not hasattr(redis, MUTATIONS_KEY):
        setattr(
            redis,
            WRAPPED_KEY,
            {},
        )
        setattr(
            redis,
            MUTATIONS_KEY,
            {},
        )
        setattr(
            redis,
            POSTFIXES_KEY,
            {},
        )
        setattr(
            redis,
            PREFIXES_KEY,
            {},
        )

    wrapped = getattr(redis, WRAPPED_KEY)
    mutations = getattr(redis, MUTATIONS_KEY)
    prefixes = getattr(redis, PREFIXES_KEY)
    postfixes = getattr(redis, POSTFIXES_KEY)

    flat_names = []

    for name in names:
        if isinstance(name, str):
            flat_names.append(name)
        else:
            for name0 in name:
                flat_names.append(name0)

    return RedisMutator(
        redis,
        flat_names,
        wrapped,
        mutations,
        prefixes,
        postfixes,
    )
