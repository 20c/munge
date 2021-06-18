# namespace imports
from .codec import find_datafile  # noqa
from .codec import get_codec  # noqa
from .codec import get_codecs  # noqa
from .codec import load_datafile  # noqa
from .config import Config

if not globals().get("MUNGE_EXPLICIT_IMPORT", False):
    from .codec import all  # noqa
else:
    print(globals())
    assert 0
