# User Activity Logging
# Test Case 6.1: Verify that key presses are correctly logged.
# Test Case 6.2: Verify that mouse clicks are correctly logged.
# Test Case 6.3: Verify the activity log correctly updates with the active window’s usage time.
# Test Case 6.4: Ensure that the log resets key presses and mouse clicks after logging.
# Test Case 6.5: Test the behavior of the logging system when the battery is low.



import unittest
from unittest.mock import patch
from datetime import datetime

from app import get_active_window, log_activity

class TestUserActivityLogging(unittest.TestCase):

    @patch('datetime.datetime.now')
    def test_logging_key_presses(self, mock_now):
        global key_presses, activity_log
        key_presses = 5
        mock_now.return_value = datetime(2024, 1, 1, 0, 0, 0)
        log_activity()
        self.assertEqual(activity_log[get_active_window()]['key_presses'], 5)

    @patch('datetime.datetime.now')
    def test_logging_mouse_clicks(self, mock_now):
        global mouse_clicks, activity_log
        mouse_clicks = 3
        mock_now.return_value = datetime(2024, 1, 1, 0, 0, 0)
        log_activity()
        self.assertEqual(activity_log[get_active_window()]['mouse_clicks'], 3)

    @patch('datetime.datetime.now')
    def test_logging_usage_time(self, mock_now):
        mock_now.side_effect = [datetime(2024, 1, 1, 0, 0, 0), datetime(2024, 1, 1, 0, 0, 5)]
        log_activity()
        self.assertGreater(activity_log[get_active_window()]['usage_time'], 0)

    @patch('builtins.print')  # Suppress print statements
    def test_low_battery_logging(self, mock_print):
        with patch('psutil.sensors_battery', return_value=type('Battery', (), {'percent': 15, 'power_plugged': False})):
            log_activity()
            self.assertNotIn(get_active_window(), activity_log)  # No logging if battery is low

