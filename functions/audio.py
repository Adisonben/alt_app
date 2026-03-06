from kivy.core.audio import SoundLoader
import threading
import pygame
import time

_current_sound = None
_pygame_initialized = False


def _init_pygame():
    global _pygame_initialized
    if not _pygame_initialized:
        pygame.mixer.init()
        _pygame_initialized = True


def _play(path):
    global _current_sound

    if _current_sound:
        _current_sound.stop()

    sound = SoundLoader.load(path)

    if sound:
        _current_sound = sound
        sound.play()


def _pygame_play(path):
    try:
        _init_pygame()
        sound = pygame.mixer.Sound(path)
        sound.play()
    except Exception as e:
        print(f"Pygame playback error: {e}")


def play_sound(path):
    thread = threading.Thread(target=_play, args=(path,))
    thread.daemon = True
    thread.start()


def pygame_play(path):
    try:
        _init_pygame()
        sound = pygame.mixer.Sound(path)
        sound.play()
    except Exception as e:
        print(f"Pygame playback error: {e}")