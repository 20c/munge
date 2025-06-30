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
            return self.loads(fobj.read(), **self.__kwargs)

        def loads(self, input_string, **kwargs):
            return tomlkit.loads(input_string, **self.__kwargs)

        def dump(self, data, fobj, **kwargs):
            return fobj.write(self.dumps(data, **kwargs))

        def dumps(self, data, **kwargs):
            return tomlkit.dumps(data)

except ImportError:
    pass
