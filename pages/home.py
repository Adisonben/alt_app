from kivymd.uix.screen import MDScreen
from functions.audio import play_sound

class Home(MDScreen):
    def on_enter(self):
        play_sound("assets/sounds/voice_welcome.wav")

    def go_next(self):
        self.manager.current = "employeeid"