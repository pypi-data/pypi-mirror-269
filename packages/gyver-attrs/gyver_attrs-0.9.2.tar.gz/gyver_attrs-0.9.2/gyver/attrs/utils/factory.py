import typing
from collections.abc import Callable

from typing_extensions import ParamSpec, Self

P = ParamSpec('P')
T = typing.TypeVar('T')


class Factory(typing.Generic[P, T]):
    __slots__ = ('func',)
    func: Callable[P, T]

    def __new__(cls, func: Callable[P, T]) -> Self:
        # Using __new__ to avoid having nested Factory instances
        if isinstance(func, cls):
            return func

        instance = object.__new__(cls)
        instance.func = func
        return instance

    def __call__(self, *args: P.args, **kwds: P.kwargs) -> T:
        return self.func(*args, **kwds)

    @property
    def __name__(self):
        return self.func.__name__


def mark_factory(func: Callable[P, T]) -> Factory[P, T]:
    return Factory(func)


def is_factory_marked(obj: typing.Any) -> bool:
    return isinstance(obj, Factory)
