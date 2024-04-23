# Unittest soft asserts.

![PyPI](https://img.shields.io/pypi/v/nrt-unittest-soft-asserts?color=blueviolet&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nrt-unittest-soft-asserts?color=greens&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/nrt-unittest-soft-asserts?color=blue&style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dd/nrt-unittest-soft-asserts?style=plastic)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nrt-unittest-soft-asserts?color=yellow&style=plastic)
[![Coverage Status](https://coveralls.io/repos/github/etuzon/python-nrt-unittest-soft-asserts/badge.svg)](https://coveralls.io/github/etuzon/pytohn-nrt-unittest-soft-asserts)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/etuzon/python-nrt-unittest-soft-asserts?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/etuzon/python-nrt-unittest-soft-asserts?style=plastic)
[![DeepSource](https://app.deepsource.com/gh/etuzon/python-nrt-unittest-soft-asserts.svg/?label=active+issues&token=WQz2lXCAZSwv8ndUhX7E7IQH)](https://app.deepsource.com/gh/etuzon/python-nrt-unittest-soft-asserts/?ref=repository-badge)

### Supported asserts:

| Assert                                                           | Description                                                                                 | Example                                                                                                      | Return                                             |
|------------------------------------------------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| soft_assert_true(condition, message=None)                        | Verify that condition is True                                                               | self.soft_assert_true(a == b)                                                                                | True if assertion passes, False if assertion fails |
| soft_assert_false(condition, message=None)                       | Verify that condition is False                                                              | self.soft_assert_false(a == b)                                                                               | True if assertion passes, False if assertion fails |
| soft_assert_equal(first, second, message=None)                   | Verify that first is equal to second                                                        | self.soft_assert_equal(a, b)                                                                                 | True if assertion passes, False if assertion fails |
| soft_assert_not_equal(first, second, message=None)               | Verify that first is not equal to second                                                    | self.soft_assert_not_equal(a, b)                                                                             | True if assertion passes, False if assertion fails |
| soft_assert_is(first, second, message=None)                      | Verify that first and second are the same object                                            | self.soft_assert_is(a, b)                                                                                    | True if assertion passes, False if assertion fails |
| soft_assert_is_not(first, second, message=None)                  | Verify that first and second are not the same object                                        | self.soft_assert_is_not(a, b)                                                                                | True if assertion passes, False if assertion fails |
| soft_assert_is_none(obj, message=None)                           | Verify that obj is None                                                                     | self.soft_assert_is_none(a)                                                                                  | True if assertion passes, False if assertion fails |
| soft_assert_is_not_none(obj, message=None)                       | Verify that obj is not None                                                                 | self.soft_assert_is_not_none(a)                                                                              | True if assertion passes, False if assertion fails |
| soft_assert_in(obj, container, message=None)                     | Verify that obj is in container                                                             | self.soft_assert_in(a, [a, b, c])                                                                            | True if assertion passes, False if assertion fails |
| soft_assert_not_in(obj, container, message=None)                 | Verify that obj is not in container                                                         | self.soft_assert_not_in(a, [b, c])                                                                           | True if assertion passes, False if assertion fails |
| soft_assert_is_instance(obj, cls, message=None)                  | Verify that obj is instance of cls                                                          | self.soft_assert_is_instance(a, A)                                                                           | True if assertion passes, False if assertion fails |
| soft_assert_is_not_instance(obj, cls, message=None)              | Verify that obj is not instance of cls                                                      | self.soft_assert_is_not_instance(a, B)                                                                       | True if assertion passes, False if assertion fails |
| soft_assert_almost_equal(first, second, delta, message=None)     | Verify that first is almost equal to second<br/>and the different is equal or less to delta | self.soft_assert_almost_equal(1.001, 1.002, 0.1)                                                             | True if assertion passes, False if assertion fails |
| soft_assert_not_almost_equal(first, second, delta, message=None) | Verify that first is not almost equal to second<br/>and the different is more than delta    | self.soft_assert_not_almost_equal(1.001, 1.002, 0.0001)                                                      | True if assertion passes, False if assertion fails |
| soft_assert_raises(exception, method: Callable, *args, **kwargs) | Verify that method execution raise exception                                                | self.soft_assert_raises(TypeError, sum, 'a', 2)                                                              | True if assertion passes, False if assertion fails |
| soft_assert_raises_with(exception, message=None)                 | Verify that execution in 'with' block raise exception                                       | with self.soft_assert_raised_with(ValueError):<br/>&nbsp;&nbsp;&nbsp;&nbsp;raise ValueError(ERROR_MESSAGE_1) |                                                    |
                                                                                                                                                        

In the end of each test, the soft asserts will be verified and the test will be marked as failed if any of the asserts failed.<br/>
To verify the soft asserts in the middle of the test, call `self.soft_assert_all()`.<br/>
<br/>
soft_assert_all() will raise _AssertionError_ if any of the asserts failed.

<br/>

### Steps

Each testing section can be divided to steps. The meaning of this is that if one of the asserts in a step failed,<br/>
then the step will be entered to list of failure steps and next test can be skipped if it is depended on the failed step.<br/> 

#### Example:

To make test be skipped if step failed, a custom decorator should be created.

This is an example of such custom decorator, but user can create its own custom decorator.


```python
import functools
from nrt_unittest_soft_asserts.soft_asserts import SoftAsserts

# Custom decorator to skip test if one of the steps failed.
def skip_steps(skip_steps_list: list[str]):
    def decorator(test_method):
        @functools.wraps(test_method)
        def wrapper(self, *args, **kwargs):
            for step in skip_steps_list:
                if self.is_step_in_failure_steps(step):
                    self.skipTest(f'Skipped because step [{step}] failed.')
            return test_method(self, *args, **kwargs)

        return wrapper

    return decorator


class SoftAssertsExamplesTests(SoftAsserts):
    STEP_1 = 'step 1'
    STEP_2 = 'step 2'
    STEP_3 = 'step 3'
    
    def test_01_assert_with_steps_test_will_fail(self):
        self.set_step(self.STEP_1)
        # result is False
        result = self.soft_assert_true(False)

        self.set_step(self.STEP_2)
        self.soft_assert_true(False)

        # From this code section steps will not be attached to failure asserts
        self.unset_step()
        self.soft_assert_true(False)

        self.soft_assert_all()

    @skip_steps([STEP_1])
    def test_02_skip_if_step_1_fail(self):
        self.soft_assert_true(False)
        self.soft_assert_all()

    @skip_steps([STEP_2])
    def test_03_skip_if_step_2_fail(self):
        self.soft_assert_true(False)
        self.soft_assert_all()

    @skip_steps([STEP_1, STEP_2])
    def test_04_skip_if_step_1_or_step2_fail(self):
        self.soft_assert_true(False)
        self.soft_assert_all()

    @skip_steps([STEP_3])
    def test_05_skip_if_step_3_fail_will_not_be_skipped(self):
        """
        Test should not be skipped because {STEP_3} is not in failure steps.
        """
        # result is True
        result = self.soft_assert_true(True)
        self.soft_assert_all()
```

### Print error on each failed assert

Each assert failure can be printed.<br/>
This can be done by adding logger or by adding a print method.<br/><br/>

In case a logger will be added, then logger.error(message) will be used.<br/>

In case a print method will be added, then print_method(message) will be used.<br/></br>

_logger and print method cannot be added together._<br/><br/>

#### logger example:

```python
import logging
from nrt_unittest_soft_asserts.soft_asserts import SoftAsserts


class SoftAssertsWithLoggerTests(SoftAsserts):
    logger = logging.getLogger('test')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.set_logger(cls.logger)
        
    def test_assert_true_fail(self):
        i = 1
        j = 2
        # logger.error() will print messages to console for each assert that fails
        self.soft_assert_true(i + j == 5)
        self.soft_assert_equal(i, j, f'{i} is different from {j}')
        self.soft_assert_all()
```

#### print method example:

```python
from nrt_unittest_soft_asserts.soft_asserts import SoftAsserts

class SoftAssertsWithPrintMethodTests(SoftAsserts):
    
    def setUp(self):
        super().setUp()
        self.set_print_method(self.__print_message)

    def test_assert_true_fail(self):
        i = 1
        j = 2
        # self.__print_message() will print messages 
        # to console for each assert that fails
        self.soft_assert_true(i + j == 5)
        self.soft_assert_equal(i, j, f'{i} is different from {j}')
        self.soft_assert_all()
        
    def __print_message(self, msg):
            print()
```

Wiki: https://github.com/etuzon/python-nrt-unittest-soft-asserts/wiki