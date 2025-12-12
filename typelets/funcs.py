"""Typing useful for defining and calling functions.

Version Added:
    1.0
"""

from __future__ import annotations

import inspect
from inspect import Parameter
from typing import Any, Generic, Dict, TYPE_CHECKING, cast, overload

from typing_extensions import ParamSpec, Protocol, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from typing_extensions import Concatenate, TypeAlias


#: Standard type for referencing a callable's parameters.
#:
#: Version Added:
#:     1.1
TParams = ParamSpec('TParams')


#: Standard type for referencing a function's return value.
#:
#: Version Added:
#:     1.1
TReturn_co = TypeVar('TReturn_co', covariant=True)


#: Standard type for the owner of a method.
#:
#: This would generally be a class.
TOwner = TypeVar('TOwner', bound=object)


#: A type indicating a dictionary used for keyword arguments.
#:
#: Version Added:
#:     1.0
KwargsDict: TypeAlias = Dict[str, Any]


class MethodDirective(Protocol[TOwner, TParams, TReturn_co]):
    """A representation of a method on a class.

    This works as a directive for converting an unbound method to a bound
    method. It can be returned in place of a :py:class:`Callable[]
    <collections.abc.Callable>` to ensure proper typing when returning a type
    for a method.

    Version Added:
        1.1
    """

    #: The owner of the method.
    __self__: TOwner

    # Note: These are left intentionally undocumented in order to avoid
    #       affecting docstrings of wrapped functions.
    @overload
    def __get__(
        self,
        instance: None,
        owner: type[TOwner],
    ) -> Callable[Concatenate[TOwner, TParams], TReturn_co]:
        ...

    @overload
    def __get__(
        self,
        instance: TOwner,
        owner: type[TOwner],
    ) -> Callable[TParams, TReturn_co]:
        ...

    def __get__(
        self,
        instance: TOwner | None,
        owner: type[TOwner],
    ) -> (Callable[Concatenate[TOwner, TParams], TReturn_co] |
          Callable[TParams, TReturn_co]):
        raise Exception('Not reached')


class BaseParamsFromFunc(Generic[TParams]):
    """Base class for defining a signature based on a function.

    This is built to be used with the :py:func:`type_func_params_as` or
    :py:func:`type_method_params_as` decorators. It references another
    function, classmethod, or staticmethod, providing access to its
    :py:class:`~typing.ParamSpec` and allows its use in a :py:meth:`__call__`
    method.

    Subclasses must implement :py:meth:`__call__`, taking in the parameters
    needed by the decorated function, and returns :py:data:`~typing.Any`
    specifically.

    Note:
        There are some things to be aware of when writing your
        :py:meth:`__call__` method:

        1. Because this is defined in a class, it *must* contain ``self``,
           even if your decorated function does not. This won't affect the
           final type of your function.

        2. :data:`typing.Any` must always be returned from the signature,
           regardless of the referenced or decorated functions.

        3. If your decorated function uses ``*``, ``/``, those must be
           present.

        4. You must include both ``TParams.args`` and ``TParams.kwargs`` at
           the end of the signature, even if the wrapped function doesn't
           use either ``*args`` or ``**kwargs``.

           This is necessary for the type checkers.

        5. Using ``/`` to indicate positional-only arguments may trigger a
           type error when decorating a class. This should not affect the
           resulting type.

           We recommend using ``# type: ignore`` on the decorator line in this
           situation.

    If your decorated function simply takes ``*args`` and/or ``**kwargs`` and
    passes them to the referenced without taking any additional parameters,
    you can use:

    * :py:class:`OnlyParamsFromFunc`

    Version Added:
        1.1

    Examples:
        .. code-block:: python
           :caption: A simple function with ``*args`` and ``**kwargs``.

           from typelets.funcs import BaseParamsFromFunc, TParams


           # This would provide typing for any of the following functions.
           #
           # def my_function(
           #     name: str,
           #     age: int,
           #     *args,
           #     **kwargs,
           # ) -> str:
           #
           # def my_function(
           #     name: str,
           #     *args,
           #     age: int,
           #     **kwargs,
           # ) -> str:
           #
           # def my_function(
           #     name: str,
           #     age: int,
           #     *args,
           # ) -> str:
           #
           # def my_function(
           #     name: str,
           #     age: int,
           #     **kwargs,
           # ) -> str:
           #
           # def my_function(
           #     *,
           #     name: str,
           #     age: int,
           #     **kwargs,
           # ) -> str:
           class MyFunctionParamsFrom(BaseParamsFromFunc[TParams]):
               def __call__(
                   self,
                   name: str,
                   age: int,
                   *args: TParams.args,
                   **kwargs: TParams.kwargs,
               ): ...
    """

    def __init__(
        self,
        func: Callable[TParams, Any],
    ) -> None:
        """Construct the signature based on a function.

        Args:
            func (callable):
                The function to pass the signature off of.
        """


