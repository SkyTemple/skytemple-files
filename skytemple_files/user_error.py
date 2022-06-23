"""
This module provides utilities to mark exceptions as 'User errors'. These errors should be handled like normal
but not be treated or reported as bugs.
"""

from __future__ import annotations

# User errors have this attribute defined.
from typing import Type, TypeVar

USER_ERROR_MARK = "_skytemple__user_error"

T = TypeVar("T", bound=BaseException)


class UserValueError(ValueError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        setattr(self, USER_ERROR_MARK, True)


def mark_as_user_err(exc: BaseException):
    """
    This marks an error as a user error, provided the exception supports it. Silently fails if it doesn't.
    Consider using make_user_err instead.
    """
    try:
        setattr(exc, USER_ERROR_MARK, True)
    except Exception:
        pass


def make_user_err(base_type: Type[T], *args, **kwargs) -> T:
    """Dynamically creates a new subclass of base_type which is marked as a user error and constructs it."""
    cls = type(base_type.__name__ + "User", (base_type,), {USER_ERROR_MARK: True})

    return cls(*args, **kwargs)
