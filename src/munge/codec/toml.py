import importlib

from munge.base import CodecBase

try:
    if "MUNGE_TOML_LIBRARY" in globals():
        importlib.import_module(f"munge.codec.toml_{globals['MUNGE_TOML_LIBRARY']}")
    else:
        import munge.codec.toml_toml
        import munge.codec.toml_tomlkit

except ImportError:
    pass
