from kivy.lang import Builder
from kivymd.app import MDApp
from session_manager import KioskSession
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from datetime import datetime
import pages  # ensure custom screen classes (Home, Authing, ...) are imported and registered for KV

IDLE_TIMEOUT = 60  # seconds

class MainApp(MDApp):
    def build(self):
        self.session = KioskSession()
        LabelBase.register(
            name="Sarabun",
            fn_regular="fonts/THSarabunNew.ttf"
        )
        # self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.primaryColor = "Blue"

        # Load all KV files from kv/ folder
        Builder.load_file("styles/home.kv")
        Builder.load_file("styles/employee_id.kv")
        Builder.load_file("styles/prepare_result.kv")
        Builder.load_file("styles/authing.kv")
        Builder.load_file("styles/breathing.kv")
        Builder.load_file("styles/test_result.kv")
        Builder.load_file("styles/show_error.kv")
        Builder.load_file("styles/idle.kv")
        root = Builder.load_file("main.kv")
        return root

    def on_start(self):
        Clock.schedule_interval(self._update_clock, 1)
        self._idle_event = Clock.schedule_once(self._trigger_idle, IDLE_TIMEOUT)

    def _update_clock(self, dt):
        now = datetime.now()
        root = self.root
        try:
            root.ids.clock_label.text = now.strftime("%H:%M:%S")
            root.ids.date_label.text = now.strftime("%d/%m/%Y")
        except Exception:
            pass

    def reset_idle_timer(self):
        if hasattr(self, '_idle_event'):
            self._idle_event.cancel()
        self._idle_event = Clock.schedule_once(self._trigger_idle, IDLE_TIMEOUT)
        try:
            idle_screen = self.root.ids.screen_manager.get_screen("idle")
            if idle_screen.opacity > 0:
                idle_screen.dismiss_idle()
        except Exception:
            pass

    def _trigger_idle(self, dt):
        sm = self.root.ids.screen_manager
        sm.current = "home"
        try:
            idle_screen = sm.get_screen("idle")
            idle_screen.show_idle()
        except Exception:
            pass

if __name__ == "__main__":
    MainApp().run()