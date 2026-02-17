from escpos.printer import File
from PIL import Image
import os

try:
    # Note: /dev/usb/lp0 is a Linux device path. 
    # This will likely fail on Windows unless running in WSL with device passthrough.
    p = File("/dev/usb/lp0")
    
    # Locate basics/logo.png relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, '..', 'assets', 'logo.png')

    if not os.path.exists(logo_path):
        print(f"Error: Logo not found at {logo_path}")
    else:
        img = Image.open(logo_path).convert("1")
        p.image(img, impl="graphics")
        p.cut()
        print("Print command sent.")

except Exception as e:
    print(f"Error: {e}")
