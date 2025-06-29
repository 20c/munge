import collections
import os
import sys

import pytest

import munge
import munge.codec.all

this_dir = os.path.dirname(__file__)
data_dir = os.path.join(this_dir, "data")

test_codecs = []
for tags, cls in list(munge.get_codecs().items()):
    if any(name in ("json", "toml", "yaml") for name in tags):
        print(f"appending codec {cls.extension}")
        test_codecs.append(cls)


class Datadict0:
    name = "dict0"
    filename = "data/" + name

    expected = {"munge": {"str0": "str0", "list0": ["item0", "item1"], "int0": 42}}


class Datalist0:
    name = "list0"
    filename = "data/" + name

    expected = [{"int0": 42, "str0": "str0"}, {"int0": 1337, "str0": "fish"}]


data = (
    Datadict0,
    Datalist0,
)


class Codec:
    def __init__(self, cls):
        self.cls = cls
        # if not os.path.exists(

    def find_file(self, name):
        prefix = os.path.join(this_dir, name)
        for ext in self.cls.extensions:
            fq_name = f"{prefix}.{ext}"
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


# Needs set_type fixing
def no_test_load_into(codec, dataset):
    obj = codec.cls()
    obj.set_type("dict", collections.OrderedDict)
    data = obj.load(open(codec.find_file(dataset.filename)))
    assert dataset.expected == data
    assert collections.OrderedDict.__name__ == type(data).__name__
    assert isinstance(data, collections.OrderedDict)


def test_open(codec, dataset):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    # with open(codec.find_file(dataset.filename)) as :

    file1_content = open(codec.find_file(dataset.filename)).read()
    file2_content = obj.open(codec.find_file(dataset.filename)).read()
    assert file1_content == file2_content

    with pytest.raises(IOError):
        obj.open("noneexistant")
    with pytest.raises(IOError):
        obj.open("", stdio=False)

    assert sys.stdin == obj.open("")
    assert sys.stdin == obj.open("-")


def test_load(codec, dataset):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    assert dataset.expected == obj.load(open(codec.find_file(dataset.filename)))


def test_loads(codec, dataset):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    data = codec.open_file(dataset.filename)
    print(data)
    print(data.read())
    assert dataset.expected == obj.loads(codec.open_file(dataset.filename).read())


def test_loadu(codec, dataset):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    assert dataset.expected == obj.loadu(codec.find_file(dataset.filename))


def test_dump(codec, dataset, tmpdir):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    dstfile = tmpdir.join("dump" + obj.extension)
    obj.dump(dataset.expected, dstfile.open("w"))
    with dstfile.open() as fobj:
        assert dataset.expected == obj.load(fobj)


def test_roundtrip(codec, dataset, tmpdir):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    if not obj.supports_roundtrip:
        return

    data = obj.load(open(codec.find_file(dataset.filename)))
    for section in dataset.expected:
        for k, v in dataset.expected[section].items():
            data[section][k] = v

    dumped = obj.dumps(data)
    print(f"dumping: {dumped}")

    dstfile = tmpdir.join("dump" + obj.extension)
    obj.dump(data, dstfile.open("w"))
    with dstfile.open() as fobj:
        assert codec.open_file(dataset.filename).read() == fobj.read()


def test_dumps(codec, dataset, tmpdir):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    dstfile = tmpdir.join("dump" + obj.extension)
    obj.dumpu(dataset.expected, str(dstfile))
    assert dataset.expected == obj.load(dstfile.open())


def test_dumpu(codec, dataset, tmpdir):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return
    dstfile = tmpdir.join("dump" + obj.extension)
    assert dstfile
    assert dataset.expected == obj.loads(obj.dumps(dataset.expected))


def test_find_datafile(codec, dataset):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return

    print(dataset.filename)
    print(data_dir)
    files = munge.find_datafile("dict0", data_dir)
    # should == number of codec tests
    assert files

    assert not munge.find_datafile("nonexistant", [])

    # test codec override
    files = munge.find_datafile(
        dataset.filename, this_dir, {("json",): munge.get_codecs()[("json",)]}
    )
    assert 1 == len(files)
    load = files[0]
    assert os.path.join(this_dir, dataset.filename + ".json") == load[1]
    assert hasattr(load[0], "load")
    assert dataset.expected == load[0]().load(open(load[1]))


def test_load_datafile(codec, dataset):
    obj = codec.cls()
    if not obj.supports_data(dataset.expected):
        return

    # TODO move the nonexistant tests to their own function so they're not repeatedly called
    with pytest.raises(IOError):
        munge.load_datafile("nonexistant", data_dir)

    # default value
    assert munge.load_datafile("nonexistant", data_dir, default=None) is None
    assert "DEFAULT" == munge.load_datafile("nonexistant", data_dir, default="DEFAULT")

    data = munge.load_datafile(dataset.filename, this_dir)
    assert data

    # test hardset extension
    assert obj.extensions
    for ext in obj.extensions:
        fq_path = f"{dataset.filename}.{ext}"
        data = munge.load_datafile(fq_path, this_dir, default=None)
        if data:
            break
        data = None
    assert data

    # test default search path '.'
    files = munge.find_datafile(fq_path, this_dir)
    assert 1 == len(files)
    relpath = os.path.relpath(files[0][1])
    data = munge.load_datafile(relpath)
    assert data

    with pytest.raises(IOError):
        munge.load_datafile(dataset.filename, this_dir, codecs={})
