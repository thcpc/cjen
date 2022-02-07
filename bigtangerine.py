class BigTangerine(object):
    """
    TODO 规范调用的顺序，目前顺序比较乱，导致取值有错误 test_new_code_list.py 调换SuccessResp中procCode 上装饰器assert 和 one 的顺序就会导致失败
    主要的工作类，运行的对象需继承改类型，才能使用一系列装饰器
    定义的方法主要可以如下几种例子:
        针对 POST 请求
        def method_name(self, data, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)
        针对 GET 请求
        def method_name(self, params, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)
        针对 PUT
        def method_name(self, data, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)
        针对 url 中带有参数的请求,以 POST 请求为例
        def method_name(self, path_variable:dict, data, resp=None, meta_json:MetaJson=None, meta_mysql:MetaMysql=None, **kwargs)
    参数的解释
        data, params, path_variable 为请求参数，根据请求类型固定名称
        resp 为接口返回内容，参数名为固定
        meta_json: 可选参数 需搭配@orange.json.factory 使用
        meta_mysql: 可选参数 需搭配@orange.mysql.factory 使用
        ** kwarg: 固定写法
    """
    def __init__(self): ...

    def __new__(cls, *args, **kwargs):
        self = super(BigTangerine, cls).__new__(cls)
        self.headers = {}
        self.context = {}
        return self

    @classmethod
    def is_class(cls, instance):
        return isinstance(instance, BigTangerine)
