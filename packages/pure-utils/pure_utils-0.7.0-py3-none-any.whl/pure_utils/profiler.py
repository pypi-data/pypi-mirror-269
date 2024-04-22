"""Helper classes for working with the cProfile."""

from cProfile import Profile
from typing import Callable, ParamSpec, Type, TypeVar

from pure_utils._internal._profile_stats import ProfileStats
from pure_utils._internal._profile_stats_serializers import (
    ProfileStatsSerializer,
    SerializedProfileStatsT,
)

__all__ = ["Profiler"]


T = TypeVar("T")
P = ParamSpec("P")


class Profiler:
    """A class provides a simple interface for profiling code.

    Example::

        from pure_utils.profiler import Profiler

        profiler = Profiler()
        some_function_retval = profiler.profile(some_func, *func_args, **func_kwargs)
        profile_result = profiler.serialize_result(SomeProfilerStatsSerializer)
    """

    __slots__ = ("_profile", "__weakref__")

    def __init__(self) -> None:
        """Initialize profiler object."""
        self._profile = Profile()

    @property
    def pstats(self) -> ProfileStats:
        """Get raw profile stats."""
        return ProfileStats(self._profile).strip_dirs().sort_stats("cumulative", "name")

    def profile(self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        """Profile function.

        Args:
            func: Function for profiling
            *args: Profiling function positional arguments.
            **kwargs: Profiling function named arguments.

        Return:
            Native profiling function return value.
        """
        return self._profile.runcall(func, *args, **kwargs)

    def serialize_result(
        self, *, serializer: Type[ProfileStatsSerializer], stack_size: int
    ) -> SerializedProfileStatsT:
        """Serialize profiler result with custom serializer class.

        Args:
            serializer: Serializer class.
            stack_size: Stack size for limitation

        Returns:
            Serialized profiler result.
        """
        return serializer(self.pstats, stack_size).serialize()
