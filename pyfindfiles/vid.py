import typing
from pathlib import Path
import asyncio
import logging
import subprocess
import shutil


def findvid(path: Path, ext: typing.Sequence[str]) -> typing.List[Path]:
    """
    recursive file search in Pure Python.
    about 10 times slower than Linux find, but platform-independent.
    """
    flist = []  # type: typing.List[Path]

    path = Path(path).expanduser()

    for e in ext:
        flist += list(path.glob("**/*" + e))

    return flist


def findvid_gnu(path: Path, exts: typing.Sequence[str]) -> typing.List[str]:
    """
    recursive file search using GNU find
    """
    path = Path(path).expanduser()
    if isinstance(exts, str):
        exts = [exts]

    find = shutil.which("find")
    if not find:
        raise FileNotFoundError('could not find "find"')

    cmd = [
        find,
        str(path),
        "-type",
        "f",
        "-regextype",
        "posix-egrep",
        "-iregex",
        r".*(" + r"|".join(exts) + r")$",
    ]
    logging.debug(" ".join(cmd))

    stdout = subprocess.check_output(cmd, universal_newlines=True).strip()

    return stdout.split("\n")


async def findvid_win(path: Path, ext: str) -> typing.List[Path]:
    """
    asynchronously find files with extension

    Parameters
    ----------

    path : pathlib.Path
        root directory to recursively search under
    ext : str
        file extension to look for

    Returns
    -------

    video: pathlib.Path
        path to video file
    """

    path = Path(path).expanduser()
    cmd = ["dir", "/s", "*" + ext]
    logging.debug(" ".join(cmd))
    # this has to be _shell due to that "dir" is part of Windows shell itself; _exec won't work.
    proc = await asyncio.create_subprocess_shell(
        " ".join(cmd),
        cwd=str(path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
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
