import unittest
from unittest.mock import patch, MagicMock
from app import take_screenshot, upload_to_s3, validate_login

class TestErrorHandling(unittest.TestCase):

    @patch('PIL.ImageGrab.grab', side_effect=Exception('Screenshot failed'))
    def test_screenshot_capture_failure(self, mock_grab):
        # Test that an exception is raised when screenshot capture fails
        with self.assertRaises(Exception) as context:
            take_screenshot()
        self.assertEqual(str(context.exception), 'Screenshot failed')

    @patch('builtins.print')  # Suppress print statements during testing
    @patch('boto3.Session')
    def test_s3_upload_failure(self, mock_session, mock_print):
        # Mock the session to raise a NoCredentialsError
        mock_session.side_effect = Exception('NoCredentialsError')
        
        with self.assertRaises(Exception) as context:
            # Assuming you provide the necessary arguments for upload_to_s3
            upload_to_s3(MagicMock(), 'bucket_name', 's3_key', 'access_key', 'secret_key', 'region')
        self.assertEqual(str(context.exception), 'NoCredentialsError')

    @patch('tkinter.messagebox.showerror')
    @patch('app.USER_CREDENTIALS', {'user': 'wrongpassword'})  # Mock credentials
    def test_login_failure_handling(self, mock_showerror):
        # Simulate login validation with incorrect credentials
        validate_login = MagicMock()
        validate_login()
        mock_showerror.assert_called_once_with("Login Failed", "Invalid username or password")

if __name__ == "__main__":
    unittest.main()

