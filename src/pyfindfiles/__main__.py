#!/usr/bin/env python
r"""
Recursively find files containing text.
This method is slower than grep or findstr, but is cross-platform and easier syntax.

## benchmarks:

time findtext xarray
18.6 sec

# note there are no "" on the command below.
# It's the equivalent of the defaults for the Python script.
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
from pathlib import Path
import shutil
import sys
import logging
import subprocess
from argparse import ArgumentParser
import dateutil.parser

from .text import findtext, TXTEXT
from .vid import findvid, findvid_gnu
from .project import detect_lang

EXCLUDEDIR = ["_site", ".git", ".eggs", "build", "dist", ".mypy_cache", ".pytest_cache"]

VIDEXT = [".avi", ".mov", ".mp4", ".mpg", ".mpeg", ".webm", ".ogv", ".mkv", ".wmv"]

# from colorama--works for Unix Terminal, PowerShell and Windows Terminal
MAGENTA = "\x1b[45m"
BLACK = "\x1b[40m"


def find_project():
    p = ArgumentParser(description="searches for projects with codemeta.json of specified language")
    p.add_argument("codelang", help="code language to search for")
    p.add_argument("dir", help="root dir to search")
    p.add_argument("-v", "--verbose", action="store_true")
    P = p.parse_args()

    # %% preflight
    root = Path(P.dir).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"{root} is not a directory.")

    req_lang = P.codelang.lower()

    dirs = (d for d in root.iterdir() if d.is_dir())

    for d in dirs:
        if req_lang in detect_lang(d):
            print(d)


def find_text():
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


def find_video():
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
