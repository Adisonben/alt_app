from kivymd.uix.screen import MDScreen
from functions.audio import pygame_play

class Home(MDScreen):
    def __init__(self, **kwargs):
        print("Home init")
        super().__init__(**kwargs)
        self.first_enter = True

    def on_enter(self):
        print("Home enter")
        if self.first_enter:
            print("first enter triggleed")
            self.first_enter = False
            return
        pygame_play("assets/sounds/voice_welcome.wav")

    def go_next(self):
        self.manager.current = "employeeid"