class BaseParamsFromMethod(Generic[TParams, TOwner]):
    """Base class for defining a signature based on a method.

    This is built to be used with the :py:func:`type_func_params_as` or
    :py:func:`type_method_params_as` decorators. It references an unbound
    method on a class, providing access to its :py:class:`~typing.ParamSpec`
    and allows its use in a :py:meth:`__call__` method.

    Subclasses must implement :py:meth:`__call__`, taking in the parameters
    needed by the decorated function, and returns :py:data:`~typing.Any`
    specifically.

    Note:
        There are some things to be aware of when writing your
        :py:meth:`__call__` method:

        1. Because this is defined in a class, it *must* contain ``self``,
           even if your decorated function does not. This won't affect the
           final type of your function.

        2. :data:`typing.Any` must always be returned from the signature,
           regardless of the referenced or decorated functions.

        3. If your decorated function uses ``*``, ``/``, those must be
           present.

        4. You must include both ``TParams.args`` and ``TParams.kwargs`` at
           the end of the signature, even if the wrapped function doesn't
           use either ``*args`` or ``**kwargs``.

           This is necessary for the type checkers.

        5. Using ``/`` to indicate positional-only arguments may trigger a
           type error when decorating a class. This should not affect the
           resulting type.

           We recommend using ``# type: ignore`` on the decorator line in this
           situation.

    If your decorated function simply takes ``*args`` and/or ``**kwargs`` and
    passes them to the referenced without taking any additional parameters,
    you can use:

    * :py:class:`OnlyParamsFromMethod`

    Version Added:
        1.1

    Examples:
        .. code-block:: python
           :caption: A simple function with ``*args`` and ``**kwargs``.

           from typelets.funcs import BaseParamsFromMethod, TOwner, TParams


           # This would provide typing for any of the following functions.
           #
           # def my_function(
           #     self,
           #     name: str,
           #     age: int,
           #     *args,
           #     **kwargs,
           # ) -> str:
           #
           # def my_function(
           #     self,
           #     name: str,
           #     *args,
           #     age: int,
           #     **kwargs,
           # ) -> str:
           #
           # def my_function(
           #     self,
           #     name: str,
           #     age: int,
           #     *args,
           # ) -> str:
           #
           # def my_function(
           #     self,
           #     name: str,
           #     age: int,
           #     **kwargs,
           # ) -> str:
           #
           # def my_function(
           #     self,
           #     *,
           #     name: str,
           #     age: int,
           #     **kwargs,
           # ) -> str:
           class MyFunctionParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
               def __call__(
                   self,
                   name: str,
                   age: int,
                   *args: TParams.args,
                   **kwargs: TParams.kwargs,
               ): ...
    """

    def __init__(
        self,
        func: Callable[Concatenate[TOwner, TParams], Any],
    ) -> None:
        """Construct the signature based on a method.

        Args:
            func (callable):
                The method to pass the signature off of.
        """


