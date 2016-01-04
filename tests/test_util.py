
import copy
import munge.util
import pytest

def test_recursive_update():
    a = {
        'a': 1,
        'd': {
            'a': 1,
            },
        'l': [1, 2, 5],
        'l2': [1, 2, 3],
        }
    b = {
        'b': 1,
        'd': {
            'a': 2,
            'c': 3,
            },
        'l2': [4, 5],
        'l3': [1, 2],
        }
    merged = {
        'a': 1,
        'b': 1,
        'd': {
            'a': 2,
            'c': 3,
            },
        'l': [1, 2, 5],
        'l2': [1, 2, 3, 4, 5],
        'l3': [1, 2],
        }

    munge.util.recursive_update(a, b)
    assert merged == a

def test_recursive_update_copy():
    d0 = {'a': {'b': {'x': '1', 'y': '2'}}}
    d1 = {'a': {'c': {'gg': {'m': '3'}, 'xx': '4'}}}

    r0 = {'a': {'b': {'x': '1', 'y': '2'}, 'c': {'gg': {'m': '3'}, 'xx': '4'}}}

    d0cp = copy.deepcopy(d0)
    res = munge.util.recursive_update(d0, d1, copy=True)
    assert r0 == res
    assert d0cp == d0
    assert r0 != d0

def test_recursive_update_lists():
    a = {
        'a': 1,
        'd': {
            'a': 1,
            },
        'l': [1, 2, 5],
        'l2': [1, 2, 3],
        }
    b = {
        'b': 1,
        'd': {
            'a': 2,
            'c': 3,
            },
        'l2': [4, 5],
        'l3': [1, 2],
        }
    merged = {
        'a': 1,
        'b': 1,
        'd': {
            'a': 2,
            'c': 3,
            },
        'l': [1, 2, 5],
        'l2': [4, 5],
        'l3': [1, 2],
        }

    munge.util.recursive_update(a, b, merge_lists=False)
    assert merged == a

