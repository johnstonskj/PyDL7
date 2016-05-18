import pytest
import divelog.files


def test_formats_dict():
    for key in divelog.files.formats:
        assert divelog.files.formats[key].FORMAT_NAME == key


def test_formats_dict_error():
    with pytest.raises(KeyError):
        divelog.files.formats['NO_TYPE']


def test_extensions_dict():
    assert divelog.files.extensions['zxu'] == 'DL7'
    assert divelog.files.extensions['json'] == 'JSON'


def test_extensions_dict_err():
    with pytest.raises(KeyError):
        divelog.files.formats['doc']


def test_module_func():
    assert divelog.files.get_module('foo.zxu').FORMAT_NAME == 'DL7'
    assert divelog.files.get_module('foo.json').FORMAT_NAME == 'JSON'


def test_module_func_err():
    assert divelog.files.get_module('foo.doc') is None
