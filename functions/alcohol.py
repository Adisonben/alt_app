from kivy.clock import Clock
try:
    import serial
except Exception:
    # serial (pyserial) may not be available in the dev environment.
    # Make module importable and let runtime functions use a simulated path.
    serial = None
import threading
import time

def measure_alcohol(callback):
    """
    ฟังก์ชันวัดค่าแอลกอฮอล์
    - callback(success: bool, value: float)
    - success: True if measurement succeeded, False on error
    - value: Alcohol level (0.0 or higher), or -1.0 on error
    """
    port = "COM3"
    baudrate = 4800
    # ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
    # if ser.in_waiting:
    #     print(f"Connected to {port} at {baudrate} baud.")
    #     prepare_alcohol = prepare(ser)
    #     if prepare_alcohol:
    #         worker(ser, callback)
    #     else:
    #         print("Cannot prepare alcolhol.")
    # else:
    #     print("Serial open unsuccess!!!") 
    Clock.schedule_once(lambda dt: callback(True, 0.00), 3)

def prepare(ser):
    try:
        while True:
            # only attempt to read from serial if a serial object is provided
            if ser is not None and getattr(ser, "in_waiting", False):  # Check if data available
                data = ser.readline().decode("utf-8", errors="ignore").strip()
                print("Received:", data)
                if "STANBY" in data.upper():
                    print("Alcohol is stanby.")
                    break
                elif "END" in data.upper():
                    send_command(ser, "$START")
            time.sleep(0.1)
        return True
    except Exception as e:
        # serial may not be available or other I/O error occurred
        print(f"Error: {e}")
        return False

def worker(ser, callback):
    try:
        # อ่าน 1 บรรทัด (sensor ส่งมาเป็น string เช่น "0.03\n")
        # line = ser.readline().decode("utf-8").strip()
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        ser.close()
        print(f"[worker] : Raw value is: {line}")
        try:
            value = float(line)   # แปลงค่าเป็น float
        except ValueError:
            value = -1.0          # ถ้าแปลงไม่ได้ ให้เป็น error code
        print(f"[worker] : Result value is: {value}")
        send_command(ser, "$RESET")
        # ส่งกลับไป callback ใน main thread
        Clock.schedule_once(lambda dt: callback(True, value), 0)

    except Exception as e:
        print("[worker] : Error reading alcohol sensor:", e)
        Clock.schedule_once(lambda dt: callback(False, -1.0), 0)

def send_command(ser, cmd):
        """ส่งคำสั่งไปยังเครื่องเป่า"""
        command = f"{cmd}\r\n".encode("ascii")  # Protocol ใช้ CRLF (0D 0A)
        ser.write(command)
        # time.sleep(0.2)
        # response = self.ser.readline().decode("ascii", errors="ignore").strip()
        # return response