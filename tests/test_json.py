import io
import pytest

import divelog.json

import examples


def test_json_parser():
    with pytest.raises(NotImplementedError):
        divelog.json.parse(None)


def test_json_writer():
    log = examples.create_log()
    file = io.StringIO()
    divelog.json.dump(log, file)
    content = file.getvalue()
    assert '"leave_surface_time": 1457175600.0' in content
    assert '"computer_serial": "8762-3478-6234"' in content
