
import collections


def recursive_update(a, b, copy=False):
    """
    recursive dict a.update(b), merges dicts and lists
    Note: will clobber non dict keys if b has a dict with same key
    """
    if copy:
        a = a.copy()

    for k, v in b.iteritems():
        if isinstance(v, collections.Mapping):
            if isinstance(a.get(k, None), collections.Mapping):
                recursive_update(a[k], v)
                continue

        elif type(v) is list:
            if type(a.get(k, None)) is list:
                a[k].extend(v)
                continue

        # warning, clobbering
        a[k] = v

    return a

