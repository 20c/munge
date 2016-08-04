

### Options
Unless `MUNGE_EXPLICIT_IMPORT` is defined and true, munge will load all codecs it can find.

## API



### Config

Munge provides the config class it uses internally to be able to parse configs of any codec it supports and provide a dict of options

```python
class DerivedConfig(munge.Config):
    defaults={
        # dictionary containing the default config
        'config': default_config,
        # directory for config
        'config_dir': '~/.appname',
        # codec to use when writing new config files
        'codec':  'yaml'
    }
```


#### methods


#### example use with click

```python
@cli.command()
@click.option('--config', envvar='APPNAME_HOME', default=click.get_app_dir('appname'))
def do_stuff(config):
    cfg = Config(read=config)
```


### Click Context

Munge provides a (click)[http://click.pocoo.org/] context for use in applications using munge config.

To use it, simply extend the context and add `app_name` and `config_class`

```python
import munge.click


class Context(munge.click.Context):
    app_name = 'example'
    config_class = example.Config

```

To use it in a command, then do

```python
@click.group()
@click.version_option()
@Context.options
@Context.pass_context()
def cli(ctx, **kwargs):
    ctx.update_options(kwargs)


@cli.command()
@Context.options
@Context.pass_context()
def command(ctx, **kwargs):
    ctx.update_options(kwargs)
```


