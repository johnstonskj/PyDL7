"""
This module implements a format handler for DAN DL7 files. These are line
oriented, character separated, and poorly documented. This parser doesn't 
handle all possible record types at this time.
"""
from divelog import *
import logging

FORMAT_NAME = 'DL7'

logger = logging.getLogger(__name__)

def __parse_file_header(log, line):
    logger.debug('parsing file header metadata')
    log.metadata['source_format'] = 'DL7'
    log.metadata['encoding_characters'] = line[0]
    log.metadata['sending_application'] = line[1]
    log.metadata['message_type'] = line[2]
    log.created = line[3]

def __parse_record_header(log, line):
    logger.debug('parsing record header')
    log.metadata['record_encoding_characters'] = line[0]
    log.computer_model = line[1]
    log.computer_serial = line[2]
    log.depth_pressure_unit = line[3]
    log.altitude_unit = line[4]
    log.temperature_unit = line[5]
    log.tank_pressure_unit = line[6]
    log.tank_volume_unit = line[7]

def __parse_dive_header(log, line):
    logger.debug('parsing dive header')
    dive = Dive()
    dive.record = []
    log.dives.append(dive)
    dive.metadata['export_sequence'] = line[0]
    dive.sequence_number = line[1]
    dive.metadata['record_type'] = line[2]
    dive.recording_interval = line[3]
    dive.leave_surface_time = line[4]
    dive.air_temperature = line[5]
    dive.tank_volume = line[6]
    dive.O2_mode = line[7]
    dive.rebreather_diluent_gas = line[8]
    dive.altitude = line[9]

def __parse_dive_profile(log, line):
    logger.debug('parsing dive profile data')
    dive = log.dives[len(log.dives)-1]
    detail = DiveDetail()
    dive.record.append(detail)
    detail.elapsed_time = line[0]
    detail.depth = line[1]
    detail.gas_switch = line[2]
    detail.current_PO2 = line[3]
    detail.ascent_rate_violation = line[4]
    detail.decompression_violation = line[5]
    detail.current_ceiling = line[6]
    detail.water_temperature = line[7]
    detail.warning_number = line[8]
    detail.main_cylinder_pressure = line[9]
    detail.diluent_cylinder_pressure = line[10]
    detail.oxygen_flow_rate = line[11]
    detail.CNS_toxicity = line[12]
    detail.OUT = line[13]
    detail.ascent_rate = line[14]

def __parse_dive_trailer(log, line):
    logger.debug('parsing dive trailer')
    dive = log.dives[len(log.dives)-1]
    # export sequence
    # internal sequence
    dive.max_depth = line[2]
    dive.reach_surface_time = line[3]
    dive.min_water_temperature = line[4]
    dive.pressure_drop = line[5]

def __parse_dive_profile_start(log, line):
    parsers[''] = parse_dive_profile

def __parse_dive_profile_end(log, line):
    parsers[''] = parse_none

def __parse_none(log, line):
    print(line)

__parsers = { # ZXU - Dive Profile
    'FSH': __parse_file_header,
    'ZAR': __parse_none, # application reserved ZAR{...}
    'ZRH': __parse_record_header,
    'ZAR': __parse_none,
    'ZDH': __parse_dive_header,
    'ZDP': __parse_dive_profile,
    'ZDP{': __parse_dive_profile_start,
    'ZDP}': __parse_dive_profile_end,
    'ZDT': __parse_dive_trailer,
    '': __parse_none
}

def __parse_line(log, line):
    fields = line.strip().split('|')
    line_type = fields[0]
    if line_type in parsers:
        __parsers[line_type](log, fields[1:])
    else:
        logger.warn('invalid input: %s' % line)

def parse(file):
    """
    Parse this file object and return either a new top-level Log
    object, or None.
    """
    logger.info('parsing DL7 dive log data')
    log = Log()
    content = file.readline()
    while not content == '':
        __parse_line(log, content)
        content = file.readline()
    return log


def dump(log, file):
    """
    Serialize the log to the provided file object.
    """
    pass
