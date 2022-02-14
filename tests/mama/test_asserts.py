import os

import pytest

import cjen
from cjen import MetaMysql, DatabasePool, MetaJson
from cjen.bigtangerine import ContextArgs, BigTangerine
from cjen.nene.helper import FileHelper


def cursor():
    return DatabasePool.cursor(host="127.0.0.1", port=3306, user='root', pwd='123456', database='cjen_test_sql')


class CompanyC01(MetaMysql):

    @cjen.operate.common.value
    @cjen.operate.asserts.equal(value=1)
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.asserts.equal(value="C01")
    @cjen.operate.asserts.in_range(ranges=["C01", "C02", "C03", "C04"])
    def name(self): ...


class Employee(MetaMysql):
    @cjen.operate.common.value
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.asserts.not_in_range(ranges=["C01", "C02", "C03", "C04"])
    @cjen.operate.asserts.in_range(ranges=["E01", "E02", "E03", "E04"])
    def name(self): ...

    @cjen.operate.common.value
    def company(self): ...


class ResponseNone(MetaJson):

    @cjen.operate.json.one(json_path="$.employees")
    @cjen.operate.asserts.not_equal(value=300)
    def procCode(self): ...

    @cjen.operate.json.one(json_path="$.employees")
    @cjen.operate.asserts.required
    def employees(self): ...


class AssertMockService(BigTangerine):

    @cjen.http.base_url(uri="http://127.0.0.1:5000")
    def __init__(self): super().__init__()

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=CompanyC01, sql="SELECT * FROM company WHERE id = 1")
    def get_c01_company(self, company: CompanyC01, **kwargs):
        assert company.id() == 1
        assert company.name() == "C01"

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=Employee,
                                sql=FileHelper.read(os.path.dirname(__file__), "employee.sql"),
                                params=dict(id=1))
    def get_e01_employee(self, employee: Employee, **kwargs):
        assert employee.name() == "E01"
        assert employee.company() == "C01"

    @cjen.http.get_mapping(uri="none_field_response")
    @cjen.operate.json.factory(clazz=ResponseNone)
    def required_xfail(self, resp=None, resp_null: ResponseNone = None, **kwargs):
        resp_null.employees()

    @cjen.http.get_mapping(uri="none_field_response")
    @cjen.operate.mysql.factory(cursor=cursor(), clazz=CompanyC01,
                                sql="SELECT * FROM company WHERE id = 1",
                                params=dict(id=1))
    @cjen.operate.json.factory(clazz=ResponseNone)
    @cjen.operate.asserts.validation_meta(meta_name="company", fields="id;name")
    @cjen.operate.asserts.validation_meta(meta_name="resp_null")
    def validation_appoint(self, resp=None, company: CompanyC01 = None, resp_null: ResponseNone = None, **kwargs): ...


def test_assert_eq_in_range():
    AssertMockService().get_c01_company()


@pytest.mark.xfail(raises=AssertionError)
def test_assert_xfail():
    ams = AssertMockService()
    ams.required_xfail()


def test_not_range_in():
    AssertMockService().get_e01_employee()


@pytest.mark.xfail(raises=AssertionError)
def test_validation_appoint():
    AssertMockService().validation_appoint()
