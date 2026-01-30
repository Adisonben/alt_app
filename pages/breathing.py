from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from functions.alcohol import measure_alcohol
from functions.camera import take_snapshot
import os
from datetime import datetime

class Breathing(MDScreen):
    _snapshot_path = None

    def on_enter(self):
        print("Start alcohol test...")
        measure_alcohol(self.on_alcohol_done)

    def on_alcohol_done(self, success, value):
        print(f"Alcohol value: {value}, Success: {success}")
        
        # Store value for later navigation
        self._last_alcohol_value = value
        
        # Only take snapshot if measurement succeeded
        if success:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self._snapshot_path = os.path.join(os.getcwd(), "assets", "snapshots", f"breathing_{timestamp}.jpg")
            take_snapshot(self._snapshot_path, self._on_snapshot_done)
        else:
            print("Alcohol measurement failed, skipping snapshot.")
            self._navigate_to_result(value, None)
    
    def _on_snapshot_done(self, success, path):
        if success:
            print(f"Snapshot saved: {path}")
        else:
            print("Snapshot failed or camera unavailable.")
            path = None
        # Navigate regardless of snapshot success
        self._navigate_to_result(self._last_alcohol_value, path)
    
    def _navigate_to_result(self, value, snapshot_path):
        result_screen = self.manager.get_screen("testresult")
        result_screen.result_value = value
        result_screen.snapshot_path = snapshot_path if snapshot_path else ""
        self.manager.current = "testresult"