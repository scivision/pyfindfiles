#!/usr/bin/env python
"""
recursively find video files based on extension.
"""
from argparse import ArgumentParser
import pyfindfiles.vid as ps

VIDEXT = ["avi", "mov", "mp4", "mpg", "mpeg", "webm", "ogv", "mkv", "wmv"]


def main():
    p = ArgumentParser()
    p.add_argument(
        "path", help="root path to start recursive search", nargs="?", default="."
    )
    p.add_argument(
        "-ext", help="video extension to search for", nargs="+", default=VIDEXT
    )
    P = p.parse_args()

    flist = ps.findvid(P.path, P.ext)

    print("\n".join(map(str, flist)))


if __name__ == "__main__":
    main()
