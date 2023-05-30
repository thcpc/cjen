import cjen
from cjen import MetaMysql

from cjen.db_bigtangerine import DBBigTangerine
from cjen.nene.database_info import DataBaseInfo


class Company(MetaMysql):

    @cjen.operate.common.value
    def id(self): ...

    @cjen.operate.common.value
    def name(self): ...


class DBObject(DBBigTangerine):
    def __init__(self, database_info):
        super().__init__(database_info)

    @cjen.operate.mysql.factory(clazz=Company, sql="SELECT * FROM company WHERE id = 1")
    def get_one_company(self, company: Company = None, **kwargs):
        assert company.id() == 1
        assert company.name() == "C01"


def test_database_info_is_dict():
    dbo = DBObject(database_info=dict(host="127.0.0.1", port=3306, user='root', pwd='root', database='cjen_test_sql'))
    dbo.get_one_company()


def test_database_info():
    dbo = DBObject(database_info=DataBaseInfo.factory(
        dict(host="127.0.0.1", port=3306, user='root', pwd='root', database='cjen_test_sql')))
    dbo.get_one_company()
