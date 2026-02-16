from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock
from functions.alcohol import measure_alcohol
from functions.camera import take_snapshot
import os
from datetime import datetime

class Breathing(MDScreen):

    def on_enter(self):
        print("Start alcohol test...")
        measure_alcohol(self.on_alcohol_done)

    def on_alcohol_done(self, success, value):
        print(f"Alcohol value: {value}, Success: {success}")
        
        app = MDApp.get_running_app()
        app.session.alcohol_value = value
        
        # Only take snapshot if measurement succeeded
        if success:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_path = os.path.join(os.getcwd(), "assets", "snapshots", f"breathing_{timestamp}.jpg")
            
            # Store path in session temporarily (or confirm after save)
            app.session.snapshot_path = snapshot_path
            
            take_snapshot(snapshot_path, self._on_snapshot_done)
        else:
            print("Alcohol measurement failed, skipping snapshot.")
            self._navigate_to_result()
    
    def _on_snapshot_done(self, success, path):
        if success:
            print(f"Snapshot saved: {path}")
        else:
            print("Snapshot failed or camera unavailable.")
            # Clear path in session if failed?
            MDApp.get_running_app().session.snapshot_path = ""
            
        # Navigate regardless of snapshot success
        self._navigate_to_result()
    
    def _navigate_to_result(self):
        self.manager.current = "testresult"