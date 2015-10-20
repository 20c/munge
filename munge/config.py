
from collections import namedtuple
from urlparse import urlsplit
import os

import munge

config_schema = {
    'input': {
        'shortcut': 'i',
    },
    'output': {
        'shortcut': 'o',
    },
}


def get_config(conf_dir='~/.munge'):
    conf_dir = os.path.expanduser(conf_dir)
    if os.path.exists(conf_dir):
        data = munge.load_datafile('config', conf_dir, default=None)
        if data:
            return data

    return {}

def write_config(data, conf_dir='~/.munge', codec=None):
    if not codec:
        codec=munge.get_codec('yaml')()
    conf_dir = os.path.expanduser(conf_dir)
    if not os.path.exists(conf_dir):
        os.mkdir(conf_dir)

    codec.dump(data, open(os.path.join(conf_dir, 'config.' + codec.extensions[0]), 'w'))

class Endpoint(object):
    def __init__(self, data):
        pass

def get_type(name, extra_schemes={}):
    """
    cls: class ctor
    open: open func
    open_args: what to pass to open
    """
    if name in extra_schemes:
        return extra_schemes[name]

    codec = munge.get_codec(name)
    if codec:
        return {'cls': codec}

    return {}

def find_cls(name, extra_schemes={}):
    if name in extra_schemes:
        return munge.get_codec(extra_schemes[name]['type'])

    return munge.get_codec(name)

class MungeURL(namedtuple('MungeURL', 'cls url')):
    pass

# TODO change extra_schemes to full config dict
def parse_url(url, extra_schemes={}):
    """
    parse a munge url

    type:URL
    URL.type

    examples:
        file.yaml
        yaml:file.txt
        http://example.com/file.yaml
        yaml:http://example.com/file.txt

        mysql://user:password@localhost/database/table
        django:///home/user/project/settings_dir.settings/app_name/model
    """

    if not url:
        url = ""

    cls = None
    res = urlsplit(url)

    # check config first
    if res.scheme in extra_schemes:
        # TODO - nerge these with any existing and recurse
        addr = extra_schemes[res.scheme]
        if 'type' in addr:
            cls = find_cls(res.scheme, extra_schemes)
        if 'url' in addr:
            url = addr['url']
            if cls:
                res = urlsplit(url)
                return MungeURL(cls, res)
            # TODO - nerge these with any existing and recurse
            return parse_url(url)

    if res.scheme:
        cls = find_cls(res.scheme, extra_schemes)

    # check file extension
    if not cls:
        (rest, sep, ext) = url.rpartition('.')
        cls = find_cls(ext, extra_schemes)

        if not cls:
            raise ValueError('unable to find codec for %s' % url)

    return MungeURL(cls, res)

