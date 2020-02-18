import typing as T
from pathlib import Path
import logging
import sys
import subprocess
import shutil


def findvid(path: Path, ext: T.Sequence[str]) -> T.Iterator[Path]:
    """
    recursive file search in Pure Python.
    about 10 times slower than Linux find, but platform-independent.
    """

    path = Path(path).expanduser()

    for e in ext:
        for file in path.glob("**/*" + e):
            yield file


def findvid_gnu(path: Path, exts: T.Sequence[str]) -> T.Iterator[str]:
    """
    recursive file search using GNU find
    """
    path = Path(path).expanduser()
    if isinstance(exts, str):
        exts = [exts]

    find = shutil.which("find")
    if not find:
        raise FileNotFoundError('could not find "find"')

    cmd = [find, str(path), "-type", "f"]

    if sys.platform != "darwin":
        cmd += ["-regextype", "posix-egrep"]

    cmd += ["-iregex", r".*(" + r"|".join(exts) + r")$"]

    logging.debug(" ".join(cmd))

    stdout = subprocess.check_output(cmd, universal_newlines=True).strip()

    for file in stdout.split("\n"):
        yield file
