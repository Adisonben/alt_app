from escpos.printer import Usb
from datetime import datetime
import os
from PIL import Image

def process_image(image_path, max_width=384):
    """
    Resizes and converts image to 1-bit black and white.
    Returns path to processed image or None if failed.
    """
    try:
        if not os.path.exists(image_path):
            return None
            
        img = Image.open(image_path)
        
        # 1. Resize if wider than max_width (standard 58mm printer ~384px)
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
        # 2. Convert to 1-bit monochrome (dithered)
        # method=Image.Dither.FLOYDSTEINBERG is default for convert('1')
        img = img.convert("1")
        
        # Save to a temporary file
        # In a real app, might want to cache this
        base, ext = os.path.splitext(image_path)
        new_path = f"{base}_bw{ext}"
        img.save(new_path)
        return new_path
        
    except Exception as e:
        print(f"Image processing error: {e}")
        return None

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
        bw_logo_path = process_image(logo_path)
        
        if bw_logo_path and os.path.exists(bw_logo_path):
            p.set(align='center')
            # Use 'graphics' implementation for better compatibility with bit images
            # or try standard image()
            try:
                p.image(bw_logo_path)
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