class OnlyParamsFromFunc(BaseParamsFromFunc[TParams]):
    """Defines a signature for inheriting all parameters from a function.

    This is used whenever you have a function or method that takes in a
    ``*args`` and/or ``**kwargs`` (but no other parameters) and passes them
    to another function.

    The ``*args`` and/or ``**kwargs`` will inherit the signature and types
    from the referenced function.

    This can be used with either :py:func:`type_func_params_as` or
    :py:func:`type_method_params_as`.

    Example:
        .. code-block:: python

           from typelets.funcs import (OnlyParamsFromFunc,
                                       type_func_params_as,
                                       type_method_params_as)


           def wrapped_func(
               a: int,
               b: str,
               /,
               c: int,
               *,
               d: bool,
           ) -> int:
               return a + c


           # Apply to a function:
           @type_func_params_as(OnlyParamsFromFunc(wrapped_func))
           def my_wrapper_func(*args, **kwargs) -> str:
               return str(wrapped_func(*args, **kwargs))


           # Or apply to a method:
           class MyClass:
               @type_method_params_as(OnlyParamsFromFunc(wrapped_func))
               def my_wrapper_func(self, *args, **kwargs) -> str:
                   return str(wrapped_func(*args, **kwargs))

    Version Added:
        1.1
    """

    # Note: This is left intentionally undocumented in order to avoid
    #       affecting docstrings of wrapped functions.
    def __call__(
        self,
        *args: TParams.args,
        **kwargs: TParams.kwargs,
    ) -> Any:
        ...


class OnlyParamsFromMethod(BaseParamsFromMethod[TParams, TOwner]):
    """Defines a signature for inheriting all parameters from a method.

    This is used whenever you have a function or method that takes in a
    ``*args`` and/or ``**kwargs`` (but no other parameters) and passes them
    to another method.

    The ``*args`` and/or ``**kwargs`` will inherit the signature and types
    from the referenced function.

    This can be used with either :py:func:`type_func_params_as` or
    :py:func:`type_method_params_as`.

    Example:
        .. code-block:: python

           from typelets.funcs import (OnlyParamsFromMethod,
                                       type_func_params_as,
                                       type_method_params_as)


           class OtherClass:
               def wrapped_func(
                   self,
                   a: int,
                   b: str,
                   /,
                   c: int,
                   *,
                   d: bool,
               ) -> int:
                   return a + c


           # Apply to a function:
           @type_func_params_as(OnlyParamsFromMethod(OtherClass.wrapped_func))
           def my_wrapper_func(*args, **kwargs) -> str:
               return str(OtherClass().wrapped_func(*args, **kwargs))


           # Or apply to a method:
           class MyClass:
               @type_method_params_as(OnlyParamsFromMethod(
                   OtherClass.wrapped_func
               ))
               def my_wrapper_func(self, *args, **kwargs) -> str:
                   return str(OtherClass().wrapped_func(*args, **kwargs))

    Version Added:
        1.1
    """

    # Note: This is left intentionally undocumented in order to avoid
    #       affecting docstrings of wrapped functions.
    def __call__(
        self,
        *args: TParams.args,
        **kwargs: TParams.kwargs,
    ) -> Any:
        ...


