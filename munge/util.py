
import collections
from copy import deepcopy


def recursive_update(a, b, **kwargs):
    """
    recursive dict a.update(b), merges dicts and lists
    Note: will clobber non dict keys if b has a dict with same key
    options:
        copy: deepcopy instead of reference (default False)
        merge_lists: merge lists as well (default True)
    """
    copy = kwargs.get('copy', False)
    merge_lists = kwargs.get('merge_lists', True)

    for k, v in b.iteritems():
        if isinstance(v, collections.Mapping):
            if isinstance(a.get(k, None), collections.Mapping):
                recursive_update(a[k], v, **kwargs)
                continue

        elif merge_lists and type(v) is list:
            if type(a.get(k, None)) is list:
                if copy:
                    a[k].extend(deepcopy(v))
                else:
                    a[k].extend(v)
                continue

        # warning, clobbering
        if copy:
            a[k] = deepcopy(v)
        else:
            a[k] = v

    return a

