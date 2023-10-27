import pathlib


class PathUtils:
    @staticmethod
    def project_path(current, name) -> pathlib.Path:
        path = pathlib.Path(current).parent
        while path.name != name:
            path = path.parent
        return path
