import os

import cjen
from cjen import DatabasePool, BigTangerine, MetaMysql

from cjen.bigtangerine import ContextArgs
from cjen.nene.helper import FileHelper


def cursor():
    return DatabasePool.cursor(host="127.0.0.1", port=3306, user='root', pwd='root', database='cjen_test_sql')


class Company(MetaMysql):

    @cjen.operate.common.value
    def id(self): ...

    @cjen.operate.common.value
    def name(self): ...


class Employee(MetaMysql):
    @cjen.operate.common.value
    def id(self): ...

    @cjen.operate.common.value
    def name(self): ...

    @cjen.operate.common.value
    def company(self): ...


class CMysql(BigTangerine):

    def __init__(self): super().__init__()

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=Company, sql="SELECT * FROM company WHERE id = 1")
    def get_one_company(self, company: Company, **kwargs):
        assert company.id() == 1
        assert company.name() == "C01"

    @cjen.operate.mysql.factory(cursor=cursor(), size=-1, clazz=Company, sql="SELECT * FROM company")
    def get_many_companies(self, companies: list[Company], **kwargs):
        assert len(companies) == 5

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=Employee, sql=FileHelper.read(os.path.dirname(__file__), "employee.sql"), 
                                params=dict(id=1))
    def get_e01_employee(self, employee: Employee, **kwargs):
        assert employee.name() == "E01"
        assert employee.company() == "C01"

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=Employee, sql=FileHelper.read(os.path.dirname(__file__), "employees.sql"),
                                params=[2, 3], size=-1)
    def get_e0203_employee(self, employees: list[Employee], **kwargs):
        assert len(employees) == 2
        assert employees[0].name() == 'E02'
        assert employees[1].name() == 'E03'
        assert employees[0].company() == 'C01'
        assert employees[1].company() == 'C01'

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=Employee, sql=FileHelper.read(os.path.dirname(__file__), "employees.sql"),
                                params=(4, 5), size=-1)
    def get_e0405_employee(self, employees: list[Employee], **kwargs):
        assert len(employees) == 2
        assert employees[0].name() == 'E04'
        assert employees[1].name() == 'E05'
        assert employees[0].company() == 'C01'
        assert employees[1].company() == 'C01'

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=Employee,
                                sql=FileHelper.cur_read(cur=__file__, file="employees_of_company.sql"),
                                params=ContextArgs(id="company_id"), size=-1)
    def get_c01_employees(self, employees: list[Employee], **kwargs):
        assert len(employees) == 7
        for employee in employees: assert employee.company() == "C01"

    @cjen.context.add(content=dict(company_id=1))
    def set_company_id(self): ...

    @cjen.operate.mysql.factory(cursor=cursor(), clazz=dict,
                                sql=FileHelper.cur_read(cur=__file__, file="employees_of_company.sql"),
                                size=-1)
    def get_c01_employees_new(self, employees: list[dict], **kwargs):
        assert len(employees) == 7
        for employee in employees: assert employee.get("company") == "C01"

def test_mysql_factory_no_params():
    CMysql().get_one_company()
    CMysql().get_many_companies()


def test_mysql_factory_with_normal_params():
    # dict
    CMysql().get_e01_employee()
    # list
    CMysql().get_e0203_employee()
    # tuple
    CMysql().get_e0405_employee()


def test_mysql_factory_with_context_args():
    cm = CMysql()
    cm.set_company_id()
    cm.get_c01_employees()

def test_mysql_factory_new_with_context_args():
    cm = CMysql()
    # cm.set_company_id()
    cm.get_c01_employees_new(id=1)
