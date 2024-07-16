"""Common symbols useful for functions, variables, and types.

Version Added:
    1.0
"""

from __future__ import annotations

from enum import Enum
from typing import TypeVar, Union

from typing_extensions import Final, Literal, TypeAlias


_T = TypeVar('_T')


class UnsetSymbol(Enum):
    """A type indicating an unsettable value.

    This can be useful in functions that take default values to distinguish
    between a value not provided and a ``False``/``None`` value.

    Version Added:
        1.0
    """

    UNSET = '<UNSET>'


#: An instance of a symbol indicating an unset value.
#:
#: Version Added:
#:     1.0
UNSET: Final[Literal[UnsetSymbol.UNSET]] = UnsetSymbol.UNSET


#: A generic type alias for marking a type as unsettable.
#:
#: This allows for usage like:
#:
#: .. code-block:: python
#:
#:    def __init__(
#:        self,
#:        value: Unsettable[str],
#:    ) -> None:
#:        ...
#:
#: Version Added:
#:     1.0
Unsettable: TypeAlias = Union[Literal[UnsetSymbol.UNSET], _T]
