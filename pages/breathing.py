from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from functions.alcohol import measure_alcohol
from functions.camera import camera_manager
import os
from datetime import datetime

class Breathing(MDScreen):
    _camera_connected = False

    def on_enter(self):
        print("Start alcohol test...")
        
        # Try to connect and start camera preview
        self._camera_connected = camera_manager.connect()
        if self._camera_connected:
            # Get the Image widget from kv
            camera_image = self.ids.get('camera_image')
            if camera_image:
                camera_manager.start_preview(camera_image)
                self.ids.camera_status.opacity = 0  # Hide status text
        else:
            # Show error message in camera card
            self.ids.camera_status.text = "Camera not available"
            self.ids.camera_status.opacity = 1
        
        measure_alcohol(self.on_alcohol_done)

    def on_alcohol_done(self, success, value):
        print(f"Alcohol value: {value}, Success: {success}")
        
        # Store value for later navigation
        self._last_alcohol_value = value
        
        # Only take snapshot if measurement succeeded and camera is connected
        if success and self._camera_connected:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_path = os.path.join(os.getcwd(), "assets", "snapshots", f"breathing_{timestamp}.jpg")
            camera_manager.take_snapshot(snapshot_path, self._on_snapshot_done)
        else:
            if not success:
                print("Alcohol measurement failed, skipping snapshot.")
            self._navigate_to_result(value)
    
    def _on_snapshot_done(self, success, path):
        if success:
            print(f"Snapshot saved: {path}")
        else:
            print("Snapshot failed or camera unavailable.")
        # Navigate regardless of snapshot success
        self._navigate_to_result(self._last_value)
    
    def _navigate_to_result(self, value):
        result_screen = self.manager.get_screen("testresult")
        result_screen.result_value = value
        self.manager.current = "testresult"


    def on_leave(self):
        # Stop camera when leaving the screen
        if self._camera_connected:
            camera_manager.stop_preview()
            camera_manager.disconnect()
            self._camera_connected = False