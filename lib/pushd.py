# from https://gist.github.com/Tatsh/7131812
from os import chdir, getcwd, remove
from os.path import realpath
import shutil 


class PushdContext:
    cwd = None
    original_dir = None

    def __init__(self, dirname):
        self.cwd = realpath(dirname)

    def __enter__(self):
        self.original_dir = getcwd()
        chdir(self.cwd)
        return self

    def __exit__(self, type, value, tb):
        chdir(self.original_dir)

def pushd(dirname):
    return PushdContext(dirname)


class TempCopy:
    src = None
    dst = None
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __enter__(self):
        shutil.copyfile(self.src, self.dst)
        return self

    def __exit__(self, type, value, tb):
        remove(self.dst)

def tempcopy(src, dst):
    return TempCopy(src, dst)