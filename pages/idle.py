from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation


class Idle(FloatLayout):
    _pulse_anim = None

    def show_idle(self):
        self.opacity = 1
        self.disabled = False
        self._start_pulse()

    def dismiss_idle(self):
        if self._pulse_anim:
            self._pulse_anim.stop(self.ids.pulse_icon)
        self.ids.pulse_icon.opacity = 1
        self.opacity = 0
        self.disabled = True

    def _start_pulse(self):
        self._pulse_anim = (
            Animation(opacity=0.3, duration=1) +
            Animation(opacity=1, duration=1)
        )
        self._pulse_anim.repeat = True
        self._pulse_anim.start(self.ids.pulse_icon)

    def on_touch_down(self, touch):
        if self.opacity > 0:
            from kivy.app import App
            App.get_running_app().reset_idle_timer()
            return True
        return super().on_touch_down(touch)
