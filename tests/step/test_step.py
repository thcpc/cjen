import cjen
from cjen import BigTangerine
from cjen.tests.step.ok_response import OKResponse
from cjen.tests.step.ok_step import OkStep
from cjen.tests.step.other_step import OtherStep


class StepMockService(BigTangerine):
    @cjen.http.base_url(uri="http://127.0.0.1:5000")
    def __init__(self):
        super().__init__()

    @cjen.headers.contentType(value="application/json")
    @cjen.http.post_mapping(uri="post_method_json",json_clazz=OKResponse)
    @cjen.step.call(stepName=OkStep.Name, argName="ok")
    @cjen.step.call(stepName=OtherStep.Name, argName="ok")
    def post_method_json(self, *, data, ok: OKResponse = None, resp=None, **kwargs): ...


def test_one_step():
    mock = StepMockService()
    OkStep(mock, None).run()
    OkStep(mock, None).run()
    # mock.post_method_json(data=dict(username="xx", pwd="yyy"))

def test_two_step():
    mock = StepMockService()
    OkStep(mock, None).run()
    OtherStep(mock, None).run()
