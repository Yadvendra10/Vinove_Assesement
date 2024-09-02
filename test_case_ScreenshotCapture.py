# Screenshot Capture
# Test Case 5.1: Verify the system takes a screenshot of the active window on a Windows machine.
# Test Case 5.2: Verify the system takes a screenshot of the active window on a MacOS machine.
# Test Case 5.3: Verify the system takes a screenshot of the active window on a Linux machine.
# Test Case 5.4: Test the system’s behavior if the screenshot capture fails.
import unittest
from unittest.mock import patch
from PIL import Image

from app import take_screenshot

class TestScreenshotCapture(unittest.TestCase):

    @patch('platform.system', return_value='Windows')
    @patch('PIL.ImageGrab.grab')
    def test_screenshot_windows(self, mock_grab, mock_platform):
        mock_grab.return_value = Image.new('RGB', (100, 100))
        self.assertIsInstance(take_screenshot(), Image.Image)

    @patch('platform.system', return_value='Darwin')
    @patch('PIL.Image.frombytes')
    def test_screenshot_mac(self, mock_frombytes, mock_platform):
        mock_frombytes.return_value = Image.new('RGB', (100, 100))
        self.assertIsInstance(take_screenshot(), Image.Image)

    @patch('platform.system', return_value='Linux')
    @patch('PIL.ImageGrab.grab')
    def test_screenshot_linux(self, mock_grab, mock_platform):
        mock_grab.return_value = Image.new('RGB', (100, 100))
        self.assertIsInstance(take_screenshot(), Image.Image)

