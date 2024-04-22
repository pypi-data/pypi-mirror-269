# pure-utils

![Build Status](https://github.com/p3t3rbr0/py3-pure-utils/actions/workflows/ci.yaml/badge.svg?branch=master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pure-utils)
![PyPI Version](https://img.shields.io/pypi/v/pure-utils)
[![Code Coverage](https://codecov.io/gh/p3t3rbr0/py3-pure-utils/graph/badge.svg?token=283H0MAGUP)](https://codecov.io/gh/p3t3rbr0/py3-pure-utils)
[![Maintainability](https://api.codeclimate.com/v1/badges/14f70c48db708a419309/maintainability)](https://codeclimate.com/github/p3t3rbr0/py3-pure-utils/maintainability)

Yet another python utilities, with the goal of collecting useful bicycles and crutches in one place ;).

Main principles:

1. No third party dependencies (standart library only).
2. Mostly pure functions without side effects.
3. Interfaces with type annotations.
4. Comprehensive documentation with examples of use.
5. Full test coverage.

**For detail information read the [doc](https://p3t3rbr0.github.io/py3-pure-utils/)**.

# Available utilities

* [common](https://p3t3rbr0.github.io/py3-pure-utils/refs/common.html) - The common purpose utilities.
  * [Singleton](https://p3t3rbr0.github.io/py3-pure-utils/refs/common.html#common.Singleton) - A metaclass that implements the singleton pattern for inheritors.
* [containers](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html) - Utilities for working with data containers (lists, dictionaries, tuples, sets, etc.).
  * [bisect](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.bisect)(collection, /) - Bisect the list into two parts/halves based on the number of elements.
  * [first](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.first)(collection, /) - Get the value of the first element from a homogeneous collection.
  * [flatten](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.flatten)(collection, /) - Make the iterated collection a flat (single nesting level).
  * [get_or_else](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.bisect)(collection, index[, default]) - Get value of element, and if it is missing, return the default value.
  * [omit](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.omit)(container, keys, /) - Omit key-value pairs from the source dictionary, by keys sequence.
  * [paginate](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.paginate)(collection, /, *, size) - Split the collection into page(s) according to the specified limit.
  * [pick](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.pick)(container, keys, /) - Pick key-value pairs from the source dictionary, by keys sequence.
  * [symmdiff](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.symmdiff)(s1, s2, /) - Obtain the symmetric difference of two sequences.
  * [unpack](https://p3t3rbr0.github.io/py3-pure-utils/refs/containers.html#containers.unpack)(container, attributes, /) - Unpack the values of container object into separate variables.
* [debug](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html) - Utilities for debugging and development.
  * [around](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.around)(*[, before, after]) - Add additional behavior before and after execution of decorated function.
  * [caller](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.caller)(*[, at_frame]) - Get the name of calling function/method (from current function/method context).
  * [deltatime](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.deltatime)(*[, logger]) - Measure execution time of decorated function and print it to log.
  * [profileit](https://p3t3rbr0.github.io/py3-pure-utils/refs/debug.html#debug.profileit)(*[, logger, stack_size]) - Profile decorated function being with 'cProfile'.
* [profiler](https://p3t3rbr0.github.io/py3-pure-utils/refs/profiler.html) - Helper classes for working with the cProfile.
  * [Profiler](https://p3t3rbr0.github.io/py3-pure-utils/refs/profiler.html#profiler.Profiler) - A class provides a simple interface for profiling code.
* [repeaters](https://p3t3rbr0.github.io/py3-pure-utils/refs/repeaters.html) - Utilities for repeatedly execute custom logic.
  * [Repeater](https://p3t3rbr0.github.io/py3-pure-utils/refs/repeaters.html#repeaters.Repeater) - Base Repeater, implements a main logic, such as constructor and execute method.
  * [ExceptionBasedRepeater](https://p3t3rbr0.github.io/py3-pure-utils/refs/repeaters.html#repeaters.ExceptionBasedRepeater) - Repeater based on catching targeted exceptions.
  * [PredicateBasedRepeater](https://p3t3rbr0.github.io/py3-pure-utils/refs/repeaters.html#repeaters.PredicateBasedRepeater) - Repeater based on predicate function.
  * [repeat](https://p3t3rbr0.github.io/py3-pure-utils/refs/repeaters.html#repeaters.repeat)(repeater: Repeater) - Repeat wrapped function by `repeater` logic.
* [strings](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html) - Utilities for working with strings.
  * [genstr](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html#strings.genstr)([length, is_uppercase]) - Generate ASCII-string with random letters.
  * [gunzip](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html#strings.gzip)(compressed_string, /) - Compress string (or bytes string) with gzip compression level.
  * [gzip](https://p3t3rbr0.github.io/py3-pure-utils/refs/strings.html#strings.gunzip)(string, /, *[, level]) - Decompress bytes (earlier compressed with gzip) to string.
* [times](https://p3t3rbr0.github.io/py3-pure-utils/refs/times.html) - Utilities for working with datetime objects.
  * [apply_tz](https://p3t3rbr0.github.io/py3-pure-utils/refs/times.html#times.apply_tz)(dt[, tz]) - Apply timezone context to datetime object.
  * [iso2format](https://p3t3rbr0.github.io/py3-pure-utils/refs/times.html#times.iso2format)(isostr, fmt, /) - Convert ISO-8601 datetime string into a string of specified format.
  * [iso2dmy](https://p3t3rbr0.github.io/py3-pure-utils/refs/times.html#times.iso2dmy)(isostr, /) - Convert ISO-8601 datetime string into a string of DMY (DD.MM.YYYY) format.
  * [iso2ymd](https://p3t3rbr0.github.io/py3-pure-utils/refs/times.html#times.iso2ymd)(isostr, /) - Convert ISO-8601 datetime string into a string of YMD (YYYY-MM-DD) format.
  * [round_by](https://p3t3rbr0.github.io/py3-pure-utils/refs/times.html#times.round_by)(dt, /, *, boundary) - Round datetime, discarding excessive precision.

# License

MIT License.

Copyright (c) 2024 Peter Bro <p3t3rbr0@gmail.com || peter@peterbro.su>

See LICENSE file for more information.
