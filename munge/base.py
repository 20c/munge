
import os
import sys
from urlparse import urlsplit
import urllib2
import requests

from . import codec


class Meta(type):
    def __init__(cls, name, bases, attrs):
        if name == 'CodecBase':
            super(Meta, cls).__init__(name, bases, attrs)
            return

        if not hasattr(cls, 'extensions'):
            raise NotImplementedError(
                "class %s failed import, must have 'extensions' defined" %
                cls.__name__)

        super(Meta, cls).__init__(name, bases, attrs)
        codec.add_codec(cls.extensions, cls)


class CodecBase(object):
    __metaclass__=Meta

    dict_type=dict
    float_type=float

    def __init__(self, config={}):
        self.config = config

    @property
    def extension(self):
        return self.extensions[0]

    def set_type(self, name, typ):
        raise NotImplementedError("missing set_type")

    def open(self, url, mode='r', stdio=True):
        """
        opens a URL, no scheme is assumed to be a file
        no path will use stdin or stdout depending on mode, unless stdio is False
        """
        # doesn't need to use config, because the object is already created
        res = urlsplit(url)

        if not res.scheme:
            if not res.path or res.path == '-':
                if not stdio:
                    raise IOError("unable to open '%s'" % (url,))

                if 'w' in mode:
                    return sys.stdout
                return sys.stdin

            return open(res.path, mode)

        if res.scheme in ('https', 'http', 'ftp'):
            req = requests.get(res.geturl(), stream=True)
            # TODO error check
            return req.raw
            #return urllib2.urlopen(res.geturl())

        raise IOError("unable to open '%s'" % (url,))

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
        return self.dump(data, self.open(url, 'w', **kwargs), **kwargs)


