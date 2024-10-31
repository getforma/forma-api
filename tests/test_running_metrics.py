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

class TestRunningMetrics(unittest.TestCase):

    def setUp(self):
        """
        importing sample data
        """
        self.sample_data = pd.read_csv('tests/running_mock_data.csv')
        self.sample_data['time'] = pd.to_datetime(self.sample_data['time'], format="%Y-%m-%dT%H:%M:%S.%fZ")
        self.sample_data, self.axis = final_clean_data(self.sample_data)

    def test_calculate_cadence(self):
        result = calculate_cadence(self.sample_data, self.axis)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 159.55608812766104, places=4)  

    def test_calculate_distance(self):
        result = calculate_distance(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 4848.356246070045, places=2)  

    def test_calculate_speed(self):
        distance = calculate_distance(self.sample_data)
        result = calculate_speed(self.sample_data, distance)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 3.265724233672104, places=4)  

    def test_calculate_vertical_oscillation(self):
        result = calculate_vertical_oscillation(self.sample_data, self.axis)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 0.1445607649730728, places=4)  

    def test_calculate_stride_length(self):
        distance = calculate_distance(self.sample_data)
        speed = calculate_speed(self.sample_data, distance)
        result = calculate_stride_length(self.sample_data, self.axis, speed)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 0.660511325062425, places=4)  

    def test_calculate_ground_contact_time(self):
        result = calculate_ground_contact_time(self.sample_data, self.axis)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 177.20541058175723, places=4)  

    def test_calculate_pace(self):
        distance = calculate_distance(self.sample_data)
        speed = calculate_speed(self.sample_data, distance)
        result = calculate_pace(self.sample_data, speed)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 5.103513179349512, places=4)  

if __name__ == '__main__':
    unittest.main()

