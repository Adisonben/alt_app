import subprocess
import base64
import binascii

CMD = ["sudo", "./finger_scan", "5000"]

try:
    proc = subprocess.Popen(
        CMD,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = proc.communicate(timeout=10)

    print("=== Finger Scan Result ===")
    print("Exit code :", proc.returncode)
    print("Byte size :", len(stdout))

    if stderr:
        print("STDERR:", stderr.decode(errors="ignore"))

    # ---- Interpret result by size ----
    if len(stdout) == 400:
        print("STATUS: SUCCESS (fingerprint template)")
    elif len(stdout) == 8:
        print("STATUS: TIMEOUT")
    elif len(stdout) == 5:
        print("STATUS: ERROR")
    else:
        print("STATUS: UNKNOWN")

    # ---- Hex preview (first 64 bytes) ----
    print("\nHex preview (first 64 bytes):")
    print(binascii.hexlify(stdout[:64]).decode())

    # ---- Base64 (for API / storage) ----
    b64 = base64.b64encode(stdout).decode()
    print("\nBase64 length:", len(b64))
    print("Base64 preview:", b64[:80] + "...")

except subprocess.TimeoutExpired:
    print("ERROR: Finger scan timed out")
except Exception as e:
    print("ERROR:", e)
