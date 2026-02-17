from escpos.printer import Usb
from datetime import datetime
import os
from PIL import Image

def process_image(image_path, max_width=384):
    img = Image.open(image_path)

    # resize
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize(
            (max_width, int(img.height * ratio)),
            Image.Resampling.LANCZOS
        )

    # convert grayscale ก่อน
    img = img.convert("L")

    # threshold เอง (ไม่ใช้ dithering)
    img = img.point(lambda x: 0 if x < 128 else 255, '1')

    return img

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
        
        # Process image before printing
        bw_logo = process_image(logo_path)
        
        if bw_logo:
            p.set(align='center')
            # Use 'graphics' implementation for better compatibility with bit images
            # or try standard image()
            try:
                p.image(bw_logo, impl="graphics", fragment_height=256)
            except Exception as img_err:
                 print(f"Printing image failed, skipping: {img_err}")
                 p.text("[LOGO]\n")
        else:
            print("Logo not found or processing failed at:", logo_path)

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