def type_func_params_as(
    params_from: Callable[TParams, Any],
    *,
    args_name: (str | None) = 'args',
    kwargs_name: (str | None) = 'kwargs',
) -> Callable[[Callable[TParams, TReturn_co]],
              Callable[TParams, TReturn_co]]:
    """Decorator for typing a function signature based on another function.

    This can be used with standard functions, classmethods, and staticmethods
    to type ``*args`` and/or ``**kwargs`` based on the arguments defined in a
    referenced function.

    It's built for functions that take in arguments for the purpose of
    passing to another function or method, which normally would mean either
    duplicating the arguments in the signature or losing out on typing
    altogether.

    This works as a decorator that takes a function signature definition
    (an instance of a :py:class:`BaseParamsFromFunc` subclass) or method
    signature (an instance of a :py:class:`BaseParamsFromMethod`), and
    retypes the decorated function using that signature. The definition is
    able to use the :py:class:`~typing.ParamSpec` of a referenced function.

    You can craft your own definition by creating a subclass of either
    of these base classes. See the documentation for examples.

    For simple cases, you can use the built-in :py:class:`OnlyParamsFromFunc`
    or :py:class:`OnlyParamsFromMethod`.

    There is minimal impact to function setup, and no impact when calling
    the function at runtime. The decorated function's ``__annotations__`` and
    ``__signature__`` will be patched at decoration time. There are no costs
    to calling the function, and no changes to function behavior.

    Warning:
        This may affect docstrings in Visual Studio Code or in other
        editors using PyLance, due to the way that docstrings are inferred
        from the first-provided callable. See
        https://github.com/microsoft/pylance-release/issues/5840.

    Version Added:
        1.1

    Args:
        params_from (callable):
            The callable function signature to base parameters off of.

            This is generally going to be an instance of a
            :py:class:`BaseParamsFromFunc` subclass.

        args_name (str, optional):
            Optional name of the ``*args`` argument.

            By default, the name will be auto-detected if ``"args"`` isn't
            the correct name. Consumers can set this to a name explicitly,
            or set it to ``None`` to avoid looking for this argument.

        kwargs_name (str, optional):
            Optional name of the ``*kwargs`` argument.

            By default, the name will be auto-detected if ``"kwargs"`` isn't
            the correct name. Consumers can set this to a name explicitly,
            or set it to ``None`` to avoid looking for this argument.

    Examples:
        .. code-block:: python
           :caption: Type a function based fully on a function

           from typelets.funcs import (OnlyParamsFromFunc,
                                       type_func_params_as,
                                       type_method_params_as)


           def wrapped_func(
               a: int,
               b: str,
               /,
               c: int,
               *,
               d: bool,
           ) -> int:
               return a + c

           @type_func_params_as(OnlyParamsFromFunc(wrapped_func))
           def my_wrapper_func(*args, **kwargs) -> str:
               return str(wrapped_func(*args, **kwargs))


        .. code-block:: python
           :caption: Type a function based fully on a method

           from typelets.funcs import (OnlyParamsFromMethod,
                                       type_method_params_as)


           class MyClass:
               def wrapped_func(
                   self,
                   a: int,
                   b: str,
                   /,
                   c: int,
                   *,
                   d: bool,
               ) -> int:
                   return a + c


           @type_func_params_as(OnlyParamsFromMethod(MyClass.wrapped_func))
           def my_wrapper_func(*args, **kwargs) -> str:
               return str(wrapped_func(*args, **kwargs))


        .. code-block:: python
           :caption: Type a method using a custom signature

           from typing import Any

           from typelets.funcs import (BaseParamsFromFunc,
                                       TParams,
                                       type_method_params_as)


           class MyParamsFrom(BaseParamsFromFunc[TParams]):
               def __call__(
                   self,
                   x: int,
                   y: bool = True,
                   *args: TParams.args,
                   **kwargs: TParams.kwargs,
               ) -> Any:
                   ...


           def wrapped_func(
               a: int,
               b: str,
               /,
               c: int,
               *,
               d: bool,
           ) -> int:
               return a + c


           @type_func_params_as(MyParamsFrom(wrapped_func))
           def my_wrapper_func(
               x: int,
               y: bool = True,
               *args,
               **kwargs,
           ) -> str:
               return str(wrapped_func(*args, **kwargs))
    """

    def _dec(
        decorated: Callable[TParams, TReturn_co],
    ) -> Callable[TParams, TReturn_co]:
        _inherit_params(params_func=params_from.__call__,  # type: ignore
                        decorated=decorated,
                        args_name=args_name,
                        kwargs_name=kwargs_name)

        return decorated

    return _dec


