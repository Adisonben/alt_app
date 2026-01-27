from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
import pages  # ensure custom screen classes (Home, Authing, ...) are imported and registered for KV

class MainApp(MDApp):
    def build(self):
        LabelBase.register(
            name="Sarabun",
            fn_regular="fonts/THSarabunNew.ttf"
        )
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
        return root

if __name__ == "__main__":
    MainApp().run()