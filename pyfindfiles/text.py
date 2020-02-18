import os
from pathlib import Path
import typing as T
from datetime import datetime

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
    root: Path, txt: str, *, globext: T.Sequence[str], exclude: T.Sequence[str] = None, age: T.Sequence[datetime] = None,
) -> T.Iterator[T.Tuple[Path, T.Dict[int, str]]]:
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

            with fn.open("r", encoding="utf8", errors="ignore") as f:
                matches = {i: str(line) for i, line in enumerate(f) if txt in line}

            if not matches:
                continue

            yield fn, matches
