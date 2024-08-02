import os
import mss
import mss.tools
import time
from datetime import datetime
from threading import Timer

# Specify the folder where screenshots will be saved
SCREENSHOT_FOLDER = "../flux_screenshots"


def clear_directory(directory):
    """Remove all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted existing file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def delete_file(filepath):
    try:
        os.remove(filepath)
        print(f"Deleted screenshot: {filepath}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")

def capture_and_schedule_deletion():
    # Clear existing files in the screenshot folder
    if not os.path.exists(SCREENSHOT_FOLDER):
        os.makedirs(SCREENSHOT_FOLDER)
    clear_directory(SCREENSHOT_FOLDER)

    with mss.mss() as sct:
        while True:
            # Capture the full screen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(SCREENSHOT_FOLDER, filename)
            screenshot = sct.grab(sct.monitors[0])
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=filepath)
            print(f"Screenshot saved at {filename}")

            # Schedule file deletion after 5 minutes
            t = Timer(30, delete_file, args=(filepath,))
            t.start()

            # Adjust this sleep time to control how often you capture the screen
            time.sleep(3)

if __name__ == "__main__":
    capture_and_schedule_deletion()