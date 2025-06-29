import copy
import os
from collections import namedtuple
from collections.abc import MutableMapping
from urllib.parse import urlsplit

import munge
import munge.util


# this wouldn't work with tabular data
# need metaclass to allow users to set info once on class
# TODO rename to BaseConfig, set standard setup for Config?
class Config(MutableMapping):
    """
    class for storing and manipulating data for config files
    """

    # internal base for defaults
    _base_defaults = {
        "config": {},
        # directory to look for config in
        "config_dir": None,
        # name of config file
        "config_name": "config",
        "codec": None,
        "autowrite": False,
        "validate": False,
    }

    def __init__(self, **kwargs):
        """
        accepts kwargs to set defaults
        data=dict to set initial data
        read=dir to open a dir
        try_read=dir to try to open a dir (and not throw if it doesn't read)
        """

        # use derived class defaults if available
        if hasattr(self, "defaults"):
            self._defaults = self._base_defaults.copy()
            self._defaults.update(self.defaults)
        else:
            self._defaults = self._base_defaults.copy()

        # override anything passed to kwargs
        for k, v in list(kwargs.items()):
            if k in self._defaults:
                self._defaults[k] = v

        self.data = kwargs.get("data", self.default())
        self._meta_config_dir = ""

        if "read" in kwargs:
            self.read(kwargs["read"])
        if "try_read" in kwargs:
            self.try_read(kwargs["try_read"])

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

    def copy(self):
        rv = self.__class__(data=self.data.copy())
        # copy meta
        rv._meta_config_dir = self._meta_config_dir
        return rv

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
        return copy.deepcopy(self._defaults["config"])

    def clear(self):
        self.data = self.default()
        self._meta_config_dir = None

    @property
    def meta(self):
        if not self._meta_config_dir:
            return {}

        return {
            "config_dir": self._meta_config_dir,
        }

    def read(self, config_dir=None, config_name=None, clear=False):
        """
        read config from config_dir
        if config_dir is None, clear to default config
        clear will clear to default before reading new file
        """

        # TODO should probably allow config_dir to be a list as well
        # get name of config directory
        if not config_dir:
            config_dir = self._defaults.get("config_dir", None)
        if not config_dir:
            raise KeyError("config_dir not set")

        # get name of config file
        if not config_name:
            config_name = self._defaults.get("config_name", None)
        if not config_name:
            raise KeyError("config_name not set")

        conf_path = os.path.expanduser(config_dir)
        if not os.path.exists(conf_path):
            raise OSError(f"config dir not found at {conf_path}")

        config = munge.load_datafile(config_name, conf_path, default=None)

        if not config:
            raise OSError(f"config file not found in {conf_path}")

        if clear:
            self.clear()

        munge.util.recursive_update(self.data, config)
        self._meta_config_dir = conf_path
        return self

    def try_read(self, config_dir=None, **kwargs):
        """
        try reading without throwing an error
        config_dir may be a list of directories to try in order, if so it
        will return after the first successful read
        other args will be passed direction to read()
        """
        if isinstance(config_dir, str):
            config_dir = (config_dir,)

        for cdir in config_dir:
            try:
                self.read(cdir, **kwargs)
                return cdir

            except OSError:
                pass

    def write(self, config_dir=None, config_name=None, codec=None):
        """
        writes config to config_dir using config_name
        """
        # get name of config directory
        if not config_dir:
            config_dir = self._meta_config_dir
            if not config_dir:
                raise OSError("config_dir not set")

        # get name of config file
        if not config_name:
            config_name = self._defaults.get("config_name", None)
        if not config_name:
            raise KeyError("config_name not set")

        if codec:
            codec = munge.get_codec(codec)()
        else:
            codec = munge.get_codec(self._defaults["codec"])()

        config_dir = os.path.expanduser(config_dir)
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        codec.dumpu(self.data, os.path.join(config_dir, "config." + codec.extension))


class MungeConfig(Config):
    defaults = {"config": {}, "config_dir": "~/.munge", "codec": "yaml"}


def find_cls(name, extra_schemes={}):
    if name in extra_schemes:
        return munge.get_codec(extra_schemes[name]["type"])

    return munge.get_codec(name)


class MungeURL(namedtuple("MungeURL", "cls url")):
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
        raise ValueError("url cannot be empty")

    cls = None
    res = urlsplit(url)

    # check config first
    if res.scheme in extra_schemes:
        # TODO - nerge these with any existing and recurse
        addr = extra_schemes[res.scheme]
        if "type" in addr:
            cls = find_cls(res.scheme, extra_schemes)
        if "url" in addr:
            url = addr["url"]
            if cls:
                res = urlsplit(url)
                return MungeURL(cls, res)
            # TODO - nerge these with any existing and recurse
            return parse_url(url)

    if res.scheme:
        cls = find_cls(res.scheme, extra_schemes)

    # check file extension
    if not cls:
        (rest, sep, ext) = url.rpartition(".")
        cls = find_cls(ext, extra_schemes)

        if not cls:
            raise ValueError(f"unable to find codec for {url}")

    return MungeURL(cls, res)
