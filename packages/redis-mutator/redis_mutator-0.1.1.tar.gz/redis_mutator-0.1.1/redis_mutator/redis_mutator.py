from typing import Callable, Dict, List, Union
from redis import Redis


ORIGINAL_METHODS_KEY = "!original_methods"
MUTATIONS_KEY = "!mutations"


class RedisMutator:
    def __init__(
        self,
        redis: Redis,
        names: List[str],
        original_methods: Dict[str, Callable],
        mutations: Dict[str, Callable],
    ):
        self.__redis = redis
        self.__names = names
        self.__original_methods = original_methods
        self.__mutations = mutations

    def __override_method(
        self,
        name: str,
        method: Callable,
    ):
        if name not in self.__original_methods:
            self.__original_methods[name] = getattr(
                self.__redis,
                name,
            )

        self.__mutations[name] = method

        setattr(self.__redis, name, method)

    def use(self, mutation: Union[Redis, Callable]):
        """
        Mutate the selected methods to use
        the given Redis connection or callable.
        """
        is_redis = isinstance(mutation, Redis)

        for name in self.__names:
            if is_redis:
                self.__override_method(
                    name,
                    getattr(mutation, name),
                )
            else:
                self.__override_method(
                    name,
                    mutation,
                )

        return self

    def remove(self):
        """
        Remove mutations from these methods.
        """
        for name in self.__names:
            if name not in self.__original_methods:
                continue

            setattr(
                self.__redis,
                name,
                self.__original_methods[name],
            )

            del self.__original_methods[name]

        return self


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
