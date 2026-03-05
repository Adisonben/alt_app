from kivymd.uix.screen import MDScreen
from functions.audio import play_sound
from kivy.clock import Clock

class Home(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.play_welcome, 10)

    def play_welcome(self, dt):
        play_sound("assets/sounds/voice_welcome.wav")

    def go_next(self):
        self.manager.current = "employeeid"