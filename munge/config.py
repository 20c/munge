
from collections import namedtuple
import collections
from urlparse import urlsplit
import os

import munge
import munge.util


# this wouldn't work with tabular data
# need metaclass to allow users to set info once on class
# TODO rename to BaseConfig
class Config(collections.MutableMapping):
    # internal base for defaults
    _base_defaults={
        'config': {},
        'config_dir': None,
        'codec':  None,

        'autowrite': False,
        'validate': False,
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
            self.defaults = self._base_defaults.copy()
            self.defaults.update(derived_defaults)
        else:
            self.defaults = self._base_defaults.copy()

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

    def get_nested(self, *args):
        """
        get a nested value, returns None if path does not exist
        """
        data = self.data
        for key in args:
            if key not in data:
                return None
            data = data[key]
        return data

    def default(self):
        return self.defaults['config'].copy()

    def clear(self):
        self.data = self.default()

    def read(self, config_dir=None, clear=False):
        """ read config from config_dir
            if config_dir is None, clear to default config
        """

        if not config_dir:
            if not self.defaults['config_dir']:
                raise IOError("default config dir not set")
            config_dir = self.defaults['config_dir']

        conf_path = os.path.expanduser(config_dir)
        if not os.path.exists(conf_path):
            raise IOError("config dir not found at %s" % (conf_path,))

        if clear:
            self.clear()

        config = munge.load_datafile('config', conf_path, default=None)

        if not config:
            raise IOError("config file not found in %s" % (conf_path,))

        munge.util.recursive_update(self.data, config)
            #data['__config_dir__'] = conf_path

        return self

    def write(self, config_dir=None, codec=None):
        if not codec:
            codec=munge.get_codec('yaml')()
        config_dir = os.path.expanduser(config_dir)
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        codec.dump(data, open(os.path.join(config_dir, 'config.' + codec.extensions[0]), 'w'))


class MungeConfig(Config):
    defaults={
        'config': {},
        'config_dir': '~/.munge',
        'codec':  'yaml'
    }

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

