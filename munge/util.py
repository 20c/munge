# TODO unit tests for these helper functions

def mergedicts(*dicts):
    """Recursively merge an arbitrary number of dictionaries.
    >>> import pprint
    >>> d1 = {'a': {'b': {'x': '1',
    ...           'y': '2'}}}
    >>> d2 = {'a': {'c': {'gg': {'m': '3'},
    ...           'xx': '4'}}}
    >>> pprint.pprint(mergedicts(d1, d2), width=2)
    {'a': {'b': {'x': '1',
           'y': '2'},
         'c': {'gg': {'m': '3'},
           'xx': '4'}}}
    """

    keys = set(k for d in dicts for k in d)

    def vals(key):
        """Returns all values for `key` in all `dicts`."""
        withkey = (d for d in dicts if key in d)
        return [d[key] for d in withkey]

    def recurse(*values):
        types = list(set([type(v) for v in values]))

        # for debugging recursive merge code:
        # print values
        # print types

        """Recurse if the values are dictionaries."""
        if isinstance(values[0], dict):
            return mergedicts(*values)
        if len(values) == 1:
            return values[0]

        if len(types) == 1 and types[0] in (list, unicode, str, basestring):
            # it's all non-merge (replace) type, and the types match. return
            # the furthest over one. is this insane? yes.
            return values[-1]

        print "except ",
        print values
        raise TypeError("Multiple non-dictionary values for a key")

    return dict((key, recurse(*vals(key))) for key in keys)

##########################################################################


def merge(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []

    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a

##########################################################################


def recursive_update(a, b):
    """recursive dict a.update(b)
       Note: will clobber non dict keys if b has a dict with same key
    """
    for k, v in b.iteritems():
        if isinstance(v, dict):
            if isinstance(a.get(k, None), dict):
                recursive_update(a[k], v)
            else:
                a[k] = v
        else:
            a[k] = v

##########################################################################
