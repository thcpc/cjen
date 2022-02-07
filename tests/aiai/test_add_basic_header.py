import pytest

import cjen
from cjen import BigOrange
from cjen.exceptions import MethodWrongErr, InstanceWrongErr


class System(BigOrange):
    @cjen.headers.basicHeaders(headers={
        "Auth": "",
        "XXX": "yyy"
    })
    def __init__(self): super().__init__()


def test_add_headers():
    system = System()
    assert system.headers.get("Auth") is not None
    assert system.headers.get("XXX") == "yyy"


class ErrorInstance(object):
    @cjen.headers.basicHeaders(headers={
        "Auth": "",
        "XXX": "yyy"
    })
    def __init__(self): pass


@pytest.mark.xfail(raises=InstanceWrongErr)
def test_add_header_fail_instance():
    ErrorInstance()


class ErrorMethod(BigOrange):

    def __init__(self):
        super().__init__()

    @cjen.headers.basicHeaders(headers={
        "Auth": "",
        "XXX": "yyy"
    })
    def error(self): pass


@pytest.mark.xfail(raises=MethodWrongErr)
def test_add_header_fail_method():
    ErrorMethod().error()


if __name__ == '__main__':
    pytest.main(["test_add_basic_header.py"])
