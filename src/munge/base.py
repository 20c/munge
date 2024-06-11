import sys
from collections.abc import Mapping
from urllib.parse import urlsplit

import requests

from munge import codec


class Meta(type):
    """Metadata class to check and register codec classes."""

    def __init__(cls, name, bases, attrs):
        if name == "CodecBase":
            super().__init__(name, bases, attrs)
            return

        if not hasattr(cls, "extensions"):
            raise NotImplementedError(
                f"class {cls.__name__} failed import, must have 'extensions' defined"
            )

        if not cls.supports_dict and not cls.supports_list:
            raise NotImplementedError(
                f"class {cls.__name__} failed import, must have either 'supports_dict' or 'supports_list' defined"
            )

        super().__init__(name, bases, attrs)
        codec.add_codec(cls.extensions, cls)


class CodecBase(metaclass=Meta):
    supports_dict = False
    supports_list = False
    supports_roundtrip = False

    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            self.config = dict()

    @property
    def extension(self):
        return self.extensions[0]

    def set_type(self, name, typ):
        raise NotImplementedError("set_type has not been implemented")

    def supports_data(self, data):
        if isinstance(data, Mapping):
            return self.supports_dict
        if isinstance(data, list):
            return self.supports_list

    def open(self, url, mode="r", stdio=True):
        """
        opens a URL, no scheme is assumed to be a file
        no path will use stdin or stdout depending on mode, unless stdio is False
        """
        # doesn't need to use config, because the object is already created
        res = urlsplit(url)

        if not res.scheme:
            if not res.path or res.path == "-":
                if not stdio:
                    raise OSError(f"unable to open '{url}'")

                if "w" in mode:
                    return sys.stdout
                return sys.stdin

            return open(res.path, mode)

        if res.scheme in ("https", "http", "ftp"):
            req = requests.get(res.geturl(), stream=True)
            # TODO error check
            return req.raw
            # return urllib2.urlopen(res.geturl())

        raise OSError(f"unable to open '{url}'")

    def loadu(self, url, **kwargs):
        """
        opens url and passes to load()
        kwargs are passed to both open and load
        """
        return self.load(self.open(url, **kwargs), **kwargs)

    def dumpu(self, data, url, **kwargs):
        """
        opens url and passes to load()
        kwargs are passed to both open and dump
        """
        return self.dump(data, self.open(url, "w", **kwargs), **kwargs)
