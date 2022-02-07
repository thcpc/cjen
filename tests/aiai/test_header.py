import pytest

from cjen import BigOrange
import cjen


class TestObj(BigOrange):

    @cjen.headers.basicHeaders(headers=dict(xx=1))
    def __init__(self): super().__init__()

    @cjen.headers.appendBasicHeaders(headers=dict(zz=3))
    @cjen.headers.addHeaders(value=dict(cheng="yyyx"))
    @cjen.headers.contentType(value="yyy")
    @cjen.headers.accept(value="xxx")
    @cjen.headers.appendBasicHeaders(headers=dict(jj=4))
    def post(self, *args, **kwargs):
        assert kwargs.get("headers").get("Content-Type") == "yyy"
        assert kwargs.get("headers").get("Accept") == "xxx"
        assert kwargs.get("headers").get("cheng") == "yyyx"
        return "success"


def test_headers():
    t = TestObj()
    assert t.post() == "success"
    assert t.headers.get("xx") == 1
    assert t.headers.get("zz") == 3
    assert t.headers.get("jj") == 4


if __name__ == '__main__':
    pytest.main(["test_header.py"])
