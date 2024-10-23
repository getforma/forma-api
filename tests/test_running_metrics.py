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
        """
        importing sample data
        """
        self.sample_data = pd.read_csv('tests/running_mock_data.csv')

    def test_calculate_cadence(self):
        result = calculate_cadence(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 169.02)  

    def test_calculate_distance(self):
        result = calculate_distance(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 4848.356246070045)  

    def test_calculate_speed(self):
        result = calculate_speed(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 3.265724233672104)  

    def test_calculate_vertical_oscillation(self):
        result = calculate_vertical_oscillation(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 0.20803382412734073)  

    def test_calculate_stride_length(self):
        result = calculate_stride_length(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 1.4861219026772634)  

    def test_calculate_ground_contact_time(self):
        result = calculate_ground_contact_time(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 293.29238133226966)  

    def test_calculate_pace(self):
        result = calculate_pace(self.sample_data)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 5.103513179349512)  

if __name__ == '__main__':
    unittest.main()

