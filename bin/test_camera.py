import time
import os
from datetime import datetime

try:
    from picamera2 import Picamera2
except ImportError:
    print("Error: picamera2 not found. This script is intended for Raspberry Pi OS (Bullseye/Bookworm).")
    print("Install it using: sudo apt install python3-picamera2")
    exit(1)

def test_camera():
    print("--- Raspberry Pi 5 Camera Test ---")
    
    # Initialize Picamera2
    try:
        picam2 = Picamera2()
    except Exception as e:
        print(f"Failed to initialize camera: {e}")
        return

    # Configure the camera
    # Use default preview configuration
    config = picam2.create_preview_configuration()
    picam2.configure(config)
    
    # Start the preview
    print("Starting preview... (3 seconds)")
    picam2.start_preview()
    
    # Wait for 3 seconds to let the camera adjust and user to see
    time.sleep(3)
    
    # Take a snapshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"snapshot_{timestamp}.jpg"
    
    print(f"Taking snapshot: {filename}")
    try:
        picam2.capture_file(filename)
        print(f"Successfully saved {filename} in current directory.")
    except Exception as e:
        print(f"Failed to capture image: {e}")
    
    # Stop preview and close
    print("Stopping preview and exiting.")
    picam2.stop_preview()
    picam2.close()

if __name__ == "__main__":
    test_camera()
