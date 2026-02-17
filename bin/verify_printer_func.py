import sys
import os

# Add project root to path so we can import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.printer import print_receipt

def test():
    print("Testing print_receipt function...")
    try:
        success = print_receipt(
            user_id="U12345",
            user_name="Test User",
            value=0.00,
            status="PASS",
            device_id="TEST-DEVICE-01"
        )
        if success:
            print("Function returned True.")
        else:
            print("Function returned False.")
    except Exception as e:
        print(f"Test failed with exception: {e}")

if __name__ == "__main__":
    test()
