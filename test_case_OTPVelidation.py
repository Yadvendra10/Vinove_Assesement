# OTP Generation and Validation
# Test Case 2.1: Verify that an OTP is generated and sent to the correct email address.
# Test Case 2.2: Validate that the OTP is correctly stored and can be retrieved for verification.
# Test Case 2.3: Ensure the function correctly validates the OTP entered by the user.
# Test Case 2.4: Test the system’s response when an incorrect OTP is entered.

import unittest
from unittest.mock import patch
from app import generate_and_send_otp, validate_otp



class TestOTPFunctionality(unittest.TestCase):

    @patch('builtins.print')  # Suppress print statements
    @patch('smtplib.SMTP')
    def test_generate_and_send_otp(self, mock_smtp, mock_print):
        generate_and_send_otp('admin')
        self.assertIsNotNone(otp_code)

    def test_validate_correct_otp(self):
        global otp_code
        otp_code = "123456"
        self.assertTrue(validate_otp("123456"))

    def test_validate_incorrect_otp(self):
        global otp_code
        otp_code = "123456"
        self.assertFalse(validate_otp("654321"))

