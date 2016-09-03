
from __future__ import print_function
from __future__ import absolute_import

import click
import os
import logging

def expand_env_var(path):
    """
    loops through a search path list, expands anything starting with $
    """

class Context(object):
    # TODO replace with full logger config
    log_format = '%(message)s'
    log_format_debug = '%(name)s %(message)s %(filename)s:%(lineno)d'
    log_format_file = '%(asctime)s %(levelname)s %(message)s'

    @classmethod
    def search_path(cls):
        return ['$%s_HOME' % cls.app_name.upper(),
                os.path.join('.', '.' + cls.app_name),
                click.get_app_dir(cls.app_name)]

    @classmethod
    def options(cls, f):
        f = click.option('--debug', help='enable extra debug output', is_flag=True, default=None)(f)
        f = click.option('--home', help='specify the home directory, by default will check in order: ' + ', '.join(cls.search_path()), default=None)(f)
        f = click.option('--verbose', help='enable more verbose output', is_flag=True, default=None)(f)
        f = click.option('--quiet', help='no output at all', is_flag=True, default=None)(f)
        return f

    @classmethod
    def get_options(cls, kwargs):
        keys = ('debug', 'home', 'verbose', 'quiet')
        return {k: kwargs.pop(k, None) for k in keys}

    @classmethod
    def pass_context(cls):
        return click.make_pass_decorator(cls, ensure=True)

    def __init__(self, **kwargs):
        self.debug = False
        self.quiet = False
        self.verbose = False

        self.home = None
        self.config = None

        self.update_options(kwargs)

    def update_options(self, kwargs):
        opt = self.__class__.get_options(kwargs)

        if opt.get('debug', None) is not None:
            self.debug = opt['debug']

        if opt.get('verbose', None) is not None:
            self.verbose = opt['verbose']

        if opt.get('quiet', None) is not None:
            self.quiet = opt['quiet']

        # TODO - probably should warn or error if passing multiple home values in?
        if opt.get('home', None) is not None:
            # if home is redefined, nuke config and load a new one
            self.home = opt['home']
            self.config = self.config_class(read=self.home)

        # if no config and home wasn't defined, check search path
        elif not self.config:
            search_path = []
            for path in self.__class__.search_path():
                if path.startswith('$'):
                    if path[1:] not in os.environ:
                        continue
                    search_path.append(os.environ[path[1:]])
                else:
                    search_path.append(path)

            self.config = self.config_class(try_read=search_path)

        self.init()

    def init(self):
        """
        call after updating options
        """
        # remove root logger, so we can reinit
        # TODO only remove our own
        # TODO move to _init, let overrides use init()
        logging.getLogger().handlers = []

        if self.debug:
            logging.basicConfig(level=logging.DEBUG, format=self.log_format_debug)
        elif self.verbose:
            logging.basicConfig(level=logging.INFO, format=self.log_format)
        elif not self.quiet:
            logging.basicConfig(level=logging.ERROR, format=self.log_format)
        else:
            logging.getLogger().addHandler(logging.NullHandler())

