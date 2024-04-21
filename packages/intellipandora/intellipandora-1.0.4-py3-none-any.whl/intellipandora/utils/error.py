# -*- coding: utf-8 -*-
# @Author: Shao Feng
# @File  : error.py
# @Time  : 2024-04-17
class IntelliPandoraError(Exception):
    """Base class for IntelliPandora Framework errors.

    Do not raise this method but use more specific errors instead.
    """

    def __init__(self, message='', details=''):
        super().__init__(message)
        self.details = details

    @property
    def message(self):
        return str(self)


class FrameworkError(IntelliPandoraError):
    """Can be used when the core framework goes to unexpected state.

    It is good to explicitly raise a FrameworkError if some framework
    component is used incorrectly. This is pretty much same as
    'Internal Error' and should of course never happen.
    """


class DataError(IntelliPandoraError):
    """Used when the provided test data is invalid.

    DataErrors are not caught by keywords that run other keywords
    (e.g. `Run Keyword And Expect Error`).
    """


class VariableError(DataError):
    """Used when variable does not exist.

    VariableErrors are caught by keywords that run other keywords
    (e.g. `Run Keyword And Expect Error`).
    """


class TimeoutError(IntelliPandoraError):
    """Used when a test or keyword timeout occurs.

    This exception is handled specially so that execution of the
    current test is always stopped immediately and it is not caught by
    keywords executing other keywords (e.g. `Run Keyword And Expect Error`).
    """

    def __init__(self, message='', test_timeout=True):
        super().__init__(message)
        self.test_timeout = test_timeout

    @property
    def keyword_timeout(self):
        return not self.test_timeout
