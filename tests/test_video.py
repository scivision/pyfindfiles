#!/usr/bin/env python
import pytest
import os
from pathlib import Path

import pyfindfiles.vid as fv

R = Path(__file__).parent


def test_findvid():

    files = fv.findvid(R, '.avi')

    flist = list(files)
    assert len(flist) == 2
