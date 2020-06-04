from pathlib import Path
import json
import typing as T


def detect_lang(path: Path) -> T.List[str]:
    """ return lowercase language name, or empty if undetermined.

    Reference:
    https://help.github.com/en/github/visualizing-repository-data-with-graphs/
        listing-the-packages-that-a-repository-depends-on#supported-package-ecosystems
    """

    cmfn = path / "codemeta.json"
    if cmfn.is_file():
        meta = json.loads(cmfn.read_text(errors="ignore"))
        try:
            return [L.lower() for L in meta["programmingLanguage"]]
        except KeyError:
            pass
    # fallback to heuristic
    if (path / "pyproject.toml").is_file() or (path / "pipfile.lock").is_file():
        return ["python"]
    if (path / "package-lock.json").is_file() or (path / "yarn.lock").is_file():
        return ["javascript"]
    if (path / "composer.lock").is_file():
        return ["php"]
    if (path / "Gemfile.lock").is_file():
        return ["ruby"]

    return []
