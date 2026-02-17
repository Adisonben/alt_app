"""
EBS-010 Breathalyzer Integration
=================================
Connects to the EBS-010 alcohol sensor via USB serial and runs
a full measurement cycle in a background thread.

Public API
----------
    measure_alcohol(on_status, on_result)
    stop_measurement()
"""

try:
    import serial
    import serial.tools.list_ports
except Exception:
    serial = None

import threading
import time
import re
from kivy.clock import Clock

# ── Protocol constants ────────────────────────────────────────
BAUDRATE = 4800
DATA_BITS = 8          # serial.EIGHTBITS
STOP_BITS = 1          # serial.STOPBITS_ONE
PARITY = "N"           # serial.PARITY_NONE
TIMEOUT = 2            # read timeout (seconds)
CR_LF = b"\x0D\x0A"
MEASUREMENT_TIMEOUT = 120  # seconds max for entire cycle

CMD_START = b"$START" + CR_LF
CMD_RESET = b"$RESET" + CR_LF

# ── Module-level state (thread control) ───────────────────────
_worker_thread = None
_stop_event = threading.Event()


# ── Port detection ────────────────────────────────────────────
def _auto_detect_port():
    """Return the device path of the first USB-serial port, or None."""
    if serial is None:
        return None
    ports = serial.tools.list_ports.comports()
    # Prefer ports whose name contains USB or ACM
    for p in ports:
        if "USB" in p.device.upper() or "ACM" in p.device.upper():
            print(f"[alcohol] Auto-detected port: {p.device} ({p.description})")
            return p.device
    # Fall back to first available port
    if ports:
        print(f"[alcohol] Using first port: {ports[0].device} ({ports[0].description})")
        return ports[0].device
    return None


# ── Response parsers ──────────────────────────────────────────
def _parse_state(line):
    """Return device state string or None."""
    if "$FLOW,ERR" in line:
        return "$FLOW,ERR"
    for s in ("$END", "$WAIT", "$STANBY", "$BREATH", "$TRIGGER", "$CALIBRATION"):
        if s in line:
            return s
    return None


def _parse_result(line):
    """Return dict {value: float, status: str} or None."""
    m = re.match(r"\$RESULT,(\d+\.\d+)-(OK|HIGH)", line)
    if m:
        return {"value": float(m.group(1)), "status": m.group(2)}
    return None


# ── Status messages ───────────────────────────────────────────
_STATUS_MSG = {
    "connecting":      "กำลังเชื่อมต่ออุปกรณ์... / Connecting...",
    "warming_up":      "กำลังอุ่นเครื่อง... / Warming up...",
    "ready":           "พร้อมเป่า! กรุณาเป่าลมหายใจ / Ready! Please blow",
    "breath_detected": "ตรวจพบลมหายใจ / Breath detected",
    "sampling":        "กำลังเก็บตัวอย่าง... / Sampling breath...",
    "analyzing":       "กำลังวิเคราะห์... / Analyzing...",
    "flow_error":      "เป่าไม่ถูกต้อง กรุณารอแล้วลองใหม่ / Incorrect breath, retrying...",
    "timeout":         "หมดเวลา กรุณาลองใหม่ / Timeout, please retry",
    "error":           "ไม่สามารถเชื่อมต่ออุปกรณ์ได้ / Device connection error",
}


def _fire_status(on_status, state):
    """Schedule on_status callback on Kivy main thread."""
    msg = _STATUS_MSG.get(state, state)
    Clock.schedule_once(lambda dt: on_status(state, msg), 0)


def _fire_result(on_result, success, value, status):
    """Schedule on_result callback on Kivy main thread."""
    Clock.schedule_once(lambda dt: on_result(success, value, status), 0)


