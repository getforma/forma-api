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
    calculate_pace
)

class TestRunningMetrics(unittest.TestCase):

    def setUp(self):
        '''
        @carson, you can create a mock dataframe for testing here. Or you can also do option 2:

        Option 1:
        self.sample_data = pd.DataFrame({
            'time': np.arange(0, 10, 0.1),
            'acceleration_x': np.random.rand(100),
            'acceleration_y': np.random.rand(100),
            'acceleration_z': np.random.rand(100),
        })
        
        Option 2:
        Read from a csv file
        self.sample_data = pd.read_csv('tests/sample_data.txt', sep='\t')

        In this case, save a sample_data.txt file in the tests folder.
        '''
        self.sample_data = pd.DataFrame({
            'time': np.arange(0, 10, 0.1),
            'acceleration_x': np.random.rand(100),
            'acceleration_y': np.random.rand(100),
            'acceleration_z': np.random.rand(100),
            # Add remaining columns here
        })

    def test_calculate_cadence(self):
        result = calculate_cadence(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)  # Update this when the function is implemented

    def test_calculate_distance(self):
        result = calculate_distance(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)  # Update this when the function is implemented

    def test_calculate_speed(self):
        result = calculate_speed(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)  # Update this when the function is implemented

    def test_calculate_vertical_oscillation(self):
        result = calculate_vertical_oscillation(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)  # Update this when the function is implemented

    def test_calculate_stride_length(self):
        result = calculate_stride_length(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)  # Update this when the function is implemented

    def test_calculate_ground_contact_time(self):
        result = calculate_ground_contact_time(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)  # Update this when the function is implemented

    def test_calculate_pace(self):
        result = calculate_pace(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)  # Update this when the function is implemented

if __name__ == '__main__':
    unittest.main()

