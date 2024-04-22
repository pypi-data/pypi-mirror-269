"""Utilities for working with data containers (lists, dictionaries, tuples, sets, etc.)."""

from typing import (
    Any,
    Generator,
    KeysView,
    Mapping,
    Optional,
    Sequence,
    TypeAlias,
    TypeVar,
)

__all__ = [
    "bisect",
    "first",
    "flatten",
    "get_or_else",
    "omit",
    "paginate",
    "pick",
    "symmdiff",
    "unpack",
]

T = TypeVar("T")
KeysT: TypeAlias = Sequence[T] | KeysView[T]


def bisect(collection: list[T], /) -> tuple[list[T], list[T]]:
    """Bisect the list into two parts/halves based on the number of elements.

    The function does not change the original collection.

    Args:
        collection: Source collection.

    Returns:
        A two-element tuple containing two lists: the first list represents the first half of the
        original collection, and the second list is the second half.

    Raises:
        AssertionError: If collection is empty.

    Example::

        from pure_utils.containers import bisect

        l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        first_half, second_half = bisect(l)
        print(first_half, second_half)
        >>> [1, 2, 3, 4, 5] [6, 7, 8, 9, 10, 11]
    """
    assert collection
    length = len(collection)
    return (collection[: length // 2], collection[length // 2 :])


def first(collection: Sequence[T], /) -> Optional[T]:
    """Get the value of the first element from a subscriptable collection.

    Args:
        collection: Subscriptable collection.

    Returns:
        The value of the first element of the collection, or None if there is none.

    Example::

        from pure_utils.containers import first

        seq = (1, 2, 3)
        print(first(seq))
        >>> 1

        seq = []
        print(first(seq))
        >>> None
    """
    return next((_ for _ in collection), None)


def flatten(collection: Sequence[T], /) -> Generator[Sequence[T] | T, None, None]:
    """Make the subscriptable collection a flat (single nesting level).

    Args:
        collection: Subscriptable collection to flatten.

    Returns:
        Generator of the flatten function.

    Example::

        from pure_utils.containers import flatten

        seq = [[1], [2], [3], [4], [5]]
        result = list(flatten(seq))
        print(result)
        >>> [1, 2, 3, 4, 5]

        seq = [[[[[[1]]]]], [[[[[2]]]]], [[[[[3]]]]], [[[[[4]]]]], [[[[[5]]]]]]
        result = list(flatten(seq))
        print(result)
        >>> [1, 2, 3, 4, 5]
    """
    if isinstance(collection, (list, tuple, set)):
        for _ in collection:
            yield from flatten(_)
    else:
        yield collection


def get_or_else(collection: Sequence[T], index: int, default: Optional[T] = None, /) -> Optional[T]:
    """Get value of element, and if it is missing, return the default value.

    Used for safety to get the value of a collection element.

    Args:
        collection: Collection of homogeneous elements.
        index: Index of the collection element to get the value.
        default: Optional default value, returned when no element at the specified index.

    Returns:
        The value of the sequence element at the specified index,
        or default value, when no element by this index.

    Example::

        from pure_utils.containers import get_or_else

        seq = (1, 2, 3)
        print(get_or_else(seq, 0))
        >>> 1
        print(get_or_else(seq, 3))
        >>> None
        print(get_or_else(seq, 3, -1))
        >>> -1

        seq = ["a", "b", "c"]
        print(get_or_else(seq, 3, "does not exists"))
        >>> does not exists
    """
    try:
        return collection[index]
    except IndexError:
        return default


def symmdiff(s1: KeysT, s2: KeysT, /) -> Sequence[T]:
    """Obtain the symmetric difference of two sequences.

    Args:
        s1: The first sequence to form a set on the LEFT.
        s2: The second sequence to form a set on the RIGHT.

    Returns:
        The symmetric difference of two sequences as a list.

    Example::

         from pure_utils.containers import symmdiff

         s1 = ["a", "b", "c"]
         s2 = ["e", "b", "a"]
         result = symmdiff(s1, s2)
         print(result)
         >>> ["c", "e"]
    """
    return list(set(s1).symmetric_difference(set(s2)))


def omit(container: Mapping[str, Any], keys: KeysT, /) -> Mapping[str, Any]:
    """Omit key-value pairs from the source dictionary, by keys sequence.

    The function does not modify the original collection.

    Args:
        container: Source data container.
        keys: A sequence of strings or keys() for omitted pairs in the source data container.

    Returns:
        A data container without omitted key-value pairs.

    Example::

        from pure_utils.containers import omit

        container = {"key1": "val1", "key2": "val2", "key3": "val3", "key4": "val4"}
        result = omit(container, ["key2", "key4"] )
        print(result)
        >>> {"key1": "val1", "key3": "val3"}
    """
    keys_diff: KeysT = symmdiff(container.keys(), keys)
    return {_: container[_] for _ in keys_diff if _ in container}


def paginate(collection: Sequence[T], /, *, size: int) -> Sequence[Sequence[T]]:
    """Split the collection into page(s), limited by size.

    The function does not modify the original collection.

    Args:
        collection: Collection of homogeneous elements.
        size: Page size of elements in one page.

    Returns:
        A collection with elements splitted into pages (nested collections).

    Raises:
        AssertionError: If size is less than zero.

    Example::

        from pure_utils.containers import paginate

        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pages = paginate(a, size=3)
        print(pages)
        >>> [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    """
    assert size > 0
    return [collection[start : start + size] for start in range(0, len(collection), size)]


def pick(container: Mapping[str, Any], keys: KeysT, /) -> Mapping[str, Any]:
    """Pick key-value pairs from the source dictionary, by keys sequence.

    All other dictionary values will be omitted.

    The function does not modify the original collection.

    Args:
        container: Source data container.
        keys: A sequence of strings or keys() for pick pairs in the source data container.

    Returns:
        A new data container with picked key-value pairs.

    Example::

        from pure_utils.containers import pick

        container = {"key1": "val1", "key2": "val2", "key3": "val3"}
        result = pick(container, ["key2", "key3"])
        print(result)
        >>> {"key2": "val2", "key3": "val3"}
    """
    return {_: container[_] for _ in keys if _ in container}


def unpack(container: Mapping[str, Any], attributes: KeysT, /) -> tuple[Any, ...]:
    """Unpack the values of container object into separate variables.

    Args:
        container: Source data container.
        attributes: A sequence of strings or keys() whose values need to be unpacked.

    Returns:
        A tuple of unpacked values of the specified attributes.

    Example::

        from pure_utils.containers import unpack

        # Unpack existent attributes
        d = {"a": 1, "b": True, "c": {"d": "test"}}
        a, b = unpack(d, ("a", "b"))
        print(a, b, sep=", ")
        >>> 1, True

        # Unpack non-existent attributes
        e, f = print(unpack(d, ("e", "f")))
        print(e, f, sep=", ")
        >>> None, None

        class A:
            def __init__(self):
                self.a = 100
                self.b = 200
                self.c = 300

        # Unpack object attributes
        obj = A()
        a, b, c = unpack(obj, ("a", "b", "c"))
        print(a, b, c, sep=", ")
        >>> 100, 200, 300
    """
    if isinstance(container, dict):
        return tuple(container.get(attr) for attr in attributes)

    unpacked_values = []

    for attr in attributes:
        try:
            unpacked_values.append(getattr(container, attr))
        except AttributeError:
            unpacked_values.append(None)

    return tuple(unpacked_values)
