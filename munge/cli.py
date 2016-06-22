
from __future__ import print_function
import click
import sys
import munge
from munge import config


def get_config():
    return {}


def list_codecs(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    print(munge.codec.list_codecs())
    ctx.exit(0)


def common_options(f):
    f = click.option('--config', envvar='MUNGE_HOME', default=click.get_app_dir('munge'))(f)
    f = click.option('--debug', is_flag=True, default=False)(f)
    return f


@click.command()
@click.version_option()
@common_options
@click.argument('input', nargs=-1)
@click.argument('output', nargs=1)
@click.option('--list-codecs', is_flag=True, callback=list_codecs,
    expose_value=False, is_eager=True)
def main(**options):
    conf = config.MungeConfig(try_read=options['config'])

    inp = options['input']
    outp = options['output']

    if not len(inp):
        # if there's only 1 argument, it's (incorrectly) put in output
        if outp:
            inp = (outp,)
            outp = None
        else:
            inp = ('-')
    elif len(inp) != 1:
        raise NotImplementedError("multi input not yet supported")

    src = config.parse_url(inp[0], conf.get('addrbook', []))
    data = src.cls().loadu(src.url.path)

    # use same input codec by defailt
    if not outp:
        dst = src
        dst.cls().dumpu(data, '-')
    else:
        dst = config.parse_url(outp, conf.get('addrbook', {}))
        dst.cls().dumpu(data, dst.url.path)


