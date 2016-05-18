"""
This module implements a format handler that writes log data into
the UDDF (not UDCF) format.

http://www.streit.cc/dive/
"""

FORMAT_NAME = 'UDDF'

def parse(file):
    """
    Parse this file object and return either a new top-level Log
    object, or None.
    """
    pass

def dump(log, file):
    """
    Serialize the log to the provided file object.
    """
    pass
