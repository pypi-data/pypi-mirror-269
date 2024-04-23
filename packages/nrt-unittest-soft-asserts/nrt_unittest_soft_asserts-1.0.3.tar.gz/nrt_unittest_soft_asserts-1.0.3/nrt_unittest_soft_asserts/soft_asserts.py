import threading
import unittest
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Failure:
    assertion_error: AssertionError
    step: str


class SoftAsserts(unittest.TestCase):
    _failures: list[Failure] = []
    _logger = None
    _print_method: Optional[Callable] = None
    _current_step_map: dict[str, str] = {}
    _failure_steps_map: dict[str, list[str]] = {}
    _steps_lock: threading.Lock = threading.Lock()

    _is_use_steps: bool = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def soft_assert_true(self, condition, message=None) -> bool:
        try:
            self.assertTrue(condition, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_false(self, condition, message=None) -> bool:
        try:
            self.assertFalse(condition, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_equal(self, first, second, message=None) -> bool:
        try:
            self.assertEqual(first, second, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_not_equal(self, first, second, message=None) -> bool:
        try:
            self.assertNotEqual(first, second, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_is(self, first, second, message=None) -> bool:
        try:
            self.assertIs(first, second, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_is_not(self, first, second, message=None) -> bool:
        try:
            self.assertIsNot(first, second, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_is_none(self, obj, message=None) -> bool:
        try:
            self.assertIsNone(obj, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_is_not_none(self, obj, message=None) -> bool:
        try:
            self.assertIsNotNone(obj, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_in(self, obj, container, message=None) -> bool:
        try:
            self.assertIn(obj, container, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_not_in(self, obj, container, message=None) -> bool:
        try:
            self.assertNotIn(obj, container, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_is_instance(self, obj, cls, message=None) -> bool:
        try:
            self.assertIsInstance(obj, cls, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_not_is_instance(self, obj, cls, message=None) -> bool:
        try:
            self.assertNotIsInstance(obj, cls, message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_almost_equal(self, first, second, delta, message=None) -> bool:
        try:
            self.assertAlmostEqual(first=first, second=second, delta=delta, msg=message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_not_almost_equal(self, first, second, delta, message=None) -> bool:
        try:
            self.assertNotAlmostEqual(
                first=first, second=second, delta=delta, msg=message)
        except AssertionError as e:
            self.__append_to_failures(e)
            return False

        return True

    def soft_assert_raises(self, exception, method: Callable, *args, **kwargs) -> bool:
        try:
            method(*args, **kwargs)
            error = f'{exception} not raised'
            self.__append_to_failures(AssertionError(error))
            return False
        except Exception as e:
            if not isinstance(e, exception):
                error = f'{e} is not instance of {exception}'
                self.__append_to_failures(AssertionError(error))
                return False

        return True

    def soft_assert_raises_with(self, exception, message=None):
        class AssertRaises:
            __exception = None
            __append_to_failures: Callable = None

            def __init__(self, e, append_to_failures: Callable):
                self.__exception = e
                self.__append_to_failures = append_to_failures

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                if exc_type is None:
                    error = message or f'{self.__exception} not raised'
                    self.__append_to_failures(AssertionError(error))
                elif exc_type != self.__exception:
                    error = message or f'{exc_type} is not type of {self.__exception}'
                    self.__append_to_failures(AssertionError(error))

                return True

        return AssertRaises(exception, self.__append_to_failures)

    def soft_assert_all(self):
        """
        Soft asserts all the asserts that were called
        since the last call to soft_assert_all.

        Raises AssertionError if any of the asserts failed.
        :return:
        """

        self.unset_step()

        if self.failures:
            failures = self.failures.copy()
            self._failures.clear()

            if self._is_use_steps:
                with SoftAsserts._steps_lock:
                    SoftAsserts._failure_steps_map[self.__class__.__name__] = \
                        list(dict.fromkeys(
                                [failure.step for failure in failures
                                 if failure.step is not None]))

            raise AssertionError(
                '\n'.join([str(failure.assertion_error) for failure in failures]))

    def is_step_in_failure_steps(self, step: str) -> bool:
        return step in self.failure_steps

    @property
    def failures(self):
        return self._failures

    @property
    def failure_steps(self):
        with SoftAsserts._steps_lock:
            return SoftAsserts._failure_steps_map.get(self.__class__.__name__) or []

    def __append_to_failures(self, assertion_error: AssertionError):
        with SoftAsserts._steps_lock:
            self._failures.append(
                Failure(assertion_error,
                        SoftAsserts._current_step_map.get(self.__class__.__name__)))
        self.__print_error_to_log(assertion_error)

    def __print_error_to_log(self, assertion_error):
        self.__validate_params()

        if self._print_method:
            self._print_method(str(assertion_error))
        elif self._logger:
            self._logger.error(str(assertion_error))

    def __validate_params(self):
        if self._logger and self._print_method:
            raise ValueError('Cannot set both logger and print_method')

    @classmethod
    def init_failure_steps(cls):
        SoftAsserts._failure_steps_map[cls.__name__] = []

    @classmethod
    def set_step(cls, step: str):
        with SoftAsserts._steps_lock:
            SoftAsserts._is_use_steps = True
        SoftAsserts._current_step_map[cls.__name__] = step

    @classmethod
    def unset_step(cls):
        with SoftAsserts._steps_lock:
            if SoftAsserts._current_step_map.get(cls.__name__):
                SoftAsserts._current_step_map.pop(cls.__name__)

    @classmethod
    def set_logger(cls, logger):
        cls._logger = logger

    @classmethod
    def unset_logger(cls):
        cls._logger = None

    @classmethod
    def set_print_method(cls, print_method: Callable):
        cls._print_method = print_method

    @classmethod
    def unset_print_method(cls):
        cls._print_method = None
