import pytest

from pure_utils.repeaters import (
    ExceptionBasedRepeater,
    PredicateBasedRepeater,
    RepeateError,
    repeat,
)


class TestExceptionBasedRepeater:
    def test_repeat_on_fail_with_default_params_and_custom_logger(self, mocker, fake_logger):
        @repeat(ExceptionBasedRepeater(exceptions=(Exception,), logger=fake_logger))
        def some_repeatable_func():
            raise Exception("some error")

        sleep_mock = mocker.patch("pure_utils.repeaters.sleep")

        # Expect RepeateError exception when function calls are exhausted
        with pytest.raises(RepeateError):
            some_repeatable_func()

        assert sleep_mock.call_count == 3
        sleep_mock.assert_has_calls([mocker.call(1), mocker.call(2), mocker.call(3)])

    def test_repeat_on_fail_with_custom_params_and_without_logger(self, mocker):
        @repeat(ExceptionBasedRepeater(exceptions=(Exception,), attempts=5, interval=1))
        def some_repeatable_func():
            raise Exception("some error")

        sleep_mock = mocker.patch("pure_utils.repeaters.sleep")

        # Expect RepeateError exception when function calls are exhausted
        with pytest.raises(RepeateError):
            some_repeatable_func()

        assert sleep_mock.call_count == 5
        sleep_mock.assert_has_calls(
            [mocker.call(1), mocker.call(2), mocker.call(3), mocker.call(4), mocker.call(5)]
        )

    def test_repeat_on_success(self, mocker):
        @repeat(ExceptionBasedRepeater(exceptions=(Exception,)))
        def some_repeatable_func():
            return "ok"

        sleep_mock = mocker.patch("pure_utils.repeaters.sleep")

        assert some_repeatable_func() == "ok"
        assert sleep_mock.call_count == 0


class TestPredicateBasedRepeater:
    def test_repeat_with_positive_predicate(self, mocker):
        @repeat(PredicateBasedRepeater(predicate=lambda x: x == "ok"))
        def some_repeatable_func():
            return "ok"

        sleep_mock = mocker.patch("pure_utils.repeaters.sleep")

        assert some_repeatable_func() == "ok"
        assert sleep_mock.call_count == 0

    def test_repeat_with_negative_predicate(self, mocker):
        @repeat(PredicateBasedRepeater(predicate=lambda x: x == "ok"))
        def some_repeatable_func():
            return "not ok"

        sleep_mock = mocker.patch("pure_utils.repeaters.sleep")

        # Expect RepeateError exception when function calls are exhausted
        with pytest.raises(RepeateError):
            some_repeatable_func()

        assert sleep_mock.call_count == 3
        sleep_mock.assert_has_calls([mocker.call(1), mocker.call(2), mocker.call(3)])
