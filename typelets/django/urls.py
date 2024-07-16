"""Typing useful for working with Django URL registration.

Version Added:
    1.0
"""

from __future__ import annotations

from typing import Union

from django.urls.resolvers import URLPattern, URLResolver
from typing_extensions import TypeAlias


#: Type alias for either a URL pattern or a URL resolver.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        url_pattern: AnyURL = path('/', my_view)
#:        url_resolver: AnyURL = path('/', include(...))
AnyURL: TypeAlias = Union[URLPattern, URLResolver]
