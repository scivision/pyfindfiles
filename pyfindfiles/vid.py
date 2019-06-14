from typing import Sequence, List, AsyncGenerator
from pathlib import Path
import asyncio

from . import FIND, DIR


def findvid(path: Path, ext: Sequence[str]) -> List[Path]:
    """
    recursive file search in Pure Python.
    about 10 times slower than Linux find, but platform-independent.
    """
    flist: List[Path] = []

    path = Path(path).expanduser()

    for e in ext:
        flist += list(path.glob(f'**/*{e}'))

    return flist


async def findvid_gnu(path: Path, exts: Sequence[str],
                      verbose: bool = False) -> AsyncGenerator[str, None]:
    """
    recursive file search using GNU find
    """
    path = Path(path).expanduser()

    assert isinstance(FIND, str)
    cmd = [FIND, str(path), '-type', 'f',
           '-regextype', 'posix-egrep',
           '-iregex', r'.*(' + r'|'.join(exts) + r')$']

    if verbose:
        print(' '.join(cmd))

    proc = await asyncio.create_subprocess_shell(' '.join(cmd), cwd=path,
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.DEVNULL)
    stdout, _ = await proc.communicate()

    for video in stdout.decode('utf8').split('\n'):
        yield video


async def findvid_win(path: Path, exts: Sequence[str]) -> AsyncGenerator[Path, None]:
    """
    asynchronously find files with extension

    Parameters
    ----------

    path : pathlib.Path
        root directory to recursively search under
    exts : list of str
        file extensions to look for

    Yields
    ------

    video: pathlib.Path
        path to video file
    """

    path = Path(path).expanduser()

    for ext in exts:
        cmd = [DIR, '/s', f'*{ext}']

        proc = await asyncio.create_subprocess_shell(' '.join(cmd), cwd=path,
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.DEVNULL)
        stdout, _ = await proc.communicate()

        for r in stdout.decode('utf8').split('\n'):
            if not r:
                continue

            el = r.split()
            if not el:
                continue

            if el[0].startswith('Directory'):
                d = Path(' '.join(el[2:]))
                continue

            if el[-1].endswith(ext):
                yield d/el[-1]
