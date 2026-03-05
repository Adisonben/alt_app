from kivy.core.audio import SoundLoader

_current_sound = None


def play_sound(path):
    global _current_sound
    if _current_sound:
        _current_sound.stop()
    sound = SoundLoader.load(path)
    if sound:
        _current_sound = sound
        sound.play()
