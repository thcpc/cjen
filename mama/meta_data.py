class MetaData(object):
    def __init__(self):
        self.cols = list(filter(
            lambda method: callable(getattr(self, method)) and not method.startswith("_") and not method.endswith(
                "_") and method != "factory" and method != "is_class"
            ,
            dir(self)))
        self.meta_data = dict.fromkeys(self.cols, None)
        self.meta_source = None
        self.context = {}

    @classmethod
    def is_class(cls, instance):
        return isinstance(instance, MetaData)

    @staticmethod
    def factory(*, clazz, data):
        meta = clazz()
        meta.meta_source = data
        print("1")
        return meta


class MetaJson(MetaData): ...


class MetaMysql(MetaData): ...
