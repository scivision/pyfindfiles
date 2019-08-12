#!/usr/bin/env python
"""
recursively find video files based on extension.
"""
import os
import logging
from pathlib import Path
import typing
import asyncio
from argparse import ArgumentParser
import itertools

import pyfindfiles.vid as fv
from pyfindfiles.runner import runner

VIDEXT = [".avi", ".mov", ".mp4", ".mpg", ".mpeg", ".webm", ".ogv", ".mkv", ".wmv"]


async def findvid_win(path: Path, exts: typing.Sequence[str]) -> typing.Iterator[Path]:
    futures = [fv.findvid_win(path, ext) for ext in exts]
    return itertools.chain.from_iterable(filter(None, await asyncio.gather(*futures)))


def main():
    p = ArgumentParser()
    p.add_argument("path", help="root path to start recursive search")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument(
        "-ext", help="video extension to search for", nargs="+", default=VIDEXT
    )
    P = p.parse_args()

    if P.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if os.name == "nt":
        videos = runner(findvid_win, P.path, P.ext)
    else:
        videos = fv.findvid_gnu(P.path, P.ext)

    for video in videos:
        print(video)


if __name__ == "__main__":
    main()
