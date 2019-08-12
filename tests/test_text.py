#!/usr/bin/env python
import subprocess
import pytest
from pathlib import Path
import pyfindfiles as pf
import os

R = Path(__file__).parent
"""
TEST_STRING_TO_MATCH
"""


@pytest.mark.skipif(
    bool(os.environ.get("CI")), reason="CI does not like recursive search"
)
def test_script():
    ret = subprocess.check_output(
        ["findtext", "import"], universal_newlines=True, cwd=str(R)
    )

    assert isinstance(ret, str)

    assert len(ret) > 0


def test_mod():
    files = pf.findtext(R, "TEST_STRING_TO_MATCH", "*.py")

    for file, _ in files:
        assert file.samefile(__file__)


if __name__ == "__main__":
    pytest.main(["-x", __file__])
