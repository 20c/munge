from munge.base import CodecBase

try:
    import tomlkit

    class TomlKit(CodecBase):
        supports_dict = True
        supports_roundtrip = True
        extensions = ["toml"]
        __kwargs = {}

        def set_type(self, name, typ):
            pass

        def load(self, fobj, **kwargs):
            return tomlkit.load(fobj, **self.__kwargs)

        def loads(self, input_string, **kwargs):
            return tomlkit.loads(input_string, **self.__kwargs)

        def dump(self, data, fobj, **kwargs):
            return tomlkit.dump(data, fobj, **kwargs)

        def dumps(self, data):
            return tomlkit.dumps(data)


except ImportError:
    pass
