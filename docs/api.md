

### Options
Unless `MUNGE_EXPLICIT_IMPORT` is defined and true, munge will load all codecs it can find.

## API



### Config

Munge provides the config class it uses internally to be able to parse configs of any codec it supports and provide a dict of options


    class DerivedConfig(munge.Config):
        defaults={
            # dictionary containing the default config
            'config': default_config,
            # directory for config
            'config_dir': '~/.appname',
            # codec to use when writing new config files
            'codec':  'yaml'
        }


#### methods


#### example use with click

    @cli.command()
    @click.option('--config', envvar='APPNAME_HOME', default=click.get_app_dir('appname'))
    def do_stuff(config):
        cfg = Config(read=config)

