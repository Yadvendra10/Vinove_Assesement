# Group- 5


# User Activity Monitor Application

## Overview
User behavior Monitor is a desktop software that monitors user behavior such as key presses, mouse clicks, and current window usage. It takes screenshots at regular intervals and supports Multi-Factor Authentication (MFA) for secure access. The application is written in Python and makes use of many libraries for cross-platform compatibility, GUI management, and email capabilities.

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




