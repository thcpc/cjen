
from cjen import BigTangerine
from cjen.commons import _get_method_params
from cjen.exceptions import _check_method, _check_instance


def basicHeaders(*, headers: dict):
    def __wrapper__(func):
        # @_get_method_params(method=func)
        @_check_instance(decorator="headers.basicHeaders", expect=BigTangerine)
        @_check_method(decorator="headers.basicHeaders", method=func, expect="__init__")
        def __inner__(instance: BigTangerine, *args, **kwargs):
            instance.headers.update(headers)
            func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def appendBasicHeaders(*, headers: dict):
    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.appendBasicHeaders", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            instance.headers.update(headers)
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def accept(*, value: str):
    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.accept", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            kwargs["headers"] = {**kwargs.get("headers", {"Accept": value}), **{"Accept": value}}
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def contentType(*, value: str):
    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.contentType", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            kwargs["headers"] = {**kwargs.get("headers", {"Content-Type": value}), **{"Content-Type": value}}
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__


def addHeaders(*, value: dict):
    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="headers.addHeaders", expect=BigTangerine)
        def __inner__(instance: BigTangerine, *args, **kwargs):
            kwargs["headers"] = {**kwargs.get("headers", value), **value}
            return func(instance, *args, **kwargs)

        return __inner__

    return __wrapper__
