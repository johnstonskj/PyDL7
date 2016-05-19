"""
This is only intended for the generation of a command-line tool, it isn't
expected to be used as a module.
"""
import argparse
import logging
import sys

import divelog.files


FORMAT = ('%(name)s:%(module)s.%(funcName)s[%(lineno)d]' +
          '%(levelname)-8s %(message)s')
logging.basicConfig(format=FORMAT, level=logging.WARN)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='Dump DL7 file')
    parser.add_argument('file', metavar='FILE', type=argparse.FileType('r'),
                        help='DL7 file to read')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='turn on verbose logging')
    parser.add_argument('--readformat', '-r', choices=divelog.files.formats,
                        help='what format to expect to read')
    parser.add_argument('--writeformat', '-w', choices=divelog.files.formats,
                        help='what format to write out (default is JSON)')
    parser.add_argument('--outfile', '-o', type=argparse.FileType('w'),
                        help='name of file to write to, or stdout')
    return parser.parse_args()


def main():
    logger.info('starting...')
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug(args.file)
    inputfile = args.file
    if args.readformat:
        inmodule = divelog.files.formats[args.readformat]
    else:
        inmodule = divelog.files.get_module(inputfile.name)
    if inmodule is not None:
        parsed = inmodule.parse(inputfile)
    else:
        logger.error('could not find file handler for %s' % inputfile.name)
        sys.exit(1)
    if args.writeformat:
        outmodule = divelog.files.formats[args.writeformat]
    else:
        outmodule = divelog.files.formats['JSON']
    if outmodule is not None:
        if args.outfile:
            outmodule.dump(parsed, args.outfile)
        else:
            outmodule.dump(parsed, sys.stdout)
    else:
        logger.error('could not find file handler for format %s' % 
                     (args.writeformat or 'JSON'))
        sys.exit(2)

if __name__ == '__main__':
    main()
