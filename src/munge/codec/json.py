import json

from munge.base import CodecBase


class Json(CodecBase):
    supports_dict = True
    supports_list = True

    extensions = ["json"]
    __kwargs = {}

    def set_type(self, name, typ):
        if name == "dict":
            self.__kwargs["object_pairs_hook"] = typ

    def load(self, fobj, **kwargs):
        return json.load(fobj, **self.__kwargs)

    def loads(self, input_string, **kwargs):
        return json.loads(input_string, **self.__kwargs)

    def dump(self, data, fobj, **kwargs):
        return json.dump(data, fobj, **kwargs)

    def dumps(self, data):
        return json.dumps(data)
