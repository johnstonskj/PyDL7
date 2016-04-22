import argparse, dl7, json, sys

def parse_args():
    parser = argparse.ArgumentParser(description='Dump DL7 file')
    parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'),
                        help='DL7 file to read')
    return parser.parse_args()

def to_json(parsed):
    def to_dict(obj):
        return obj.__dict__
    
    print(json.dumps(parsed, default=to_dict, indent=2))

def main():
    args = parse_args()
    inputfile = args.file
    parsed = dl7.parse(inputfile)
    to_json(parsed)
