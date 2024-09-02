# GUI Functionality
# Test Case 7.1: Verify that the login screen is displayed correctly when the application starts.
# Test Case 7.2: Verify that the OTP input screen appears after a successful login.
# Test Case 7.3: Ensure that the main window with activity logs and screenshots is displayed after OTP validation.
# Test Case 7.4: Test the logout button to ensure it returns the user to the login screen.
# Test Case 7.5: Test the GUI update functionality to ensure the activity log tree view is populated correctly.
# Test Case 7.6: Verify the screenshot display functionality in the GUI.

import unittest
from unittest.mock import patch
import tkinter as tk

from app import show_login_window, show_main_window, show_otp_window

class TestGUIFunctionality(unittest.TestCase):

    @patch('tkinter.Tk')
    def test_login_window_display(self, mock_tk):
        root = mock_tk.return_value
        show_login_window(root)
        root.winfo_children.assert_called()

    @patch('tkinter.Tk')
    def test_otp_window_display(self, mock_tk):
        root = mock_tk.return_value
        show_otp_window(root, 'admin')
        root.winfo_children.assert_called()

    @patch('tkinter.Tk')
    def test_main_window_display(self, mock_tk):
        root = mock_tk.return_value
        show_main_window(root)
        root.winfo_children.assert_called()

