from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty

class TestResult(MDScreen):
    result_value = NumericProperty(0.00)
    snapshot_path = StringProperty("")

    def on_enter(self):
        print(f"Result = {self.result_value}")
        Clock.schedule_once(self.go_home, 5)

    def go_home(self, dt):
        self.manager.current = "home"