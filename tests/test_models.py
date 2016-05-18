import pytest
import divelog


def test_log_slots():
    slots = ['metadata', 'created', 'computer_model', 'computer_serial',
             'depth_unit', 'depth_pressure_unit', 'altitude_unit',
             'temperature_unit', 'tank_pressure_unit', 'tank_volume_unit',
             'dives']
    log = divelog.Log()
    for slot in slots:
        assert slot in dir(log)


def test_log_setter():
    log = divelog.Log()
    assert log.depth_pressure_unit == 'MSWG'
    for unit in divelog.NMRI_PRESSURE_CODE:
        log.depth_pressure_unit = unit
        assert log.depth_pressure_unit == unit
    unit = log.depth_pressure_unit
    with pytest.raises(ValueError):
        log.depth_pressure_unit = 'lightyear'
    assert log.depth_pressure_unit == unit


def test_log_setter_type():
    log = divelog.Log()
    log.created = '20160518'
    assert log.created.year == 2016
    assert log.created.month == 5
    assert log.created.day == 18
    with pytest.raises(ValueError):
        log.created = 'April 1st'


def test_log_setter_slots():
    log = divelog.Log()
    assert ('computer_color' not in dir(log))
    with pytest.raises(AttributeError):
        log.computer_color = 'red'
    assert ('computer_color' not in dir(log))
