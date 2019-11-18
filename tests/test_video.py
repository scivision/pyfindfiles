#!/usr/bin/env python
import pytest
from pathlib import Path
import subprocess
import os

import pyfindfiles.vid as fv
from pyfindfiles.runner import runner

R = Path(__file__).parent


def test_findvid_serial():

    files = fv.findvid(R, ".avi")

    flist = list(files)
    assert len(flist) == 2


def test_findvid_concurrent():
    if os.name == "nt":
        files = runner(fv.findvid_win, R, ".avi")
    else:
        files = fv.findvid_gnu(R, ".avi")
    assert len(files) == 2


def test_script():
    files = subprocess.check_output(["findvid", str(R)], universal_newlines=True).strip()
    assert len(files.split("\n")) == 2


if __name__ == "__main__":
    pytest.main([__file__])
