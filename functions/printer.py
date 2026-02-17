from escpos.printer import Usb
from datetime import datetime
import os
from PIL import Image

def print_receipt(user_id, user_name, value, status, device_id="Kiosk-001"):
    try:
        # Vendor ID and Product ID from bin/test_printer.py
        p = Usb(0x04b8, 0x0e28)
    except Exception as e:
        print(f"Printer error: {e}")
        return False

    try:
        # 1. Logo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, '..', 'assets', 'logo.png')
        
        if not os.path.exists(logo_path):
            print(f"Error: Logo not found at {logo_path}")
        else:
            img = Image.open(logo_path).convert("1")
            p.image(img, impl="graphics")

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
