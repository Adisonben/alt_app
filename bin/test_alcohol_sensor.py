#!/usr/bin/env python3
"""
EBS-010 Breathalyzer Sensor Test Script
========================================
ทดสอบการเชื่อมต่อและสื่อสารกับเซ็นเซอร์วัดแอลกอฮอล์ EBS-010 ผ่าน USB Serial

Protocol:
  - Baudrate: 4800, Data: 8, Stop: 1, Parity: None
  - Commands end with 0x0D 0x0A (CR+LF)
  - Commands must be UPPERCASE

Usage:
  python3 test_alcohol_sensor.py                  # Auto-detect USB port
  python3 test_alcohol_sensor.py /dev/ttyUSB0     # Specify port
  python3 test_alcohol_sensor.py --list            # List available ports
"""

import serial
import serial.tools.list_ports
import sys
import time
import re

# ======== Configuration ========
BAUDRATE = 4800
DATA_BITS = serial.EIGHTBITS
STOP_BITS = serial.STOPBITS_ONE
PARITY = serial.PARITY_NONE
TIMEOUT = 2  # seconds
CR_LF = b"\x0D\x0A"

# ======== Commands (Computer -> EBS-010) ========
CMD_START = b"$START" + CR_LF
CMD_END = b"$END" + CR_LF
CMD_WAIT = b"$WAIT" + CR_LF
CMD_STANBY = b"$STANBY" + CR_LF
CMD_BREATH = b"$BREATH" + CR_LF
CMD_TRIGGER = b"$TRIGGER" + CR_LF
CMD_RESET = b"$RESET" + CR_LF
CMD_RECALL = b"$RECALL" + CR_LF
CMD_CALIBRATION = b"$CALIBRATION" + CR_LF


def list_serial_ports():
    """แสดง serial ports ที่มีอยู่ในระบบ"""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("[!] ไม่พบ serial port ใดๆ ในระบบ")
        return []
    print("=" * 60)
    print(" Serial Ports ที่พบในระบบ")
    print("=" * 60)
    for p in ports:
        print(f"  Port : {p.device}")
        print(f"  Desc : {p.description}")
        print(f"  HWID : {p.hwid}")
        print("-" * 60)
    return ports


def auto_detect_port():
    """พยายาม auto-detect USB serial port ของ EBS-010"""
    ports = serial.tools.list_ports.comports()
    usb_ports = [p for p in ports if "USB" in p.device.upper() or "ACM" in p.device.upper()]
    if usb_ports:
        print(f"[*] Auto-detected port: {usb_ports[0].device} ({usb_ports[0].description})")
        return usb_ports[0].device
    if ports:
        print(f"[*] ใช้ port แรกที่พบ: {ports[0].device} ({ports[0].description})")
        return ports[0].device
    return None


def open_serial(port):
    """เปิด serial connection ไปยัง EBS-010"""
    try:
        ser = serial.Serial(
            port=port,
            baudrate=BAUDRATE,
            bytesize=DATA_BITS,
            stopbits=STOP_BITS,
            parity=PARITY,
            timeout=TIMEOUT,
        )
        print(f"[OK] เปิด serial port สำเร็จ: {port} @ {BAUDRATE} baud")
        return ser
    except serial.SerialException as e:
        print(f"[ERROR] ไม่สามารถเปิด port {port}: {e}")
        return None


def send_command(ser, cmd, label=""):
    """ส่งคำสั่งไปยัง EBS-010 และแสดงผล"""
    cmd_str = cmd.rstrip(b"\x0D\x0A").decode("ascii", errors="replace")
    print(f"\n[TX] ส่งคำสั่ง: {cmd_str}  {label}")
    ser.write(cmd)
    ser.flush()


def read_response(ser, wait_sec=2, max_lines=10):
    """อ่าน response จาก EBS-010"""
    responses = []
    end_time = time.time() + wait_sec
    while time.time() < end_time and len(responses) < max_lines:
        line = ser.readline()
        if line:
            decoded = line.decode("ascii", errors="replace").strip()
            if decoded:
                responses.append(decoded)
                print(f"[RX] << {decoded}")
        else:
            if responses:
                break
    if not responses:
        print("[RX] (ไม่มี response)")
    return responses


