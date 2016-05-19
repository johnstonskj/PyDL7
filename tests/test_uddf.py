import io
import pytest

import divelog.uddf

import examples


def test_uddf_parser():
    with pytest.raises(NotImplementedError):
        divelog.uddf.parse(None)


def test_uddf_writer():
    log = examples.create_log()
    with pytest.raises(NotImplementedError):
        divelog.uddf.dump(log, None)