def type_method_params_as(
    params_from: Callable[TParams, Any],
    *,
    args_name: (str | None) = 'args',
    kwargs_name: (str | None) = 'kwargs',
) -> Callable[[Callable[Concatenate[TOwner, TParams], TReturn_co]],
              MethodDirective[TOwner, TParams, TReturn_co]]:
    """Decorator for typing a function signature based on another method.

    This can be used with unbound methods on classes to type ``*args`` and/or
    ``**kwargs`` based on the arguments defined in a referenced function.

    It's built for methods that take in arguments for the purpose of passing
    to another function or method, which normally would mean either
    duplicating the arguments in the signature or losing out on typing
    altogether.

    This works as a decorator that takes a function signature definition
    (an instance of a :py:class:`BaseParamsFromFunc` subclass) or method
    signature (an instance of a :py:class:`BaseParamsFromMethod`), and
    retypes the decorated method using that signature. The definition is
    able to use the :py:class:`~typing.ParamSpec` of a referenced function.

    Both the unbound method and bound method will have the correct signature.

    You can craft your own definition by creating a subclass of either
    of these base classes. See the documentation for examples.

    For simple cases, you can use the built-in :py:class:`OnlyParamsFromFunc`
    or :py:class:`OnlyParamsFromMethod`.

    There is minimal impact to function setup, and no impact when calling
    the function at runtime. The decorated function's ``__annotations__`` and
    ``__signature__`` will be patched at decoration time. There are no costs
    to calling the function, and no changes to function behavior.

    Warning:
        This may affect docstrings in Visual Studio Code or in other
        editors using PyLance, due to the way that docstrings are inferred
        from the first-provided callable. See
        https://github.com/microsoft/pylance-release/issues/5840.

    Version Added:
        1.1

    Args:
        params_from (callable):
            The callable function signature to base parameters off of.

            This is generally going to be an instance of a
            :py:class:`BaseParamsFromFunc` subclass.

        args_name (str, optional):
            Optional name of the ``*args`` argument.

            By default, the name will be auto-detected if ``"args"`` isn't
            the correct name. Consumers can set this to a name explicitly,
            or set it to ``None`` to avoid looking for this argument.

        kwargs_name (str, optional):
            Optional name of the ``*kwargs`` argument.

            By default, the name will be auto-detected if ``"kwargs"`` isn't
            the correct name. Consumers can set this to a name explicitly,
            or set it to ``None`` to avoid looking for this argument.

    Examples:
        .. code-block:: python
           :caption: Type a method based fully on a function

           from typelets.funcs import (OnlyParamsFromFunc,
                                       type_method_params_as)


           def wrapped_func(
               a: int,
               b: str,
               /,
               c: int,
               *,
               d: bool,
           ) -> int:
               return a + c

           class MyClass:
               @type_method_params_as(OnlyParamsFromFunc(wrapped_func))
               def my_wrapper_func(self, *args, **kwargs) -> str:
                   return str(wrapped_func(*args, **kwargs))


        .. code-block:: python
           :caption: Type a method based fully on a method

           from typelets.funcs import (OnlyParamsFromMethod,
                                       type_method_params_as)


           class MyClass:
               def wrapped_func(
                   self,
                   a: int,
                   b: str,
                   /,
                   c: int,
                   *,
                   d: bool,
               ) -> int:
                   return a + c

               @type_method_params_as(OnlyParamsFromMethod(wrapped_func))
               def my_wrapper_func(self, *args, **kwargs) -> str:
                   return str(self.wrapped_func(*args, **kwargs))


        .. code-block:: python
           :caption: Type a method using a custom signature

           from typing import Any

           from typelets.funcs import (BaseParamsFromMethod,
                                       TParams,
                                       TOwner,
                                       type_method_params_as)


           class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
               def __call__(
                   self,
                   x: int,
                   y: bool = True,
                   *args: TParams.args,
                   **kwargs: TParams.kwargs,
               ) -> Any:
                   ...


           class MyClass:
               def wrapped_func(
                   self,
                   a: int,
                   b: str,
                   /,
                   c: int,
                   *,
                   d: bool,
               ) -> int:
                   return a + c

               @type_method_params_as(MyParamsFrom(wrapped_func))
               def my_wrapper_func(
                   self,
                   x: int,
                   y: bool = True,
                   *args,
                   **kwargs,
               ) -> str:
                   return str(self.wrapped_func(*args, **kwargs))
    """
    def _dec(
        decorated: Callable[Concatenate[TOwner, TParams], TReturn_co],
    ) -> MethodDirective[TOwner, TParams, TReturn_co]:
        _inherit_params(params_func=params_from.__call__,  # type: ignore
                        decorated=decorated,
                        args_name=args_name,
                        kwargs_name=kwargs_name)

        return cast(MethodDirective, decorated)

    return _dec


