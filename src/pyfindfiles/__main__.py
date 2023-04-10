#!/usr/bin/env python3
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
from argparse import ArgumentParser

from .project import detect_lang


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
