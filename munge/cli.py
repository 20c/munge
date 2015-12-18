
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
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs=1, default='', help='input url')
    parser.add_argument('output', nargs=1, default='-', help='output url')
    parser.add_argument('--list-codecs', action='store_true', help='list all available codecs')

    return parser.parse_known_args(argv)


def main(argv=sys.argv):
    conf = config.MungeConfig()
    (args, left) = parse_args(argv[1:], conf)

    if getattr(args, 'list_codecs', False):
        print(munge.codec.list_codecs())
        return 0

    if hasattr(args, 'input'):
        instr = args.input[0]

        src = config.parse_url(instr, conf.get('addrbook', []))

    else:
        # check config
        pass

    if hasattr(args, 'output'):
        outstr = args.output[0]

        dst = config.parse_url(outstr, conf.get('addrbook', {}))

    data = src.cls().loadu(src.url.path)
    dst.cls().dumpu(data, dst.url.path)


