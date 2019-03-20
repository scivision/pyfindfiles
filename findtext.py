#!/usr/bin/env python
r"""
Recursively find files containing text.
This method is slower than grep, but is cross-platform and easier syntax.

benchmarks:

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
import os
import logging
from pathlib import Path
import subprocess
import shutil
from binaryornot.check import is_binary
from typing import List, Union, Iterable
from argparse import ArgumentParser
try:
    import colorama
    MAGENTA = colorama.Back.MAGENTA
    BLACK = colorama.Back.BLACK
    colorama.init()
except ImportError:
    MAGENTA = BLACK = ''

MAXSIZE = 20e6  # [bytes]
EXT = ['*.py', '*.cfg', '*.ini',
       '*.txt', '*.pdf',
       '*.md', '*.rst',
       '*.tex',
       '*.cmake',
       '*.f', '*.f90', '*.for', '*.f95',
       '*.c', '*.h', '*.cpp', '*.cxx', '*.cc', '*.hpp',
       '*.m']

EXCLUDEDIR = ['_site', '.git', '.eggs', 'build', 'dist', '.mypy_cache', '.pytest_cache']


GREP = shutil.which('grep')
if not GREP:
    logging.warning('grep not found, cannot search binary files')


def findtext(root: Path, txt: str,
             globext: Union[str, Path, List[str]],
             exclude: List[str], verbose: bool):
    """
    multiple extensions with braces like Linux does not work in .rglob()
    """

    root = Path(root).expanduser()

    if isinstance(globext, (str, Path)):
        globext = [str(globext)]

    for ext in globext:
        searchlist(root.rglob(ext), txt, exclude, verbose)


def searchlist(flist: Union[List[Path], Iterable[Path]],
               txt: str, exclude: List[str],
               verbose: bool):

    mat = []
    exc = set(exclude)

    for f in flist:
        if exc.intersection(set(str(f.resolve()).split(os.sep))):
            continue
        # note that searchfile() does NOT work for PDF even with text inside...but Grep does. Hmm..
        if f.is_file() and f.stat().st_size < MAXSIZE:
            if not is_binary(str(f)):
                matches = searchfile(f, txt)
            elif f.suffix == '.pdf':
                matches = searchbinary(f, txt)
            else:
                logging.info('skipped {}'.format(f))
                continue

            if matches:
                mat.append(f)
                if verbose:
                    print(MAGENTA + str(f))
                    print(BLACK + '\n'.join(matches))
                else:
                    print(f)


def searchbinary(f: Path, txt: str) -> List[str]:
    # FIXME: use Python directly to make cross-platform Windows
    if not GREP:
        return []

    ret = subprocess.run([GREP, txt, f],
                         stdout=subprocess.PIPE)  # grep return 0 if match, 1 if no match

    return [ret.stdout]


def searchfile(fn: Path, txt: str) -> List[str]:
    """
    NO speedup observed from doing this first
    if not txt in str(f):
       return here,matchinglines
    """

    with fn.open('r', encoding='utf8', errors='ignore') as f:
        return ['{}: {}'.format(i, line) for i, line in enumerate(f) if txt in line]


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
