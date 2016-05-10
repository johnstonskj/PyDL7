"""
This is only intended for the generation of a command-line tool, it isn't expected to 
be used as a module.
"""
import argparse, logging, sys
import divelog.files

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
    inmodule = divelog.files.get_module(inputfile.name)
    if not inmodule is None:
        parsed = inmodule.parse(inputfile)
    else:
        logger.error('could not find file handler for %s' % inputfile.name)
        sys.exit(1)
    outmodule = divelog.files.formats['JSON']
    if not outmodule is None:
        outmodule.dump(parsed, sys.stdout)
    else:
        logger.error('could not find file handler for format %s' % 'JSON')
        sys.exit(2)

if __name__ == '__main__':
    main()
