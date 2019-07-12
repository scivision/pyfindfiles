[![Build Status](https://travis-ci.com/scivision/pyfindfiles.svg?branch=master)](https://travis-ci.com/scivision/pyfindfiles)
[![Coverage Status](https://coveralls.io/repos/github/scivision/pyfindfiles/badge.svg?branch=master)](https://coveralls.io/github/scivision/pyfindfiles?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/bcakhhoaj4uv5ec3?svg=true)](https://ci.appveyor.com/project/scivision/pyfindfiles)
[![pypi versions](https://img.shields.io/pypi/pyversions/pyfindfiles.svg)](https://pypi.python.org/pypi/pyfindfiles)
[![PyPi Download stats](http://pepy.tech/badge/pyfindfiles)](http://pepy.tech/project/pyfindfiles)

# PyFindFiles

Find files (text or binary) containing text or patterns efficiently with Python, cross-platform.
Default is to only search files smaller than 100 MBytes.
Uses pipelining and asyncio to speed up operations.


## Install

```sh
git clone https://github.com/scivision/pyfindfiles

cd pyfindfiles

python -m pip install -e .
```

## Usage

`findtext` looks for strings inside text or binary files, and reports filename text is found in.

* `-v`: filename, line number, and text found


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

