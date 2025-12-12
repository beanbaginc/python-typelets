"""Unit tests for typelets.funcs.

Version Added:
    1.1
"""

from __future__ import annotations

import inspect
from inspect import Parameter, Signature
from typing import TYPE_CHECKING
from unittest import TestCase

import typelets.funcs as funcs_module
from typelets.funcs import (BaseParamsFromFunc,
                            BaseParamsFromMethod,
                            OnlyParamsFromFunc,
                            OnlyParamsFromMethod,
                            TOwner,
                            TParams,
                            type_func_params_as,
                            type_method_params_as)

try:
    from inspect import get_annotations
except ImportError:
    if TYPE_CHECKING:
        assert False
    else:
        def get_annotations(func):
            return func.__annotations__

if TYPE_CHECKING:
    from typing import Any


funcs_module_dict = funcs_module.__dict__


class _WrappedMethods:
    def func(
        self,
        a: int,
        b: str,
        c: int = 3,
        d: bool = True,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42

    def func_mixed(
        self,
        a: int,
        /,
        b: str,
        c: int,
        *,
        d: bool = True,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42

    def func_posonly(
        self,
        a: int,
        b: str,
        c: int,
        d: bool = True,
        /,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42

    def func_kwonly(
        self,
        *,
        a: int,
        b: str,
        c: int,
        d: bool = True,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42


class _WrappedClassMethods:
    @classmethod
    def func(
        cls,
        a: int,
        b: str,
        c: int = 3,
        d: bool = True,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42

    @classmethod
    def func_mixed(
        cls,
        a: int,
        /,
        b: str,
        c: int,
        *,
        d: bool = True,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42

    @classmethod
    def func_posonly(
        cls,
        a: int,
        b: str,
        c: int,
        d: bool = True,
        /,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42

    @classmethod
    def func_kwonly(
        cls,
        *,
        a: int,
        b: str,
        c: int,
        d: bool = True,
    ) -> int:
        """Wrapped function."""
        assert a == 1
        assert b == 'foo'
        assert c == 3
        assert d is True

        return 42


def _wrapped_func(
    a: int,
    b: str,
    c: int,
    d: bool = True,
) -> int:
    """Wrapped function."""
    assert a == 1
    assert b == 'foo'
    assert c == 3
    assert d is True

    return 42


def _wrapped_func_mixed(
    a: int,
    /,
    b: str,
    c: int,
    *,
    d: bool = True,
) -> int:
    """Wrapped function."""
    assert a == 1
    assert b == 'foo'
    assert c == 3
    assert d is True

    return 42


def _wrapped_func_posonly(
    a: int,
    b: str,
    c: int,
    d: bool = True,
    /,
) -> int:
    """Wrapped function."""
    assert a == 1
    assert b == 'foo'
    assert c == 3
    assert d is True

    return 42


def _wrapped_func_kwonly(
    *,
    a: int,
    b: str,
    c: int,
    d: bool = True,
) -> int:
    """Wrapped function."""
    assert a == 1
    assert b == 'foo'
    assert c == 3
    assert d is True

    return 42


class TypeFuncParamsAsWithOnlyParamsFromFuncTests(TestCase):
    """Unit tests for @type_func_params_as with OnlyParamsFromFunc.

    Version Added:
        1.1
    """

    def test_with_function_pos_or_kw_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        positional-or-keyword args
        """
        @type_func_params_as(OnlyParamsFromFunc(_wrapped_func))
        def wrapper_func(*args, **kwargs) -> str:
            """Wrapper function."""
            return str(_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_posonly_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        positional-only args
        """
        @type_func_params_as(OnlyParamsFromFunc(_wrapped_func_posonly))
        def wrapper_func(*args) -> str:
            """Wrapper function."""
            return str(_wrapped_func_posonly(*args))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', 3, True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_function_kwonly_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        keyword-only args
        """
        @type_func_params_as(OnlyParamsFromFunc(_wrapped_func_kwonly))
        def wrapper_func(**kwargs) -> str:
            """Wrapper function."""
            return str(_wrapped_func_kwonly(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(a=1, b='foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_mixed_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        positional-or-keyword args, positional-only args, and keyword-only args
        """
        @type_func_params_as(OnlyParamsFromFunc(_wrapped_func_mixed))
        def wrapper_func(*args, **kwargs) -> str:
            """Wrapper function."""
            return str(_wrapped_func_mixed(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_renamed_args_kwargs(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        renamed *args, **kwargs
        """
        @type_func_params_as(OnlyParamsFromFunc(_wrapped_func))
        def wrapper_func(*xargs, **xkwargs) -> str:
            """Wrapper function."""
            return str(_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_pos_or_kw_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        positional-or-keyword args
        """
        @type_func_params_as(OnlyParamsFromMethod(_WrappedMethods.func))
        def wrapper_func(*args, **kwargs) -> str:
            """Wrapper function."""
            return str(_WrappedMethods().func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_posonly_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        positional-only args
        """
        @type_func_params_as(OnlyParamsFromMethod(
            _WrappedMethods.func_posonly
        ))
        def wrapper_func(*args) -> str:
            """Wrapper function."""
            return str(_WrappedMethods().func_posonly(*args))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', 3, True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_method_kwonly_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        keyword-only args
        """
        @type_func_params_as(OnlyParamsFromMethod(_WrappedMethods.func_kwonly))
        def wrapper_func(**kwargs) -> str:
            """Wrapper function."""
            return str(_WrappedMethods().func_kwonly(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(a=1, b='foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_mixed_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromMethod with
        positional-or-keyword args, positional-only args, and keyword-only args
        """
        @type_func_params_as(OnlyParamsFromMethod(_WrappedMethods.func_mixed))
        def wrapper_func(*args, **kwargs) -> str:
            """Wrapper function."""
            return str(_WrappedMethods().func_mixed(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_renamed_args_kwargs(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromMethod with
        renamed *args, **kwargs
        """
        @type_func_params_as(OnlyParamsFromMethod(_WrappedMethods.func))
        def wrapper_func(*xargs, **xkwargs) -> str:
            """Wrapper function."""
            return str(_WrappedMethods().func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_pos_or_kw_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        positional-or-keyword args
        """
        @type_func_params_as(OnlyParamsFromFunc(
            _WrappedClassMethods.func
        ))
        def wrapper_func(*args, **kwargs) -> str:
            """Wrapper function."""
            return str(_WrappedClassMethods.func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_posonly_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        positional-only args
        """
        @type_func_params_as(OnlyParamsFromFunc(
            _WrappedClassMethods.func_posonly
        ))
        def wrapper_func(*args) -> str:
            """Wrapper function."""
            return str(_WrappedClassMethods.func_posonly(*args))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', 3, True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_classmethod_kwonly_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc with
        keyword-only args
        """
        @type_func_params_as(OnlyParamsFromFunc(
            _WrappedClassMethods.func_kwonly
        ))
        def wrapper_func(**kwargs) -> str:
            """Wrapper function."""
            return str(_WrappedClassMethods.func_kwonly(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(a=1, b='foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_mixed_args(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromMethod with
        positional-or-keyword args, positional-only args, and keyword-only args
        """
        @type_func_params_as(OnlyParamsFromFunc(
            _WrappedClassMethods.func_mixed
        ))
        def wrapper_func(*args, **kwargs) -> str:
            """Wrapper function."""
            return str(_WrappedClassMethods.func_mixed(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_renamed_args_kwargs(self) -> None:
        """Testing @type_func_params_as with OnlyParamsFromFunc classmethod
        with renamed *args, **kwargs
        """
        @type_func_params_as(OnlyParamsFromFunc(
            _WrappedClassMethods.func
        ))
        def wrapper_func(*xargs, **xkwargs) -> str:
            """Wrapper function."""
            return str(_WrappedClassMethods.func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 'foo', c=3, d=True),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })


class TypeFuncParamsAsWithCustomSignatureTests(TestCase):
    """Unit tests for @type_func_params_as with custom signature.

    Version Added:
        1.1
    """

    def test_with_function_pos_or_kw_args(self) -> None:
        """Testing @type_func_params_as with custom signature from function
        with positional-or-keyword args
        """
        def new_wrapped_func(
            a: int,
            b: bool = False,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(new_wrapped_func))
        def wrapper_func(
            x: int,
            *args,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 1

            return str(new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 2, True, 'foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_and_posonly_args(self) -> None:
        """Testing @type_func_params_as with custom signature from function
        with positional-only args
        """
        def new_wrapped_func(
            a: int,
            b: bool = False,
            c: str = '',
            /,
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            *args,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(new_wrapped_func(*args))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, True, 'foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_function_and_kwonly_args(self) -> None:
        """Testing @type_func_params_as with custom signature from function
        with keyword-only args
        """
        def new_wrapped_func(
            *,
            a: int,
            b: bool = False,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(new_wrapped_func(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, a=2, b=True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_and_mixed_args(self) -> None:
        """Testing @type_func_params_as with custom function signature from
        function with positional-or-keyword args, positional-only args, and
        keyword-only args
        """
        def new_wrapped_func(
            a: int,
            /,
            b: bool = False,
            *,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                /,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            /,
            *args,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, b=True, c='foo'),
                         '42')
        self.assertEqual(wrapper_func(100, True, 2, True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_ONLY,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_ONLY,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_renamed_args_kwargs(self) -> None:
        """Testing @type_func_params_as custom signature function from
        function with renamed *args, **kwargs
        """
        def new_wrapped_func(
            a: int,
            b: bool = False,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            *xargs,
            **xkwargs,
        ) -> str:
            """Wrapper function."""
            return str(new_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, True, 'foo'),
                         '42')
        self.assertEqual(wrapper_func(100, True, a=2, b=True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_pos_or_kw_args(self) -> None:
        """Testing @type_func_params_as with custom signature from method
        with positional-or-keyword args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            *args,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 1

            return str(MyClass().new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 2, True, 'foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_and_posonly_args(self) -> None:
        """Testing @type_func_params_as with custom signature from method
        with positional-only args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                b: bool = False,
                c: str = '',
                /,
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            *args,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass().new_wrapped_func(*args))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, True, 'foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_method_and_kwonly_args(self) -> None:
        """Testing @type_func_params_as with custom signature from method
        with keyword-only args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                *,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                /,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            /,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass().new_wrapped_func(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, a=2, b=True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_ONLY,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_ONLY,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_and_mixed_args(self) -> None:
        """Testing @type_func_params_as with custom signature from method
        with positional-or-keyword args, positional-only args, and
        keyword-only args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                /,
                b: bool = False,
                *,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                /,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            /,
            *args,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass().new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, b=True, c='foo'),
                         '42')
        self.assertEqual(wrapper_func(100, True, 2, True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_ONLY,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_ONLY,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_renamed_args_kwargs(self) -> None:
        """Testing @type_func_params_as custom signature method from
        function with renamed *args, **kwargs
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            *xargs,
            **xkwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass().new_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, b=True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_pos_or_kw_args(self) -> None:
        """Testing @type_func_params_as with custom signature from classmethod
        with positional-or-keyword args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            *args,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 1

            return str(MyClass.new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(1, 2, True, 'foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_and_posonly_args(self) -> None:
        """Testing @type_func_params_as with custom signature from classmethod
        with positional-only args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                b: bool = False,
                c: str = '',
                /,
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            *args,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass.new_wrapped_func(*args))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, True, 'foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_classmethod_and_kwonly_args(self) -> None:
        """Testing @type_func_params_as with custom signature from classmethod
        with keyword-only args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                *,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                /,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            /,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass.new_wrapped_func(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, a=2, b=True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_ONLY,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_ONLY,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_and_mixed_args(self) -> None:
        """Testing @type_func_params_as with custom signature from classmethod
        with positional-or-keyword args, positional-only args, and
        keyword-only args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                /,
                b: bool = False,
                *,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                /,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            *args,
            **kwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass().new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, b=True, c='foo'),
                         '42')
        self.assertEqual(wrapper_func(100, True, 2, True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_renamed_args_kwargs(self) -> None:
        """Testing @type_func_params_as custom signature classmethod from
        function with renamed *args, **kwargs
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        @type_func_params_as(MyParamsFrom(MyClass.new_wrapped_func))
        def wrapper_func(
            x: int,
            y: bool = False,
            *xargs,
            **xkwargs,
        ) -> str:
            """Wrapper function."""
            assert x == 100
            assert y is True

            return str(MyClass().new_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(wrapper_func(100, True, 2, b=True, c='foo'),
                         '42')

        # Check the attributes.
        self.assertEqual(wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })


class TypeMethodParamsAsWithOnlyParamsFromFuncTests(TestCase):
    """Unit tests for @type_method_params_as with OnlyParamsFromFunc.

    Version Added:
        1.1
    """

    def test_with_function_pos_or_kw_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        positional-or-keyword args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(_wrapped_func))
            def wrapper_func(self, *args, **kwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_posonly_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        positional-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(  # type: ignore
                _wrapped_func_posonly
            ))
            def wrapper_func(self, *args) -> str:
                """Wrapper function."""
                return str(_wrapped_func_posonly(*args))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', 3, True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', 3, True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_function_kwonly_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        keyword-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(_wrapped_func_kwonly))
            def wrapper_func(self, **kwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func_kwonly(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(a=1, b='foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), a=1, b='foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_mixed_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        positional-or-keyword args, positional-only args, and keyword-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(_wrapped_func_mixed))
            def wrapper_func(self, *args, **kwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func_mixed(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_renamed_args_kwargs(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        renamed *args, **kwargs
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(_wrapped_func))
            def wrapper_func(self, *xargs, **xkwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_pos_or_kw_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        positional-or-keyword args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromMethod(_WrappedMethods.func))
            def wrapper_func(self, *args, **kwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_posonly_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        positional-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromMethod(  # type: ignore
                _WrappedMethods.func_posonly
            ))
            def wrapper_func(self, *args) -> str:
                """Wrapper function."""
                return str(_wrapped_func_posonly(*args))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', 3, True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', 3, True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_method_kwonly_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        keyword-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromMethod(
                _WrappedMethods.func_kwonly
            ))
            def wrapper_func(self, **kwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func_kwonly(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(a=1, b='foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), a=1, b='foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_mixed_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromMethod with
        positional-or-keyword args, positional-only args, and keyword-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromMethod(
                _WrappedMethods.func_mixed
            ))
            def wrapper_func(self, *args, **kwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func_mixed(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_renamed_args_kwargs(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromMethod with
        renamed *args, **kwargs
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromMethod(_WrappedMethods.func))
            def wrapper_func(self, *xargs, **xkwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_pos_or_kw_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        positional-or-keyword args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(
                _WrappedClassMethods.func
            ))
            def wrapper_func(self, *args, **kwargs) -> str:
                """Wrapper function."""
                return str(_WrappedClassMethods.func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_posonly_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        positional-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(  # type: ignore
                _WrappedClassMethods.func_posonly
            ))
            def wrapper_func(self, *args) -> str:
                """Wrapper function."""
                return str(_WrappedClassMethods.func_posonly(*args))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', 3, True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', 3, True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_classmethod_kwonly_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc with
        keyword-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(
                _WrappedClassMethods.func_kwonly
            ))
            def wrapper_func(self, **kwargs) -> str:
                """Wrapper function."""
                return str(_WrappedClassMethods.func_kwonly(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(a=1, b='foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), a=1, b='foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_mixed_args(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromMethod with
        positional-or-keyword args, positional-only args, and keyword-only args
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(
                _WrappedClassMethods.func_mixed
            ))
            def wrapper_func(self, *args, **kwargs) -> str:
                """Wrapper function."""
                return str(_WrappedClassMethods.func_mixed(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_renamed_args_kwargs(self) -> None:
        """Testing @type_method_params_as with OnlyParamsFromFunc
        classmethod with renamed *args, **kwargs
        """
        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(
                _WrappedClassMethods.func
            ))
            def wrapper_func(self, *xargs, **xkwargs) -> str:
                """Wrapper function."""
                return str(_WrappedClassMethods.func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })


class TypeMethodParamsAsWithCustomSignatureTests(TestCase):
    """Unit tests for @type_method_params_as with custom signature.

    Version Added:
        1.1
    """

    def test_with_function_pos_or_kw_args(self) -> None:
        """Testing @type_method_params_as with custom signature from function
        with positional-or-keyword args
        """
        def new_wrapped_func(
            a: int,
            b: bool = False,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                *args,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 1

                return str(new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 2, True, 'foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 2, True, 'foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_and_posonly_args(self) -> None:
        """Testing @type_method_params_as with custom signature from function
        with positional-only args
        """
        def new_wrapped_func(
            a: int,
            b: bool = False,
            c: str = '',
            /,
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(  # type: ignore
                new_wrapped_func
            ))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *args,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(new_wrapped_func(*args))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, True, 'foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, True, 'foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_function_and_kwonly_args(self) -> None:
        """Testing @type_method_params_as with custom signature from function
        with keyword-only args
        """
        def new_wrapped_func(
            *,
            a: int,
            b: bool = False,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(new_wrapped_func(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, a=2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, a=2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_and_mixed_args(self) -> None:
        """Testing @type_method_params_as with custom function signature from
        function with positional-or-keyword args, positional-only args, and
        keyword-only args
        """
        def new_wrapped_func(
            a: int,
            /,
            b: bool = False,
            *,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *args,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_function_renamed_args_kwargs(self) -> None:
        """Testing @type_method_params_as custom signature function from
        function with renamed *args, **kwargs
        """
        def new_wrapped_func(
            a: int,
            b: bool = False,
            c: str = '',
        ) -> int:
            assert a == 2
            assert b is True
            assert c == 'foo'

            return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(OnlyParamsFromFunc(_wrapped_func))
            def wrapper_func(self, *xargs, **xkwargs) -> str:
                """Wrapper function."""
                return str(_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 'foo', c=3, d=True),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 'foo', c=3, d=True),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_pos_or_kw_args(self) -> None:
        """Testing @type_method_params_as with custom signature from method
        with positional-or-keyword args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                *args,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 1

                return str(MyClass().new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 2, True, 'foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 2, True, 'foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_and_posonly_args(self) -> None:
        """Testing @type_method_params_as with custom signature from method
        with positional-only args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                b: bool = False,
                c: str = '',
                /,
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(  # type: ignore
                MyClass.new_wrapped_func
            ))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *args,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass().new_wrapped_func(*args))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, True, 'foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, True, 'foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_method_and_kwonly_args(self) -> None:
        """Testing @type_method_params_as with custom signature from method
        with keyword-only args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                *,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass().new_wrapped_func(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, a=2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, a=2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_and_mixed_args(self) -> None:
        """Testing @type_method_params_as with custom signature from method
        with positional-or-keyword args, positional-only args, and
        keyword-only args
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                /,
                b: bool = False,
                *,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *args,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass().new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_method_renamed_args_kwargs(self) -> None:
        """Testing @type_method_params_as custom signature method from
        function with renamed *args, **kwargs
        """
        class MyClass:
            def new_wrapped_func(
                self,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromMethod[TParams, TOwner]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *xargs,
                **xkwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass().new_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_pos_or_kw_args(self) -> None:
        """Testing @type_method_params_as with custom signature from
        classmethod with positional-or-keyword args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                *args,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 1

                return str(MyClass.new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(1, 2, True, 'foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 1, 2, True, 'foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_and_posonly_args(self) -> None:
        """Testing @type_method_params_as with custom signature from
        classmethod with positional-only args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                b: bool = False,
                c: str = '',
                /,
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(  # type: ignore
                MyClass.new_wrapped_func
            ))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *args,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass.new_wrapped_func(*args))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, True, 'foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, True, 'foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'return': 'str',
            })

    def test_with_classmethod_and_kwonly_args(self) -> None:
        """Testing @type_method_params_as with custom signature from
        classmethod with keyword-only args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                *,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass.new_wrapped_func(**kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, a=2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, a=2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_and_mixed_args(self) -> None:
        """Testing @type_method_params_as with custom signature from
        classmethod with positional-or-keyword args, positional-only args,
        and keyword-only args
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                /,
                b: bool = False,
                *,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                /,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *args,
                **kwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass().new_wrapped_func(*args, **kwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('args', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('kwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'args': 'TParams.args',
                'kwargs': 'TParams.kwargs',
                'return': 'str',
            })

    def test_with_classmethod_renamed_args_kwargs(self) -> None:
        """Testing @type_method_params_as custom signature classmethod from
        function with renamed *args, **kwargs
        """
        class MyClass:
            @classmethod
            def new_wrapped_func(
                cls,
                a: int,
                b: bool = False,
                c: str = '',
            ) -> int:
                assert a == 2
                assert b is True
                assert c == 'foo'

                return 42

        class MyParamsFrom(BaseParamsFromFunc[TParams]):
            def __call__(
                self,
                x: int,
                y: bool = False,
                *args: TParams.args,
                **kwargs: TParams.kwargs,
            ) -> Any:
                ...

        class MyNewClass:
            @type_method_params_as(MyParamsFrom(MyClass.new_wrapped_func))
            def wrapper_func(
                self,
                x: int,
                y: bool = False,
                *xargs,
                **xkwargs,
            ) -> str:
                """Wrapper function."""
                assert x == 100
                assert y is True

                return str(MyClass().new_wrapped_func(*xargs, **xkwargs))

        # Check the runtime behavior.
        self.assertEqual(
            MyNewClass().wrapper_func(100, True, 2, b=True, c='foo'),
            '42')
        self.assertEqual(
            MyNewClass.wrapper_func(MyNewClass(), 100, True, 2, b=True,
                                    c='foo'),
            '42')

        # Check the attributes.
        self.assertEqual(MyNewClass.wrapper_func.__name__, 'wrapper_func')
        self.assertEqual(MyNewClass.wrapper_func.__doc__, 'Wrapper function.')

        self.assertEqual(
            inspect.signature(MyNewClass.wrapper_func),
            Signature(
                [
                    Parameter('self', Parameter.POSITIONAL_OR_KEYWORD),
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))
        self.assertEqual(
            inspect.signature(MyNewClass().wrapper_func),
            Signature(
                [
                    Parameter('x', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='int'),
                    Parameter('y', Parameter.POSITIONAL_OR_KEYWORD,
                              annotation='bool',
                              default=False),
                    Parameter('xargs', Parameter.VAR_POSITIONAL,
                              annotation='TParams.args'),
                    Parameter('xkwargs', Parameter.VAR_KEYWORD,
                              annotation='TParams.kwargs'),
                ],
                return_annotation='str',
            ))

        self.assertEqual(
            get_annotations(MyNewClass.wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })
        self.assertEqual(
            get_annotations(MyNewClass().wrapper_func),
            {
                'x': 'int',
                'y': 'bool',
                'xargs': 'TParams.args',
                'xkwargs': 'TParams.kwargs',
                'return': 'str',
            })
