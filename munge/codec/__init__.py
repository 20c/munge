
import os
import imp

__all__ = ['django', 'mysql', 'json', 'yaml']
__codecs = {}

# TODO move to .load?
def _do_find_import(directory, skiplist=None, suffixes=None):
    #  explicitly look for None, suffixes=[] might be passed to not load anything
    if suffixes == None:
        suffixes = [t[0] for t in imp.get_suffixes()]

    loaded = dict()
    for module in os.listdir(directory):
        name, ext = os.path.splitext(module)
        if name in loaded:
            continue

        if name in skiplist:
            continue

        if ext in suffixes:
            #print "finding %s in %s" % (name, directory)
            #mod = imp.load_module(name, *imp.find_module(name, [directory]))
            try:
                imp_args = imp.find_module(name, [directory])
                mod = imp.load_module(name, *imp_args)
                loaded[name] = mod.__file__
            finally:
                try:
                    imp_args[0].close()
                    print "file closed"
                except:
                    pass

    return loaded

def find_import():

    this = os.path.split(__file__)
    this_dir = this[0]
    # remove trailing c if cached bytecode
    #this_file = this[1].rstrip('c')
    _do_find_import(this_dir, ('all', '__init__'))


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
    for exts, cls in __codecs.items():
        if tag in exts:
            return cls

def find_datafile(name, search_path=['.'], codecs=get_codecs()):
    """
    find all matching data files in search_path
    search_path: path of directories to load from
    codecs: allow to override from list of installed
    returns array of tuples (codec_object, filename)
    """
    rv = []

    if isinstance(search_path, basestring):
        search_path = [search_path]

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
            filename="%s.%s" % (name, ext)
            for each in search_path:
                fq_filename = os.path.join(each, filename)
                if os.path.exists(fq_filename):
                    rv.append((obj, fq_filename))

    return rv

def load_datafile(name, search_path=['.'], codecs=get_codecs(), **kwargs):
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

