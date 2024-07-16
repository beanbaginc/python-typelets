"""Typing useful for defining and calling functions.

Version Added:
    1.0
"""

from __future__ import annotations

from typing import Any, Dict

from typing_extensions import TypeAlias


#: A type indicating a dictionary used for keyword arguments.
#:
#: Version Added:
#:     1.0
KwargsDict: TypeAlias = Dict[str, Any]
