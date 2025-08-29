from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from functions.alcohol import measure_alcohol

# def measure_alcohol(callback):
#     Clock.schedule_once(lambda dt: callback(0.33), 3)

class Breathing(MDScreen):
    def on_enter(self):
        print("Start alcohol test...")
        measure_alcohol(self.on_alcohol_done)

    def on_alcohol_done(self, value):
        result_screen = self.manager.get_screen("testresult")
        result_screen.result_value = value
        self.manager.current = "testresult"