"""Typing useful for working with Django strings.

Version Added:
    1.0
"""

from __future__ import annotations

from typing import NewType, TYPE_CHECKING, Union
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from django.utils.functional import _StrOrPromise, _StrPromise
else:
    from django.utils.functional import Promise

    # The main reason we're using NewType here is to avoid Sphinx thinking
    # this is an attribute during doc generation. At runtime here, NewType()
    # will just return Promise.
    _StrPromise: TypeAlias = NewType('StrPromise', Promise)
    _StrOrPromise: TypeAlias = Union[str, _StrPromise]


#: A type indicating a Unicode string or lazily-localized string.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:         s1: StrOrPromise = gettext_lazy('...')
#:         s2: StrOrPromise = gettext('...')
#:         s3: StrOrPromise = '...'
StrOrPromise: TypeAlias = _StrOrPromise


#: A type indicating a lazily-localized string.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:         s: StrOrPromise = gettext_lazy('...')
StrPromise: TypeAlias = _StrPromise
