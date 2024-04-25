from typing import Callable, Dict, List, Union
from redis import Redis

BASE_KEY = "!redis_mutator_"
WRAPPED_KEY = f"{BASE_KEY}wrapped"
MUTATIONS_KEY = f"{BASE_KEY}mutations"
PREFIXES_KEY = f"{BASE_KEY}prefixes"
POSTFIXES_KEY = f"{BASE_KEY}postfixes"


class RedisMutator:
    def __init__(
        self,
        redis: Redis,
        names: List[str],
        wrapped: Dict[str, bool],
        mutations: Dict[str, Callable],
        prefixes: Dict[str, List[Callable]],
        postfixes: Dict[str, List[Callable]],
    ):
        self.__redis = redis
        self.__names = names
        self.__wrapped = wrapped
        self.__mutations = mutations
        self.__prefixes = prefixes
        self.__postfixes = postfixes

        for name in names:
            if name not in self.__wrapped:
                self.__wrapped[name] = True

                self.__wrap(name)

    def __wrap(self, name: str):
        raw = getattr(self.__redis, name)

        def wrapper(*args, **kwargs):
            if name in self.__prefixes:
                for hook in self.__prefixes[name]:
                    hook(*args, **kwargs)

            value = None

            if name in self.__mutations:
                value = self.__mutations[name](*args, **kwargs)
            else:
                value = raw(*args, **kwargs)

            if name in self.__postfixes:
                for hook in self.__postfixes:
                    for hook in self.__postfixes[name]:
                        hook(value, args, kwargs)

            return value

        setattr(self.__redis, name, wrapper)

    def prefix(self, hook: Callable):
        for name in self.__names:
            if name not in self.__prefixes:
                self.__prefixes[name] = []

            self.__prefixes[name].append(hook)

        return self

    def postfix(self, hook: Callable):
        for name in self.__names:
            if name not in self.__postfixes:
                self.__postfixes[name] = []

            self.__postfixes[name].append(hook)

        return self

    def use(self, mutation: Union[Redis, Callable]):
        """
        Mutate the selected methods to use
        the given Redis connection or callable.
        """
        is_redis = isinstance(mutation, Redis)

        for name in self.__names:
            if is_redis:
                self.__mutations[name] = getattr(mutation, name)
            else:
                self.__mutations[name] = mutation

        return self

    def remove_postfix(self, callable: Callable):
        for name in self.__names:
            if name not in self.__postfixes:
                continue

            self.__postfixes[name].remove(callable)

        return self

    def remove_prefix(self, callable: Callable):
        for name in self.__names:
            if name not in self.__prefixes:
                continue

            self.__prefixes[name].remove(callable)

        return self

    def remove(self):
        """
        Remove mutations from these methods.
        """
        for name in self.__names:
            if name in self.__mutations:
                del self.__mutations[name]

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
