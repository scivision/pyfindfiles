#!/usr/bin/env python
"""
recursively find video files based on extension.
"""
import sys
import logging
from pathlib import Path
from argparse import ArgumentParser

import pyfindfiles.vid as fv

VIDEXT = [".avi", ".mov", ".mp4", ".mpg", ".mpeg", ".webm", ".ogv", ".mkv", ".wmv"]


def main():
    p = ArgumentParser()
    p.add_argument("path", help="root path to start recursive search")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("-ext", help="video extension to search for", nargs="+", default=VIDEXT)
    P = p.parse_args()

    root = Path(P.path).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"{root} is not a directory.")

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if sys.platform == "linux":
        videos = fv.findvid_gnu(root, P.ext)
    else:
        videos = fv.findvid(root, P.ext)

    for video in videos:
        print(video)


if __name__ == "__main__":
    main()
