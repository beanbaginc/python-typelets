"""Typing useful for working with Django's JSON serialization.

Version Added:
    1.0
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Union
from uuid import UUID

from typing_extensions import TypeAlias

from typelets.django.strings import StrPromise
from typelets.json import (BaseSerializableJSONList,
                           BaseSerializableJSONListImmutable,
                           BaseSerializableJSONValue,
                           BaseSerializableJSONDict,
                           BaseSerializableJSONDictImmutable)


_SerializableJSONValueTypes: TypeAlias = Union[
    Decimal,
    StrPromise,
    UUID,
    date,
    datetime,
    time,
    timedelta,
]


#: A type indicating a valid value that can be serialized to JSON.
#:
#: These values are all supported in
#: :py:class:`~djblets.util.serializers.DjbletsJSONEncoder`.
#:
#: Version Added:
#:     4.0
SerializableDjangoJSONValue: TypeAlias = \
    BaseSerializableJSONValue[_SerializableJSONValueTypes]


#: A type for a dictionary mapping strings to JSON-serializable values.
#:
#: These values are all supported in
#: :py:class:`~djblets.util.serializers.DjbletsJSONEncoder`.
#:
#: Version Added:
#:     4.0
SerializableDjangoJSONDict: TypeAlias = \
    BaseSerializableJSONDict[_SerializableJSONValueTypes]


#: An immutable type mapping strings to JSON-serializable values.
#:
#: This is an immutable version of :py:class:`SerializableJSONDict`, which
#: cannot be modified once set. It can help with type narrowing and is
#: recommended when returning data from a function that should not be changed.
#:
#: These values are all supported in
#: :py:class:`~djblets.util.serializers.DjbletsJSONEncoder`.
#:
#: Version Added:
#:     4.0
SerializableDjangoJSONDictImmutable: TypeAlias = \
    BaseSerializableJSONDictImmutable[_SerializableJSONValueTypes]


#: A type for a list of JSON-serializable values.
#:
#: These values are all supported in
#: :py:class:`~djblets.util.serializers.DjbletsJSONEncoder`.
#:
#: Version Added:
#:     4.0
SerializableDjangoJSONList: TypeAlias = \
    BaseSerializableJSONList[_SerializableJSONValueTypes]


#: An immutable type of a list of JSON-serializable values.
#:
#: This is an immutable version of :py:class:`SerializableJSONList`, which
#: cannot be modified once set. It can help with type narrowing and is
#: recommended when returning data from a function that should not be changed.
#:
#: These values are all supported in
#: :py:class:`~djblets.util.serializers.DjbletsJSONEncoder`.
#:
#: Version Added:
#:     4.0
SerializableDjangoJSONListImmutable: TypeAlias = \
    BaseSerializableJSONListImmutable[_SerializableJSONValueTypes]
