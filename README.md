# PyFindFiles

![ci](https://github.com/scivision/pyfindfiles/workflows/ci/badge.svg)

[![pypi versions](https://img.shields.io/pypi/pyversions/pyfindfiles.svg)](https://pypi.python.org/pypi/pyfindfiles)
[![PyPi Download stats](http://pepy.tech/badge/pyfindfiles)](http://pepy.tech/project/pyfindfiles)

Find files (text or binary) containing text or patterns efficiently with Python, cross-platform.
Default is to only search files smaller than 10 MBytes.
Uses pipelining and asyncio to speed up operations.

## Install

Normally install by

```sh
pip install pyfindfiles
```

for latest development code

```sh
git clone https://github.com/scivision/pyfindfiles

pip install -e pyfindfiles
```

## Usage

`findtext` looks for strings inside text or binary files, and reports filename text is found in.

* `-v`: filename, line number, and text found
* `-t`: search for files newer than date, or between dates if two dates given.

```sh
findtext Pattern "*.ext" root
```

Pattern
: text to search for

"*.ext"
: file extension(s) to search for

root
: top-level directory to search under

---

`findvid`

`findvid root` looks under top-level directory `root` for video files (by common file extensions)
