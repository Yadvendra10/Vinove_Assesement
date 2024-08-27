# User Activity Monitor Application

## Purpose
The User Activity Monitor Application is designed to monitor and log user activity on desktop systems. It provides real-time tracking of user actions, including screenshots, key presses, and mouse clicks.

## Features
- **Captures screenshots** of the currently active window.
- **Tracks key presses and mouse clicks**.
- **Uploads screenshots** to an AWS S3 bucket.
- **Provides a GUI** for real-time activity monitoring.

## Cross-Platform Support
The application supports the following platforms:
- **Windows**
- **macOS**
- **Linux**

## Dependencies

### Python Libraries
- `time`: Time-related functions.
- `platform`: Platform detection.
- `tkinter`: GUI components.
- `Pillow (PIL)`: Image processing and screenshot functionality.
- `io`: In-memory file object handling.
- `boto3`: AWS SDK for Python.
- `botocore.exceptions`: AWS-related exceptions.
- `pynput`: Keyboard and mouse monitoring.
- `threading`: Thread management.
- `datetime`: Date and time functions.

### Platform-Specific Modules
- **Windows**: `win32gui`, `ImageGrab` from Pillow.
- **macOS**: `AppKit`, `Quartz`, `CoreGraphics`.
- **Linux**: `subprocess`, `ImageGrab` from Pillow.

## Installation

To install the necessary dependencies, run:

```sh
pip install Pillow boto3 pynput



