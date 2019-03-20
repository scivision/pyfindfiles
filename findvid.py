#!/usr/bin/env python
"""
recursively find video files based on extension.
"""
import os
import asyncio
from argparse import ArgumentParser
import pyfindfiles.coro as psc
import pyfindfiles.sync as pss

VIDEXT = ['avi', 'mov', 'mp4', 'mpg', 'mpeg', 'webm', 'ogv', 'mkv', 'wmv']


def main():
    p = ArgumentParser()
    p.add_argument('path', help='root path to start recursive search',
                   nargs='?', default='.')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-ext', help='video extension to search for', nargs='+', default=VIDEXT)
    P = p.parse_args()

    if os.name == 'nt':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        flist = loop.run_until_complete(psc.findvid(P.path, P.ext))
    else:
        flist = pss.findvid_gnu(P.path, P.ext)

        print('\n'.join(map(str, flist)))


if __name__ == '__main__':
    main()
