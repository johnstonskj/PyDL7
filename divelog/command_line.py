import argparse, dl7, dljson, logging, sys

FORMAT = '%(name)s:%(module)s.%(funcName)s[%(lineno)d] %(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='Dump DL7 file')
    parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'),
                        help='DL7 file to read')
    parser.add_argument('--verbose', '-v', action='store_true')
    return parser.parse_args()

def main():
    logger.info('starting...')
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug(args.file)
    inputfile = args.file
    parsed = dl7.parse(inputfile)
    dljson.dump(parsed, sys.stdout)

if __name__ == '__main__':
    main()
