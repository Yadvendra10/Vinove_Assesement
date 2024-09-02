# Active Window Retrieval
# Test Case 4.1: Verify the function correctly identifies the active window on a Windows machine.
# Test Case 4.2: Verify the function correctly identifies the active window on a MacOS machine.
# Test Case 4.3: Verify the function correctly identifies the active window on a Linux machine.
# Test Case 4.4: Ensure the function handles cases where no active window can be detected.

import unittest
from unittest.mock import patch

from app import get_active_window


class TestActiveWindowRetrieval(unittest.TestCase):

    @patch('platform.system', return_value='Windows')
    @patch('win32gui.GetWindowText')
    def test_active_window_windows(self, mock_window_text, mock_platform):
        mock_window_text.return_value = 'Test Window'
        self.assertEqual(get_active_window(), 'Test Window')

    @patch('platform.system', return_value='Darwin')
    @patch('AppKit.NSWorkspace.sharedWorkspace().activeApplication')
    def test_active_window_mac(self, mock_active_app, mock_platform):
        mock_active_app.return_value = {'NSApplicationName': 'Test App'}
        self.assertEqual(get_active_window(), 'Test App')

    @patch('platform.system', return_value='Linux')
    @patch('subprocess.check_output')
    def test_active_window_linux(self, mock_check_output, mock_platform):
        mock_check_output.return_value = b'Test Window'
        self.assertEqual(get_active_window(), 'Test Window')

