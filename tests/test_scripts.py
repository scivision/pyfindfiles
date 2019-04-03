#!/usr/bin/env python
import subprocess
import pytest
from pathlib import Path
import pyfindfiles as pf

R = Path(__file__).parent


def test_script():
    ret = subprocess.check_output(['findtext', 'import'], universal_newlines=True,
                                  cwd=str(R))

    assert isinstance(ret, str)

    assert len(ret) > 0


def test_mod():
    mat = pf.findtext(R, 'import', '*.py')

    for k, v in mat.items():
        assert k.samefile(__file__)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
