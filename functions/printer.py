import os
import sys
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw, ImageOps
from escpos.printer import Usb

def get_font_path():
    # Check common locations
    candidates = [
        "fonts/THSarabunNew.ttf",
        "resources/fonts/Loma.ttf",
        "Loma.ttf",
        "THSarabunNew.ttf"
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    
    # Try looking in project root if we are in functions subdirectory
    # (Assuming script runs from root, but just in case)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for path in candidates:
        full_path = os.path.join(base_dir, path)
        if os.path.exists(full_path):
            return full_path
            
    return None

def img_font(text, font_size=28, line_height=5):
    font_path = get_font_path()
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Calculate text size
    # Handle getsize vs getbbox (newer Pillow)
    if hasattr(font, 'getbbox'):
        bbox = font.getbbox(text)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        # Adjust for baseline
        height += 4 
    else:
        width, height = font.getsize(text)

    # Create image (Black background, White text -> Invert) to match pure_printer style
    # Or just White background, Black text.
    # pure_printer: Image.new('RGB', ..., (0,0,0) implicitly) -> draw white -> invert -> black on white.
    # simpler: White background, Black text.
    
    image = Image.new('RGB', (width, height + line_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=(0, 0, 0))
    
    return image

def print_receipt(user_id, user_name, value, status, device_id):
    """
    Prints the test result receipt.
    
    Args:
        user_id (str): The ID of the user.
        user_name (str): The name of the user.
        value (float/str): The alcohol test value.
        status (str): The result status (e.g., PASS, FAIL).
        device_id (str): The ID of the device.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Vendor ID 0x04b8, Product ID 0x0e28 per user instructions
        p = Usb(0x04b8, 0x0e28)
        
        # Center alignment
        p.set(align='center')
        
        # Header "ALT Iddrives"
        # Using image for consistency across potential language inputs
        p.image(img_font("ALT Iddrives", font_size=34))
        p.text("\n")
        
        # Reset to left align for details? Or keep center?
        # User requirement format:
        # - "ALT Iddrives" (Header)
        # - date and time
        # - user id
        # - user name
        # - value & status
        # - device id
        
        # Let's align left for details
        p.set(align='left')
        
        dt_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.image(img_font(f"Date: {dt_str}"))
        
        p.image(img_font(f"User ID: {user_id}"))
        p.image(img_font(f"Name: {user_name}"))
        
        # Value & Status
        p.image(img_font(f"Value: {value} mg%"))
        p.image(img_font(f"Result: {status}"))
        
        p.image(img_font(f"Device ID: {device_id}"))
        
        # Space bottom for cut
        p.text("\n\n\n")
        p.cut()
        
        # Close connection implicitly handled or explicitly if needed?
        # escpos Usb usually handles it.
        
        return True
        
    except Exception as e:
        print(f"Print Error: {e}")
        # In production, we might want to log this but not crash
        return False
