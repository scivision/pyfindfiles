from typing import Sequence, List
from pathlib import Path
import subprocess
from . import FIND, DIR


def findvid(path: Path, ext: Sequence[str]) -> List[Path]:
    """
    recursive file search in Pure Python.
    about 10 times slower than Linux find, but platform-independent.
    """
    flist: List[Path] = []

    path = Path(path).expanduser()

    for e in ext:
        flist += list(path.glob('**/*.{}'.format(e)))

    return flist


def findvid_win(path: Path, ext: Sequence[str]) -> List[Path]:

    path = Path(path).expanduser()
    flist = []

    for e in ext:
        ret = subprocess.run([DIR, '/s', '*.'+e], universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL,
                             cwd=path, shell=True)

        for r in ret.stdout.split('\n'):
            if not r:
                continue
            el = r.split()
            if el[0].startswith('Directory'):
                d = Path(' '.join(el[2:]))
                continue
            if el[-1].endswith('.'+e):
                flist.append(d/el[-1])

    return flist


def findvid_gnu(path: Path, ext: Sequence[str], verbose: bool = False) -> List[Path]:
    """
    recursive file search using GNU find
    """
    path = Path(path).expanduser()

    assert isinstance(FIND, str)
    cmd = [FIND, str(path), '-type', 'f',
           '-regextype', 'posix-egrep',
           '-iregex', r'.*\.(' + '|'.join(ext) + ')$']

    if verbose:
        print(' '.join(cmd))

    ret = subprocess.run(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL,
                         universal_newlines=True)

    returncode: int = ret.returncode
    if returncode in (0, 1):
        pass
    else:
        raise OSError(returncode)

    return ret.stdout.split('\n')
