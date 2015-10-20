
from __future__ import absolute_import

from munge.base import CodecBase

try:
    import yaml

except:
    pass


class Yaml(CodecBase):
    extensions=['yaml', 'yml']

    def set_type(self, name, typ):
        pass

    def load(self, *args, **kwargs):
        return yaml.safe_load(*args, **kwargs)

    def loads(self, *args, **kwargs):
        return self.load(*args, **kwargs)

    def dump(self, data, fobj):
        return fobj.write(yaml.safe_dump(data, default_flow_style=False))

    def dumps(self, data):
        return yaml.safe_dump(data, default_flow_style=False)