# ── Background worker ────────────────────────────────────────
def _measurement_worker(on_status, on_result):
    """Run the full $START → listen → $RESULT cycle."""
    ser = None
    try:
        # 1. Detect port
        _fire_status(on_status, "connecting")
        port = _auto_detect_port()
        if port is None:
            print("[alcohol] No serial port found.")
            _fire_status(on_status, "error")
            _fire_result(on_result, False, -1.0, "NO_PORT")
            return

        # 2. Open serial
        if serial is None:
            print("[alcohol] pyserial not installed.")
            _fire_status(on_status, "error")
            _fire_result(on_result, False, -1.0, "NO_PYSERIAL")
            return

        ser = serial.Serial(
            port=port,
            baudrate=BAUDRATE,
            bytesize=DATA_BITS,
            stopbits=STOP_BITS,
            parity=PARITY,
            timeout=TIMEOUT,
        )
        print(f"[alcohol] Serial opened: {port} @ {BAUDRATE}")

        # 3. Send $START
        ser.write(CMD_START)
        ser.flush()
        print("[alcohol] Sent $START")
        _fire_status(on_status, "warming_up")

        # 4. Listen for state transitions
        deadline = time.time() + MEASUREMENT_TIMEOUT
        result_found = False

        while time.time() < deadline and not _stop_event.is_set():
            raw = ser.readline()
            if not raw:
                continue

            decoded = raw.decode("ascii", errors="replace").strip()
            if not decoded:
                continue

            print(f"[alcohol] RX: {decoded}")

            # -- Check for result first --
            result = _parse_result(decoded)
            if result:
                print(f"[alcohol] RESULT value={result['value']} status={result['status']}")
                result_found = True
                _fire_result(on_result, True, result["value"], result["status"])
                # Wait for the subsequent $END before closing
                continue

            # -- State machine --
            state = _parse_state(decoded)
            if state == "$WAIT":
                _fire_status(on_status, "warming_up")
            elif state == "$STANBY":
                _fire_status(on_status, "ready")
            elif state == "$TRIGGER":
                _fire_status(on_status, "breath_detected")
            elif state == "$BREATH":
                _fire_status(on_status, "sampling")
            elif state == "$FLOW,ERR":
                _fire_status(on_status, "flow_error")
            elif state == "$END":
                if result_found:
                    print("[alcohol] Measurement cycle complete.")
                    break
                # $END before result = device was idle, keep listening
            elif state == "$CALIBRATION":
                _fire_status(on_status, "analyzing")

        # Timeout check
        if not result_found and not _stop_event.is_set():
            print("[alcohol] Timeout — no result in time.")
            _fire_status(on_status, "timeout")
            _fire_result(on_result, False, -1.0, "TIMEOUT")

    except Exception as e:
        print(f"[alcohol] Error: {e}")
        _fire_status(on_status, "error")
        _fire_result(on_result, False, -1.0, "ERROR")

    finally:
        if ser and ser.is_open:
            try:
                ser.close()
                print("[alcohol] Serial port closed.")
            except Exception:
                pass


# ── Public API ────────────────────────────────────────────────
def measure_alcohol(on_status, on_result):
    """
    Start an EBS-010 measurement cycle in a background thread.

    Parameters
    ----------
    on_status : callable(state: str, message: str)
        Called on the Kivy main thread whenever the device state changes.
        States: connecting, warming_up, ready, breath_detected, sampling,
                flow_error, analyzing, timeout, error
    on_result : callable(success: bool, value: float, status: str)
        Called once when measurement completes.
        success=True  → value is the BAC reading, status is "OK" or "HIGH"
        success=False → value=-1.0, status in ("NO_PORT","NO_PYSERIAL","TIMEOUT","ERROR")
    """
    global _worker_thread
    _stop_event.clear()
    _worker_thread = threading.Thread(
        target=_measurement_worker,
        args=(on_status, on_result),
        daemon=True,
    )
    _worker_thread.start()


def stop_measurement():
    """Signal the background worker to stop (e.g. when leaving the screen)."""
    _stop_event.set()