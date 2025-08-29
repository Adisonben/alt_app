from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
import serial
import threading
import time

# Import pages
from pages import Home, Authing, PrepareResult, Breathing, TestResult, ShowError

LabelBase.register(name="Sarabun", fn_regular="fonts/THSarabunNew.ttf")

def uart_listener(port="COM3", baudrate=4800, timeout=1):
    try:
        ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        print(f"Connected to {port} at {baudrate} baud.")

        while True:
            if ser.in_waiting:  # Check if data available
                data = ser.readline().decode("utf-8", errors="ignore").strip()
                if data:
                    print("Received:", data)   # You can also update a Kivy label here
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error: {e}")

class MainApp(MDApp):
    def build(self):
        # self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.primaryColor = "Blue"

        # Load all KV files from kv/ folder
        Builder.load_file("styles/home.kv")
        Builder.load_file("styles/prepare_result.kv")
        Builder.load_file("styles/authing.kv")
        Builder.load_file("styles/breathing.kv")
        Builder.load_file("styles/test_result.kv")
        Builder.load_file("styles/show_error.kv")
        root = Builder.load_file("main.kv")

        # Start UART listener in background
        # threading.Thread(target=uart_listener, daemon=True).start()

        return root

if __name__ == "__main__":
    MainApp().run()