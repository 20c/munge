
from __future__ import absolute_import

from munge.base import CodecBase

try:
    pass
    #from django.conf import settings

except ImportError as exc:
    pass



class Django(CodecBase):

    extensions=['django']
    __kwargs={}

    def load(self, fobj):
        return django.load(fobj)

    def loads(self, instr):
        return django.loads(instr)

    def dump(self, data, fobj):
        return django.dump(data)

    def dumps(self, data):
        return skep.dumps(data)


# config:

#tag:
#    type: json
#    user: balh
#    pass:

# rc
# .munge/config.<ext>
