from kivy.core.audio import SoundLoader

_current_voice = None  # track currently playing voice sound


def play_voice(filename: str):
    """
    Load and play a voice file from assets/sounds/.
    Stops any previously playing voice before playing the new one.
    """
    global _current_voice

    # Stop and unload the previous voice if still playing
    if _current_voice is not None:
        try:
            _current_voice.stop()
            _current_voice.unload()
        except Exception:
            pass
        _current_voice = None

    sound = SoundLoader.load(f'assets/sounds/{filename}')
    if sound:
        _current_voice = sound
        sound.play()
    else:
        print(f'[audio] Warning: sound file not found — assets/sounds/{filename}')


def stop_voice():
    """Stop the currently playing voice sound."""
    global _current_voice
    if _current_voice is not None:
        try:
            _current_voice.stop()
            _current_voice.unload()
        except Exception:
            pass
        _current_voice = None
