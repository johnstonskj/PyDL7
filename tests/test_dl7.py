import io
import pytest

import divelog.dl7

import examples


def test_dl7_parser_FSH():
    file = io.StringIO("""
FSH|^~<>{}|DLMw01|ZXU|20160420083103|
""")
    log = divelog.dl7.parse(file)
    assert log.metadata['source_format'] == 'DL7'
    assert log.created.year == 2016
    assert log.created.month == 4
    assert log.created.day == 20


def test_dl7_parser_ZRH():
    file = io.StringIO("""
FSH|^~<>{}|DLMw01|ZXU|20160420083103|
ZRH|^~<>{}|Mares Sport|12345|MSWG|ThM|C|bar|L|
""")
    log = divelog.dl7.parse(file)
    assert log.computer_model == 'Mares Sport'
    assert log.computer_serial == '12345'
    assert log.depth_pressure_unit == 'MSWG'
    assert log.altitude_unit == 'ThM'
    assert log.temperature_unit == 'C'
    assert log.tank_pressure_unit == 'bar'
    assert log.tank_volume_unit == 'L'


def test_dl7_parser_ZDH():
    file = io.StringIO("""
FSH|^~<>{}|DLMw01|ZXU|20160420083103|
ZRH|^~<>{}|||MSWG|ThM|C|bar|L|
ZDH|1|1|I|Q5S|20160320114300||||||
""")
    log = divelog.dl7.parse(file)
    assert len(log.dives) == 1
    dive = log.dives[0]
    assert dive.metadata['export_sequence'] == 1
    assert dive.metadata['record_type'] == 'I'
    assert dive.sequence_number == 1
    assert dive.recording_interval == 'Q5S'
    assert dive.leave_surface_time.year == 2016
    assert dive.leave_surface_time.month == 3
    assert dive.leave_surface_time.day == 20


def test_dl7_parser_ZDT():
    file = io.StringIO("""
FSH|^~<>{}|DLMw01|ZXU|20160420083103|
ZRH|^~<>{}|||MSWG|ThM|C|bar|L|
ZDH|1|1|I|Q5S|20160320114300||||||
ZDT|1|1|15.00|20160320121005|9.4||
""")
    log = divelog.dl7.parse(file)
    assert len(log.dives) == 1
    dive = log.dives[0]
    assert dive.max_depth == 15.0
    assert dive.min_water_temperature == 9.4
    assert dive.reach_surface_time.year == 2016
    assert dive.reach_surface_time.month == 3
    assert dive.reach_surface_time.day == 20


def test_dl7_parser_ZDT():
    file = io.StringIO("""
FSH|^~<>{}|DLMw01|ZXU|20160420083103|
ZRH|^~<>{}|||MSWG|ThM|C|bar|L|
ZDH|1|1|I|Q5S|20160320114300||||||
ZDP{
|0.000|0.00|1|||||9.9||206.8|||||
|0.083|2.00|||T|T||9.9|||||||
ZDP}
ZDT|1|1|15.00|20160320121005|9.4||
""")
    log = divelog.dl7.parse(file)
    assert len(log.dives) == 1
    dive = log.dives[0]
    assert len(dive.record) == 2
    detail = dive.record[0]
    assert detail.elapsed_time == 0.0
    assert detail.depth == 0.0
    assert detail.gas_switch == 1
    assert detail.water_temperature == 9.9
    assert detail.main_cylinder_pressure == 206.8
    detail = dive.record[1]
    assert detail.elapsed_time == 0.083
    assert detail.depth == 2.0
    assert detail.gas_switch == 0
    assert detail.ascent_rate_violation is True
    assert detail.decompression_violation is True
    assert detail.water_temperature == 9.9
    assert detail.main_cylinder_pressure == 0


def test_dl7_parser_bad_line(caplog):
    file = io.StringIO("""
ZZZ|||
""")
    log = divelog.dl7.parse(file)
    for record in caplog.records:
        if record.levelname == 'WARN':
            assert record.message == 'invalid input: ZZZ|||'


def test_dl7_writer():
    log = examples.create_log()
    file = io.StringIO()
    divelog.dl7.dump(log, file)
    content = file.getvalue()
    assert content.startswith('FSH|^~<>{}|PyDL7|ZXU|')
    # TODO: more tests
