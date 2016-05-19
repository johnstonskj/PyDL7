import datetime
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
    for slot in dir(log):
        if not slot[0:2] == '__':
            assert slot in slots


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


def test_log_setter_created():
    log = divelog.Log()
    log.created = '20160518'
    assert log.created.year == 2016
    assert log.created.month == 5
    assert log.created.day == 18
    with pytest.raises(ValueError):
        log.created = 'April 1st'
    log.created = datetime.datetime.now()


def test_log_setter_metadata():
    log = divelog.Log()
    log.metadata = {'a': 1}
    assert 'a' in log.metadata
    assert log.metadata['a'] == 1
    with pytest.raises(ValueError):
        log.metadata = ()


def test_log_setter_dives():
    log = divelog.Log()
    log.dives = [divelog.Dive()]
    assert len(log.dives) == 1
    with pytest.raises(ValueError):
        log.dives = {}


def test_log_setter_unknown():
    log = divelog.Log()
    assert ('computer_color' not in dir(log))
    with pytest.raises(AttributeError):
        log.computer_color = 'red'
    assert ('computer_color' not in dir(log))


def test_dive_slots():
    slots = ['metadata', 'sequence_number', 'recording_interval',
             'leave_surface_time', 'reach_surface_time',
             'air_temperature', 'min_water_temperature',
             'max_depth', 'pressure_drop', 'altitude',
             'number_of_tanks', 'tank_volume',
             'tank_start_pressure', 'O2_mode',
             'rebreather_diluent_gas', 'record']
    dive = divelog.Dive()
    for slot in slots:
        assert slot in dir(dive)
    for slot in dir(dive):
        if not slot[0:2] == '__':
            assert slot in slots
