from kivymd.uix.screen import MDScreen
from functions.audio import pygame_play

class Home(MDScreen):
    def on_enter(self):
        pygame_play("assets/sounds/voice_welcome.mp3")

    def go_next(self):
        self.manager.current = "employeeid"