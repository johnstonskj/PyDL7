# PyDL7
Python API for parsing Dive Log files, primarily DAN DL7 format.

![Travis Status](https://travis-ci.org/johnstonskj/PyDL7.svg)

This package consists of a number of modules, note that either read or write
in parenthesis implies not yet implemented:

```
-- divelog     --> the DiveLog classes
   |-- files   --> file formats and extensions
   |-- dl7     --> read/write DAN DL7 files
   |-- json    --> (read)/write custom JSON files
   |-- html    --> write simple HTML file
   '-- uddf    --> (read)/(write) UDDF files
```

The modules that read and write files all export functions of the following 
form:

```python
def parse(file) : Log

def dump(log : Log, file)
```

The `parse` function will return either a top-level `Log` object that contains
separate `Dive` objects and their dive details. If there are parsing errors 
the function will return `None`.

The `dump` function will take a top-level `Log` object, and a file-like object 
and serialize the log to the file stream. This function does not close the
file object.

The `divelog.files` module helps to determine which of these formatting modules
to use for different file types. It contains a dictionary that maps from 
format names to the formatting module, and from known file extensions to the
file types. To aid in determining the correct formatting module for a file 
name the following function takes a file name and returns either the formatter
module, or `None`.

```python
def get_module(filename) : formatter module
```

## Command Line Tool

The module `divelog.command_line` is used to create a tool called `dl7dump` 
that can be used to dump the contents of a divelog, and do some conversion
between supported formats. The following is the format for the command, and
it's arguments.

```bash
usage: command_line.py [-h] [--verbose] [--readformat {HTML,DL7,JSON}]
                       [--writeformat {HTML,DL7,JSON}] [--outfile OUTFILE]
                       FILE

Dump DL7 file

positional arguments:
  FILE                  DL7 file to read

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         turn on verbose logging
  --readformat {HTML,DL7,JSON}, -r {HTML,DL7,JSON}
                        what format to expect to read (will try and guess if
                        not specified)
  --writeformat {HTML,DL7,JSON}, -w {HTML,DL7,JSON}
                        what format to write out (default is JSON)
  --outfile OUTFILE, -o OUTFILE
                        name of file to write to, if not specified, writes to
                        stdout
```

The most basic form, `dl7dump divelog.zxu` will convert from the DL7 format to
a simply JSON form and display on stdout.

## Repositories

* [Github code repository](https://github.com/johnstonskj/PyDL7)
* [Travis CI build and test](https://travis-ci.org/johnstonskj/PyDL7)
* [Python Cheeseshop distribution](https://pypi.python.org/pypi/PyDL7)
