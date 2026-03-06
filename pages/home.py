from kivymd.uix.screen import MDScreen
from functions.audio import pygame_play

class Home(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_enter = True
        
    def on_enter(self):
        if self.first_enter:
            self.first_enter = False
            return
        pygame_play("assets/sounds/voice_welcome.mp3")

    def go_next(self):
        self.manager.current = "employeeid"