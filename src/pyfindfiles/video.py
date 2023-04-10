from __future__ import annotations
import typing as T
from pathlib import Path
import logging
import sys
import subprocess
import shutil
from argparse import ArgumentParser

VIDEXT = [".avi", ".mov", ".mp4", ".mpg", ".mpeg", ".webm", ".ogv", ".mkv", ".wmv"]


def findvid(path: Path, ext: list[str]) -> T.Iterator[Path]:
    """
    recursive file search in Pure Python.
    about 10 times slower than Linux find, but platform-independent.
    """

    path = Path(path).expanduser()

    for e in ext:
        for file in path.glob("**/*" + e):
            yield file


def findvid_gnu(path: Path, exts: list[str]) -> T.Iterator[str]:
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


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("path", help="root path to start recursive search")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-ext", help="video extension to search for", nargs="+", default=VIDEXT)
    P = p.parse_args()

    root = Path(P.path).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if sys.platform == "linux":
        videos = findvid_gnu(root, P.ext)
    else:
        videos = findvid(root, P.ext)

    for video in videos:
        print(video)
