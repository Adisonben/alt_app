import os
import subprocess
import threading
import base64
from kivy.clock import Clock

# Path to the finger_scan binary
# Based on the project structure, it should be in the 'bin' folder
BIN_PATH = os.path.join(os.getcwd(), "bin", "finger_scan2")
SCAN_CMD = ["sudo", BIN_PATH, "10000"] # 10 seconds timeout
# Path to the match_template binary
MATCH_BIN_PATH = os.path.join(os.getcwd(), "bin", "match_template")
MATCH_CMD_BASE = ["sudo", MATCH_BIN_PATH]

SCAN_PROCESS_TIMEOUT = 15  # seconds before killing the scan subprocess

def raw_to_base64(raw_bytes):
    """Convert raw bytes to base64 string"""
    if raw_bytes is None:
        return ""
    return base64.b64encode(raw_bytes).decode('utf-8')

def base64_to_raw(base64_str):
    """Convert base64 string to raw bytes"""
    if not base64_str:
        return b""
    try:
        return base64.b64decode(base64_str)
    except Exception as e:
        print(f"[Fingerprint] Base64 decode error: {e}")
        return b""

def check_fingerprint_device():
    """
    Quick check: returns True if the fingerprint binary exists.
    Does NOT open the device — just verifies the binary is present.
    """
    exists = os.path.exists(BIN_PATH)
    if not exists:
        print(f"[Fingerprint] Device check FAILED: binary not found at {BIN_PATH}")
    else:
        print(f"[Fingerprint] Device check OK: binary found at {BIN_PATH}")
    return exists


def scan_fingerprint(callback):
    """
    Real fingerprint scan function
    - Runs in a background thread
    - Calls 'finger_scan' binary
    - Returns (success, base64_data) via callback
    """
    def _scan_thread():
        print(f"[Fingerprint] Starting scan command: {' '.join(SCAN_CMD)}")
        proc = None
        try:
            if not os.path.exists(BIN_PATH):
                print(f"[Fingerprint] ERROR: Binary not found at {BIN_PATH}")
                Clock.schedule_once(lambda dt: callback(False, None), 0)
                return

            proc = subprocess.Popen(
                SCAN_CMD,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            try:
                stdout, stderr = proc.communicate(timeout=SCAN_PROCESS_TIMEOUT)
            except subprocess.TimeoutExpired:
                print(f"[Fingerprint] Process timeout after {SCAN_PROCESS_TIMEOUT}s — killing")
                proc.kill()
                proc.communicate()
                Clock.schedule_once(lambda dt: callback(False, None), 0)
                return

            if stderr:
                print(f"[Fingerprint] STDERR: {stderr.decode(errors='ignore').strip()}")

            success = False
            b64_data = None

            if len(stdout) == 400:
                print("[Fingerprint] STATUS: SUCCESS")
                success = True
                b64_data = raw_to_base64(stdout)
            elif len(stdout) == 8:
                print("[Fingerprint] STATUS: TIMEOUT")
            elif len(stdout) == 5:
                print("[Fingerprint] STATUS: ERROR")
            else:
                print(f"[Fingerprint] STATUS: UNKNOWN (Size: {len(stdout)})")
            
            Clock.schedule_once(lambda dt: callback(success, b64_data), 0)

        except Exception as e:
            print(f"[Fingerprint] Thread Error: {e}")
            if proc:
                try:
                    proc.kill()
                except Exception:
                    pass
            Clock.schedule_once(lambda dt: callback(False, None), 0)

    threading.Thread(target=_scan_thread, daemon=True).start()


def compare_fingerprints(b64_data1, b64_data2, callback):
    """
    Compare two fingerprint templates (Base64 strings).
    - runs in a background thread
    - decodes base64 to raw bytes
    - writes data to temp files
    - calls 'match_template' binary
    - callback(result: bool, message: str)
    """
    def _compare_thread():
        import tempfile
        
        try:
            # Decode base64 to raw bytes
            data1 = base64_to_raw(b64_data1)
            data2 = base64_to_raw(b64_data2)

            if len(data1) != 400 or len(data2) != 400:
                 Clock.schedule_once(lambda dt: callback(False, "Invalid template size"), 0)
                 return
            
            # Create temp files
            t1 = tempfile.NamedTemporaryFile(delete=False)
            t2 = tempfile.NamedTemporaryFile(delete=False)
            
            t1.write(data1)
            t2.write(data2)
            
            t1.flush()
            t2.flush()
            
            t1.close()
            t2.close()
            
            fpath1 = t1.name
            fpath2 = t2.name
            
            cmd = MATCH_CMD_BASE + [fpath1, fpath2]
            print(f"[Fingerprint] Starting match command: {' '.join(cmd)}")
            
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = proc.communicate(timeout=5)
            
            if stderr:
                 print(f"[Fingerprint] Match STDERR: {stderr.decode(errors='ignore').strip()}")
                 
            result_str = stdout.decode().strip()
            print(f"[Fingerprint] Match Result Output: {result_str}")
            
            match_success = False
            msg = f"Unknown result: {result_str}"
            
            if result_str == "1":
                match_success = True
                msg = "Match"
            elif result_str == "0":
                match_success = False
                msg = "No Match"
            else:
                match_success = False
                msg = f"Error: {result_str}"

            Clock.schedule_once(lambda dt: callback(match_success, msg), 0)

        except Exception as e:
            print(f"[Fingerprint] Comparison Error: {e}")
            Clock.schedule_once(lambda dt: callback(False, str(e)), 0)
            
        finally:
            # Cleanup temp files
            try:
                if 'fpath1' in locals() and os.path.exists(fpath1):
                    os.remove(fpath1)
                if 'fpath2' in locals() and os.path.exists(fpath2):
                    os.remove(fpath2)
            except Exception as e:
                print(f"[Fingerprint] Cleanup Error: {e}")

    threading.Thread(target=_compare_thread, daemon=True).start()
