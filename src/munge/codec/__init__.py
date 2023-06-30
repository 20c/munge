import os

__all__ = ["mysql", "json", "toml", "yaml"]
__codecs = {}


def add_codec(exts, cls):
    if not isinstance(exts, tuple):
        exts = tuple(exts)

    # check for dupe extensions
    dupe_exts = {ext for k in list(__codecs.keys()) for ext in k}.intersection(exts)
    if dupe_exts:
        raise ValueError(f"duplicate extension {str(dupe_exts)}")

    __codecs[exts] = cls


# TODO - could take a type argument to get only codecs that can handle that data type
def get_codecs():
    """Get all currently registered codecs."""
    return __codecs


def list_codecs():
    return [ext[0] for ext in list(get_codecs().keys())]


def get_codec(tag, codecs=get_codecs()):
    for exts, cls in list(codecs.items()):
        if tag in exts:
            return cls


def find_datafile(name, search_path=("."), codecs=get_codecs()):
    """
    find all matching data files in search_path
    search_path: path of directories to load from
    codecs: allow to override from list of installed
    returns array of tuples (codec_object, filename)
    """
    rv = []

    if isinstance(search_path, str):
        search_path = (search_path,)

    ext = os.path.splitext(name)[1][1:]

    cls = get_codec(ext)
    if cls:
        for each in search_path:
            fq_filename = os.path.join(each, name)
            if os.path.exists(fq_filename):
                rv.append((cls, fq_filename))

    for exts, obj in list(codecs.items()):
        for ext in exts:
            filename = f"{name}.{ext}"
            for each in search_path:
                fq_filename = os.path.join(each, filename)
                if os.path.exists(fq_filename):
                    rv.append((obj, fq_filename))

    return rv


def load_datafile(name, search_path=("."), codecs=get_codecs(), **kwargs):
    """
    find datafile and load them from codec
    TODO only does the first one
    kwargs:
    default = if passed will return that on failure instead of throwing
    """
    mod = find_datafile(name, search_path, codecs)
    if not mod:
        if "default" in kwargs:
            return kwargs["default"]
        raise OSError(f"file {name} not found in search path {str(search_path)}")

    (codec, datafile) = mod[0]
    return codec().load(open(datafile))
