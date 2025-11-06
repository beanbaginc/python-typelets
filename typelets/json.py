"""Typing useful for working with JSON structures.

Version Added:
    1.0
"""

from __future__ import annotations

from typing import Dict, List, Mapping, Sequence, TypeVar, Union

from typing_extensions import TypeAlias


_T = TypeVar('_T')


#: A type indicating a valid value in JSON data.
#:
#: All values are natively-supported JSON data. Custom serializers that
#: support more data types will need to add their own special type.
#:
#: Version Added:
#:     1.0
JSONValue: TypeAlias = Union[
    'JSONDict',
    'JSONDictImmutable',
    'JSONList',
    'JSONListImmutable',
    None,
    bool,
    float,
    int,
    str,
]


#: A type for a dictionary mapping strings to JSON values.
#:
#: All values are natively-supported JSON data.
#:
#: All values are natively-supported JSON data. Custom serializers that
#: support more data types will need to add their own special type.
#:
#: Version Added:
#:     1.0
JSONDict: TypeAlias = Dict[str, JSONValue]


#: An immutable type mapping strings to JSON values.
#:
#: This is an immutable version of :py:class:`JSONDict`, which cannot be
#: modified once set. It can help with type narrowing and is recommended when
#: returning data from a function that should not be changed.
#:
#: All values are natively-supported JSON data. Custom serializers that
#: support more data types will need to add their own special type.
#:
#: Version Added:
#:     1.0
JSONDictImmutable: TypeAlias = Mapping[str, JSONValue]


#: A type for a list of JSON values.
#:
#: All values are natively-supported JSON data. Custom serializers that
#: support more data types will need to add their own special type.
#:
#: Version Added:
#:     1.0
JSONList: TypeAlias = List[JSONValue]


#: An immutable type of a list of JSON values.
#:
#: This is an immutable version of :py:class:`JSONList`, which cannot be
#: modified once set. It can help with type narrowing and is recommended when
#: returning data from a function that should not be changed.
#:
#: All values are natively-supported JSON data. Custom serializers that
#: support more data types will need to add their own special type.
#:
#: Version Added:
#:     1.0
JSONListImmutable: TypeAlias = Sequence[JSONValue]


#: Base type indicating a valid value that can be serialized to JSON.
#:
#: Consumers can create a type alias for this that provides a set of
#: additional types that can be serialized to JSON.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        SerializableJSONValue: TypeAlias = \
#:            BaseSerializableJSONValue[Union[datetime, UUID]]
BaseSerializableJSONValue: TypeAlias = Union[
    'BaseSerializableJSONDict[_T]',
    'BaseSerializableJSONList[_T]',
    'BaseSerializableJSONDictImmutable[_T]',
    'BaseSerializableJSONListImmutable[_T]',
    JSONValue,
    _T,
]


#: Base type for a dictionary mapping strings to JSON-serializable values.
#:
#: Consumers can create a type alias for this that provides a set of
#: additional types that can be serialized to JSON.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        SerializableJSONDict: TypeAlias = \
#:            BaseSerializableJSONDict[Union[datetime, UUID]]
BaseSerializableJSONDict: TypeAlias = \
    Dict[str, BaseSerializableJSONValue[_T]]


#: Base type for an immutable mapping of strings to JSON-serializable values.
#:
#: Consumers can create a type alias for this that provides a set of
#: additional types that can be serialized to JSON.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        SerializableJSONDictImmutable: TypeAlias = \
#:            BaseSerializableJSONDictImmutable[Union[datetime, UUID]]
BaseSerializableJSONDictImmutable: TypeAlias = \
    Mapping[str, BaseSerializableJSONValue[_T]]


#: Base type for a list of JSON-serializable values.
#:
#: Consumers can create a type alias for this that provides a set of
#: additional types that can be serialized to JSON.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        SerializableJSONList: TypeAlias = \
#:            BaseSerializableJSONList[Union[datetime, UUID]]
BaseSerializableJSONList: TypeAlias = List[BaseSerializableJSONValue[_T]]


#: Base type for an immutable sequence of JSON-serializable values.
#:
#: Consumers can create a type alias for this that provides a set of
#: additional types that can be serialized to JSON.
#:
#: Version Added:
#:     1.0
#:
#: Example:
#:     .. code-block:: python
#:
#:        SerializableJSONListImmutable: TypeAlias = \
#:            BaseSerializableJSONListImmutable[Union[datetime, UUID]]
BaseSerializableJSONListImmutable: TypeAlias = \
    Sequence[BaseSerializableJSONValue[_T]]
