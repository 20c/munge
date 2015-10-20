
from __future__ import absolute_import

from munge.base import CodecBase

import json

class Json(CodecBase):

    extensions=['json']
    __kwargs={}

    def set_type(self, name, typ):
        if name == 'dict':
            self.__kwargs['object_pairs_hook'] = typ

    def load(self, fobj, **kwargs):
        return json.load(fobj, **self.__kwargs)

    def loads(self, instr, **kwargs):
        return json.loads(instr, **self.__kwargs)

    def dump(self, data, fobj, **kwargs):
        return json.dump(data, fobj, **kwargs)

    def dumps(self, data):
        return json.dumps(data)

