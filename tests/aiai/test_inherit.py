from cjen import BigTangerine
import cjen


class Level1(BigTangerine):
    def __init__(self):
        super().__init__()


class Level2(Level1):
    @cjen.headers.basicHeaders(headers=dict(xx=1))
    def __init__(self):
        super().__init__()


def test_inherit():
    a = Level2()
    assert a.headers.get("xx") == 1
