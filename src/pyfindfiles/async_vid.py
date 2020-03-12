from pathlib import Path
import typing as T
import logging
import asyncio
import itertools


async def findvid_win_run(path: Path, exts: T.Sequence[str]) -> T.Iterator[Path]:
    futures = [findvid_win(path, ext) for ext in exts]
    return itertools.chain.from_iterable(filter(None, await asyncio.gather(*futures)))


async def findvid_win(path: Path, ext: str) -> T.List[Path]:
    """
    asynchronously find files with extension

    Parameters
    ----------

    path : pathlib.Path
        root directory to recursively search under
    ext : str
        file extension to look for

    Yields
    -------

    video: pathlib.Path
        path to video file
    """

    path = Path(path).expanduser()
    cmd = ["dir", "/s", "*" + ext]
    logging.debug(" ".join(cmd))
    # this has to be _shell due to that "dir" is part of Windows shell itself; _exec won't work.
    proc = await asyncio.create_subprocess_shell(
        " ".join(cmd), cwd=str(path), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
    )
    stdout, _ = await proc.communicate()

    flist = []
    for r in stdout.decode("utf8").split("\n"):
        if not r:
            continue

        el = r.split()
        if not el:
            continue

        if el[0].startswith("Directory"):
            d = Path(" ".join(el[2:]))
            continue

        if el[-1].endswith(ext):
            flist.append(d / el[-1])

    return flist
