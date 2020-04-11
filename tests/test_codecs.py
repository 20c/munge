
from builtins import str
from builtins import object

import collections
import filecmp
import imp
import os
import pytest
import sys

#from munge.codec.yaml import Yaml
#import munge.codec
import munge
import munge.codec.all

this_dir = os.path.dirname(__file__)
data_dir = os.path.join(this_dir, 'data')

test_codecs=[]
for tags, cls in list(munge.get_codecs().items()):
    if any(name in ('json', 'yaml') for name in tags):
        test_codecs.append(cls)

class DataSet0(object):
    name='set0'
    filename='data/' + name

    expected = {'munge': {'str0': 'str0', 'list0': ['item0', 'item1'], 'int0': 42}}

data = (
    DataSet0,
    )

class DataTab0(object):
    name='tab0'
    filename='data/' + name

    expected = [{'int0': 42, 'str0': 'str0'}, {'int0': 1337, 'str0': 'fish'}]


data = (
    DataSet0,
    DataTab0,
    )

class Codec(object):
    def __init__(self, cls):
        self.cls = cls
        #if not os.path.exists(

    def find_file(self, name):
        prefix = os.path.join(this_dir, name)
        for ext in self.cls.extensions:
            fq_name = "%s.%s" % (prefix, ext)
            print("checking", fq_name)
            if os.path.exists(fq_name):
                return fq_name

    def open_file(self, name, *args, **kwargs):
        return open(self.find_file(name), *args, **kwargs)


@pytest.fixture(scope="module", params=data)
def dataset(request):
    print(request.param)
    obj = request.param()
    print(obj)
    assert obj.expected
    return obj
    return request.param()

@pytest.fixture(scope="module", params=test_codecs)
def codec(request):
    print(request.param)
    return Codec(request.param)

def test_codec_registry():
    assert munge.get_codecs()

def test_extesion(codec, dataset):
    obj = codec.cls()
    assert obj.extensions[0] == obj.extension

def no_test_load_into(codec, dataset):
    src = codec.cls()
    src.set_type('dict', collections.OrderedDict)
    data = src.load(open(codec.find_file(dataset.filename)))
    assert dataset.expected == data
    assert collections.OrderedDict.__name__ == type(data).__name__
    assert isinstance(data, collections.OrderedDict)

def test_open(codec, dataset):
    src = codec.cls()
    assert open(codec.find_file(dataset.filename)).read() == src.open(codec.find_file(dataset.filename)).read()

    with pytest.raises(IOError):
        src.open('noneexistant')
    with pytest.raises(IOError):
        src.open('', stdio=False)

    assert sys.stdin == src.open('')
    assert sys.stdin == src.open('-')

def test_load(codec, dataset):
    src = codec.cls()
    assert dataset.expected == src.load(open(codec.find_file(dataset.filename)))

def test_loads(codec, dataset):
    src = codec.cls()
    data = codec.open_file(dataset.filename)
    print(data)
    print(data.read())
    assert dataset.expected == src.loads(codec.open_file(dataset.filename).read())

def test_loadu(codec, dataset):
    src = codec.cls()
    assert dataset.expected == src.loadu(codec.find_file(dataset.filename))

def test_dump(codec, dataset, tmpdir):
    obj = codec.cls()
    dstfile = tmpdir.join('dump' + obj.extension)
    obj.dump(dataset.expected, dstfile.open('w'))
    assert dataset.expected == obj.load(dstfile.open())
    #assert codec.open_file(dataset.filename).read() == dstfile.read()

def test_dumps(codec, dataset, tmpdir):
    obj = codec.cls()
    dstfile = tmpdir.join('dump' + obj.extension)
    obj.dumpu(dataset.expected, str(dstfile))
    assert dataset.expected == obj.load(dstfile.open())

def test_dumpu(codec, dataset, tmpdir):
    obj = codec.cls()
    dstfile = tmpdir.join('dump' + obj.extension)
    assert dataset.expected == obj.loads(obj.dumps(dataset.expected))

def test_find_datafile(codec, dataset):
    obj = codec.cls()

    print(dataset.filename)
    print(data_dir)
    files = munge.find_datafile('set0', data_dir)
    # should == number of codec tests
    assert files

    assert not munge.find_datafile('nonexistant', [])

    # test codec override
    files = munge.find_datafile(dataset.filename, this_dir, {('json',): munge.get_codecs()[('json',)]})
    assert 1 == len(files)
    load = files[0]
    assert os.path.join(this_dir, dataset.filename + '.json') == load[1]
    assert hasattr(load[0], 'load')
    assert dataset.expected == load[0]().load(open(load[1]))

def test_load_datafile(codec, dataset):
    obj = codec.cls()

    with pytest.raises(IOError):
        munge.load_datafile('nonexistant', data_dir)

    # default value
    assert None == munge.load_datafile('nonexistant', data_dir, default=None)
    assert 'DEFAULT' == munge.load_datafile('nonexistant', data_dir, default='DEFAULT')

    data = munge.load_datafile(dataset.filename, this_dir)
    assert data

    # test hardset extension
    assert obj.extensions
    for ext in obj.extensions:
        fq_path = "%s.%s" % (dataset.filename, ext)
        data = munge.load_datafile(fq_path, this_dir, default=None)
        if data:
            break
        data = None
    assert data

    # test default search path '.'
    #files = munge.find_datafile('set0', data_dir)
    files = munge.find_datafile(fq_path, this_dir)
    assert 1 == len(files)
    relpath = os.path.relpath(files[0][1])
    data = munge.load_datafile(relpath)
    assert data

    with pytest.raises(IOError):
        munge.load_datafile(dataset.filename, this_dir, codecs={})

