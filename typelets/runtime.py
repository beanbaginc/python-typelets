"""Utility for asserting never types with more flexibility.

Version Added:
    1.1
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Never


def raise_invalid_type(
    value: Never,
    message: str,
    exception_type: type[Exception] = ValueError,
) -> Never:
    """Raise an exception far an invalid type.

    In many cases, especially for public APIs, we want runtime checking for
    argument types as well as type checking. This method can be used as a type
    guard in those cases where that code would be flagged by the type checkers
    as unreachable.

    This works similarly to :py:func:`typing.assert_never`, but allows
    customization of the exception type and message, since
    :py:class:`AssertionError` is not great from an API standpoint.

    Version Added:
        1.1

    Args:
        value (object):
            The value which was not of a usable type.

        message (str):
            The message to use for the exception.

        exception_type (type, optional):
            The exception type to raise.

    Raises:
        Exception:
            This method always raises an exception.
    """
    raise exception_type(message)
