"""Typing useful for Django authentication.

Version Added:
    1.0
"""

from __future__ import annotations

from typing import Union

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from typing_extensions import TypeAlias


#: Type alias for a logged-in user or an anonymous user.
AnyUser: TypeAlias = Union[AbstractBaseUser, AnonymousUser]
