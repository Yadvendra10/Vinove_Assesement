# Battery Check
# Test Case 3.1: Verify the system correctly identifies when the battery level is below 20% and is not plugged in.
# Test Case 3.2: Verify that the system does not trigger low battery alerts when the battery is above 20%.
# Test Case 3.3: Test that the function returns False if the battery sensor is not available (e.g., in a desktop environment).

import unittest
from unittest.mock import patch

from app import check_battery

class TestBatteryCheck(unittest.TestCase):

    @patch('psutil.sensors_battery')
    def test_low_battery_detected(self, mock_battery):
        mock_battery.return_value = type('Battery', (), {'percent': 15, 'power_plugged': False})
        self.assertTrue(check_battery())

    @patch('psutil.sensors_battery')
    def test_battery_above_20(self, mock_battery):
        mock_battery.return_value = type('Battery', (), {'percent': 25, 'power_plugged': False})
        self.assertFalse(check_battery())

    @patch('psutil.sensors_battery')
    def test_no_battery_sensor(self, mock_battery):
        mock_battery.return_value = None
        self.assertFalse(check_battery())

