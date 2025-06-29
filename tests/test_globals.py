import os
import sys


def unload_munge():
    for key in list(sys.modules.keys()):
        if key.startswith("munge"):
            del sys.modules[key]


def test_toml_library():
    import munge

    codec = munge.get_codec("toml")
    assert codec.supports_roundtrip

    os.environ["MUNGE_TOML_LIBRARY"] = "toml"
    unload_munge()
    import munge

    codec = munge.get_codec("toml")
    assert not codec.supports_roundtrip
