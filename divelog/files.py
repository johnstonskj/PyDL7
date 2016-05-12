"""
This module provides a simple mechanism for dealing with multiple dive log
formats in files, specifically it maintains a mapping from format name to
a module that handles that format, and a mapping from known file extensions
to format names.

Format handlers are modules that implement the following pair of functions:

    def parse(file) --> Log
    def dump(log, file)

These allow for reading and writing files in a specific format.
"""
import os.path
import divelog.dl7, divelog.json, divelog.html

formats = {
    divelog.json.FORMAT_NAME: divelog.json,
    divelog.dl7.FORMAT_NAME:  divelog.dl7,
    divelog.html.FORMAT_NAME: divelog.html
    }

extensions = {
    'json': divelog.json.FORMAT_NAME,
    'ztr':  divelog.dl7.FORMAT_NAME,     # PDE Registration
    'zxu':  divelog.dl7.FORMAT_NAME,     # Dive Profile
    'zxl':  divelog.dl7.FORMAT_NAME,     # Diver Demographics, Dive Profile, Dive Log
    'zma':  divelog.dl7.FORMAT_NAME,     # Medical Report Add
    'zmu':  divelog.dl7.FORMAT_NAME      # Medical Report Update
}

def get_module(filename):
    """
    This function will return the correct format handler module for a given
    file name. It uses the file extension to determine the format and then
    the module from the format. If no format handler exists for the file
    format, or the format cannot be determined, the value is None.
    """
    pair = os.path.splitext(filename)
    if pair[1] and pair[1][0] == '.':
        extension = pair[1][1:].lower()
        if extension in extensions:
            return formats[extensions[extension]]
    return None
