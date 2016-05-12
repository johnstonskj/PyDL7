"""
This module implements a format handler that writes log data into
JSON in a direct representation of the Log objects in the divelog
module.
"""
import json

FORMAT_NAME = 'JSON'

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
    def to_dict(obj):
        d = obj.__dict__
        if 'metadata' in d:
            del d['metadata']
        return d

    json.dump(log, file, default=to_dict, indent=2)
