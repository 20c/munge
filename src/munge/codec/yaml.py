from munge.base import CodecBase

try:
    import yaml

    class Yaml(CodecBase):
        supports_dict = True
        supports_list = True
        extensions = ["yaml", "yml"]

        def set_type(self, name, typ):
            pass

        def load(self, *args, **kwargs):
            return yaml.safe_load(*args, **kwargs)

        def loads(self, *args, **kwargs):
            return self.load(*args, **kwargs)

        def dump(self, data, fobj):
            return fobj.write(
                yaml.safe_dump(data, default_flow_style=False, sort_keys=False)
            )

        def dumps(self, data):
            return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)

except ImportError:
    pass
