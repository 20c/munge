from munge.base import CodecBase

try:
    pass
    # from django.conf import settings

except ImportError as exc:
    pass


class Django(CodecBase):

    extensions = ["django"]
    __kwargs = {}

    def load(self, fobj):
        raise NotImplementedError()

    def loads(self, instr):
        raise NotImplementedError()

    def dump(self, data, fobj):
        raise NotImplementedError()

    def dumps(self, data):
        raise NotImplementedError()
