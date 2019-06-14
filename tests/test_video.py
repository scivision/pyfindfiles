#!/usr/bin/env python
import pytest
from pathlib import Path

import pyfindfiles.vid as fv

R = Path(__file__).parent


def test_findvid():

    files = fv.findvid(R, '.avi')

    flist = list(files)
    assert len(flist) == 2


if __name__ == '__main__':
    pytest.main([__file__])
