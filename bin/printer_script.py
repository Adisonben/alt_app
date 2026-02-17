
import sys
from escpos.printer import Usb
from datetime import datetime

def print_result(user_name, status, value):
    try:
        # Vendor ID 0x04b8, Product ID 0x0e28
        p = Usb(0x04b8, 0x0e28)

        p.set(align='center', bold=True, width=2, height=2)
        p.text("ALCOHOL TEST RESULT\n")
        p.set(align='left', bold=False, width=1, height=1)

        p.text("--------------------------------\n")
        p.text(f"Name : {user_name}\n")
        p.text(f"Result : {status}\n")
        p.text(f"Value : {value} mg%\n")
        dt_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        p.text(f"Date : {dt_str}\n")
        p.text("--------------------------------\n")

        if status == "PASS":
            p.set(align='center', bold=True)
            p.text("\n*** PASS ***\n")
        else:
            p.set(align='center', bold=True)
            p.text("\n*** FAIL ***\n")

        p.text("\n\n")
        p.cut()
        p.close() # Explicitly close
        print("SUCCESS")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python printer_script.py <user_name> <status> <value>")
        sys.exit(1)
    
    user_name = sys.argv[1]
    status = sys.argv[2]
    value = sys.argv[3]
    
    print_result(user_name, status, value)
