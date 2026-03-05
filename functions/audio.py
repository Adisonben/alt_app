from kivy.core.audio import SoundLoader
import threading

_current_sound = None


def _play(path):
    global _current_sound

    if _current_sound:
        _current_sound.stop()

    sound = SoundLoader.load(path)

    if sound:
        _current_sound = sound
        sound.play()


def play_sound(path):
    thread = threading.Thread(target=_play, args=(path,))
    thread.daemon = True
    thread.start()