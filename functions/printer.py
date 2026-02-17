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
        
    try:
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
    except Exception as e:
        print(f"Image processing error: {e}")
        return None

def print_receipt(user_id, user_name, value, status, device_id="Kiosk-001"):
    p = None
    try:
        # Vendor ID and Product ID
        # 0x04b8 (Epson), 0x0e28 (TM-T20II or similar)
        p = Usb(0x04b8, 0x0e28)
        
        # 1. Logo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, '..', 'assets', 'logo.png')
        
        bw_logo = process_image(logo_path)
        
        if bw_logo:
            p.set(align='center')
            try:
                # impl="graphics" provides better compatibility/quality for images
                p.image(bw_logo, impl="graphics")
            except Exception as img_err:
                 print(f"Printing image failed: {img_err}")
                 p.text("[LOGO]\n")
        else:
            print("Logo not found or invalid at:", logo_path)

        # 2. Header "ALT Iddrives"
        p.set(align='center', bold=True, width=2, height=2)
        p.text("ALT Iddrives\n")
        
        # Reset font settings
        p.set(align='left', bold=False, width=1, height=1)
        p.text("--------------------------------\n")

        # 3. Date and Time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p.text(f"Date: {now}\n")

        # 4. User ID and User Name
        # Handle cases where data might be None
        u_id = user_id if user_id else "-"
        u_name = user_name if user_name else "-"
        
        p.text(f"User ID: {u_id}\n")
        p.text(f"Name: {u_name}\n")

        # 5. Value & Status
        val = value if value is not None else 0.0
        stat = status if status else "-"
        
        p.text(f"Value: {val} mg%\n")
        p.text(f"Status: {stat}\n")

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
        # CRITICAL: Always close the connection to release the USB resource.
        # If not closed, subsequent attempts (or other apps) will get "Input/Output Error"
        # or "Resource Busy".
        if p:
            try:
                p.close()
                print("Printer connection closed.")
            except Exception as close_err:
                print(f"Error closing printer: {close_err}")
