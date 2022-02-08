import pytest

from cjen import BigTangerine, JWTFrom, JWTAction
import cjen
from cjen.exceptions import JwtWrongErr


class Obj3(object):

    def __init__(self):
        self.headers = dict(xxxx=9999)

    def json(self): return dict(yyyy=8888)


class Obj2(object):

    def __init__(self):
        self.headers = dict(auth=9999)

    def json(self): return dict(auth=8888)


class Obj1(object):

    def __init__(self):
        self.headers = dict(auth=234)

    def json(self): return dict(auth=123)


class TestObj(BigTangerine):

    @cjen.headers.basicHeaders(headers={"AUTH": ""})
    def __init__(self): super().__init__()

    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.BODY, action=JWTAction.INIT)
    def post1(self):
        return Obj1()

    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.HEADER, action=JWTAction.INIT)
    def post2(self):
        return Obj1()


class TestObj2(BigTangerine):
    def __init__(self): super().__init__()

    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.BODY, action=JWTAction.INIT)
    def post1(self):
        return Obj2()

    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.HEADER, action=JWTAction.INIT)
    def post2(self):
        return Obj2()


class TestObj3(BigTangerine):
    def __init__(self): super().__init__()

    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.BODY, action=JWTAction.INIT)
    def post1(self):
        return Obj3()

    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.HEADER, action=JWTAction.INIT)
    def post2(self):
        return Obj3()


class TestObj4(BigTangerine):
    def __init__(self): super().__init__()

    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.BODY, action=JWTAction.INIT)
    @cjen.headers.accept(value="JJJJJ")
    def post1(self, *args, **kwargs):
        assert kwargs["headers"]["Accept"] == "JJJJJ"
        return Obj1()

    @cjen.headers.contentType(value="LLLL")
    @cjen.jwt(key="AUTH", json_path="$.auth", jwt_from=JWTFrom.HEADER, action=JWTAction.INIT)
    def post2(self, *args, **kwargs):
        assert kwargs["headers"]["Content-Type"] == "LLLL"
        return Obj1()


def test_jwt_ok():
    t1 = TestObj()
    t1.post1()
    assert t1.headers["AUTH"] == 123
    t1.post2()
    assert t1.headers["AUTH"] == 234

    t2 = TestObj2()
    t2.post1()
    assert t2.headers["AUTH"] == 8888
    t2.post2()
    assert t2.headers["AUTH"] == 9999

    t4 = TestObj4()
    t4.post1()
    assert t4.headers["AUTH"] == 123
    t4.post2()
    assert t4.headers["AUTH"] == 234


@pytest.mark.xfail(raises=JwtWrongErr)
def test_jwt_fail_header():
    t = TestObj3()
    t.post2()


@pytest.mark.xfail(raises=JwtWrongErr)
def test_jwt_fail_body():
    t = TestObj3()
    t.post1()


if __name__ == '__main__':
    pytest.main(["test_jwt_ok.py", "test_jwt_fail_header.py", "test_jwt_fail_body.py"])
    # pytest.main(["test_jwt_fail_body.py"])
