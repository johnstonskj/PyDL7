import io
import pytest

import divelog.json

import examples


def test_json_parser():
    file = io.StringIO("""
{
  "computer_model": "Mares Sport",
  "temperature_unit": "C",
  "depth_pressure_unit": "MSWG",
  "computer_serial": "8762-3478-6234",
  "altitude_unit": "ThM",
  "created": 1463616000.0,
  "depth_unit": "M",
  "tank_volume_unit": "L",
  "tank_pressure_unit": "bar",
  "dives": [
    {
      "air_temperature": 29.0,
      "number_of_tanks": 1,
      "tank_start_pressure": 0,
      "leave_surface_time": 1457175600.0,
      "pressure_drop": 0,
      "rebreather_diluent_gas": 0,
      "O2_mode": "",
      "recording_interval": "Q1M",
      "tank_volume": 0,
      "reach_surface_time": 1457176200.0,
      "min_water_temperature": 26.0,
      "max_depth": 50.0,
      "altitude": 0.0,
      "sequence_number": 0,
      "record": [
        {
          "elapsed_time": 0.0,
          "depth": 10.0,
          "OUT": 0,
          "ascent_rate": 0,
          "warning_number": 0,
          "ascent_rate_violation": false,
          "gas_switch": 0.0,
          "current_PO2": 0,
          "oxygen_flow_rate": 0,
          "current_ceiling": 0.0,
          "water_temperature": 26.0,
          "main_cylinder_pressure": 0.0,
          "CNS_toxicity": 0,
          "diluent_cylinder_pressure": 0,
          "decompression_violation": false
        },
        {
          "elapsed_time": 1.0,
          "depth": 20.0,
          "OUT": 0,
          "ascent_rate": 0,
          "warning_number": 0,
          "ascent_rate_violation": false,
          "gas_switch": 0.0,
          "current_PO2": 0,
          "oxygen_flow_rate": 0,
          "current_ceiling": 0.0,
          "water_temperature": 26.0,
          "main_cylinder_pressure": 0.0,
          "CNS_toxicity": 0,
          "diluent_cylinder_pressure": 0,
          "decompression_violation": false
        }
      ]
    }
  ]
}

""")
    log = divelog.json.parse(file)
    assert log.computer_model == 'Mares Sport'
    assert len(log.dives) == 1
    assert len(log.dives[0].record) == 2


def test_json_writer():
    log = examples.create_log()
    file = io.StringIO()
    divelog.json.dump(log, file)
    content = file.getvalue()
    assert '"leave_surface_time": 1457175600.0' in content
    assert '"computer_serial": "8762-3478-6234"' in content


def test_round_trip():
    examples.round_trip(divelog.json)
