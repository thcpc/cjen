from cjen import BigOrange
import cjen


class Obj(BigOrange):

    @cjen.http.base_url(uri="http://200.200.101.113/api/admin")
    def __init__(self):
        super().__init__()

    @cjen.headers.contentType(value="application/json;charset=UTF-8")
    @cjen.headers.accept(value="application/json, text/plain, */*")
    @cjen.http.post_mapping(uri="/auth")
    def api(self, data, resp=None, **kwargs):
        print(resp)


print(Obj().api(data={"userName": "cc", "password": "cc"}))
