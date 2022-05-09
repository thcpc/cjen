import jsonpath

from cjen import BigTangerine
from enum import Enum

from cjen.commons import _get_method_params
from cjen.exceptions import JwtWrongErr


class JWTFrom(Enum):
    BODY = 0,
    HEADER = 1


class JWTAction(Enum):
    INIT = 101
    EXCHANGE = 102
    REFRESH = 103


def jwt(*, key: str, json_path: str, jwt_from: JWTFrom = JWTFrom.BODY, action: JWTAction = JWTAction.INIT):
    """
    usually use on login api, init the jwt token to headers.
    only support json response
    :param action:
    :param jwt_from:
    :param key:
    :param json_path:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        def __inner__(ins: BigTangerine, *args, **kwargs):
            rsp = func(ins, *args, **kwargs)
            rsp = rsp if jwt_from == JWTFrom.BODY else kwargs.get("response_content").headers
            if not jsonpath.jsonpath(rsp, json_path):
                if action == JWTAction.INIT or action == JWTAction.EXCHANGE:
                    raise JwtWrongErr(f"can not find jwt key in {rsp}")
            else:
                ins.headers[key] = jsonpath.jsonpath(rsp, json_path)[0] if json_path else rsp
            return rsp

        return __inner__

    return __wrapper__