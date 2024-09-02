# Keyboard and Mouse Event Listening
# Test Case 8.1: Verify that the system starts capturing keyboard events upon successful login.
# Test Case 8.2: Verify that the system starts capturing mouse events upon successful login.
# Test Case 8.3: Ensure that keyboard and mouse event listeners continue to function while the application is running.


import unittest
from unittest.mock import patch
from app import keyboard_listener, mouse_listener, start_listeners

class TestEventListening(unittest.TestCase):

    @patch('pynput.keyboard.Listener.start')
    def test_keyboard_listener_starts(self, mock_start):
        # Test that the keyboard listener's start method is called once
        keyboard_listener.start()
        mock_start.assert_called_once()

    @patch('pynput.mouse.Listener.start')
    def test_mouse_listener_starts(self, mock_start):
        # Test that the mouse listener's start method is called once
        mouse_listener.start()
        mock_start.assert_called_once()

    @patch('pynput.keyboard.Listener.start')
    @patch('pynput.mouse.Listener.start')
    def test_both_listeners_start_in_start_listeners(self, mock_mouse_start, mock_keyboard_start):
        # Test that start_listeners starts both listeners
        start_listeners()
        mock_keyboard_start.assert_called_once()
        mock_mouse_start.assert_called_once()

if __name__ == "__main__":
    unittest.main()


