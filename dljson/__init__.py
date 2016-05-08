# Serializer for JSON

import json

def parse(file):
    pass

def dump(log, file):
    def to_dict(obj):
        d = obj.__dict__
        if 'metadata' in d:
            del d['metadata']
        return d

    json.dump(log, file, default=to_dict, indent=2)
