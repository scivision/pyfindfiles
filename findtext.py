#!/usr/bin/env python
r"""
Recursively find files containing text.
This method is slower than grep or findstr, but is cross-platform and easier syntax.

For Windows, we require that you have Microsoft SysInternals "strings.exe" on your PATH,
which can be obtained from:

https://docs.microsoft.com/en-us/sysinternals/downloads/strings


## benchmarks:

time findtext xarray
18.6 sec

# note there are no "" on the command below. It's the equivalent of the defaults for the Python script.
time grep -r -l \
  --exclude-dir={\_site,\.git,\.eggs,build,dist,\.mypy_cache,.pytest_cache,*\.egg-info} \
  --include=*.{py,cfg,ini,txt,pdf,md,rst,tex,f,f90,for,f95,c,h,cpp,hpp,m} \
  xarray .
0.55 sec

---
time findtext xarray "*.py"
1.14 sec

time grep -r -l \
  --exclude-dir={\_site,\.git,\.eggs,build,dist,\.mypy_cache,.pytest_cache,*\.egg-info} \
  --include=*.py  xarray .
0.15 sec

"""
import io
import os
import logging
from pathlib import Path
import subprocess
import shutil
from binaryornot.check import is_binary
from typing import Dict, Iterable, IO, AnyStr
from argparse import ArgumentParser
try:
    import colorama
    MAGENTA = colorama.Back.MAGENTA
    BLACK = colorama.Back.BLACK
    colorama.init()
except ImportError:
    MAGENTA = BLACK = ''

MAXSIZE = 50e6  # [bytes]
EXT = ['*.py', '*.cfg', '*.ini',
       '*.txt', '*.pdf',
       '*.md', '*.rst',
       '*.tex',
       '*.cmake',
       '*.f', '*.f90', '*.for', '*.f95',
       '*.c', '*.h', '*.cpp', '*.cxx', '*.cc', '*.hpp',
       '*.m']

EXCLUDEDIR = ['_site', '.git', '.eggs', 'build', 'dist', '.mypy_cache', '.pytest_cache']


STRINGS = shutil.which('strings')
if not STRINGS:
    logging.warning('"strings" program not found, cannot search binary files')


def findtext(root: Path, txt: str,
             globext: Iterable[str],
             exclude: Iterable[str], verbose: bool):
    """
    multiple extensions with braces like Linux does not work in .rglob()
    """

    root = Path(root).expanduser()
    if not root.is_dir():
        raise NotADirectoryError('{} is not a directory'.format(root))

    if isinstance(globext, (str, Path)):
        globext = [str(globext)]

    for ext in globext:
        searchlist(root.rglob(ext), txt, exclude, verbose)


def searchlist(flist: Iterable[Path],
               txt: str, exclude: Iterable[str],
               verbose: bool):

    mat = []
    exc = set(exclude)

    for fn in flist:
        if (exc.intersection(set(str(fn.resolve()).split(os.sep)))
            or not fn.is_file()
                or fn.stat().st_size > MAXSIZE):
            continue

        if is_binary(str(fn)):
            raw = get_text(fn)
            matches = get_matches(io.StringIO(raw), txt)
        else:
            with fn.open('r', encoding='utf8', errors='ignore') as f:
                matches = get_matches(f, txt)

        if not matches:
            continue

        mat.append(fn)

        if verbose:
            print(MAGENTA + str(fn) + BLACK)
            for k, v in matches.items():
                print('{}: {}'.format(k, v))
        else:
            print(fn)


def get_text(f: Path) -> str:
    if not STRINGS:
        return ''

    return subprocess.run([STRINGS, str(f)], stdout=subprocess.PIPE,
                          universal_newlines=True).stdout


def get_matches(f: IO[AnyStr], txt: str) -> Dict[int, AnyStr]:
    """
    returns line number and matching line text
    """
    return {i: line for i, line in enumerate(f) if txt in line}


def main():
    p = ArgumentParser(description='searches for TEXT under DIR and echos back filenames')
    p.add_argument('txt', help='text to search for')  # required
    p.add_argument('globext', help='filename glob', nargs='?', default=EXT)
    p.add_argument('dir', help='root dir to search', nargs='?', default='.')
    p.add_argument('-e', '--exclude', help='exclude files/dirs', nargs='+', default=EXCLUDEDIR)
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    findtext(P.dir, P.txt, P.globext, P.exclude, P.verbose)


if __name__ == '__main__':
    main()
