"""
Camera functions using picamera2 for Raspberry Pi.
Provides snapshot capture only.
"""
import os
from kivy.clock import Clock

# Try to import picamera2, set flag if unavailable
try:
    from picamera2 import Picamera2
    PICAMERA_AVAILABLE = True
except ImportError:
    PICAMERA_AVAILABLE = False
    print("[Camera] picamera2 not available. Camera functions disabled.")


def take_snapshot(filepath, callback=None):
    """
    Capture a still image and save to file.
    
    Args:
        filepath: Path to save the image.
        callback: Optional callback(success: bool, path: str) called on completion.
    """
    if not PICAMERA_AVAILABLE:
        print("[Camera] picamera2 module not installed.")
        if callback:
            Clock.schedule_once(lambda dt: callback(False, None), 0)
        return
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create camera, configure, capture, and close
        picam2 = Picamera2()
        config = picam2.create_still_configuration(
            main={"size": (1920, 1080)},
            lores={"size": (640, 480)},
            display="lores"
        )
        picam2.configure(config)
        picam2.start()
        
        # Small delay to let camera warm up
        import time
        time.sleep(0.5)
        
        # Capture image
        picam2.capture_file(filepath)
        print(f"[Camera] Snapshot saved: {filepath}")
        
        picam2.stop()
        picam2.close()
        
        if callback:
            Clock.schedule_once(lambda dt: callback(True, filepath), 0)
    except Exception as e:
        print(f"[Camera] Snapshot error: {e}")
        if callback:
            Clock.schedule_once(lambda dt: callback(False, None), 0)
