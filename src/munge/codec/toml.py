from munge.base import CodecBase

try:
    import toml

except:
    pass

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
# XXX        data = dict(data=data)
        print(data)
        print(fobj)
        return toml.dump(data, fobj, **kwargs)

    def dumps(self, data):
        return toml.dumps(data)
