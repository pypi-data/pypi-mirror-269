from typing import List, Union
from redis import Redis
from .redis_mutator import RedisMutator


ORIGINAL_METHODS_KEY = "!original_methods"
MUTATIONS_KEY = "!mutations"


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
            ORIGINAL_METHODS_KEY,
            {},
        )
        setattr(
            redis,
            MUTATIONS_KEY,
            {},
        )

        pipeline_method = redis.pipeline

        def wrapper(*args, **kwargs):
            pipe = pipeline_method(*args, **kwargs)
            mutations = getattr(redis, MUTATIONS_KEY)

            for name, method in mutations.items():
                setattr(pipe, name, method)

            return pipe

        setattr(redis, "pipeline", wrapper)

    original_methods = getattr(redis, ORIGINAL_METHODS_KEY)
    mutations = getattr(redis, MUTATIONS_KEY)

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
        original_methods,
        mutations,
    )
