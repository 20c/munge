
# options:
# input : source
# output : source

def get_config():
    return {}

def write_config(conf_dir='~/.munge'):
    print os.path.expanduser(conf_dir)

