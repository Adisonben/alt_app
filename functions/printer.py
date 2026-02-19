from escpos.printer import Usb
from datetime import datetime
import os
from PIL import Image

def print_result(user_name, user_id, device_id, status, value):
    """
    Directly prints receipt using python-escpos.
    Should be called ONLY when alcohol sensor is inactive.
    """
    try:
        # 1. Connect (Vendor ID 0x04b8, Product ID 0x0e28)
        p = Usb(0x04b8, 0x0e28)

        # Locate basics/logo.png relative to this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, '..', 'assets', 'logo.png')
        
        # 2. Print Content
        p.set(align='center', bold=True, width=3, height=3)
        if not os.path.exists(logo_path):
            print(f"Error: Logo not found at {logo_path}")
        else:
            img = Image.open(logo_path).convert("1")
            p.image(img, impl="graphics")
            print("Print command sent.")
        
        p.text("\nALCOHOL TEST RESULT\n")
        p.set(align='left', bold=False, width=2, height=2)

        p.text("--------------------------------\n")
        p.text(f"เครื่องทดสอบ (Device ID) : {device_id}\n")
        p.text(f"รหัสผู้ทดสอบ (User ID)   : {user_id}\n")
        p.text(f"ชื่อผู้ทดสอบ (Name)      : {user_name}\n")
        p.text(f"ปริมาณแอลกอฮอล์ (Value) : {value} mg/100ml\n")
        p.text(f"สรุปผลการทดสอบ (Result) : {status}\n")
        dt_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"วันที่ (Date) : {dt_str}\n")
        p.text("--------------------------------\n")

        if status == "PASS":
            p.set(align='center', bold=True, width=2, height=2)
            p.text("*** PASS ***")
        elif status == "FAIL":
            p.set(align='center', bold=True, width=2, height=2)
            p.text("*** FAIL ***")
        else:
            p.set(align='center', bold=True, width=2, height=2)
            p.text("*** ERROR ***")
        
        # 3. Cut & Close
        p.cut()
        p.close() # Explicitly close
        print("[printer] Print success.")
        return True
        
    except Exception as e:
        print(f"[printer] Error: {e}")
        return False