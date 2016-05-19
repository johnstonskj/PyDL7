import io
import pytest

import divelog.html

import examples


def test_html_parser():
    with pytest.raises(NotImplementedError):
        divelog.html.parse(None)


def test_html_writer():
    def wrap(s):
        return '<div class="col-md-10">%s</div>' % s

    log = examples.create_log()
    file = io.StringIO()
    divelog.html.dump(log, file)
    content = file.getvalue()
    assert wrap('Saturday, 05. March 2016 11:10AM') in content
    assert wrap('Every 1 minute') in content
