
import argparse
import sys
import munge
from munge import config


# options:
# input : source
# output : source

def get_config():
    return {}

def write_config(conf_dir='~/.munge'):
    print os.path.expanduser(conf_dir)

class ListCodecs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print("LIST CODECS", option_string)

def parse_args(argv, conf=None):
    print(">>>>", argv)

    parser = argparse.ArgumentParser()
    #parser.add_argument('-i', '--input', dest='input', action='store', help='input')
    #parser.add_argument('-o', '--output', dest='output', action='store', help='output')
    parser.add_argument('input', nargs='*', default='', help='input url')
    parser.add_argument('output', nargs='?', default='-', help='output url')

    #parser.add_argument('--list-codecs', action='store_true', help='list all available codecs')
    parser.add_argument('--list-codecs', action='store_true', help='list all available codecs')
    # add --write-config to make a skel config
#    config.write_config(conf)

    #args = parser.parse_args()
    return parser.parse_known_args(argv)


def main(argv=sys.argv):
    conf = config.get_config()
    (args, left) = parse_args(argv[1:], conf)

    if getattr(args, 'list_codecs', False):
        print(munge.codec.list_codecs())
        return 0

    if hasattr(args, 'input'):
        print args.input
        instr = args.input

        src = config.parse_url(instr, conf.get('addrbook', []))

    else:
        # check config
        pass

#    print(instr)
#    print(src)
#    print(src.url.username)
#    print('===================')


    if hasattr(args, 'output'):
        outstr = args.output

        dst = config.parse_url(outstr, conf.get('addrbook', {}))

#    print(instr)
#    print(src)
#    print(outstr)
#    print(dst)

    data = src.cls().loadu(src.url.path)
    dst.cls().dumpu(data, dst.url.path)
#    print(args.accumulate(args.integers))


