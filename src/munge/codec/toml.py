import importlib

from munge.base import CodecBase

try:
    if "MUNGE_TOML_LIBRARY" in globals():
        importlib.import_module(f"munge.codec.toml_{globals['MUNGE_TOML_LIBRARY']}")
    else:
        import munge.codec.toml_tomlkit
        import munge.codec.toml_toml

except ValueError as exc:
    # don't load both toml modules
    if str(exc).startswith("duplicate extension"):
        pass
except ImportError:
    pass
