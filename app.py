import time
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
import boto3
from botocore.exceptions import NoCredentialsError
from pynput import keyboard, mouse
from threading import Thread
from datetime import datetime
import psutil
import random
import smtplib
from email.mime.text import MIMEText
import urllib.request  # Added for checking internet connectivity

# Global flags
tree_initialized = False

# Platform-specific imports
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
AWS_ACCESS_KEY = 'AKIA2RSH2FF23GML6TMA'
AWS_SECRET_KEY = 'GPL+6ucD3qpRWJPKAyYjFD1nw0OrwYYoTtgKlUnL'
BUCKET_NAME = 'myvinoveproject'
S3_REGION = 'us-east-1'
UPLOAD_PATH = 'screenshots/'

# Sample user credentials (for demonstration purposes)
USER_CREDENTIALS = {
    'admin': 'password123',
}

# OTP storage
otp_code = None

# Define global variables for GUI components
screenshot_label = None
tree = None

# Function to check internet connectivity
def checkInternetUrllib(url='http://google.com', timeout=3):
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except Exception as e:
        print(e)
        return False

# Function to send OTP via email
def send_otp(to_email, otp):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "abhiibaghel1011@gmail.com"
    sender_password = "qeqz hxlx juxy tzqk"

    msg = MIMEText(f"Your OTP is: {otp}")
    msg['Subject'] = "Your OTP Code"
    msg['From'] = sender_email
    msg['To'] = to_email

    if not checkInternetUrllib():  # Check if internet is available
        print("No internet connection. Unable to send OTP.")
        messagebox.showwarning("No internet connection. Unable to send OTP.")
        return

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print("OTP sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

def generate_and_send_otp(username):
    global otp_code
    otp_code = str(random.randint(100000, 999999))
    user_email = f"{username}@example.com"  # Example: generate email based on username
    send_otp(user_email, otp_code)

def validate_otp(user_input_otp):
    global otp_code
    return user_input_otp == otp_code

def check_battery():
    battery = psutil.sensors_battery()
    if battery is not None and not battery.power_plugged and battery.percent < 20:
        print("Low battery detected. Suspending activity tracking...")
        messagebox.showwarning("Battery Low", "Battery level is below 20%. Activity tracking is suspended.")
        return True
    return False


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
        if check_battery():
            time.sleep(60)  # Wait for a minute before checking again
            continue

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


        # Schedule GUI updates in the main thread
        root.after(0, display_screenshot, screenshot)

        # Update GUI tree
        root.after(0, update_gui)

        time.sleep(5)  # Adjust the sleep time as needed

def display_screenshot(img):
    global screenshot_label
    img = ImageTk.PhotoImage(img.resize((400, 250)))  # Resize the image
    screenshot_label.config(image=img)
    screenshot_label.image = img  # Keep a reference to the image to prevent garbage collection

def update_gui():
    global tree
    for widget in tree.get_children():
        tree.delete(widget)
        
    for app, info in activity_log.items():
        tree.insert("", "end", values=(app, info['start_time'].strftime("%Y-%m-%d %H:%M:%S"), 
                                       f"{info['usage_time']:.2f}", info['key_presses'], info['mouse_clicks']))

def display_screenshot(img):
    global screenshot_label
    img = ImageTk.PhotoImage(img.resize((400, 250)))  # Slightly larger size
    screenshot_label.config(image=img)
    screenshot_label.image = img

def on_press(key):
    global key_presses
    key_presses += 1

def on_click(x, y, button, pressed):
    global mouse_clicks
    if pressed:
        mouse_clicks += 1

def show_login_window(root):
    # Destroy any existing windows (in case of logout)
    for widget in root.winfo_children():
        widget.destroy()

    # Title Frame
    title_frame = tk.Frame(root, bg="#000080")
    title_frame.pack(fill="x")
    tk.Label(title_frame, text="Vinove", font=("Arial", 16, "bold"), bg="#000080", fg="white", pady=10).pack()

    # Login frame with modern style and border
    login_frame = tk.Frame(root, padx=20, pady=20, bg="#f7f7f7", 
                           highlightbackground="#080808", highlightcolor="#080808", highlightthickness=2)
    login_frame.pack(pady=50)

    tk.Label(login_frame, text="Username", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(login_frame, text="Password", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, padx=10, pady=10)

    username_entry = tk.Entry(login_frame, font=("Arial", 12))
    password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12))

    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def validate_login():
        username = username_entry.get()
        password = password_entry.get()
        if USER_CREDENTIALS.get(username) == password:
            generate_and_send_otp(username)  # Generate and send OTP
            show_otp_window(root, username)  # Show OTP window
            print("Genuine Person Detected...")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            print("User Invalid...")

    login_button = tk.Button(login_frame, text="Login", command=validate_login, bg="#000066", fg="white", font=("Arial", 12))
    login_button.grid(row=2, columnspan=2, pady=20)

