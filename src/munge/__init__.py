# namespace imports
from .codec import (
    find_datafile,  # noqa: F401
    get_codec,  # noqa: F401
    get_codecs,  # noqa: F401
    load_datafile,  # noqa: F401
)
from .config import Config  # noqa: F401

if not globals().get("MUNGE_EXPLICIT_IMPORT", False):
    from .codec import all  # noqa: F401
else:
    print(globals())
    assert 0
