
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
        }

    munge.util.recursive_update(a, b)
    assert merged == a
