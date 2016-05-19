"""
This module creates data that can be shared by different test modules.
"""
import datetime
import io

import divelog


def create_log(add_dives=True):
    log = divelog.Log()
    log.computer_model = 'Mares Sport'
    log.computer_serial = '8762-3478-6234'
    if add_dives:
        log.dives.append(create_dive(True))
    return log


def create_dive(add_record=True, sequence_number=0, records=10):
    dive = divelog.Dive()
    dive.sequence_number = sequence_number
    dive.recording_interval = 'Q1M'
    dive.leave_surface_time = datetime.datetime(2016, 3, 5+sequence_number,
                                                11, 0,
                                                tzinfo=datetime.timezone.utc)
    dive.reach_surface_time = datetime.datetime(2016, 3, 5+sequence_number,
                                                11, records,
                                                tzinfo=datetime.timezone.utc)
    dive.air_temperature = 29.0
    dive.min_water_temperature = 26.0
    dive.max_depth = (records / 2) * 10
    if add_record:
        dive.record = create_record(records)
    return dive


def create_record(iterations):
    mid = iterations / 2
    depth = 0
    record = []
    for i in range(iterations):
        detail = divelog.DiveDetail()
        detail.elapsed_time = i
        if i < mid:
            depth = depth + 10
        else:
            depth = depth - 10
        detail.depth = depth
        detail.water_temperature = 26.0
        if i == iterations-1:
            detail.ascent_rate_violation = True
            detail.decompression_violation = True
        record.append(detail)
    return record


def round_trip(module):
    # Does not compare metadata!
    log = create_log()
    outp = io.StringIO()
    module.dump(log, outp)
    content = outp.getvalue()
    inp = io.StringIO(content)
    log2 = module.parse(inp)
    assert log2.created == log.created
    assert log2.computer_model == log.computer_model
    assert log2.computer_serial == log.computer_serial
    assert log2.depth_pressure_unit == log.depth_pressure_unit
    assert log2.altitude_unit == log.altitude_unit
    assert log2.temperature_unit == log.temperature_unit
    assert log2.tank_pressure_unit == log.tank_pressure_unit
    assert log2.tank_volume_unit == log.tank_volume_unit
    assert len(log2.dives) == len(log.dives)
    for i in range(len(log2.dives)):
        dive = log.dives[i]
        dive2 = log2.dives[i]
        assert dive2.sequence_number == dive.sequence_number
        assert dive2.recording_interval == dive.recording_interval
        assert dive2.leave_surface_time == dive.leave_surface_time
        assert dive2.max_depth == dive.max_depth
        assert dive2.min_water_temperature == dive.min_water_temperature
        assert dive2.reach_surface_time == dive.reach_surface_time
        assert len(dive2.record) == len(dive.record)
        for j in range(len(dive2.record)):
            det = dive.record[j]
            det2 = dive2.record[j]
            assert det2.elapsed_time == det.elapsed_time
            assert det2.depth == det.depth
            assert det2.current_ceiling == det.current_ceiling
            assert det2.water_temperature == det.water_temperature
            assert det2.ascent_rate == det.ascent_rate
            assert det2.gas_switch == det.gas_switch
            assert det2.current_PO2 == det.current_PO2
            assert det2.main_cylinder_pressure == det.main_cylinder_pressure
            assert (det2.diluent_cylinder_pressure ==
                    det.diluent_cylinder_pressure)
            assert det2.oxygen_flow_rate == det.oxygen_flow_rate
            assert det2.CNS_toxicity == det.CNS_toxicity
            assert det2.OUT == det.OUT
            assert det2.warning_number == det.warning_number
            assert det2.ascent_rate_violation == det.ascent_rate_violation
            assert det2.decompression_violation == det.decompression_violation
