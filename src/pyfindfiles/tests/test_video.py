#!/usr/bin/env python
import pytest
from pathlib import Path
import subprocess
import sys

import pyfindfiles.vid as fv

if __file__ is None:
    R = None
else:
    R = Path(__file__).parent


@pytest.mark.skipif(R is None, reason="__file__ missing")
def test_findvid_serial():

    files = fv.findvid(R, ".avi")

    flist = list(files)
    print(flist)
    assert len(flist) == 2


@pytest.mark.skipif(R is None, reason="__file__ missing")
@pytest.mark.skipif(sys.platform != "linux", reason="Linux only test")
def test_findvid_gnu():

    files = list(fv.findvid_gnu(R, ".avi"))

    assert len(files) == 2


@pytest.mark.skipif(R is None, reason="__file__ missing")
def test_script():
    files = subprocess.check_output(["findvid", str(R)], universal_newlines=True).strip()
    flist = files.split("\n")
    print(flist)
    assert len(flist) == 2
