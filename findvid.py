#!/usr/bin/env python
"""
recursively find video files based on extension.
"""
import os
import sys
import asyncio
from pathlib import Path
from typing import Sequence
from argparse import ArgumentParser
import pyfindfiles.vid as fv

VIDEXT = ['.avi', '.mov', '.mp4', '.mpg', '.mpeg', '.webm', '.ogv', '.mkv', '.wmv']


async def findvid_win(path: Path, ext: Sequence[str]):
    async for video in fv.findvid_win(path, ext):
        print(video)


async def findvid_gnu(path: Path, ext: Sequence[str], verbose: bool):
    async for video in fv.findvid_gnu(path, ext, verbose):
        print(video)


def main():
    p = ArgumentParser()
    p.add_argument('path', help='root path to start recursive search',
                   nargs='?', default='.')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-ext', help='video extension to search for', nargs='+', default=VIDEXT)
    P = p.parse_args()

    if os.name == 'nt':
        if sys.version_info < (3, 8):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        asyncio.run(findvid_win(P.path, P.ext))
    else:
        asyncio.run(findvid_gnu(P.path, P.ext, P.verbose))


if __name__ == '__main__':
    main()
