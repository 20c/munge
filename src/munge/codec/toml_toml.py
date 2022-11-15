from munge.base import CodecBase

try:
    import toml

    class Toml(CodecBase):
        supports_dict = True
        extensions = ["toml"]
        __kwargs = {}

        def set_type(self, name, typ):
            pass

        def load(self, fobj, **kwargs):
            return toml.load(fobj, **self.__kwargs)

        def loads(self, input_string, **kwargs):
            return toml.loads(input_string, **self.__kwargs)

        def dump(self, data, fobj, **kwargs):
            return toml.dump(data, fobj, **kwargs)

        def dumps(self, data):
            return toml.dumps(data)

except ImportError:
    pass
