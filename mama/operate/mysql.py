import time
from typing import IO

from pymysql.cursors import Cursor

import cjen
# from cjen import BigTangerine, MetaMysql

# TODO 时区转换的装饰器
from cjen.bigtangerine import ContextArgs, BigTangerine
from cjen.commons import _get_method_params
from cjen.exceptions import _check_instance, _check_params_factory
from cjen.mama.meta_data import MetaData, MetaMysql
from cjen.mama.operate.common import value


@cjen.haha(LogPath="", LogName="CJEN.log")
def track_sql(msg: dict, io: IO):
    io.write("{sql}\n".format(**msg))


def type_boolean(*, true, false):
    """
    TODO 待测试
    covert to True or False
    :param true:
    :param false:
    :return:
    """

    def __wrapper__(func):
        def __inner__(ins: MetaData, *args, **kwargs):
            field = func(ins, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
            if ins.meta_data.get(field) == true: return True
            if ins.meta_data.get(field) == false: return False
            raise Exception("type_boolean can not matched")

        return __inner__

    return __wrapper__()


def timezone(*, zone: str): pass


def type_str_datetime(*, fmt: str): pass


def factory(*, cursor: Cursor, clazz, sql: str, params=None, size=1, track=False):
    """
    使用条件: 作用在 类型 BigTangerine 或 其子类的 对象 \n
    位置：放在http.post_mapping 等请求装饰器之后 \n
    作用：创建针对MYSQL 的 MetaData \n
    注意：只支持查询语句

    :param track: 是否打开日志，记录查询SQL
    :param cursor:
    :param size: -1 代表取所有的,
    :param params: sql的查询条件,
    :param sql: 查询的 sql
    :param clazz:
    :return: 支持返回一个对象 或 对象列表
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_params_factory(clazz=MetaMysql)
        @_check_instance(decorator="operate.mysql.factory", expect=BigTangerine)
        def __inner__(ins, *args, **kwargs):

            try:
                query_args = ins.context.pick_up(context_args=params) if isinstance(params, ContextArgs) else params
                cursor.execute(sql, args=query_args)
                if track: track_sql(dict(sql=cursor.mogrify(sql, args=query_args)))
                values = cursor.fetchall()
                cols = [col[0] for col in cursor.description]
                data = [dict(zip(cols, ele)) for ele in values]
                if size != -1:
                    assert cursor.rowcount == size, f"the record number is not eql {size}"
                for key, val in kwargs.get("method.__annotations__").items():
                    if issubclass(val, clazz) or (
                            "__origin__" in dir(val) and val.__origin__ == list and issubclass(val.__args__[0], clazz)):
                        metas = [MetaData.factory(clazz=clazz, data=ele) for ele in data]
                        for meta in metas:
                            meta.meta_data = meta.meta_source
                            if ins.context:
                                meta.context.update(ins.context)
                        kwargs[key] = metas[0] if size == 1 else metas

                return func(ins, *args, **kwargs)
            except Exception as e:
                raise e
            finally:
                cursor.close()

        return __inner__

    return __wrapper__


def type_datetime_str(*, fmt: str):
    """
    TODO 待测试
    convert datetime to str
    :param fmt:
    :return:
    """

    def __wrapper__(func):
        def __inner__(ins: MetaData, *args, **kwargs):
            field = func(ins, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
            return time.strftime(ins.meta_data.get(field), fmt)

        return __inner__

    return __wrapper__


def type_datetime_stamp(func):
    """
    TODO 待测试
    covert datetime to timestamp
    :param func:
    :return:
    """

    def __inner__(ins: MetaData, *args, **kwargs):
        field = func(ins, *args, **kwargs) if func.__name__ == '__inner__' else func.__name__
        time_array = time.strftime(ins.meta_data.get(field), "%Y-%m-%d %H:%M:%S")
        return time.mktime(time_array)

    return __inner__


class TestObj(MetaMysql):
    @value
    def id(self): ...

# cusor = DatabasePool.cursor(host="200.200.101.113", user="root", port=3306, pwd="Admin123",
#                             database="eclinical_design_dev_56")


# class Api(BigTangerine):
#
#     def __init__(self):
#         super().__init__()
#
#     @factory(cursor=cusor, clazz=TestObj, sql="SELECT * FROM eclinical_odm_item WHERE id = 1", size=-1)
#     def xx(self, metas: list[TestObj] = None, **kwargs):
#         for meta in metas:
#             print(meta.id())
#
#     @factory(cursor=cusor, clazz=TestObj,
#              sql="""SELECT * FROM eclinical_odm_item WHERE id = %s and crf_version_id =5 and is_delete = 0""",
#              params=(1,))
#     def yy(self, meta: TestObj = None, **kwargs):
#         print(meta.id())
#
#
# if __name__ == '__main__':
#     Api().yy()
# Api().xx()
