import os
import logging
from pathlib import Path
import shutil
from typing import Dict, Iterable, IO, AnyStr

# from colorama, would need Win32 calls for Windows Command Prompt
if os.name != 'nt':
    MAGENTA = '\x1b[45m'
    BLACK = '\x1b[40m'
else:
    MAGENTA = BLACK = ''

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

STRINGS = shutil.which('strings')
if not STRINGS:
    logging.warning('"strings" program not found, cannot search binary files')


def findtext(root: Path, txt: str,
             globext: Iterable[str],
             exclude: Iterable[str] = [],
             verbose: bool = False) -> Dict[Path, Dict[int, str]]:
    """
    multiple extensions with braces like Linux does not work in .rglob()
    """

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError('{} is not a directory'.format(root))

    if isinstance(globext, (str, Path)):
        globext = [str(globext)]

    mat = {}

    for ext in globext:
        mat.update(searchlist(root.rglob(ext), txt, exclude, verbose))

    return mat


def searchlist(flist: Iterable[Path],
               txt: str,
               exclude: Iterable[str],
               verbose: bool) -> Dict[Path, Dict[int, str]]:

    mat = {}
    exc = set(exclude)

    for fn in flist:
        excluded = exc.intersection(set(str(fn.resolve()).split(os.sep)))
        if excluded or not fn.is_file() or fn.stat().st_size > MAXSIZE:
            continue

        with fn.open('r', encoding='utf8', errors='ignore') as f:
            matches = get_matches(f, txt)

        if not matches:
            continue

        mat[fn] = matches

        if verbose:
            print(MAGENTA + str(fn) + BLACK)
            for k, v in matches.items():
                print(k, ':', v)

    return mat


def get_matches(f: IO[AnyStr], txt: str) -> Dict[int, str]:
    """
    returns line number and matching line text
    """
    return {i: str(line) for i, line in enumerate(f) if txt in line}
