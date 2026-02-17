from escpos.printer import Usb
from datetime import datetime
import os
from PIL import Image

def process_image(image_path, max_width=384):
    """
    Resizes and converts image to 1-bit black and white.
    """
    if not os.path.exists(image_path):
        return None
        
    img = Image.open(image_path)

    # resize
    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int(float(img.height) * ratio)
        img = img.resize(
            (max_width, new_height),
            Image.Resampling.LANCZOS
        )

    # convert to 1-bit monochrome (standard)
    img = img.convert("1")
    return img

import threading
import time

# Create a lock for the printer
printer_lock = threading.Lock()

def print_receipt(user_id, user_name, value, status, device_id="Kiosk-001"):
    # Attempt to acquire lock to ensure only one print job at a time
    if not printer_lock.acquire(blocking=False):
        print("Printer is busy. Skipping this print request.")
        return False

    p = None
    try:
        print("Acquired printer lock. Starting print job...")
        # Small delay to let UI or other USB ops settle
        time.sleep(0.5)
        
        # Vendor ID and Product ID from bin/test_printer.py
        p = Usb(0x04b8, 0x0e28)
        
        # 1. Logo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, '..', 'assets', 'logo.png')
        
        # Process image before printing
        bw_logo = process_image(logo_path)
        
        if bw_logo:
            p.set(align='center')
            try:
                # impl="graphics" worked in the minimal test
                p.image(bw_logo, impl="graphics")
            except Exception as img_err:
                 print(f"Printing image failed, skipping: {img_err}")
                 p.text("[LOGO]\n")
        else:
            print("Logo not found at:", logo_path)
            p.text("[LOGO Placeholder]\n")

        # 2. Header "ALT Iddrives"
        p.set(align='center', bold=True, width=2, height=2)
        p.text("ALT Iddrives\n")
        
        # Reset font for details
        p.set(align='left', bold=False, width=1, height=1)
        p.text("--------------------------------\n")

        # 3. Date and Time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.text(f"Date: {now}\n")

        # 4. User ID and User Name
        p.text(f"User ID: {user_id}\n")
        p.text(f"Name: {user_name}\n")

        # 5. Value & Status
        p.text(f"Value: {value} mg%\n")
        p.text(f"Status: {status}\n")

        # 6. Device ID
        p.text(f"Device ID: {device_id}\n")
        p.text("--------------------------------\n")
        
        # 7. Space top and bottom for cut
        p.text("\n\n\n")
        p.cut()
        
        print("Receipt printed successfully.")
        return True

    except Exception as e:
        print(f"Printing failed: {e}")
        return False
    finally:
        if p:
            try:
                p.close()
                print("Printer connection closed.")
            except Exception as close_err:
                print(f"Error closing printer: {close_err}")
        
        printer_lock.release()
        print("Released printer lock.")
