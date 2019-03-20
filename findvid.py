#!/usr/bin/env python
"""
recursively find video files based on extension.
"""
import os
from pathlib import Path
import subprocess
from argparse import ArgumentParser
import shutil
from typing import Sequence, List

FIND = shutil.which('find')
DIR = 'dir'  # not shutil.which since there isn't actually an exe for shell-intrinsic

VIDEXT = ['avi', 'mov', 'mp4', 'mpg', 'mpeg', 'webm', 'ogv', 'mkv', 'wmv']


def findvid(path: Path, ext: Sequence[str]):
    """
    recursive file search in Pure Python.
    about 10 times slower than Linux find, but platform-independent.

    can break on Windows with FileNotFoundError
    """

    path = Path(path).expanduser()

    for e in ext:
        flist = list(path.glob('**/*.{}'.format(e)))
        if not flist:
            continue

        print('\n'.join(map(str, flist)))


def findvid_win(path: Path, ext: Sequence[str]) -> List[Path]:

    path = Path(path).expanduser()
    flist = []

    for e in ext:
        ret = subprocess.run([DIR, '/s', '*.'+e], universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL,
                             cwd=path, shell=True)

        for r in ret.stdout.split('\n'):
            if not r:
                continue
            el = r.split()
            if el[0].startswith('Directory'):
                d = Path(' '.join(el[2:]))
                continue
            if el[-1].endswith('.'+e):
                flist.append(d/el[-1])
                print(d/el[-1])

    return flist


def findvid_linux(path: Path, ext: Sequence[str], verbose: bool = False) -> List[Path]:
    """
    recursive file search using GNU find
    """
    path = Path(path).expanduser()

    assert isinstance(FIND, str)
    cmd = [FIND, str(path), '-type', 'f',
           '-regextype', 'posix-egrep',
           '-iregex', r'.*\.(' + '|'.join(ext) + ')$']

    if verbose:
        print(' '.join(cmd))

    ret = subprocess.run(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL,
                         universal_newlines=True)

    returncode: int = ret.returncode
    if returncode in (0, 1):
        pass
    else:
        raise OSError(returncode)

    vids = ret.stdout.split('\n')
    if vids:
        print('\n'.join(vids))

    return vids


def main():
    p = ArgumentParser()
    p.add_argument('path', help='root path to start recursive search',
                   nargs='?', default='.')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-ext', help='video extension to search for', nargs='+', default=VIDEXT)
    P = p.parse_args()

    if os.name == 'nt':
        findvid_win(P.path, P.ext)
    else:
        findvid_linux(P.path, P.verbose)


if __name__ == '__main__':
    main()
