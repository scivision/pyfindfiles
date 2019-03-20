from typing import List, Sequence
from pathlib import Path
import asyncio
import logging
import itertools

from . import DIR

TIMEOUT = 600  # seconds, arbitrary


async def findvid(path: Path, ext: Sequence[str]) -> List[Path]:
    """
    asynchronously find files with extension

    Parameters
    ----------

    path : pathlib.Path
        root directory to recursively search under
    ext : list of str
        file extensions to look for
    """

    futures = [_arbiter(path, e) for e in ext]

    flist = await asyncio.gather(*futures)

    return list(itertools.chain.from_iterable(flist))


async def _arbiter(path: Path, ext: str) -> List[Path]:

    try:
        flist = await asyncio.wait_for(_worker_win(path, ext), timeout=TIMEOUT)
    except (asyncio.TimeoutError, FileNotFoundError, PermissionError) as e:
        logging.error(f'{path}   {e}')
        flist = []

    return flist


async def _worker_win(path: Path, ext: str) -> List[Path]:

    path = Path(path).expanduser()
    flist = []
    cmd = [DIR, '/s', '*.'+ext]

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
        if el[-1].endswith('.'+ext):
            flist.append(d/el[-1])
            print(d/el[-1])

    return flist
