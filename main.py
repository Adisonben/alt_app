from kivy.lang import Builder
from kivymd.app import MDApp
from session_manager import KioskSession
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
from datetime import datetime
from kivy.core.audio import SoundLoader
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
        # โหลดและเล่น BG music
        self.bg_music = SoundLoader.load('assets/sounds/bg_music.mp3')
        if self.bg_music:
            self.bg_music.loop = True   # วนซ้ำตลอด
            self.bg_music.volume = 0.4  # ปรับความดัง (0.0 - 1.0)
            self.bg_music.play()

        Clock.schedule_interval(self._update_clock, 1)
        self._idle_event = None
        sm = self.root.ids.screen_manager
        sm.bind(current=self._on_screen_change)
        # Start timer immediately since app opens on home
        self.start_idle_timer()

    def _update_clock(self, dt):
        now = datetime.now()
        try:
            self.root.ids.clock_label.text = now.strftime("%H:%M:%S")
            self.root.ids.date_label.text = now.strftime("%d/%m/%Y")
        except Exception:
            pass

    def _on_screen_change(self, sm, current):
        if current == "home":
            self.start_idle_timer()
        else:
            self._cancel_idle_timer()

    def start_idle_timer(self):
        self._cancel_idle_timer()
        self._idle_event = Clock.schedule_once(self._trigger_idle, IDLE_TIMEOUT)

    def _cancel_idle_timer(self):
        if self._idle_event is not None:
            self._idle_event.cancel()
            self._idle_event = None

    def _trigger_idle(self, dt):
        self.root.ids.screen_manager.current = "screensaver"

if __name__ == "__main__":
    MainApp().run()