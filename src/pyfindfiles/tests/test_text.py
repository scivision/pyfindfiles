#!/usr/bin/env python
import subprocess
import pytest
import pyfindfiles as pf
import os
from datetime import datetime

"""
TEST_STRING_TO_MATCH
"""


@pytest.mark.skipif(bool(os.environ.get("CI")), reason="CI does not like recursive search")
def test_script(tmp_path):
    (tmp_path / "foo.py").write_text("import datetime")
    ret = subprocess.check_output(["findtext", "import", "*.py", str(tmp_path)], universal_newlines=True)

    assert isinstance(ret, str)

    assert len(ret) > 0


def test_glob(tmp_path):

    fn = tmp_path / "foo.py"
    fn.write_text("MATCH_ME_NOW_PLEASE")

    files = pf.findtext(tmp_path, "MATCH_ME_NOW", globext="*.py")

    for file, _ in files:
        assert file.samefile(fn)


def test_age(tmp_path):

    fn = tmp_path / "foo.py"
    fn.write_text("MATCH_ME_NOW_PLEASE")

    files = pf.findtext(tmp_path, "MATCH_ME_NOW", globext="*.py", age=[datetime(2019, 1, 1)])

    for file, _ in files:
        assert file.samefile(fn)