def parse_result(response_line):
    """แยกวิเคราะห์ผลลัพธ์จาก $RESULT,X.XXX-OK/HIGH"""
    match = re.match(r"\$RESULT,(\d+\.\d+)-(OK|HIGH)", response_line)
    if match:
        value = float(match.group(1))
        status = match.group(2)
        return {"value": value, "status": status}
    return None


def parse_detail(response_line):
    """แยกวิเคราะห์ผลลัพธ์จาก $U/B,L/000,H/000,T/0000"""
    match = re.match(r"\$U/([BGM]),L/(\d+),H/(\d+),T/(\d+)", response_line)
    if match:
        unit_map = {"B": "%BAC", "G": "g/L", "M": "mg/L"}
        unit_code = match.group(1)
        return {
            "unit": unit_map.get(unit_code, unit_code),
            "low_count": int(match.group(2)),
            "high_count": int(match.group(3)),
            "test_number": int(match.group(4)),
        }
    return None


def run_full_test(ser):
    """ทดสอบการทำงานเต็มรูปแบบ: START -> warm-up -> STANBY -> BREATH -> ผลลัพธ์"""
    print("\n" + "=" * 60)
    print(" EBS-010 Full Measurement Test")
    print("=" * 60)

    # Step 1: Start
    print("\n--- Step 1: START (เริ่มอุ่นเครื่อง) ---")
    send_command(ser, CMD_START, "(เริ่มต้นอุ่นเครื่อง)")
    responses = read_response(ser, wait_sec=3)

    # Step 2: Wait for warm-up
    print("\n--- Step 2: WAIT (รอ warm-up) ---")
    warmup_done = False
    for i in range(30):  # รอ warm-up สูงสุด 60 วินาที
        send_command(ser, CMD_WAIT, f"(รอ warm-up... {i+1}/30)")
        responses = read_response(ser, wait_sec=2)
        for r in responses:
            if "$STANBY" in r or "STANBY" in r.upper():
                warmup_done = True
                break
        if warmup_done:
            print("[OK] Warm-up เสร็จสิ้น!")
            break
        time.sleep(1)
    if not warmup_done:
        print("[!] Warm-up timeout — อาจยังไม่เสร็จ, ลองดำเนินการต่อ...")

    # Step 3: Standby
    print("\n--- Step 3: STANBY ---")
    send_command(ser, CMD_STANBY)
    responses = read_response(ser, wait_sec=2)

    # Step 4: Breath
    print("\n--- Step 4: BREATH (เริ่มเป่า) ---")
    print("[!] กรุณาเป่าลมเข้าเซ็นเซอร์...")
    send_command(ser, CMD_BREATH, "(เปิดรับลมหายใจ)")
    responses = read_response(ser, wait_sec=10)
    for r in responses:
        if "$FLOW,ERR" in r:
            print("[!] FLOW ERROR — เป่าลมไม่ถูกต้อง กรุณาลองใหม่")

    # Step 5: Trigger (ถ้าจำเป็น)
    print("\n--- Step 5: TRIGGER ---")
    send_command(ser, CMD_TRIGGER)
    responses = read_response(ser, wait_sec=5)

    # Step 6: รอผลลัพธ์
    print("\n--- Step 6: รอผลลัพธ์ ---")
    result_found = False
    for i in range(10):
        responses = read_response(ser, wait_sec=2)
        for r in responses:
            result = parse_result(r)
            if result:
                print(f"\n{'=' * 40}")
                print(f"  ผลการวัดแอลกอฮอล์")
                print(f"  ค่า   : {result['value']}")
                print(f"  สถานะ : {result['status']}")
                print(f"{'=' * 40}")
                result_found = True
            detail = parse_detail(r)
            if detail:
                print(f"  หน่วย      : {detail['unit']}")
                print(f"  LOW count  : {detail['low_count']}")
                print(f"  HIGH count : {detail['high_count']}")
                print(f"  Test #     : {detail['test_number']}")
        if result_found:
            break
        time.sleep(1)

    if not result_found:
        print("[!] ไม่ได้รับผลลัพธ์ — อาจต้องเป่าลมใหม่")

    # Step 7: End
    print("\n--- Step 7: END ---")
    send_command(ser, CMD_END)
    read_response(ser, wait_sec=2)

    return result_found


