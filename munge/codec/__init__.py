
import os
import imp

__all__ = ['django', 'mysql', 'json', 'yaml']
__codecs = {}


def add_codec(exts, cls):
    if not isinstance(exts, tuple):
        exts = tuple(exts)

    # check for dupe extensions
    dupe_exts = set(ext for k in __codecs.keys() for ext in k).intersection(exts)
    if dupe_exts:
        raise ValueError("duplicate extension %s" % str(dupe_exts))

    __codecs[exts] = cls

def get_codecs():
    return __codecs

def list_codecs():
    return [ext[0] for ext in get_codecs().keys()]

def get_codec(tag, codecs=get_codecs()):
    for exts, cls in codecs.items():
        if tag in exts:
            return cls

def find_datafile(name, search_path=('.'), codecs=get_codecs()):
    """
    find all matching data files in search_path
    search_path: path of directories to load from
    codecs: allow to override from list of installed
    returns array of tuples (codec_object, filename)
    """
    rv = []

    if isinstance(search_path, basestring):
        search_path = (search_path,)

    #print "search path ", str(search_path)

    ext = os.path.splitext(name)[1][1:]

    cls = get_codec(ext)
    if cls:
        for each in search_path:
            fq_filename = os.path.join(each, name)
            if os.path.exists(fq_filename):
                rv.append((cls, fq_filename))

    for exts, obj in codecs.items():
        for ext in exts:
            filename = "%s.%s" % (name, ext)
            for each in search_path:
                fq_filename = os.path.join(each, filename)
                if os.path.exists(fq_filename):
                    rv.append((obj, fq_filename))

    return rv

def load_datafile(name, search_path=('.'), codecs=get_codecs(), **kwargs):
    """
    find datafile and load them from codec
    TODO only does the first one
    kwargs:
    default = if passed will return that on failure instead of throwing
    """
    mod = find_datafile(name, search_path, codecs)
    if not mod:
        if 'default' in kwargs:
            return kwargs['default']
        raise IOError("file %s not found in search path %s" %(name, str(search_path)))

    (codec, datafile) = mod[0]
    return codec().load(open(datafile))

