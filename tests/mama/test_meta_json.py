import os

import cjen
from cjen import MetaJson, BigTangerine


class Company(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.id")
    def id(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.name")
    def name(self): ...


class Area(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.listOf(clazz=Company)
    @cjen.operate.json.one(json_path="$.companies")
    def companies(self) -> list[Company]: ...


class C01Employees(MetaJson):

    @cjen.operate.common.value
    @cjen.operate.json.many(json_path="$.employees[?(@.company_id==1)]", filter_keys=["name", "company_id"])
    def employees(self): ...

    @cjen.operate.common.value
    @cjen.operate.json.one(json_path="$.procCode")
    def procCode(self): ...


class JsonMockService(BigTangerine):
    @cjen.http.base_url(uri="http://127.0.0.1:5000")
    def __init__(self):
        super().__init__()

    @cjen.http.get_mapping(uri="company/{company_id}")
    @cjen.operate.json.factory(clazz=Company)
    def get_company(self, *, path_variable: dict, resp=None, company: Company = None, **kwargs):
        assert company.id() == path_variable.get("company_id")
        assert company.name() == "C02"
        assert company.procCode() == 200

    @cjen.http.get_mapping(uri="all_employees")
    @cjen.operate.json.factory(clazz=C01Employees)
    def c01_employees(self, resp=None, employees: C01Employees = None, **kwargs):
        assert employees.procCode() == 200
        for i, val in enumerate(employees.employees()):
            assert f"E0{i + 1}" == val.get("name")
            assert val.get("company_id") == 1

    @cjen.http.get_mapping(uri="companies")
    @cjen.operate.json.factory(clazz=Area)
    def all_company(self, resp=None, area: Area = None, **kwargs):
        assert area.procCode() == 200
        for i, company in enumerate(area.companies()):
            assert company.id() == int(f"{i + 1}")
            assert company.name() == f"C0{i + 1}"

    @cjen.http.get_mapping(uri="company/{company_id}", json_clazz=Company)
    def get_json(self, *, path_variable: dict, resp=None, company: Company = None, **kwargs):
        assert company.id() == path_variable.get("company_id")
        assert company.name() == "C02"
        assert company.procCode() == 200

    @cjen.http.put_mapping(uri="company/{company_id}", json_clazz=Company)
    def put_json(self, *, path_variable: dict, resp=None, company: Company = None, **kwargs):
        assert company.id() == path_variable.get("company_id")
        assert company.name() == "C02"
        assert company.procCode() == 200

    @cjen.http.post_mapping(uri="company/{company_id}", json_clazz=Company)
    def post_json(self, *, path_variable: dict, resp=None, company: Company = None, **kwargs):
        assert company.id() == path_variable.get("company_id")
        assert company.name() == "C02"
        assert company.procCode() == 200

    @cjen.http.delete_mapping(uri="company/{company_id}", json_clazz=Company)
    def delete_json(self, *, path_variable: dict, resp=None, company: Company = None, **kwargs):
        assert company.id() == path_variable.get("company_id")
        assert company.name() == "C02"
        assert company.procCode() == 200

    @cjen.http.upload_mapping(uri="company/{company_id}", json_clazz=Company)
    def upload_json(self, *, path_variable: dict, data, resp=None, company: Company = None, **kwargs):
        assert company.id() == path_variable.get("company_id")
        assert company.name() == "C02"
        assert company.procCode() == 200


def test_one():
    mock = JsonMockService()
    mock.get_company(path_variable=dict(company_id=2))


def test_many():
    mock = JsonMockService()
    mock.c01_employees()


def test_listOf():
    mock = JsonMockService()
    mock.all_company()


def test_http_json():
    mock = JsonMockService()
    mock.get_json(path_variable=dict(company_id=2))
    mock.post_json(path_variable=dict(company_id=2))
    mock.delete_json(path_variable=dict(company_id=2))
    mock.put_json(path_variable=dict(company_id=2))
    mock.upload_json(path_variable=dict(company_id=2),
                     data=dict(file=os.path.join(os.path.dirname(os.path.dirname(__file__)), "download_file.txt")))
