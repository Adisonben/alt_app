"""
Camera functions using picamera2 for Raspberry Pi.
Provides preview streaming to Kivy Image widget and snapshot capture.
"""
import os
import threading
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# Try to import picamera2, set flag if unavailable
try:
    from picamera2 import Picamera2
    PICAMERA_AVAILABLE = True
except ImportError:
    PICAMERA_AVAILABLE = False
    print("[Camera] picamera2 not available. Camera functions disabled.")


class CameraManager:
    """Manages camera preview and snapshot operations."""
    
    def __init__(self):
        self._camera = None
        self._preview_widget = None
        self._preview_active = False
        self._preview_event = None
        self._is_connected = False
    
    def is_available(self):
        """Check if camera hardware is available."""
        return PICAMERA_AVAILABLE and self._is_connected
    
    def connect(self):
        """
        Try to connect to the camera.
        Returns True if successful, False otherwise.
        """
        if not PICAMERA_AVAILABLE:
            print("[Camera] picamera2 module not installed.")
            return False
        
        try:
            self._camera = Picamera2()
            # Explicitly request RGB format to avoid YUV conversion issues
            config = self._camera.create_preview_configuration(
                main={"size": (640, 480), "format": "RGB888"},
                lores={"size": (320, 240), "format": "RGB888"},
                display="lores"
            )
            self._camera.configure(config)
            self._is_connected = True
            print("[Camera] Connected successfully.")
            return True
        except Exception as e:
            print(f"[Camera] Failed to connect: {e}")
            self._camera = None
            self._is_connected = False
            return False
    
    def disconnect(self):
        """Disconnect the camera and release resources."""
        self.stop_preview()
        if self._camera:
            try:
                self._camera.stop()
                self._camera.close()
            except Exception as e:
                print(f"[Camera] Error during disconnect: {e}")
            finally:
                self._camera = None
                self._is_connected = False
        print("[Camera] Disconnected.")
    
    def start_preview(self, image_widget):
        """
        Start streaming camera frames to a Kivy Image widget.
        
        Args:
            image_widget: Kivy Image widget to display frames.
        """
        if not self._is_connected or not self._camera:
            print("[Camera] Cannot start preview: Camera not connected.")
            return False
        
        self._preview_widget = image_widget
        self._preview_active = True
        
        try:
            self._camera.start()
            # Schedule frame updates
            self._preview_event = Clock.schedule_interval(self._update_frame, 1.0 / 15)  # 15 FPS
            print("[Camera] Preview started.")
            return True
        except Exception as e:
            print(f"[Camera] Failed to start preview: {e}")
            self._preview_active = False
            return False
    
    def _update_frame(self, dt):
        """Update the preview widget with the latest camera frame."""
        if not self._preview_active or not self._camera or not self._preview_widget:
            return
        
        try:
            import numpy as np
            # Capture frame as numpy array (already RGB888 format)
            frame = self._camera.capture_array("lores")
            
            h, w = frame.shape[:2]
            
            # Determine color format based on shape
            if len(frame.shape) == 3 and frame.shape[2] >= 3:
                colorfmt = 'rgb'
                # Use only first 3 channels if RGBA
                frame_rgb = frame[:, :, :3] if frame.shape[2] > 3 else frame
            else:
                colorfmt = 'luminance'
                frame_rgb = frame
            
            # Create texture and blit buffer
            texture = Texture.create(size=(w, h), colorfmt=colorfmt)
            # Flip vertically for Kivy coordinate system
            frame_flipped = np.flipud(frame_rgb)
            texture.blit_buffer(frame_flipped.tobytes(), colorfmt=colorfmt, bufferfmt='ubyte')
            
            # Update widget
            self._preview_widget.texture = texture
        except Exception as e:
            print(f"[Camera] Frame update error: {e}")
    
    def stop_preview(self):
        """Stop the camera preview."""
        self._preview_active = False
        
        if self._preview_event:
            self._preview_event.cancel()
            self._preview_event = None
        
        if self._camera and self._is_connected:
            try:
                self._camera.stop()
            except Exception as e:
                print(f"[Camera] Error stopping camera: {e}")
        
        print("[Camera] Preview stopped.")
    
    def take_snapshot(self, filepath, callback=None):
        """
        Capture a still image and save to file.
        
        Args:
            filepath: Path to save the image.
            callback: Optional callback(success: bool, path: str) called on completion.
        """
        if not self._is_connected or not self._camera:
            print("[Camera] Cannot take snapshot: Camera not connected.")
            if callback:
                Clock.schedule_once(lambda dt: callback(False, None), 0)
            return
        
        def _capture_thread():
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                # Capture image
                self._camera.capture_file(filepath)
                print(f"[Camera] Snapshot saved: {filepath}")
                
                if callback:
                    Clock.schedule_once(lambda dt: callback(True, filepath), 0)
            except Exception as e:
                print(f"[Camera] Snapshot error: {e}")
                if callback:
                    Clock.schedule_once(lambda dt: callback(False, None), 0)
        
        threading.Thread(target=_capture_thread, daemon=True).start()


# Singleton instance
camera_manager = CameraManager()
