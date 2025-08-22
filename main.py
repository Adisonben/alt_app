from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager

# Import pages
from pages import Home, Authing, AuthResult, Breathing, TestResult, ShowError

LabelBase.register(name="Sarabun", fn_regular="fonts/THSarabunNew.ttf")

class MainApp(MDApp):
    def build(self):
        # self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.primaryColor = "Blue"

        # Load all KV files from kv/ folder
        Builder.load_file("styles/home.kv")
        Builder.load_file("styles/auth_result.kv")
        Builder.load_file("styles/authing.kv")
        Builder.load_file("styles/breathing.kv")
        Builder.load_file("styles/test_result.kv")
        Builder.load_file("styles/show_error.kv")
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    MainApp().run()