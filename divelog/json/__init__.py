"""
This module implements a format handler that writes log data into
JSON in a direct representation of the Log objects in the divelog
module.
"""
import datetime
import json

import divelog

FORMAT_NAME = 'JSON'


def parse(file):
    """
    Parse this file object and return either a new top-level Log
    object, or None.
    """
    def copy_obj(src, tgt, ignore):
        for key in src:
            if not key == ignore:
                setattr(tgt, key, src[key])
    log = divelog.Log()
    jobj = json.load(file)
    copy_obj(jobj, log, 'dives')
    for jdive in jobj['dives']:
        dive = divelog.Dive()
        log.dives.append(dive)
        copy_obj(jdive, dive, 'record')
        for jdet in jdive['record']:
            detail = divelog.DiveDetail()
            dive.record.append(detail)
            copy_obj(jdet, detail, None)
    return log

def dump(log, file):
    """
    Serialize the log to the provided file object.
    """
    def to_dict(obj):
        if isinstance(obj, datetime.datetime):
            return obj.replace(tzinfo=datetime.timezone.utc).timestamp()
        else:
            d = obj.__dict__
            if 'metadata' in d:
                del d['metadata']
            return d
    json.dump(log, file, default=to_dict, indent=2)
