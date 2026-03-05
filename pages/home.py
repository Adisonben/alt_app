from kivymd.uix.screen import MDScreen
from functions.audio import play_voice
from config import KIOSK_MODE

class Home(MDScreen):
    def on_enter(self):
        play_voice('voice_welcome.mp3')
        # self._apply_kiosk_mode()

    # def _apply_kiosk_mode(self):
    #     normal_card = self.ids.get("normal_card")
    #     free_card = self.ids.get("free_card")
    #     if KIOSK_MODE == "normal":
    #         if normal_card:
    #             normal_card.opacity = 1
    #             normal_card.size_hint_x = 1
    #             normal_card.disabled = False
    #         if free_card:
    #             free_card.opacity = 0
    #             free_card.size_hint_x = 0
    #             free_card.disabled = True
    #     elif KIOSK_MODE == "free":
    #         if normal_card:
    #             normal_card.opacity = 0
    #             normal_card.size_hint_x = 0
    #             normal_card.disabled = True
    #         if free_card:
    #             free_card.opacity = 1
    #             free_card.size_hint_x = 1
    #             free_card.disabled = False
    #     else:
    #         if normal_card:
    #             normal_card.opacity = 1
    #             normal_card.size_hint_x = 1
    #             normal_card.disabled = False
    #         if free_card:
    #             free_card.opacity = 1
    #             free_card.size_hint_x = 1
    #             free_card.disabled = False

    def go_next(self):
        self.manager.current = "employeeid"