from kivymd.uix.screen import MDScreen
from kivy.animation import Animation


class Idle(MDScreen):
    _pulse_anim = None

    def on_enter(self):
        self._start_pulse()

    def on_leave(self):
        if self._pulse_anim:
            self._pulse_anim.stop(self.ids.pulse_icon)
        self.ids.pulse_icon.opacity = 1

    def _start_pulse(self):
        self._pulse_anim = (
            Animation(opacity=0.3, duration=1) +
            Animation(opacity=1, duration=1)
        )
        self._pulse_anim.repeat = True
        self._pulse_anim.start(self.ids.pulse_icon)

    def on_touch_down(self, touch):
        from kivy.app import App
        app = App.get_running_app()
        self.manager.current = "home"
        self.manager.transition.direction = "right"
        app.start_idle_timer()
        return True
