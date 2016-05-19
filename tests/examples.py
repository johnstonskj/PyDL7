"""
This module creates data that can be shared by different test modules.
"""
import datetime

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
                                                11, 0)
    dive.reach_surface_time = datetime.datetime(2016, 3, 5+sequence_number,
                                                11, records)
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
        record.append(detail)
    return record
