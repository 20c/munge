
from collections import namedtuple
import collections
from urlparse import urlsplit
import os

import munge
import munge.util


# this wouldn't work with tabular data
# need metaclass to allow users to set info once on class
class Config(collections.MutableMapping):
    __defaults={
        'config': {},
        'conf_dir': None,
        'codec':  None,
    }

    def __init__(self, **kwargs):
        """
        accepts kwargs to set defaults
        data=dict to set initial data
        read=dir to open a dir
        """
        # use derived class defaults if available
        if hasattr(self, 'defaults'):
            derived_defaults = self.defaults
            self.defaults = self.__defaults
            self.defaults.update(derived_defaults)
        else:
            self.defaults = self.__defaults

        # override anything passed to kwargs
        for k,v in kwargs.items():
            if k in self.defaults:
                self.defaults[k] = v

        self.data = kwargs.get('data', self.default())
        self._meta_config_dir = ''

        if 'read' in kwargs:
            self.read(kwargs['read'])

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def default(self):
        return self.defaults['config'].copy()

    def reset(self):
        self.data = self.default()

    def read(self, conf_dir=None, reset=False):
        """ read config from conf_dir
            if conf_dir is None, reset to default config
        """

        if not conf_dir:
            if not self.defaults['conf_dir']:
                raise IOError("default config dir not set")

        conf_path = os.path.expanduser(conf_dir)
        if not os.path.exists(conf_path):
            raise IOError("config dir not found at %s" % (conf_path,))

        if reset:
            self.reset()

        config = munge.load_datafile('config', conf_path, default=None)
        if config:
            munge.util.recursive_update(self.data, config)
            #data['__config_dir__'] = conf_path

    def write(self, conf_dir=None, codec=None):
        if not codec:
            codec=munge.get_codec('yaml')()
        conf_dir = os.path.expanduser(conf_dir)
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)

        codec.dump(data, open(os.path.join(conf_dir, 'config.' + codec.extensions[0]), 'w'))


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