def show_otp_window(root, username):
    # Destroy login widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Title Frame
    title_frame = tk.Frame(root, bg="#000080")
    title_frame.pack(fill="x")
    tk.Label(title_frame, text="Vinove", font=("Arial", 16, "bold"), bg="#000080", fg="white", pady=10).pack()

    # OTP frame
    otp_frame = tk.Frame(root, padx=20, pady=20, bg="#f7f7f7", 
                         highlightbackground="#080808", highlightcolor="#080808", highlightthickness=2)
    otp_frame.pack(pady=50)

    tk.Label(otp_frame, text="Enter OTP", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, padx=10, pady=10)
    
    otp_entry = tk.Entry(otp_frame, font=("Arial", 12))
    otp_entry.grid(row=0, column=1, padx=10, pady=10)

    def validate_otp_code():
        user_otp = otp_entry.get()
        if validate_otp(user_otp):
            show_main_window(root)  # Proceed to the main window
            print("OTP Validated...")
        else:
            messagebox.showerror("OTP Failed", "Invalid OTP")
            print("OTP Invalid...")

    otp_button = tk.Button(otp_frame, text="Validate OTP", command=validate_otp_code, bg="#000066", fg="white", font=("Arial", 12))
    otp_button.grid(row=1, columnspan=2, pady=20)

def show_main_window(root):
    # Destroy login widgets
    for widget in root.winfo_children():
        widget.destroy()

    global tree, screenshot_label

    # Title Frame
    title_frame = tk.Frame(root, bg="#000080")
    title_frame.pack(fill="x")
    tk.Label(title_frame, text="Vinove", font=("Arial", 16, "bold"), bg="#000080", fg="white", pady=10).pack()

    # Create main frame
    main_frame = tk.Frame(root, padx=10, pady=10, bg="#ffffff")
    main_frame.pack(fill="both", expand=True)

    # Define columns
    columns = ("Application", "Start Time", "Usage Time (s)", "Key Presses", "Mouse Clicks")
    
    # Create treeview with style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12))
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    tree.heading("Application", text="Application")
    tree.heading("Start Time", text="Start Time")
    tree.heading("Usage Time (s)", text="Usage Time (s)")
    tree.heading("Key Presses", text="Key Presses")
    tree.heading("Mouse Clicks", text="Mouse Clicks")
    
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Create label for screenshot with border
    screenshot_frame = tk.Frame(main_frame, bg="#dddddd", padx=5, pady=5)
    screenshot_frame.pack(pady=10)

    screenshot_label = tk.Label(screenshot_frame, bg="#ffffff")
    screenshot_label.pack()

    logout_button = tk.Button(main_frame, text="Logout", command=lambda: show_login_window(root), bg="#f44336", fg="white", font=("Arial", 12))
    logout_button.pack(pady=10)

def create_gui():
    # Initialize main window
    root = tk.Tk()
    root.title("User Activity Monitor")
    root.geometry("1100x700")
    root.configure(bg="#f0f0f0")  # Light gray background

    show_login_window(root)  # Start with the login window

    return root

if __name__ == "__main__":
    # Create and start the GUI
    root = create_gui()

    # Start logging thread after successful login
    logging_thread = Thread(target=log_activity,daemon=True)
    logging_thread.start()

    # Start listening for keyboard and mouse
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener.start()
    mouse_listener.start()

    # Run the GUI main loop
    root.mainloop()
