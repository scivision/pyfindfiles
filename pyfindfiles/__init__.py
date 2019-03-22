from .text import findtext  # noqa: F401
import shutil

DIR = 'dir'  # not shutil.which since there isn't actually an exe for shell-intrinsic
FIND = shutil.which('find')
