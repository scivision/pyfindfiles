#!/usr/bin/env python
"""
recursively find video files based on extension.
"""
import os
from argparse import ArgumentParser
import pyfindfiles.sync as ps

VIDEXT = ['avi', 'mov', 'mp4', 'mpg', 'mpeg', 'webm', 'ogv', 'mkv', 'wmv']


def main():
    p = ArgumentParser()
    p.add_argument('path', help='root path to start recursive search',
                   nargs='?', default='.')
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-ext', help='video extension to search for', nargs='+', default=VIDEXT)
    P = p.parse_args()

    if os.name == 'nt':
        flist = ps.findvid_win(P.path, P.ext)
    else:
        flist = ps.findvid_gnu(P.path, P.ext)

    print('\n'.join(map(str, flist)))


if __name__ == '__main__':
    main()
