"""
This module only contains the classes used to store parsed dive log data. These
classes may be used directly to create a model and write to a file, or more
likely they are the result of a parse() function on an input file.

The structure of a log in memory consists of a list of dives, each of which
contains a list of dive details (the dive record). Dive details are recorded
by a dive computer and represent depth, temperature, and so on.

  Log
    .dives = [
      Dive
        .record = [
          DiveDetails
        ]
    ]

Note that certain objects contain a dictionary 'metadata' that is not defined
by this model and typically contains details included in the serialized format
that may be required when writing it back to a file but doesn't represent
details of the dive itself.
"""
import collections
import datetime
import logging
import re


logger = logging.getLogger(__name__)


NMRI_PRESSURE_CODE = {
    'ATA': 'atmospheres absolute',
    'bar': 'bar absolute',
    'FFWG': 'feet freshwater, gauge',
    'FL': 'Altitude: FL or Flight Level, Feet/10**2',
    'FSWG': 'feet seawater gauge',
    'kgsc': 'kg/cm**2 absolute',
    'kPa': 'kilopascal absolute',
    'MFWA': 'meters freshwater absolute',
    'MFWG': 'meters freshwater, gauge',
    'MPa': 'megapascal absolute',
    'MSWG': 'meters seawater gauge',
    'PSIA': 'pounds per square inch absolute',
    'ThFt': 'Altitude:  Feet/10**3',
    'ThM': 'Altitude: Meters/10**3',
    'barg': 'Bar gauge pressure'
    }


DEPTH_UNITS = {
    'M': 'meters',
    'FT': 'feet'
    }


TEMP_UNITS = {
    'F': 'degree Fahrenheit',
    'C': 'degree Celsius',
    'K': 'degree Kelvin'
    }


VOLUME_UNITS = {
    'L': 'liter',
    'CF': 'cubic feet'
    }


__now__ = datetime.datetime.now()
DEFAULT_NOW = __now__.strftime('%Y%m%d')


def value_error(value, name):
    message = 'invalid value (%s) for property %s, ignoring' % (value, name)
    logger.warn(message)
    raise ValueError(message)


def attribute_error(obj, name):
    raise AttributeError('no property named %s on class %s' %
                         (name, obj.__class__.__name__))


