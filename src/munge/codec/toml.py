import importlib
import os

try:
    if os.environ.get("MUNGE_TOML_LIBRARY", None):
        importlib.import_module(f"munge.codec.toml_{os.environ['MUNGE_TOML_LIBRARY']}")
    else:
        import munge.codec.toml_tomlkit  # noqa isort:skip
        import munge.codec.toml_toml  # noqa

except ValueError as exc:
    # don't load both toml modules
    if str(exc).startswith("duplicate extension"):
        pass
except ImportError:
    pass
