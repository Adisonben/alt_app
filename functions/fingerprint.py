from kivy.clock import Clock

def scan_fingerprint(callback):
    """
    ฟังก์ชันสแกนนิ้ว
    - จำลอง hardware ด้วย Clock.schedule_once
    - ในของจริงสามารถใช้ thread อ่านจาก serial แล้วค่อย callback
    """
    Clock.schedule_once(lambda dt: callback(True), 2)
