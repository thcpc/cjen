import os
from enum import unique, Enum

import requests
import yaml
from requests_toolbelt import MultipartEncoder

from cjen.bigtangerine import BigTangerine
from cjen.commons import _get_method_params
from cjen.exceptions import _check_uri, NetWorkErr, _check_instance


def _multipart_form(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        data_form = kwargs.get("data")
        files = {}
        others = {}
        for k, v in data_form.items():
            if os.path.exists(v):
                files[k] = v
            else:
                others[k] = v
        if not files: raise Exception("there is no file!")
        for k, v in files.items():
            with open(v, 'rb') as f:
                *rest, postfix = f.name.split(".")
                files[k] = (os.path.basename(f.name), f.read(), _file_type(file_postfix=f".{postfix}"))

        kwargs["form_data"] = MultipartEncoder(fields={**files, **others})
        ins.headers["Content-Type"] = kwargs["form_data"].content_type
        return func(ins, *args, **kwargs)

    return __inner__


def _file_type(*, file_postfix):
    with open(os.path.join(os.path.dirname(__file__), "file-content-type.yaml"), "r") as f:
        content_type = yaml.load(f.read(), Loader=yaml.FullLoader).get("ContentType")
        if content_type.get(file_postfix):
            return content_type.get(file_postfix)
    raise Exception(f"{file_postfix} can not support !")


@unique
class ContentType(Enum):
    JSON = "json"
    FILE_STREAM = "stream"


def _response(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):

        if kwargs.get("resp").status_code == 200:
            if "application/json" in kwargs.get("resp").headers.get("Content-Type"):
                kwargs["response_content"] = kwargs.get("resp")
                kwargs["resp"] = kwargs.get("resp").json() if kwargs.get("resp").content else None
                return func(ins, *args, **kwargs)
            kwargs["resp"] = kwargs.get("resp").content
            return func(ins, *args, **kwargs)
        else:
            raise NetWorkErr(f'{kwargs.get("url")} {kwargs.get("resp").status_code}')

    return __inner__


def _url(*, uri: str):
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            path_variable = kwargs.get("path_variable")
            kwargs["url"] = "/".join([ins.base_url, uri])
            if path_variable:
                kwargs["url"] = kwargs["url"].format(**path_variable)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def base_url(*, uri: str):
    def __wrapper__(func):
        def __inner__(ins: BigTangerine, *args, **kwargs):
            ins.__setattr__("base_url", uri)
            return func(ins, *args, **kwargs)

        return __inner__

    return __wrapper__


def _delete(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        headers = {**ins.headers, **kwargs.get("headers")} if kwargs.get("headers") else ins.headers
        if headers.get("Content-Type") and "json" in headers.get("Content-Type"):
            kwargs["resp"] = requests.delete(url=kwargs["url"], headers=headers, json=kwargs.get("data"))
        else: kwargs["resp"] = requests.delete(url=kwargs["url"], headers=headers, data=kwargs.get("data"))
        return func(ins, *args, **kwargs)

    return __inner__


def _get(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        headers = {**ins.headers, **kwargs.get("headers")} if kwargs.get("headers") else ins.headers
        kwargs["resp"] = requests.get(url=kwargs["url"], headers=headers,
                                      params=kwargs.get("params"))
        return func(ins, *args, **kwargs)

    return __inner__


def _post(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        headers = {**ins.headers, **kwargs.get("headers")} if kwargs.get("headers") else ins.headers
        if headers.get("Content-Type") and "json" in headers.get("Content-Type"):
            kwargs["resp"] = requests.post(url=kwargs["url"], headers=headers, json=kwargs.get("data"))
        elif headers.get("Content-Type") and "multipart/form-data" in headers.get("Content-Type"):
            kwargs["resp"] = requests.post(url=kwargs["url"], headers=headers, data=kwargs.get("form_data"))
        else:
            kwargs["resp"] = requests.post(url=kwargs["url"], headers=headers, data=kwargs.get("data"))
        return func(ins, *args, **kwargs)

    return __inner__


def _put(func):
    def __inner__(ins: BigTangerine, *args, **kwargs):
        headers = {**ins.headers, **kwargs.get("headers")} if kwargs.get("headers") else ins.headers
        if headers.get("Content-Type") and "json" in headers.get("Content-Type"):
            kwargs["resp"] = requests.put(url=kwargs["url"], headers=headers, json=kwargs.get("data"))
        else:
            kwargs["resp"] = requests.put(url=kwargs["url"], headers=headers, data=kwargs.get("data"))
        return func(ins, *args, **kwargs)

    return __inner__


def get_mapping(*, uri: str):
    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.get_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_get
        @_response
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def post_mapping(*, uri: str):
    """
    使用范围：BigTangerine 或其 子类对象
    位置：装饰函数的顶层装饰器
    发送 Post 请求，并返回结果
    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.post_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_post
        @_response
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def put_mapping(*, uri: str):
    """
    使用范围：BigTangerine 或其 子类对象
    位置：装饰函数的顶层装饰器
    发送 PUT 请求，并返回结果
    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.put_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_put
        @_response
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def upload_mapping(*, uri: str):
    """
    使用范围：BigTangerine 或其 子类对象
    位置：装饰函数的顶层装饰器
    发送 上传文件 请求，并返回结果
    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.upload_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_multipart_form
        @_post
        @_response
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__


def delete_mapping(*, uri: str):
    """
    使用范围：BigTangerine 或其 子类对象
    位置：装饰函数的顶层装饰器
    发送 delete 请求，并返回结果
    :param uri:
    :return:
    """

    def __wrapper__(func):
        @_get_method_params(method=func)
        @_check_instance(decorator="http.delete_mapping", expect=BigTangerine)
        @_check_uri(uri=uri)
        @_url(uri=uri)
        @_delete
        @_response
        def __inner__(ins: BigTangerine, *args, **kwargs):
            func(ins, *args, **kwargs)
            return kwargs.get("resp")

        return __inner__

    return __wrapper__
