"""Typing useful for Django models.

Version Added:
    1.0
"""

from __future__ import annotations

from typing import Any

from typing_extensions import TypeAlias


#: Type alias for a primary key.
#:
#: Django primary keys default to :py:class:`~typing.Any`, which doesn't
#: particularly help code stay readable.
#:
#: This type can be used instead to specifically document a type as being any
#: compatible form of a model primary key.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        pk: ModelAnyPK = obj.pk
ModelAnyPK: TypeAlias = Any


#: Type alias for an int-based primary key.
#:
#: Django primary keys default to :py:class:`~typing.Any`, which doesn't
#: particularly help code stay readable. And sometimes a codebase knows that
#: it's only going to be working with integer-based primary keys.
#:
#: This type can be used instead to specifically document an integer-based
#: primary key for a model.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        pk: ModelIntPK = obj.pk
ModelIntPK: TypeAlias = int