class Log(object):
    """
    The Log class is the top-level object for parsed data.
    """
    def __init__(self):
        self.metadata = {}
        self.created = DEFAULT_NOW
        # recorder
        self.computer_model = ''
        self.computer_serial = ''
        # units (metric)
        self.depth_unit = 'M'
        self.depth_pressure_unit = 'MSWG'
        self.altitude_unit = 'ThM'
        self.temperature_unit = 'C'
        self.tank_pressure_unit = 'bar'
        self.tank_volume_unit = 'L'
        # actual dives
        self.dives = []

    def __setattr__(self, name, value):
        if name == 'created':
            if isinstance(value, str):
                try:
                    parsed = parse_timestamp(value)
                    super(Log, self).__setattr__(name, parsed)
                except ValueError:
                    value_error(value, name)
            elif isinstance(value, datetime.datetime):
                super(Log, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name == 'depth_unit':
            if value in DEPTH_UNITS:
                super(Log, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name in ['depth_pressure_unit', 'altitude_unit',
                      'tank_pressure_unit']:
            if value in NMRI_PRESSURE_CODE:
                super(Log, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name == 'temperature_unit':
            if value in TEMP_UNITS:
                super(Log, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name == 'tank_volume_unit':
            if value in VOLUME_UNITS:
                super(Log, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name == 'metadata':
            if isinstance(value, collections.Mapping):
                super(Log, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name == 'dives':
            if isinstance(value, collections.Sequence):
                super(Log, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name in ['computer_model', 'computer_serial']:
            super(Log, self).__setattr__(name, value)
        else:
            attribute_error(self, name)

def parse_timestamp(ts):
    """
    Parse a timestamp in the specified DL7 format into a standard Python
    datetime object. Return a datetime, or None if the input is not valid.

    DL7 timestamp format:
      YYYY[MM[DD[HHMM[SS[.S[S[S[S]]]]]]]][+/-ZZZZ]^<degree of precision>
    """
    m = re.match('(?P<Y>\d\d\d\d)(?P<M>\d\d)?(?P<D>\d\d)?' +
                 '(?P<HM>\d\d\d\d)?(?P<S>\d\d)?(?P<MS>\.\d+)?' +
                 '(?P<Z>[\+\-]\d\d\d\d)?(?P<P>\^\d+)?', ts)
    if m:
        year = int(m.group('Y'))
        month = int((m.group('M') or 0))
        day = int((m.group('D') or 0))
        if m.group('HM'):
            hour = int(m.group('HM')[0:2])
            minute = int(m.group('HM')[2:])
        else:
            hour = minute = 0
        seconds = int((m.group('S') or 0))
        if m.group('MS'):
            millis = int(m.group('MS')[1:]) * 100000
        else:
            millis = 0
        # This raises ValueError on bad input
        return datetime.datetime(year, month, day, hour,
                                 minute, seconds, millis)
    else:
        raise ValueError('invalid format (%s) for timestamp' % ts)


class Diver(object):
    """
    Currently undefined
    """
    pass


class Dive(object):
    def __init__(self):
        self.metadata = {}
        self.sequence_number = 0
        self.recording_interval = 'V'
        # environment
        self.leave_surface_time = DEFAULT_NOW
        self.reach_surface_time = DEFAULT_NOW
        self.air_temperature = 0.0
        self.min_water_temperature = 0.0
        self.max_depth = 0.0
        self.pressure_drop = 0
        self.altitude = 0
        # equipment
        self.number_of_tanks = 1
        self.tank_volume = 0
        self.tank_start_pressure = 0
        self.O2_mode = ''
        self.rebreather_diluent_gas = 0
        self.record = []

    def __setattr__(self, name, value):
        if name == 'metadata':
            if isinstance(value, collections.Mapping):
                super(Dive, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name in ['sequence_number', 'pressure_drop',
                      'number_of_tanks', 'tank_volume',
                      'tank_start_pressure', 'rebreather_diluent_gas']:
            if value == '':
                value = 0
            try:
                super(Dive, self).__setattr__(name, int(value))
            except ValueError:
                value_error(value, name)
        elif name in ['leave_surface_time', 'reach_surface_time']:
            if isinstance(value, str):
                try:
                    parsed = parse_timestamp(value)
                    super(Dive, self).__setattr__(name, parsed)
                except ValueError:
                    value_error(value, name)
            elif isinstance(value, datetime.datetime):
                super(Dive, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name in ['air_temperature', 'altitude',
                      'min_water_temperature', 'max_depth']:
            if value == '':
                value = 0.0
            try:
                super(Dive, self).__setattr__(name, float(value))
            except ValueError:
                value_error(value, name)
        elif name == 'recording_interval':
            try:
                sri = split_recording_interval(value)
                super(Dive, self).__setattr__(name, value)
            except ValueError:
                value_error(value, name)
        elif name == 'O2_mode':
            if value in ['PO2', 'FO2', '']:  # '' = unknown
                super(Dive, self).__setattr__(name, value)
            else:
                value_error(value, name)
        elif name == 'record':
            if isinstance(value, collections.Sequence):
                super(Dive, self).__setattr__(name, value)
            else:
                value_error(value, name)
        else:
            attribute_error(self, name)


def split_recording_interval(ri):
    t = ''
    i = ''
    u = ''
    if ri[0] in ['Q', 'D']:
        t = ri[0]
        if ri[-1:] in {'Q': ['S', 'M', 'W', 'L'], 'D': ['f', 'm', 'b']}[t]:
            u = ri[-1:]
            try:
                i = int(ri[1:-1])
            except ValueError:
                logger.warn('invalid value (%s) for recording interval value' % ri)
                raise
        else:
            logger.warn('invalid value (%s) for recording interval unit' % ri)
            raise ValueError()
    elif ri[0] in ['C', 'V']:
        t = ri[0]
    else:
        logger.warn('invalid value (%s) for recording interval type' % ri)
        raise ValueError()
    return (t, i, u)


def format_recording_interval(ri):
    (t, i, u) = split_recording_interval(ri)
    t = {'Q': 'Every', 'C': 'Continuously',
         'V': 'Variable', 'D': 'On Change'}[t]
    u = {
        'S': 'second', 'M': 'minute',
        'f': 'feet', 'm': 'meter', 'b': 'bar'}[u]
    return ('%s %s %s' % (t, i, u)).strip()


class DiveDetail(object):
    def __init__(self):
        self.elapsed_time = 0.0
        # environment
        self.depth = 0.0
        self.current_ceiling = 0.0
        self.water_temperature = 0.0
        self.ascent_rate = 0
        # equipment
        self.gas_switch = 0
        self.current_PO2 = 0
        self.main_cylinder_pressure = 0
        self.diluent_cylinder_pressure = 0
        self.oxygen_flow_rate = 0
        self.CNS_toxicity = 0
        self.OUT = 0
        # flags
        self.warning_number = 0
        self.ascent_rate_violation = False
        self.decompression_violation = False

    def __setattr__(self, name, value):
        if name in ['ascent_rate', 'current_PO2',
                    'diluent_cylinder_pressure', 'oxygen_flow_rate',
                    'CNS_toxicity', 'OUT', 'warning_number']:
            if value == '':
                value = 0
            try:
                super(DiveDetail, self).__setattr__(name, int(value))
            except ValueError:
                value_error(value, name)
        elif name in ['current_ceiling', 'elapsed_time', 'depth', 
                      'water_temperature', 'gas_switch', 
                      'main_cylinder_pressure']:
            if value == '':
                value = 0.0
            try:
                super(DiveDetail, self).__setattr__(name, float(value))
            except ValueError:
                value_error(value, name)
        elif name in ['ascent_rate_violation', 'decompression_violation']:
            if value in [True, 'True', 'T', 1]:
                super(DiveDetail, self).__setattr__(name, True)
            else:
                super(DiveDetail, self).__setattr__(name, False)
        else:
            attribute_error(self, name)