def _inherit_params(
    *,
    params_func: Callable[..., Any],
    decorated: Callable[..., Any],
    args_name: str | None,
    kwargs_name: str | None,
) -> None:
    """Patch the signature and annotations of a function to inherit params.

    This will determine first whether the decorated signature should have
    any ``*args`` or ``**kwargs`` updates applied. If so, it will fetch those
    parameters, searching for alternate names if needed, and then patch the
    signatures and annotations to reference ``TParams.args`` or
    ``TParams.kwargs``, enabling type checkers and IDEs to include the
    referenced arguments in the signature.

    Attempts are made to do as little as possible, in order to keep this
    as fast as possible. In an unrealistic case of no ``*args`` or
    ``**kwargs``, this will do nothing other than fetch the signature. In
    most cases, it will perform the full signature introspection and patching.
    This is overall pretty fast, though.

    Version Added:
        1.1

    Args:
        params_func (callable):
            The callable containing the parameter signature to reference.

        decorated (callable):
            The decorated function to patch.

        args_name (str):
            The name of the ``*args`` argument.

            This can be set to ``None`` to avoid looking for this argument.

        kwargs_name (str, optional):
            The name of the ``*kwargs`` argument.

            This can be set to ``None`` to avoid looking for this argument.
    """
    decorated_sig = inspect.signature(decorated)
    decorated_sig_params = decorated_sig.parameters

    if args_name:
        has_args = args_name in decorated_sig_params
        find_args = not has_args
    else:
        has_args = False
        find_args = False

    if kwargs_name:
        has_kwargs = kwargs_name in decorated_sig_params
        find_kwargs = not has_kwargs
    else:
        has_kwargs = False
        find_kwargs = False

    if find_args or find_kwargs:
        # The *args or **kwargs parameter was not found in the signature
        # under the supplied name. Try to find it.
        for param_name, param in decorated_sig_params.items():
            if find_args and param.kind == Parameter.VAR_POSITIONAL:
                args_name = param_name
                has_args = True
                find_args = False
            elif find_kwargs and param.kind == Parameter.VAR_KEYWORD:
                kwargs_name = param_name
                has_kwargs = True
                find_kwargs = False
            else:
                continue

            if not find_args and not find_kwargs:
                # We're done searching for what we want to find.
                break

    if has_args or has_kwargs:
        param_overrides: dict[str, inspect.Parameter] = {}
        decorated_annotations = decorated.__annotations__
        params_annotations = params_func.__annotations__

        if has_args and args_name not in decorated_annotations:
            assert args_name

            args_annotation = params_annotations['args']
            decorated_annotations[args_name] = args_annotation
            param_overrides[args_name] = Parameter(
                args_name,
                kind=Parameter.VAR_POSITIONAL,
                annotation=args_annotation)

        if has_kwargs and kwargs_name not in decorated_annotations:
            assert kwargs_name

            kwargs_annotation = params_annotations['kwargs']
            decorated_annotations[kwargs_name] = kwargs_annotation
            param_overrides[kwargs_name] = Parameter(
                kwargs_name,
                kind=Parameter.VAR_KEYWORD,
                annotation=kwargs_annotation)

        setattr(decorated, '__annotations__', decorated_annotations)

        if param_overrides:
            new_sig_params: list[Parameter] = [
                param_overrides.get(param_name, param)
                for param_name, param in decorated_sig.parameters.items()
            ]

            setattr(decorated, '__signature__', (
                inspect.signature(decorated)
                .replace(parameters=new_sig_params)
            ))
