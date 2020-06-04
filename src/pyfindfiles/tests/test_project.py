import pytest
from pathlib import Path
import pyfindfiles as pf

R = Path(__file__).resolve().parents[3]


def test_find_project():

    langs = pf.detect_lang(R)

    assert len(langs) == 1
    assert "python" in langs


if __name__ == "__main__":
    pytest.main([__file__])
