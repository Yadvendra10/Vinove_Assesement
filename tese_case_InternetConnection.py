# Internet Connectivity Check
# Test Case 1.1: Verify the function returns True when internet connectivity is available.
# Test Case 1.2: Verify the function returns False when internet connectivity is not available.
# Test Case 1.3: Verify the function handles exceptions gracefully when the URL is unreachable.


import unittest
from unittest.mock import patch, Mock
from app import checkInternetUrllib

class TestInternetConnectivity(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_check_internet_connectivity_success(self, mock_urlopen):
        # Simulate successful internet connection
        mock_urlopen.return_value = Mock()
        self.assertTrue(checkInternetUrllib())

    @patch('urllib.request.urlopen', side_effect=Exception("No Internet"))
    def test_check_internet_connectivity_failure(self, mock_urlopen):
        # Simulate failed internet connection
        self.assertFalse(checkInternetUrllib())

if __name__ == '__main__':
    unittest.main()
