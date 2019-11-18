#!/usr/bin/env python
r"""
Recursively find files containing text.
This method is slower than grep or findstr, but is cross-platform and easier syntax.

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
import shutil
import subprocess
from argparse import ArgumentParser

import pyfindfiles.text as pf

EXCLUDEDIR = ["_site", ".git", ".eggs", "build", "dist", ".mypy_cache", ".pytest_cache"]

# from colorama--works for Unix Terminal, PowerShell and Windows Terminal
MAGENTA = "\x1b[45m"
BLACK = "\x1b[40m"


def main():
    p = ArgumentParser(description="searches for TEXT under DIR and echos back filenames")
    p.add_argument("txt", help="text to search for")  # required
    p.add_argument("globext", help="filename glob", nargs="?", default=pf.TXTEXT)
    p.add_argument("dir", help="root dir to search", nargs="?", default=".")
    p.add_argument("-c", "--run", help="command to run on files e.g. notepad++")
    p.add_argument("-e", "--exclude", help="exclude files/dirs", nargs="+", default=EXCLUDEDIR)
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    files = pf.findtext(P.dir, P.txt, P.globext, P.exclude)

    flist = []
    if P.verbose:
        for fn, matches in files:
            flist.append(str(fn))
            print(MAGENTA + str(fn) + BLACK)
            for k, v in matches.items():
                print(k, ":", v)
    else:
        for fn, _ in files:
            flist.append(str(fn))
            print(fn)

    if P.run:
        exe = shutil.which(P.run)  # necessary for some Windows program e.g. VScode
        if exe:
            subprocess.run([exe] + flist)
        else:
            raise SystemExit("could not find {}".format(exe))


if __name__ == "__main__":
    main()
