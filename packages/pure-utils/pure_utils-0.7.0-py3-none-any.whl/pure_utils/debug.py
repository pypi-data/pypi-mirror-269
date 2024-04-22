"""Utilities for debugging and development."""

from copy import deepcopy
from functools import wraps
from inspect import stack
from logging import Logger
from time import time
from typing import Any, Callable, Optional, TypeAlias

from pure_utils._internal._profile_stats_serializers import (
    ProfileStatsStringSerializer,
    SerializedProfileStatsT,
)
from pure_utils.profiler import Profiler

__all__ = ["around", "caller", "deltatime", "profileit"]

AnyCallableT: TypeAlias = Callable[[Any], Any]

DEFAULT_STACK_SIZE: int = 20
DEFAULT_STACK_FRAME: int = 2


def around(*, before: Optional[Callable] = None, after: Optional[Callable] = None) -> Callable:
    """Add additional behavior before and after execution of decorated function.

    Args:
        before: A reference to afunction/method that must be executed
                BEFORE calling the decorated function.
        after: A reference to afunction/method that must be executed
               AFTER calling the decorated function.

    The decorator highlights additional memory for data exchange
    capabilities between before and after handlers.

    This memory is transferred in the form of additional parameter ("_pipe")
    in the kwargs named argument dictionary.

    Raises:
        ValueError: If one of the handlers (`before`, `after`) is not specified.

    Example::

        from pure_utils.debug import around

        def before_handler(*args, **kwargs):
            kwargs["_pipe"]["key"] = "some data (from before to after handlers)"
            print("before!")

        def after_handler(*args, **kwargs):
            print(f"after: {kwargs['_pipe']['key']} !")

        @around(before=before_handler, after=after_handler)
        def func():
            print("in da func")

        func()
        >>> before!
        >>> in da func
        >>> after: some data (from before to after handlers) !

        # !!! Use around with only BEFORE handler !!!
        @around(before=before_handler)
        def func2():
            print("in da func2")
        >>> before!
        >>> in da func2

        # !!! Use around with only AFTER handler !!!
        @around(after=after_handler)
        def func3():
            print("in da func3")
        >>> after!
        >>> in da func3
    """

    def decorate(func) -> AnyCallableT:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not before and not after:
                raise ValueError(
                    "One of the handlers (`before`, `after`) is not specified. Read the doc - "
                    "https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.around"
                )

            _buffer = {}
            _args, _kwargs = (deepcopy(args), kwargs.copy())

            if before:
                before(*_args, _pipe=_buffer, **_kwargs)

            result = func(*args, **kwargs)

            if after:
                after(*_args, _pipe=_buffer, **_kwargs)

            return result

        return wrapper

    return decorate


def caller(*, at_frame: int = DEFAULT_STACK_FRAME) -> str:
    """Get the name of calling function/method (from current function/method context).

    Args:
        at_frame: The frame index number on the call stack (default 2).
                  Need increased with each wrap to decorator.

    Returns:
        The name of calling function/method.

    Example::

        from pure_utils.debug import caller

        def func1(*args, **kwargs):
            print(f"I'am 'func1', '{caller()}' called me.")

        def func2(*args, **kwargs):
            return func1()

        func2()
        >>> I'am 'func1', 'func2' called me.
    """
    return str(stack()[at_frame].function)


def deltatime(*, logger: Optional[Logger] = None) -> Callable:
    """Measure execution time of decorated function and print it to log.

    Args:
        logger: Optional logger object for printing execution time to file.

    Example::

        from pure_utils.debug import deltatime

        @deltatime()
        def aim_func():
            for _ in range(1, 1000_000):
                ...

        result, delta = aim_func()
        print(f"Execution time of aim_func: {delta} sec.")
        >>> Execution time of aim_func: 0.025 sec.

        # !!! Or use decorator with logger (side effect) !!!

        from logging import getLogger, DEBUG, basicConfig
        basicConfig(level=DEBUG)

        @deltatime(logger=getLogger())
        def aim_func2():
            for _ in range(1, 1000_000):
                ...

        result, _ = aim_func2()
        >>> DEBUG:root:[DELTATIME]: 'aim_func2' (0.025 sec.)
    """

    def decorate(func) -> AnyCallableT:
        @wraps(func)
        def wrapper(*args, **kwargs) -> tuple[Any, float]:
            t0 = time()
            retval = func(*args, **kwargs)
            delta = float(f"{time() - t0:.3f}")
            if logger:
                logger.log(
                    msg=f"[DELTATIME]: '{func.__name__}' ({delta} sec.)",
                    level=logger.level,
                )
            return retval, delta

        return wrapper

    return decorate


def profileit(*, logger: Optional[Logger] = None, stack_size: int = DEFAULT_STACK_SIZE) -> Callable:
    """Profile decorated function being with 'cProfile'.

    Args:
        logger: Optional logger object for printing execution time to file.
        stack_size: Stack size limit for profiler results.

    Example::

        from pure_utils.debug import profileit

        def func1():
            ...

        def func2():
            func1()

        def func3():
            func2()

        @profileit()
        def func4():
            func3()

        _, profile_info = func4()
        print(profile_info)

        5 function calls in 0.000 seconds
           Ordered by: cumulative time, function name
           ncalls  tottime  percall  cumtime  percall filename:lineno(function)
              1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
              1    0.000    0.000    0.000    0.000 scriptname.py:13(func4)
              1    0.000    0.000    0.000    0.000 scriptname.py:10(func3)
              1    0.000    0.000    0.000    0.000 scriptname.py:7(func2)
              1    0.000    0.000    0.000    0.000 scriptname.py:4(func1)
        <pstats.Stats object at 0x10cf1a390>

        # !!! Or use decorator with logger (side effect) !!!

        from logging import getLogger, DEBUG, basicConfig
        basicConfig(level=DEBUG)

        @profileit(logger=getLogger())
        def func4():
            func3()

        func4()
    """

    def decorate(func) -> AnyCallableT:
        @wraps(func)
        def wrapper(*args, **kwargs) -> tuple[Any, SerializedProfileStatsT]:
            retval = None
            profiler = Profiler()

            try:
                retval = profiler.profile(func, *args, **kwargs)
            finally:
                profiler_stats = profiler.serialize_result(
                    serializer=ProfileStatsStringSerializer, stack_size=stack_size
                )

            if logger:
                logger.log(msg=f"[PROFILEIT]: {str(profiler_stats)}", level=logger.level)

            return retval, profiler_stats

        return wrapper

    return decorate
