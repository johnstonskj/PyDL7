# PyDL7
Python API for parsing Dive Log files, primarily DAN DL7 format.

![Travis Status](https://travis-ci.org/johnstonskj/PyDL7.svg)

This package consists of a number of modules:

```
,-- divelog     --> the DiveLog classes
|   '-- files   --> file formats and extensions
|-- dl7         --> read/write DAN DL7 files
'-- dlson       --> read/write JSON files
```

The modules that read files, dl7, and dljson, both export functions of
the following form:

```python
def parse(file) --> divelog.Log

def dump(log, file)
```

The parser function will return either a top-level Log object that contains
separate Dive objects and their dive details. If there are parsing errors 
the function will return None.

The dump function will take a top-level Log object, and a file-like object 
and serialize the log to the file stream. This function does not close the
file object.

The divelog.files module helps to determine which of these formatting modules
to use for different file types. It contains a dictionary that maps from 
format names to the formatting module, and from known file extensions to the
file types. To aid in determining the correct formatting module for a file 
name the following function takes a file name and returns either the formatter
module, or None.

```python
def get_module(filename) --> formatter module
```

## Repositories


* [Github code repository](https://github.com/johnstonskj/PyDL7)
* [Travis build system[(https://travis-ci.org/johnstonskj/PyDL7)
* [Python Cheeseshop distribution[(https://pypi.python.org/pypi/PyDL7)
