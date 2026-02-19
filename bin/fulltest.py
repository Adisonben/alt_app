#!/usr/bin/env python3
"""
Full Hardware Test
==================
ทดสอบอุปกรณ์ทั้งหมดในระบบ:
  1. Fingerprint Scanner
  2. Printer (USB)
  3. Alcohol Sensor (EBS-010)
  4. Camera

Usage:
  python3 fulltest.py          # ทดสอบทุกอย่าง
  python3 fulltest.py 1        # ทดสอบเฉพาะ Fingerprint
  python3 fulltest.py 2        # ทดสอบเฉพาะ Printer
  python3 fulltest.py 3        # ทดสอบเฉพาะ Alcohol Sensor
  python3 fulltest.py 4        # ทดสอบเฉพาะ Camera
"""

import sys
import os
import subprocess
import time
import re

# ── Results tracking ──────────────────────────────────────────
results = {}


def header(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def result_ok(name, detail=""):
    results[name] = "PASS"
    msg = f"  [PASS] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)


def result_fail(name, detail=""):
    results[name] = "FAIL"
    msg = f"  [FAIL] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)


# ── 1. Fingerprint Scanner ───────────────────────────────────
def test_fingerprint():
    header("1. Fingerprint Scanner")
    SCAN_CMD = ["sudo", "./finger_scan2", "5000"]
    print("  กรุณาวางนิ้วบน scanner... (Please place finger on scanner...)")
    try:
        proc = subprocess.Popen(
            SCAN_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate(timeout=15)

        if len(stdout) == 400:
            result_ok("Fingerprint", f"Template captured ({len(stdout)} bytes)")
        elif len(stdout) == 8:
            result_fail("Fingerprint", "Timeout — no finger detected")
        elif len(stdout) == 5:
            result_fail("Fingerprint", "Sensor error")
        else:
            result_fail("Fingerprint", f"Unexpected response size: {len(stdout)}")

    except subprocess.TimeoutExpired:
        result_fail("Fingerprint", "Process timed out")
    except FileNotFoundError:
        result_fail("Fingerprint", "finger_scan2 not found")
    except Exception as e:
        result_fail("Fingerprint", str(e))


# ── 2. Printer ────────────────────────────────────────────────
def test_printer():
    header("2. Printer (USB)")
    try:
        from escpos.printer import Usb
        from datetime import datetime

        p = Usb(0x04B8, 0x0E28)
        p.set(align="center", bold=True, width=2, height=2)
        p.text("HARDWARE TEST\n")
        p.set(align="left", bold=False, width=1, height=1)
        p.text("--------------------------------\n")
        p.text(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        p.text("Status : Printer OK\n")
        p.text("--------------------------------\n\n")
        p.cut()
        result_ok("Printer", "Test page printed")

    except ImportError:
        result_fail("Printer", "python-escpos not installed")
    except Exception as e:
        result_fail("Printer", str(e))


# ── 3. Alcohol Sensor (EBS-010) ──────────────────────────────
def test_alcohol_sensor():
    header("3. Alcohol Sensor (EBS-010)")
    try:
        import serial
        import serial.tools.list_ports
    except ImportError:
        result_fail("Alcohol Sensor", "pyserial not installed")
        return

    # Auto-detect port
    ports = serial.tools.list_ports.comports()
    port = None
    for p in ports:
        if "USB" in p.device.upper() or "ACM" in p.device.upper():
            port = p.device
            break
    if not port and ports:
        port = ports[0].device
    if not port:
        result_fail("Alcohol Sensor", "No serial port found")
        return

    try:
        ser = serial.Serial(
            port=port,
            baudrate=4800,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=2,
        )
        print(f"  Serial opened: {port} @ 4800")

        # Send $START
        ser.write(b"$START\x0D\x0A")
        ser.flush()
        print("  Sent $START — กรุณาเป่า (please blow when ready)...")

        deadline = time.time() + 120
        result_found = False

        while time.time() < deadline:
            raw = ser.readline()
            if not raw:
                continue
            decoded = raw.decode("ascii", errors="replace").strip()
            if not decoded:
                continue

            print(f"  [RX] {decoded}")

            # Check result
            m = re.match(r"\$RESULT,(\d+\.\d+)-(OK|HIGH)", decoded)
            if m:
                value = float(m.group(1))
                status = m.group(2)
                result_ok("Alcohol Sensor", f"Value={value}, Status={status}")
                result_found = True
                continue

            if "$END" in decoded and result_found:
                break

        if not result_found:
            result_fail("Alcohol Sensor", "Timeout — no result within 2 minutes")

        ser.close()

    except Exception as e:
        result_fail("Alcohol Sensor", str(e))


# ── 4. Camera ────────────────────────────────────────────────
def test_camera():
    header("4. Camera")
    try:
        from picamera2 import Picamera2

        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            main={"size": (1920, 1080)},
            lores={"size": (640, 480)},
        )
        picam2.configure(config)
        picam2.start()
        time.sleep(2)

        test_path = "/tmp/fulltest_camera.jpg"
        picam2.capture_file(test_path)
        picam2.stop()
        picam2.close()

        if os.path.exists(test_path) and os.path.getsize(test_path) > 0:
            size_kb = os.path.getsize(test_path) / 1024
            result_ok("Camera", f"Captured {size_kb:.0f} KB -> {test_path}")
            os.remove(test_path)
        else:
            result_fail("Camera", "Capture file is empty or missing")

    except ImportError:
        result_fail("Camera", "picamera2 not installed")
    except Exception as e:
        result_fail("Camera", str(e))


# ── Summary ──────────────────────────────────────────────────
def print_summary():
    header("SUMMARY")
    total = len(results)
    passed = sum(1 for v in results.values() if v == "PASS")
    failed = total - passed

    for name, status in results.items():
        icon = "✓" if status == "PASS" else "✗"
        print(f"  {icon} {name}: {status}")

    print(f"\n  Total: {total}  |  Pass: {passed}  |  Fail: {failed}")

    if failed == 0:
        print("\n  *** ALL TESTS PASSED ***")
    else:
        print(f"\n  *** {failed} TEST(S) FAILED ***")


# ── Main ─────────────────────────────────────────────────────
ALL_TESTS = {
    "1": ("Fingerprint", test_fingerprint),
    "2": ("Printer", test_printer),
    "3": ("Alcohol Sensor", test_alcohol_sensor),
    "4": ("Camera", test_camera),
}


def main():
    print("=" * 60)
    print("  FULL HARDWARE TEST")
    print("=" * 60)

    # Determine which tests to run
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        if choice in ALL_TESTS:
            name, func = ALL_TESTS[choice]
            print(f"  Running: {name} only")
            func()
        else:
            print(f"  Unknown test: {choice}")
            print("  Usage: python3 fulltest.py [1|2|3|4]")
            sys.exit(1)
    else:
        print("  Running ALL tests...")
        for key in sorted(ALL_TESTS):
            _, func = ALL_TESTS[key]
            func()

    print_summary()


if __name__ == "__main__":
    main()
