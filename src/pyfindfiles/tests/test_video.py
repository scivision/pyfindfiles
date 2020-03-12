#!/usr/bin/env python
import pytest
from pathlib import Path
import subprocess
import sys

import pyfindfiles.vid as fv

R = Path(__file__).parent


def test_findvid_serial():

    files = fv.findvid(R, ".avi")

    flist = list(files)
    print(flist)
    assert len(flist) == 2


@pytest.mark.skipif(sys.platform != "linux", reason="Linux only test")
def test_findvid_gnu():

    files = list(fv.findvid_gnu(R, ".avi"))

    assert len(files) == 2


def test_script():
    files = subprocess.check_output(["findvid", str(R)], universal_newlines=True).strip()
    flist = files.split("\n")
    print(flist)
    assert len(flist) == 2


if __name__ == "__main__":
    pytest.main([__file__])
