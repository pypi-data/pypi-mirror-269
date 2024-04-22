import pytest

from pure_utils.containers import (
    bisect,
    first,
    flatten,
    get_or_else,
    omit,
    paginate,
    pick,
    symmdiff,
    unpack,
)


class TestBisect:
    def test_on_non_empty_list(self):
        source_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        a, b = bisect(source_list)

        assert a == [1, 2, 3, 4, 5]
        assert b == [6, 7, 8, 9, 10, 11]

        # Source list not changed.
        assert source_list == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def test_on_empty_list(self):
        source_list = []

        with pytest.raises(AssertionError):
            bisect(source_list)

        assert source_list == []


class TestFirst:
    def test_on_non_empty_list(self):
        assert first([1, 2, 3]) == 1

    def test_on_non_empty_set(self):
        assert first(set([1, 2, 3])) == 1

    def test_on_non_empty_tuple(self):
        assert first((1, 2, 3)) == 1

    def test_on_empty_list(self):
        assert first([]) is None


class TestFlatten:
    def test_on_one_dimention_list_seequence(self):
        seq = [1, 2, 3, 4, 5]
        result = list(flatten(seq))

        assert result == [1, 2, 3, 4, 5]

    def test_on_one_dimention_set_seequence(self):
        seq = {1, 2, 3, 4, 5}
        result = set(flatten(seq))

        assert result == {1, 2, 3, 4, 5}

    def test_on_one_dimention_tuple_seequence(self):
        seq = (1, 2, 3, 4, 5)
        result = tuple(flatten(seq))

        assert result == (1, 2, 3, 4, 5)

    def test_on_two_dimention_list_seequence(self):
        seq = [[1], [2], [3], [4], [5]]
        result = list(flatten(seq))

        assert result == [1, 2, 3, 4, 5]

    def test_on_two_dimention_tuple_seequence(self):
        seq = ((1,), (2,), (3,), (4,), (5,))
        result = tuple(flatten(seq))

        assert result == (1, 2, 3, 4, 5)

    def test_on_multiple_dimention_list_seequence(self):
        seq = [[[[[[1]]]]], [[[[[2]]]]], [[[[[3]]]]], [[[[[4]]]]], [[[[[5]]]]]]
        result = list(flatten(seq))

        assert result == [1, 2, 3, 4, 5]

    def test_on_multiple_dimention_tuple_seequence(self):
        seq = (
            (((((1,),),),),),
            (((((2,),),),),),
            (((((3,),),),),),
            (((((4,),),),),),
            (((((5,),),),),),
        )
        result = tuple(flatten(seq))

        assert result == (1, 2, 3, 4, 5)


class TestGetOrElse:
    def test_regular_usage(self):
        seq = (1, 2, 3)
        assert get_or_else(seq, 0) == 1
        assert get_or_else(seq, 3) is None
        assert get_or_else(seq, 3, -1) == -1

        seq = ["a", "b", "c"]
        assert get_or_else(seq, 5, "does not exists") == "does not exists"


class TestSymmdiff:
    def test_on_two_lists(self):
        l1 = ["a", "b", "c"]
        l2 = ["e", "b", "a"]
        diff = symmdiff(l1, l2)

        assert sorted(diff) == ["c", "e"]

        # The original lists has not changed
        assert l1 == ["a", "b", "c"]
        assert l2 == ["e", "b", "a"]

    def test_on_two_tuples(self):
        t1 = ("a", "b", "c")
        t2 = ("e", "b", "a")
        diff = symmdiff(t1, t2)

        assert sorted(diff) == ["c", "e"]

    def test_on_two_sets(self):
        s1 = set(["a", "b", "c"])
        s2 = set(["e", "b", "a"])
        diff = symmdiff(s1, s2)

        assert sorted(diff) == ["c", "e"]


class TestOmit:
    def test_regular_usage(self):
        source_dict = {"key1": "val1", "key2": "val2"}
        dict_without_omittes_pairs = omit(source_dict, ["key1"])

        assert dict_without_omittes_pairs == {"key2": "val2"}

        # The original dictionary has not changed
        assert source_dict == {"key1": "val1", "key2": "val2"}


class TestPaginate:
    def test_on_list_with_odd_size(self):
        source_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pages = paginate(source_list, size=3)
        assert pages == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    def test_on_list_with_even_size(self):
        source_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        pages = paginate(source_list, size=5)
        assert pages == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]

    def test_on_list_with_signle_element(self):
        source_list = [1]
        pages = paginate(source_list, size=5)
        assert pages == [[1]]

    def test_on_empty_list(self):
        assert paginate([], size=2) == []

    def test_on_zero_size(self):
        with pytest.raises(AssertionError):
            paginate([1, 2], size=0)

    def test_on_negative_size(self):
        with pytest.raises(AssertionError):
            paginate([1, 2], size=-1)

    def test_on_tuple(self):
        source_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        pages = paginate(source_tuple, size=5)
        assert pages == [(1, 2, 3, 4, 5), (6, 7, 8, 9, 10)]


class TestPick:
    def test_on_existing_keys(self):
        source_dict = {"key1": "val1", "key2": "val2", "key3": "val3"}
        modified_dict = pick(source_dict, ["key2"])

        assert modified_dict == {"key2": "val2"}

        # The original dictionary has not changed
        assert source_dict == {"key1": "val1", "key2": "val2", "key3": "val3"}

    def test_on_not_existing_keys(self):
        source_dict = {"key1": "val1", "key2": "val2", "key3": "val3"}
        modified_dict = pick(source_dict, ["key4"])

        assert modified_dict == {}


class TestUnpack:
    def test_on_dict(self):
        d = {"a": 1, "b": True, "c": {"d": "test"}}
        a, b, c = unpack(d, ("a", "b", "c"))

        assert a == 1
        assert b is True
        assert c == {"d": "test"}

        # Unpack value by non-existent key
        (f,) = unpack(d, ("f",))
        assert f is None

    def test_on_object(self):
        class A:
            def __init__(self):
                self.a = 100
                self.b = 200
                self.c = 300

        obj = A()
        a, b, c = unpack(obj, ("a", "b", "c"))
        assert a == 100
        assert b == 200
        assert c == 300

        # Unpack value by non-existent attribute
        (d,) = unpack(obj, ("d"))
        assert d is None
