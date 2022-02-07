import os


class FileHelper(object):

    @classmethod
    def read(cls, *path):
        with open(os.path.join(*path), 'r') as f:
            return f.read()

    @classmethod
    def replace(cls, rep: dict, *path):
        with open(os.path.join(*path), 'r') as f:
            return f.read().format(**rep)

    @classmethod
    def readlines_str(cls, *path):
        with open(os.path.join(*path), 'r') as f:
            return [line.rstrip() for line in f.readlines()]

    @classmethod
    def readlines_int(cls, path: str):
        with open(path, 'r') as f:
            return [int(line.rstrip()) for line in f.readlines()]
