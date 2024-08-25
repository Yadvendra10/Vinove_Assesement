import time
import platform
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import boto3
from botocore.exceptions import NoCredentialsError
from pynput import keyboard, mouse
from threading import Thread
from datetime import datetime


# Import platform-specific modules
if platform.system() == 'Windows':
    import win32gui
    from PIL import ImageGrab
elif platform.system() == 'Darwin':
    import AppKit
    from Quartz import CGWindowListCreateImage, kCGWindowListOptionOnScreenOnly
    from CoreGraphics import CGRectMake
elif platform.system() == 'Linux':
    import subprocess
    from PIL import ImageGrab

# Dictionary to store usage data
activity_log = {}

# Variables to track user input
key_presses = 0
mouse_clicks = 0

# AWS S3 configuration
#AWS_ACCESS_KEY = 'AKIA2RSH2FF23GML6TMA'
#AWS_SECRET_KEY = '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'
#BUCKET_NAME = 'myvinoveproject'
#S3_REGION = 'us-east-1'
#UPLOAD_PATH = 'screenshots/'

def get_active_window():
    if platform.system() == 'Windows':
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    elif platform.system() == 'Darwin':
        return AppKit.NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    elif platform.system() == 'Linux':
        return subprocess.check_output(['xdotool', 'getwindowfocus', 'getwindowname']).decode('utf-8').strip()
    return "Unknown"

def take_screenshot():
    if platform.system() == 'Windows':
        bbox = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        img = ImageGrab.grab(bbox)
    elif platform.system() == 'Darwin':
        window_id = AppKit.NSWorkspace.sharedWorkspace().activeApplication()['NSWindowNumber']
        image = CGWindowListCreateImage(CGRectMake(0, 0, 0, 0), kCGWindowListOptionOnScreenOnly, window_id, 0)
        img = Image.frombytes('RGB', (image.width, image.height), image.data)
    elif platform.system() == 'Linux':
        bbox = subprocess.check_output(['xdotool', 'getwindowfocus', 'getwindowgeometry']).decode('utf-8').split()
        x, y, w, h = map(int, bbox[1:5])
        img = ImageGrab.grab((x, y, x+w, y+h))
    return img

def upload_to_s3(file_stream, bucket_name, s3_key, aws_access_key, aws_secret_key, region):
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
        s3 = session.client('s3')
        s3.upload_fileobj(file_stream, bucket_name, s3_key, ExtraArgs={'ContentType': 'image/png'})
        print(f"Uploaded to S3 at {s3_key}")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"Error occurred: {e}")

def log_activity():
    global key_presses, mouse_clicks
    while True:
        current_time = datetime.now()
        active_window = get_active_window()

        if active_window not in activity_log:
            activity_log[active_window] = {
                'start_time': current_time,
                'key_presses': 0,
                'mouse_clicks': 0,
                'usage_time': 0
            }

        # Update activity log
        activity = activity_log[active_window]
        activity['usage_time'] = (current_time - activity['start_time']).total_seconds()
        activity['key_presses'] += key_presses
        activity['mouse_clicks'] += mouse_clicks

        # Reset input counters
        key_presses = 0
        mouse_clicks = 0

        # Take and upload screenshot
        screenshot = take_screenshot()
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        buffered.seek(0)
        s3_key = f"{UPLOAD_PATH}screenshot_{current_time.strftime('%Y%m%d_%H%M%S')}.png"
        upload_to_s3(buffered, BUCKET_NAME, s3_key, AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_REGION)

        # Display screenshot     
        display_screenshot(screenshot)

        # Update GUI
        update_gui()

        time.sleep(5)  # Adjust the sleep time as needed

def update_gui():
    global tree
    for widget in tree.get_children():
        tree.delete(widget)
        
    for app, info in activity_log.items():
        tree.insert("", "end", values=(app, info['start_time'].strftime("%Y-%m-%d %H:%M:%S"), 
                                       f"{info['usage_time']:.2f}", info['key_presses'], info['mouse_clicks']))

def display_screenshot(img):
    global screenshot_label
    img = ImageTk.PhotoImage(img.resize((300, 200)))
    screenshot_label.config(image=img)
    screenshot_label.image = img

def on_press(key):
    global key_presses
    key_presses += 1

def on_click(x, y, button, pressed):
    global mouse_clicks
    if pressed:
        mouse_clicks += 1

def create_gui():
    global tree, screenshot_label

    # Initialize main window
    root = tk.Tk()
    root.title("User Activity Monitor")
    root.geometry("1000x600")
    
    # Define columns
    columns = ("Application", "Start Time", "Usage Time (s)", "Key Presses", "Mouse Clicks")
    
    # Create treeview
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("Application", text="Application")
    tree.heading("Start Time", text="Start Time")
    tree.heading("Usage Time (s)", text="Usage Time (s)")
    tree.heading("Key Presses", text="Key Presses")
    tree.heading("Mouse Clicks", text="Mouse Clicks")
    
    tree.pack(fill="both", expand=True)

    # Create label for screenshot
    screenshot_label = tk.Label(root)
    screenshot_label.pack()

    return root

if __name__ == "__main__":
    # Create and start the GUI
    root = create_gui()
    
    # Start logging thread
    logging_thread = Thread(target=log_activity)
    logging_thread.start()  # Avoid daemon=True to prevent shutdown issues

    # Start listening for keyboard and mouse events
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener.start()
    mouse_listener.start()

    # Run the GUI main loop
    root.mainloop()