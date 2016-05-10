# PyDL7
Python API for parsing Dive Log files, primarily DAN DL7 format.

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
