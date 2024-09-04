# Group- 5


# User Activity Monitor Application

## Overview
User behavior Monitor is a desktop software that monitors user behavior such as key presses, mouse clicks, and current window usage. It takes screenshots at regular intervals and supports Multi-Factor Authentication (MFA) for secure access. The application is written in Python and makes use of many libraries for cross-platform compatibility, GUI management, and email capabilities.

## Application Report File
- **Report File:** https://docs.google.com/document/d/1Q8tHfXOVBB-TluB7rfQ3AG5mPcixWENCvtS-m60tFQ4/edit?usp=sharing

## Application Zip File
- **Zip File:** https://drive.google.com/file/d/16XAe4R9V0_ht8aBtKBSv3m--4HA61AIc/view?usp=sharing

## Features
- **Cross-Platform Support:** Works with Windows, macOS, and Linux.
- **Activity tracking:** records key presses, mouse clicks, and current window usage.
- **Screenshot Capture:** Takes screenshots of the current window.
- **Email OTP Verification:** Sends a One-Time Password (OTP) via email to ensure secure login.
- **Battery Monitoring:** Stops monitoring if the battery is critically low.
- **GUI Interface:** A user-friendly interface for login and activity tracking.


## Cross-Platform Support
The application supports the following platforms:
- **Windows**
- **macOS**
- **Linux**

## Requirements
Python 3.x
- tkinter (for GUI)
- Pillow (for image processing)
- boto3 (for AWS S3 integration)
- pynput (for input monitoring)
- psutil (for battery status)
- smtplib (for sending emails)
- urllib (for internet connectivity checks)
- Platform-specific libraries (e.g., win32gui, AppKit, xdotool)

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/user-activity-monitor.git
    cd user-activity-monitor
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

   *Note: You may need to create a `requirements.txt` file with the following contents if it does not exist:*

    ```txt
    Pillow
    boto3
    pynput
    psutil
    ```

3. **Set up email credentials:**

    Replace the `sender_email` and `sender_password` in the `send_otp` function with your own email credentials.

4. **Configure AWS S3 integration:**

    Uncomment and configure the AWS S3 integration in the `log_activity` function by providing the appropriate `BUCKET_NAME`, `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, and `S3_REGION`.
   ## Usage

1. **Run the application:**

    ```sh
    python app.py
    ```

2. **Login:**

   - Enter the username and password.
   - If valid, an OTP will be sent to the email associated with the username.
   - Enter the OTP to access the main window.

3. **Activity Monitoring:**

   - The application will track and log user activity.
   - Screenshots will be captured and displayed in the GUI.

4. **Logout:**

   - Click the "Logout" button to return to the login screen.

## Configuration

- **Email OTP Settings:**
  - Modify `smtp_server`, `smtp_port`, `sender_email`, and `sender_password` to configure email settings.

- **Battery Monitoring:**
  - Adjust the battery threshold in the `check_battery` function as needed.

- **Screenshot Size:**
  - Modify the `resize` parameters in the `display_screenshot` function to adjust screenshot size.

## Troubleshooting

- **Internet Connectivity Issues:**
  - Ensure you have an active internet connection. The OTP feature requires internet access to send emails.

- **Cross-Platform Issues:**
  - Ensure the correct platform-specific libraries are installed for Windows, macOS, or Linux.

## Testing

### Unit Tests

The application includes a set of unit tests to verify the correctness of key functionalities, such as error handling, listener start-ups, and the integration of external services like AWS S3 and email OTP.

### Running Tests

To run the unit tests, follow these steps:

1. **Navigate to the project directory:**

    ```sh
    cd user-activity-monitor
    ```

2. **Execute the tests using `unittest`:**

    ```sh
    python -m unittest discover -s tests
    ```

    This command will automatically discover and run all test cases defined in the `tests` directory.

### Test Coverage

The tests cover the following functionalities:

1. **Internet Connectivity Check**
   - Verify the function returns the correct status based on internet connectivity availability and handles exceptions.

2. **OTP Generation and Validation**
   - Ensure that OTP is generated, stored, sent to the correct email, and validated correctly, including handling incorrect entries.

3. **Battery Check**
   - Verify that the system correctly identifies low battery levels, both when the battery is below and above 20%, and handles cases without battery sensors.

4. **Active Window Retrieval**
   - Ensure the function correctly identifies the active window across Windows, macOS, and Linux, and handles cases where no active window is detected.

5. **Screenshot Capture**
   - Verify that the system captures screenshots correctly across different platforms and handles capture failures.

6. **User Activity Logging**
   - Ensure that key presses and mouse clicks are logged, the active window’s usage time is updated, and the log behaves correctly when the battery is low.

7. **GUI Functionality**
   - Verify that the login screen, OTP input, and main window display correctly and that the logout button functions properly.

8. **Keyboard and Mouse Event Listening**
   - Ensure that keyboard and mouse event listeners start upon login and continue functioning while the application runs.

9. **Error Handling**
   - Verify that the application handles failures gracefully, including screenshot failures, AWS S3 upload issues, and login errors.





