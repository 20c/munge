import os

import pytest

import munge
import munge.click

test_dir = os.path.relpath(os.path.dirname(__file__))
data_dir = os.path.join(test_dir, "data")
conf0_dir = os.path.join(data_dir, "conf0")


class Config(munge.Config):
    pass


class Context(munge.click.Context):
    app_name = "munge_test"
    config_class = munge.Config


@pytest.fixture()
def ctx():
    return Context()


def test_searchpath(ctx):
    assert 4 == len(ctx.search_path())


def test_find_home_kwargs(ctx):
    ctx.update_options({"home": conf0_dir})
    assert conf0_dir == ctx.home


def test_find_home_env(ctx):
    os.environ["MUNGE_TEST_HOME"] = conf0_dir
    ctx.update_options({})
    assert conf0_dir == ctx.home


def test_find_home_nonexistant(ctx):
    with pytest.raises(IOError):
        ctx.update_options({"home": "nonexistant"})
