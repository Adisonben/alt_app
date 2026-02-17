from escpos.printer import Usb
from datetime import datetime

def print_result(user_name, status, value):
    """
    Directly prints receipt using python-escpos.
    Should be called ONLY when alcohol sensor is inactive.
    """
    try:
        # 1. Connect (Vendor ID 0x04b8, Product ID 0x0e28)
        p = Usb(0x04b8, 0x0e28)
        
        # 2. Print Content
        p.set(align='center', bold=True, width=3, height=3)
        p.text("ALCOHOL TEST RESULT\n")
        p.set(align='left', bold=False, width=2, height=2)

        p.text("--------------------------------\n")
        p.text(f"Name : {user_name}\n")
        p.text(f"Result : {status}\n")
        p.text(f"Value : {value} mg%\n")
        dt_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"Date : {dt_str}\n")
        p.text("--------------------------------\n")

        if status == "PASS":
            p.set(align='center', bold=True, width=2, height=2)
            p.text("\n*** PASS ***\n")
        else:
            p.set(align='center', bold=True, width=2, height=2)
            p.text("\n*** FAIL ***\n")

        p.text("\n\n")
        
        # 3. Cut & Close
        p.cut()
        p.close() # Explicitly close
        print("[printer] Print success.")
        return True
        
    except Exception as e:
        print(f"[printer] Error: {e}")
        return False