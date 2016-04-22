from divelog import *

def parse_file_header(log, line):
    log.metadata['source_format'] = 'DL7'
    log.metadata['encoding_characters'] = line[0]
    log.metadata['sending_application'] = line[1]
    log.metadata['message_type'] = line[2]
    log.created = line[3]

def parse_record_header(log, line):
    log.metadata['record_encoding_characters'] = line[0]
    log.computer_model = line[1]
    log.computer_serial = line[2]
    log.depth_pressure_unit = line[3]
    log.altitude_unit = line[4]
    log.temperature_unit = line[5]
    log.tank_pressure_unit = line[6]
    log.tank_volume_unit = line[7]

def parse_dive_header(log, line):
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

def parse_dive_profile(log, line):
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

def parse_dive_trailer(log, line):
    dive = log.dives[len(log.dives)-1]
    # export sequence
    # internal sequence
    dive.max_depth = line[2]
    dive.reach_surface_time = line[3]
    dive.min_water_temperature = line[4]
    dive.pressure_drop = line[5]

def parse_dive_profile_start(log, line):
    parsers[''] = parse_dive_profile

def parse_dive_profile_end(log, line):
    parsers[''] = parse_none

def parse_none(log, line):
    print(line)

parsers = { # ZXU - Dive Profile
    'FSH': parse_file_header,
    'ZAR': parse_none, # application reserved ZAR{...}
    'ZRH': parse_record_header,
    'ZAR': parse_none,
    'ZDH': parse_dive_header,
    'ZDP': parse_dive_profile,
    'ZDP{': parse_dive_profile_start,
    'ZDP}': parse_dive_profile_end,
    'ZDT': parse_dive_trailer,
    '': parse_none
}

def parseline(log, line):
    fields = line.strip().split('|')
    line_type = fields[0]
    if line_type in parsers:
        parsers[line_type](log, fields[1:])
#    else:
#        print(line)

def parse(file):
    log = Log()
    content = file.readline()
    while not content == '':
        parseline(log, content)
        content = file.readline()
    return log


def dump(log, file):
    pass
