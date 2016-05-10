"""
This module only contains the classes used to store parsed dive log data.
"""

class Log(object):
    """
    The Log class is the top-level object for parsed data.
    """
    def __init__(self):
        self.metadata = {}
        self.created = 0
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

class Diver(object):
    pass

class Dive(object):
    def __init__(self):
        self.metadata = {}
        self.sequence_number = 0
        self.recording_interval = 0
        # environment
        self.leave_surface_time = 0
        self.reach_surface_time = 0
        self.air_temperature = 0
        self.min_water_temperature = 0
        self.max_depth = 0
        self.pressure_drop = 0
        self.altitude = 0
        # equipment
        self.number_of_tanks = 1
        self.tank_volume = 0
        self.tank_start_pressure = 0
        self.O2_mode = ''
        self.rebreather_diluent_gas = 0
        self.record = []

class DiveDetail(object):
    def __init__(self):
        self.elapsed_time = 0
        # environment
        self.depth = 0
        self.current_ceiling = 0
        self.water_temperature = 0
        self.ascent_rate = 0
        # equipment
        self.gas_switch = 0
        self.current_PO2 = 0
        self.main_cynilder_pressure = 0
        self.diluent_cylinder_pressure = 0
        self.oxygen_flow_rate = 0
        self.CNS_toxicity = 0
        self.OUT = 0
        # flags
        self.warning_number = 0
        self.ascent_rate_violation = False
        self.decompression_violation = False

