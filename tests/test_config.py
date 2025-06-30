import os
import shutil

import pytest

import munge
from munge import config

# import sys  # noqa: F401


test_dir = os.path.relpath(os.path.dirname(__file__))
data_dir = os.path.join(test_dir, "data")
conf0_dir = os.path.join(data_dir, "conf0")
extra_schemes = {"tyam": {"type": "toml", "cls": munge.get_codec("toml")}}


def test_parse_url():
    mysql = munge.get_codec("mysql")
    assert mysql
    json = munge.get_codec("json")
    toml = munge.get_codec("toml")

    # fail on empty
    with pytest.raises(ValueError):
        config.parse_url("")

    conf = config.parse_url("toml:test")
    conf = config.parse_url("toml:test")
    assert toml == conf.cls
    assert "test" == conf.url.path

    conf = config.parse_url("test.toml")
    assert toml == conf.cls
    assert "test.toml" == conf.url.path

    conf = config.parse_url("tyam:test", extra_schemes)
    assert toml == conf.cls
    assert "test" == conf.url.path

    conf = config.parse_url("json:http://example.com/test.txt")
    assert json == conf.cls
    assert "http://example.com/test.txt" == conf.url.path
    #    assert 'app_name/model' == conf.url.query

    with pytest.raises(ValueError):
        config.parse_url("nonexistant:test", extra_schemes)


default_config = {"addrbook": {}}

conf0_data = {
    "addrbook": {
        "site0": {
            "url": "https://example.com/data.json",
            "password": "secr3t",
            "user": "user",
            "timeout": 60,
        }
    }
}


class DefaultConfig(munge.Config):
    defaults = {"config": default_config, "config_dir": "~/.mungeX", "codec": "toml"}

    class Defaults:
        config = default_config


def mk_base_conf():
    return munge.config.Config(**DefaultConfig.defaults)


def mk_derived_conf():
    return DefaultConfig()


conf_obj_ctors = (
    mk_base_conf,
    mk_derived_conf,
)


def mk_base_conf0():
    conf = munge.config.Config(**DefaultConfig.defaults)
    conf.read(conf0_dir)
    return conf


def mk_base_conf0_init():
    return munge.config.Config(read=conf0_dir, **DefaultConfig.defaults)


def mk_base_conf0_init_data():
    return munge.config.Config(data=conf0_data, **DefaultConfig.defaults)


def mk_derived_conf0():
    conf = DefaultConfig()
    conf.read(conf0_dir)
    return conf


conf0_obj_ctors = (
    mk_base_conf0,
    mk_base_conf0_init,
    mk_base_conf0_init_data,
    mk_derived_conf0,
)


@pytest.fixture(scope="module", params=conf_obj_ctors)
def conf(request):
    return request.param()


@pytest.fixture(scope="module", params=conf0_obj_ctors)
def conf0(request):
    return request.param()


def test_derived_config_obj(conf):
    assert default_config == conf.default()
    baseconf = munge.config.Config(**DefaultConfig.defaults)
    assert baseconf


def test_config_obj(conf):
    assert default_config == conf.default()
    assert default_config == conf.data
    conf.data["foo"] = 42
    assert default_config != conf.data
    conf.clear()
    assert default_config == conf.data


def test_base_config_read():
    cfg = munge.Config()

    assert cfg._base_defaults == cfg._defaults

    with pytest.raises(IOError):
        cfg.read("nonexistant")

    # read with no config_dir and no default
    with pytest.raises(KeyError) as e:
        cfg.read()
    assert "'config_dir not set'" == str(e.value)

    # config_dir from arg, name set from base_defaults
    assert conf0_data == cfg.read(conf0_dir).data

    # config_dir from arg, name set to nome
    cfg._defaults["config_name"] = None
    with pytest.raises(KeyError) as e:
        cfg.read(conf0_dir)
    assert "'config_name not set'" == str(e.value)

    # config_dir from defaults
    cfg = munge.Config()
    cfg._defaults["config_dir"] = conf0_dir
    assert conf0_data == cfg.read().data

    # defaults is copy
    assert cfg._base_defaults != cfg._defaults

    # ctor read
    cfg = munge.Config(read=conf0_dir)
    assert conf0_data == cfg.data

    with pytest.raises(IOError):
        cfg = munge.Config(read="nonexistant")

    with pytest.raises(IOError):
        cfg.read(os.getcwd())


def test_config_copy():
    cfg = munge.Config(read=conf0_dir)
    cp = cfg.copy()
    assert cfg == cp
    assert cfg.meta == cp.meta

    cp.data["NEW"] = "KEY"
    assert "NEW" not in cfg.data


def test_config_defaults():
    cfg0 = DefaultConfig(read=conf0_dir)
    assert cfg0.defaults == DefaultConfig.defaults
    cfg1 = DefaultConfig(read=conf0_dir)
    assert cfg0.defaults == cfg1.defaults
    assert cfg0._defaults == cfg1._defaults
    assert cfg0.default() == cfg1.default()


def test_base_config_clear():
    cfg = munge.Config(read=conf0_dir)
    assert conf0_data == cfg.data
    assert conf0_dir == cfg.meta["config_dir"]

    cfg.clear()
    assert {} == cfg.meta


def test_config_clear(conf):
    assert default_config == conf.default()
    assert default_config == conf.data
    conf.data["foo"] = 42
    assert default_config != conf.data
    assert not conf.meta
    conf.clear()
    assert default_config == conf.data


def test_base_config_ctor_try_read():
    cfg = munge.Config(try_read="nonexistant")
    assert {} == cfg.meta


def test_base_config_ctor_try_read2():
    cfg = munge.Config()
    cfg.try_read(["nonexistant", "nonexistant2"])
    assert {} == cfg.meta

    cfg.try_read(["nonexistant", "nonexistant2", conf0_dir])
    assert conf0_data == cfg.data
    assert cfg.meta


def test_base_config_mapping():
    cfg = munge.Config(read=conf0_dir)
    data = conf0_data.copy()
    assert data == cfg.data

    # test __len__
    assert len(data) == len(cfg)

    # test __del__
    del data["addrbook"]
    del cfg["addrbook"]
    assert data == cfg.data


def test_config_write(conf, tmpdir):
    with pytest.raises(IOError):
        type(conf)().write()

    cdir = tmpdir.mkdir(type(conf).__name__)
    conf.write(str(cdir), "toml")

    # create an exact copy
    kwargs = conf._defaults.copy()
    kwargs["read"] = str(cdir)
    conf2 = type(conf)(**kwargs)

    assert conf == conf2
    assert conf._defaults == conf2._defaults
    assert conf.data == conf2.data

    #    conf = type(conf)(read=str(cdir))
    shutil.rmtree(str(cdir))
    conf2.write()
    assert conf == conf2
    assert conf._defaults == conf2._defaults
    assert conf.data == conf2.data


def test_conf0(conf0):
    assert conf0_data == conf0.data

    assert conf0_data["addrbook"]["site0"]["url"] == conf0.get_nested(
        "addrbook", "site0", "url"
    )
    assert conf0.get_nested("addrbook", "site1", "url") is None
