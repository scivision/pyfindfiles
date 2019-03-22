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
from argparse import ArgumentParser

import pyfindfiles as pf

EXT = ['*.py', '*.cfg', '*.ini',
       '*.txt', '*.pdf',
       '*.md', '*.rst',
       '*.tex',
       '*.cmake',
       '*.f', '*.f90', '*.for', '*.f95',
       '*.c', '*.h', '*.cpp', '*.cxx', '*.cc', '*.hpp',
       '*.m']

EXCLUDEDIR = ['_site', '.git', '.eggs', 'build', 'dist', '.mypy_cache', '.pytest_cache']


def main():
    p = ArgumentParser(description='searches for TEXT under DIR and echos back filenames')
    p.add_argument('txt', help='text to search for')  # required
    p.add_argument('globext', help='filename glob', nargs='?', default=EXT)
    p.add_argument('dir', help='root dir to search', nargs='?', default='.')
    p.add_argument('-e', '--exclude', help='exclude files/dirs', nargs='+', default=EXCLUDEDIR)
    p.add_argument('-v', '--verbose', action='store_true')
    P = p.parse_args()

    mat = pf.findtext(P.dir, P.txt, P.globext, P.exclude, P.verbose)

    assert isinstance(mat, dict)

    if not P.verbose:
        for k, v in mat.items():
            print(k)


if __name__ == '__main__':
    main()
