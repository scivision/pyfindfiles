import os
from pathlib import Path
from typing import Dict, Iterable, Sequence, Tuple

TXTEXT = ['*.py', '*.cfg', '*.ini',
          '*.txt',
          '*.md', '*.rst',
          '*.tex',
          '*.cmake',
          '*.f', '*.f90', '*.for', '*.f95',
          '*.c', '*.h', '*.cpp', '*.cxx', '*.cc', '*.hpp',
          '*.m']

BINEXT = ['*.pdf', ]

MAXSIZE = 100e6  # arbitrary, bytes


def findtext(root: Path, txt: str,
             globext: Sequence[str],
             exclude: Sequence[str] = []) -> Iterable[Tuple[Path, Dict[int, str]]]:
    """
    multiple extensions with braces like Linux does not work in .rglob()
    """

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError(root)

    if isinstance(globext, (str, Path)):
        globext = [str(globext)]

    exc = set(exclude)

    for ext in globext:
        for fn in root.rglob(ext):
            excluded = exc.intersection(set(str(fn.resolve()).split(os.sep)))
            if excluded or not fn.is_file() or fn.stat().st_size > MAXSIZE:
                continue

            with fn.open('r', encoding='utf8', errors='ignore') as f:
                matches = {i: str(line) for i, line in enumerate(f) if txt in line}

            if not matches:
                continue

            yield fn, matches
