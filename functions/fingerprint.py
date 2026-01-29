import os
import subprocess
import threading
from kivy.clock import Clock

# Path to the finger_scan binary
# Based on the project structure, it should be in the 'bin' folder
BIN_PATH = os.path.join(os.getcwd(), "bin", "finger_scan")
SCAN_CMD = ["sudo", BIN_PATH, "10000"] # 10 seconds timeout

def scan_fingerprint(callback):
    """
    Real fingerprint scan function
    - Runs in a background thread to avoid blocking the Kivy UI
    - Calls the 'finger_scan' binary
    - Returns (success, raw_data) via callback
    """
    def _scan_thread():
        print(f"[Fingerprint] Starting scan command: {' '.join(SCAN_CMD)}")
        try:
            # Check if binary exists
            if not os.path.exists(BIN_PATH):
                print(f"[Fingerprint] ERROR: Binary not found at {BIN_PATH}")
                Clock.schedule_once(lambda dt: callback(False, None), 0)
                return

            proc = subprocess.Popen(
                SCAN_CMD,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Wait for the process to complete (timeout handled by the binary itself)
            stdout, stderr = proc.communicate()

            if stderr:
                print(f"[Fingerprint] STDERR: {stderr.decode(errors='ignore').strip()}")

            success = False
            raw_data = None

            # Interpret result by output size (as seen in test_finger_scan.py)
            if len(stdout) == 400:
                print("[Fingerprint] STATUS: SUCCESS")
                success = True
                raw_data = stdout
            elif len(stdout) == 8:
                print("[Fingerprint] STATUS: TIMEOUT")
            elif len(stdout) == 5:
                print("[Fingerprint] STATUS: ERROR")
            else:
                print(f"[Fingerprint] STATUS: UNKNOWN (Size: {len(stdout)})")
            
            # Use Clock.schedule_once to call the callback on the main Kivy thread
            Clock.schedule_once(lambda dt: callback(success, raw_data), 0)

        except Exception as e:
            print(f"[Fingerprint] Thread Error: {e}")
            Clock.schedule_once(lambda dt: callback(False, None), 0)

    # Start the scanning in a background thread
    threading.Thread(target=_scan_thread, daemon=True).start()
