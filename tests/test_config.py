
import collections
import filecmp
import imp
import os
import pytest
import sys

import munge
from munge import config


extra_schemes = {
    'tyam': {
        'type': 'yaml',
        'cls': munge.get_codec('yaml')
    }
}

def test_parse_url():
    django = munge.get_codec('django')
    mysql = munge.get_codec('mysql')
    json = munge.get_codec('json')
    yaml = munge.get_codec('yaml')

    conf = config.parse_url('yaml:test')
    assert yaml == conf.cls
    assert 'test' == conf.url.path

    conf = config.parse_url('test.yaml')
    assert yaml == conf.cls
    assert 'test.yaml' == conf.url.path

    conf = config.parse_url('tyam:test', extra_schemes)
    assert yaml == conf.cls
    assert 'test' == conf.url.path

    conf = config.parse_url('django:///home/user/project/settings_dir.settings?app_name/model')
    assert django == conf.cls
    assert '/home/user/project/settings_dir.settings' == conf.url.path
    assert 'app_name/model' == conf.url.query

    conf = config.parse_url('json:http://example.com/test.txt')
    assert json == conf.cls
    assert 'http://example.com/test.txt' == conf.url.path
#    assert 'app_name/model' == conf.url.query

    with pytest.raises(ValueError):
        config.parse_url('nonexistant:test', extra_schemes)