def run_connection_test(ser):
    """ทดสอบการเชื่อมต่อพื้นฐาน"""
    print("\n" + "=" * 60)
    print(" EBS-010 Connection Test")
    print("=" * 60)

    # ส่ง $END ก่อนเพื่อ reset state
    print("\n--- ส่ง $END เพื่อ reset state ---")
    send_command(ser, CMD_END)
    responses = read_response(ser, wait_sec=2)

    # ทดสอบ $RECALL (ตรวจค่าที่ตั้งไว้)
    print("\n--- ส่ง $RECALL เพื่อตรวจค่าที่ตั้งไว้ ---")
    send_command(ser, CMD_RECALL)
    responses = read_response(ser, wait_sec=3)

    # ทดสอบ $CALIBRATION
    print("\n--- ส่ง $CALIBRATION เพื่อตรวจสอบรอบ calibration ---")
    send_command(ser, CMD_CALIBRATION)
    responses = read_response(ser, wait_sec=3)

    if responses:
        print("\n[OK] เซ็นเซอร์ตอบกลับ — การเชื่อมต่อสำเร็จ!")
        return True
    else:
        print("\n[!] ไม่มี response — ตรวจสอบสาย USB และ port")
        return False


def run_listen_mode(ser):
    """โหมดฟัง — อ่านข้อมูลจาก sensor แบบต่อเนื่อง"""
    print("\n" + "=" * 60)
    print(" EBS-010 Listen Mode (Ctrl+C เพื่อหยุด)")
    print("=" * 60)
    try:
        while True:
            line = ser.readline()
            if line:
                decoded = line.decode("ascii", errors="replace").strip()
                if decoded:
                    timestamp = time.strftime("%H:%M:%S")
                    print(f"[{timestamp}] {decoded}")

                    result = parse_result(decoded)
                    if result:
                        print(f"           -> ค่าแอลกอฮอล์: {result['value']} ({result['status']})")
                    detail = parse_detail(decoded)
                    if detail:
                        print(f"           -> หน่วย: {detail['unit']}, Test#{detail['test_number']}")
    except KeyboardInterrupt:
        print("\n[*] หยุด Listen Mode")


def show_menu():
    """แสดงเมนูทดสอบ"""
    print("\n" + "=" * 60)
    print(" EBS-010 Breathalyzer Test Menu")
    print("=" * 60)
    print("  1. Connection Test    — ทดสอบการเชื่อมต่อ")
    print("  2. Full Measurement   — ทดสอบวัดค่าแอลกอฮอล์")
    print("  3. Listen Mode        — ฟังข้อมูลจาก sensor")
    print("  4. Send Custom Cmd    — ส่งคำสั่งเอง")
    print("  5. Reset (OFF)        — ปิดเครื่อง")
    print("  0. Exit               — ออก")
    print("=" * 60)


def main():
    # Handle --list flag
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_serial_ports()
        sys.exit(0)

    # Determine port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        print("[*] กำลังค้นหา serial ports...")
        list_serial_ports()
        port = auto_detect_port()
        if not port:
            print("[ERROR] ไม่พบ serial port — กรุณาระบุ port เช่น /dev/ttyUSB0")
            sys.exit(1)

    # Open serial
    ser = open_serial(port)
    if not ser:
        sys.exit(1)

    try:
        while True:
            show_menu()
            choice = input("\nเลือกเมนู [0-5]: ").strip()

            if choice == "1":
                run_connection_test(ser)
            elif choice == "2":
                run_full_test(ser)
            elif choice == "3":
                run_listen_mode(ser)
            elif choice == "4":
                cmd = input("ใส่คำสั่ง (ไม่ต้องใส่ CR/LF): ").strip().upper()
                if cmd:
                    send_command(ser, cmd.encode("ascii") + CR_LF)
                    read_response(ser, wait_sec=3)
            elif choice == "5":
                print("[*] กำลังส่ง $RESET เพื่อปิดเครื่อง...")
                send_command(ser, CMD_STANBY)
                time.sleep(1)
                send_command(ser, CMD_RESET, "(ปิดเครื่อง)")
                read_response(ser, wait_sec=2)
            elif choice == "0":
                print("[*] ออกจากโปรแกรม")
                break
            else:
                print("[!] กรุณาเลือก 0-5")

    except KeyboardInterrupt:
        print("\n[*] ออกจากโปรแกรม (Ctrl+C)")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("[OK] ปิด serial port แล้ว")


if __name__ == "__main__":
    main()
