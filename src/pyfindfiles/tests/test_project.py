import pyfindfiles as pf


def test_find_project(tmp_path):

    r = tmp_path
    (r / "pyproject.toml").touch()

    langs = pf.detect_lang(r)

    assert len(langs) == 1
    assert "python" in langs
