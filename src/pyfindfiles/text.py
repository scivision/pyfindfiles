from __future__ import annotations
import os
from pathlib import Path
import typing as T
from datetime import datetime
from argparse import ArgumentParser
import dateutil.parser
import shutil
import subprocess
from . import MAGENTA, BLACK

EXCLUDEDIR = ["_site", ".git", ".eggs", "build", "dist", ".mypy_cache", ".pytest_cache"]

TXTEXT = [
    "*.py",
    "*.cfg",
    "*.ini",
    "*.txt",
    "*.md",
    "*.rst",
    "*.tex",
    "*.build",
    "*.cmake",
    "*.f",
    "*.f90",
    "*.for",
    "*.f95",
    "*.c",
    "*.h",
    "*.cpp",
    "*.cxx",
    "*.cc",
    "*.hpp",
    "*.m",
]

BINEXT = ["*.pdf"]

MAXSIZE = 10e6  # arbitrary, bytes


def findtext(
    root: Path,
    txt: str,
    *,
    globext: list[str],
    exclude: list[str] | None = None,
    age: list[datetime] | None = None,
) -> T.Iterator[tuple[Path, dict[int, str]]]:
    """
    multiple extensions with braces like Linux does not work in .rglob()
    """

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError(root)

    if isinstance(globext, (str, Path)):
        globext = [str(globext)]

    exc = set(exclude) if exclude else None

    for ext in globext:
        for fn in root.rglob(ext):
            if age is not None:
                finf = fn.stat()
                mt = datetime.utcfromtimestamp(finf.st_mtime)
                if mt < age[0]:
                    continue
                if len(age) == 2 and mt > age[1]:
                    continue

            if exc:
                excluded = exc.intersection(set(str(fn.resolve()).split(os.sep)))
                if excluded or not fn.is_file() or fn.stat().st_size > MAXSIZE:
                    continue

            try:
                with fn.open("r", encoding="utf8", errors="ignore") as f:
                    matches = {i: str(line) for i, line in enumerate(f) if txt in line}
            except PermissionError:
                continue

            if not matches:
                continue

            yield fn, matches


def cli():
    p = ArgumentParser(description="searches for TEXT under DIR and echos back filenames")
    p.add_argument("txt", help="text to search for")  # required
    p.add_argument("globext", help="filename glob", nargs="?", default=TXTEXT)
    p.add_argument("dir", help="root dir to search", nargs="?", default=".")
    p.add_argument("-t", "--time", help="newer than date or between dates", nargs="+")
    p.add_argument("-c", "--run", help="command to run on files e.g. notepad++")
    p.add_argument("-e", "--exclude", help="exclude files/dirs", nargs="+", default=EXCLUDEDIR)
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    # %% preflight
    root = Path(P.dir).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"{root} is not a directory.")

    if P.run:
        exe = shutil.which(P.run)  # necessary for some Windows program e.g. VScode
        if not exe:
            raise SystemExit(f"could not find {exe}")

    time = None
    if P.time:
        time = [dateutil.parser.parse(t) for t in P.time]
    # %% main
    for fn, matches in findtext(P.dir, P.txt, globext=P.globext, exclude=P.exclude, age=time):
        if P.verbose:
            print(MAGENTA + str(fn) + BLACK)
            for k, v in matches.items():
                print(k, ":", v)
        else:
            print(fn)

        if P.run:
            subprocess.run([exe, str(fn)])


if __name__ == "__main__":
    cli()
