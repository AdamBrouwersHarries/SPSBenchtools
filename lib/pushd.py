# from https://gist.github.com/Tatsh/7131812
from os import chdir, getcwd, remove
from os.path import realpath
import shutil 

# A set of useful temporary classes for use in "with ... :" statements to handle
# temporary directory change, and temporary file creation jobs.

# pushd/popd like behaviour for temporary directory change management
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

# wrapper function for PushdContext class. 
# example usage:
#   with pushd("directory") as d:
#       do something within d.cwd
#       ... 
#   now back at d.original_dir
def pushd(dirname):
    return PushdContext(dirname)

# Temporary file creation behaviour
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

# wrapper function for TempCopy class
# example usage:
#   with tempcopy("filesrc", "dst") as cp:
#       do something with cp.dst
#       ...
#   cp.dst now deleted
def tempcopy(src, dst):
    return TempCopy(src, dst)