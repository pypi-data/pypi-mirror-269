from abc import ABC, abstractmethod
from typing import Awaitable, Callable


class Resource(ABC):
    @property
    @abstractmethod
    def active(self) -> bool:
        ...

    @abstractmethod
    def usages(self) -> int:
        ...

    @abstractmethod
    def start(self) -> Awaitable[None] | None:
        ...

    @abstractmethod
    def stop(self) -> Awaitable[None] | None:
        ...


type ResourceStartFn[T] = Callable[[T], Awaitable[None] | None]
type ResourceStopFn[T] = Callable[[T], Awaitable[None] | None]
type ResourceActivityFn[T] = Callable[[T], bool]
type ResourceUsageFn[T] = Callable[[T], int]


class ResourceAdapter[T](Resource):
    def __init__(
        self, obj: T, start_fn: ResourceStartFn, stop_fn: ResourceStopFn,
        activity_fn: ResourceActivityFn, usage_fn: ResourceUsageFn,
    ):
        self._obj = obj
        self._start_fn = start_fn
        self._stop_fn = stop_fn
        self._activity_fn = activity_fn
        self._usage_fn = usage_fn

    @property
    def active(self) -> bool:
        return self._activity_fn(self._obj)

    def usages(self) -> int:
        return self._usage_fn(self._obj)

    def start(self) -> Awaitable[None] | None:
        return self._start_fn(self._obj)

    def stop(self) -> Awaitable[None] | None:
        return self._stop_fn(self._obj)


def make_resource[T](
    obj: T, start_fn: ResourceStartFn, stop_fn: ResourceStopFn,
    activity_fn: ResourceActivityFn, usage_fn: ResourceUsageFn,
) -> ResourceAdapter[T]:
    return ResourceAdapter[T](obj, start_fn, stop_fn, activity_fn, usage_fn)
