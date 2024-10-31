import unittest
import numpy as np
import pandas as pd


from app.utils.running_metrics import (
    calculate_cadence,
    calculate_distance,
    calculate_speed,
    calculate_vertical_oscillation,
    calculate_stride_length,
    calculate_ground_contact_time,
    calculate_pace,
    final_clean_data
)

from app.endpoints import *

class test_endpoints(unittest.TestCase):
    def setUp(self):
        """
        importing sample data
        """
        self.sample_data = pd.read_csv('tests/running_mock_data.csv')
        self.sample_data['time'] = pd.to_datetime(self.sample_data['time'], format="%Y-%m-%dT%H:%M:%S.%fZ")
        self.sample_data, self.axis = final_clean_data(self.sample_data)

    def test_endpoints(self):
        result = register_endpoints(self.sample_data)
        
        return 0.0
    
        