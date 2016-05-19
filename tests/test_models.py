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


def test_log_setter_errors():
    log = divelog.Log()
    time = log.created
    with pytest.raises(ValueError):
        log.created = {'msg': 'this is not a date'}
    assert log.created == time
    with pytest.raises(ValueError):
        log.depth_unit = 'lightyear'
    assert log.depth_unit == 'M'
    with pytest.raises(ValueError):
        log.depth_pressure_unit = 'lightyear'
    assert log.depth_pressure_unit == 'MSWG'
    with pytest.raises(ValueError):
        log.altitude_unit = 'lightyear'
    assert log.altitude_unit == 'ThM'
    with pytest.raises(ValueError):
        log.temperature_unit = 'lightyear'
    assert log.temperature_unit == 'C'
    with pytest.raises(ValueError):
        log.tank_pressure_unit = 'lightyear'
    assert log.tank_pressure_unit == 'bar'
    with pytest.raises(ValueError):
        log.tank_volume_unit = 'lightyear'
    assert log.tank_volume_unit == 'L'


def test_log_setter_created():
    log = divelog.Log()
    #   format:    YYYYMMDDhhmmss.s
    log.created = '20160518083029.2'
    assert log.created.year == 2016
    assert log.created.month == 5
    assert log.created.day == 18
    assert log.created.hour == 8
    assert log.created.minute == 30
    assert log.created.second == 29
    assert log.created.microsecond == 200000
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


def test_dive_setter_interval():
    dive = divelog.Dive()
    for ri in ['C', 'V', 'Q1S', 'Q1M', 'Q1W', 'Q1L',
               'D1f', 'D1m', 'D1b']:
        dive.recording_interval = ri
        assert dive.recording_interval == ri
    dive.recording_interval = 'C'
    for ri in ['Z', 'QS', 'QZM', 'Q1', 'Q1Z',
               'Df', 'DZm', 'D1Z']:
        print('***' + ri)
        with pytest.raises(ValueError):
            dive.recording_interval = ri
        assert dive.recording_interval == 'C'


def test_dive_setter_errors():
    dive = divelog.Dive()
    with pytest.raises(ValueError):
        dive.sequence_number = 'A'
    assert dive.sequence_number == 0
    with pytest.raises(ValueError):
        dive.air_temperature = 'cold'
    assert dive.air_temperature == 0.0
    with pytest.raises(ValueError):
        dive.min_water_temperature = 'cold'
    assert dive.min_water_temperature == 0.0
    with pytest.raises(ValueError):
        dive.max_depth = 'deep'
    assert dive.max_depth == 0.0
    with pytest.raises(ValueError):
        dive.O2_mode = 'unknown'
    assert dive.O2_mode == ''
    time = dive.leave_surface_time
    with pytest.raises(ValueError):
        dive.leave_surface_time = 20160420
    assert dive.leave_surface_time == time
    with pytest.raises(ValueError):
        dive.leave_surface_time = '20160499'
    assert dive.leave_surface_time == time
    with pytest.raises(ValueError):
        dive.leave_surface_time = {'msg': 'this is not a date'}
    assert dive.leave_surface_time == time


def test_dive_setter_metadata():
    dive = divelog.Dive()
    dive.metadata = {'a': 1}
    assert 'a' in dive.metadata
    assert dive.metadata['a'] == 1
    with pytest.raises(ValueError):
        dive.metadata = ()


def test_dive_setter_dives():
    dive = divelog.Dive()
    dive.record = [divelog.DiveDetail()]
    assert len(dive.record) == 1
    with pytest.raises(ValueError):
        dive.record = {}


def test_dive_setter_unknown():
    dive = divelog.Dive()
    assert ('location' not in dir(dive))
    with pytest.raises(AttributeError):
        dive.location = 'red'
    assert ('location' not in dir(dive))


def test_detail_slots():
    slots = ['elapsed_time', 'depth', 'current_ceiling', 'water_temperature',
             'ascent_rate', 'gas_switch', 'current_PO2',
             'main_cylinder_pressure', 'diluent_cylinder_pressure',
             'oxygen_flow_rate', 'CNS_toxicity', 'OUT',
             'warning_number', 'ascent_rate_violation',
             'decompression_violation']
    detail = divelog.DiveDetail()
    for slot in slots:
        assert slot in dir(detail)
    for slot in dir(detail):
        if not slot[0:2] == '__':
            assert slot in slots


def test_detail_setter_errors():
    detail = divelog.DiveDetail()
    with pytest.raises(ValueError):
        detail.elapsed_time = 'awhile'
    assert detail.elapsed_time == 0.0
    with pytest.raises(ValueError):
        detail.depth = 'deep'
    assert detail.depth == 0.0
    with pytest.raises(ValueError):
        detail.water_temperature = 'cold'
    assert detail.water_temperature == 0.0
    with pytest.raises(ValueError):
        detail.ascent_rate = 'fast'
    assert detail.ascent_rate == 0
    with pytest.raises(ValueError):
        detail.warning_number = 'nope'
    assert detail.warning_number == 0


def test_detail_setter_booleans():
    detail = divelog.DiveDetail()
    for value in [True, 'True', 'T', 1]:
        detail.ascent_rate_violation = value
        assert detail.ascent_rate_violation is True
    for value in [False, 'False', 'No', 'Nada', 'F', 0]:
        detail.ascent_rate_violation = value
        assert detail.ascent_rate_violation is False


def test_detail_setter_unknown():
    detail = divelog.DiveDetail()
    assert ('water_color' not in dir(detail))
    with pytest.raises(AttributeError):
        detail.water_color = 'greenish'
    assert ('water_color' not in dir(detail))
