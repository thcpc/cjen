import time

import pytest

from cjen.tests.aiai.test_http import MockService


def read(file_name):
    start = time.perf_counter()
    with open(file_name, 'r') as f:
        f.read()
    print(time.perf_counter() - start)


if __name__ == '__main__':
    # pytest.main(["aiai/test_http.py::test_download", "aiai/test_http.py::test_put", "-n=2"])
    mock = MockService()
    read("download_file.txt")
    # for i in range(10):
        # mock.post_method_json(data=dict(username="xx", pwd="yyy"))
        # mock.get_method_variable(path_variable=dict(id=2))
    mock.get_method_variable(path_variable=dict(id=2))
    read("download_file.txt")
