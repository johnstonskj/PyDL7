class Log(object):
    pass

class Diver(object):
    pass

class Dive(object):
    pass

class DiveDetail(object):
    pass

def parse_file_header(log, line):
    log.encodingCharacters = line[0]
    log.sendingApplication = line[1]
    log.messageType = line[2]
    log.creationDateTime = line[3]
    log.dives = []

def parse_record_header(log, line):
    log.recordEncodingCharacters = line[0]
    log.recordingComputer = line[1]
    log.recordingComputerSerial = line[2]
    log.depthPressureUnit = line[3]
    log.altitudeUnit = line[4]
    log.temperatureUnit = line[5]
    log.tankPressureUnit = line[6]
    log.tankVolumeUnit = line[7]

def parse_dive_header(log, line):
    dive = Dive()
    dive.record = []
    log.dives.append(dive)
    dive.exportSequence = line[0]
    dive.internalSequence = line[1]
    dive.recordType = line[2]
    dive.recordingInterval = line[3]
    dive.leaveSurfaceTime = line[4]
    dive.airTemperature = line[5]
    dive.tankVolume = line[6]
    dive.o2Mode = line[7]
    dive.rebreatherDiluentGas = line[8]
    dive.Altitude = line[9]

def parse_dive_profile(log, line):
    dive = log.dives[len(log.dives)-1]
    detail = DiveDetail()
    dive.record.append(detail)
    detail.time = line[0]
    detail.depth = line[1]
    detail.gasSwitch = line[2]
    detail.currentPO2 = line[3]
    detail.ascentRateViolation = line[4]
    detail.decompressionViolation = line[5]
    detail.currentCeiling = line[6]
    detail.currentWaterTemperature = line[7]
    detail.warningNumber = line[8]
    detail.mainCylinderPressure = line[9]
    detail.diluentCylinderPressure = line[10]
    detail.oxygenFlowRate = line[11]
    detail.CNSToxicity = line[12]
    detail.OUT = line[13]
    detail.ascentRate = line[14]

def parse_dive_trailer(log, line):
    dive = log.dives[len(log.dives)-1]
    # export sequence
    # internal sequence
    dive.maximumDepth = line[2]
    dive.reachSurfaceTime = line[3]
    dive.minimumWaterTemperature = line[4]
    dive.pressureDrop = line[5]

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
