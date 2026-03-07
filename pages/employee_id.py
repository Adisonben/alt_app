from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock
from time import monotonic
from functions.api import get_user_by_id

class EmployeeID(MDScreen):

    input_cooldown = 0.5

    def on_enter(self):
        self.clear_digits()
        self._last_input_at = 0.0
        # Ensure session is reset or ready? 
        # Ideally, we are here because we want to start a new auth flow.
        
    def add_digit(self, digit):
        now = monotonic()
        if now - getattr(self, "_last_input_at", 0.0) < self.input_cooldown:
            return

        self._last_input_at = now
        if len(self.ids.input_display.text) < 6:
            self.ids.input_display.text += digit

    def clear_digits(self):
        self._last_input_at = 0.0
        self.ids.input_display.text = ""

    def submit_id(self):
        employee_id = self.ids.input_display.text
        if not employee_id:
            return
        
        print(f"Verifying ID: {employee_id}")
        user = get_user_by_id(employee_id)
        
        if user:
            print(f"User found: {user}")
            
            # Store candidate in session
            app = MDApp.get_running_app()
            app.session.candidate_user = user
            
            # Navigate to Authing (Fingerprint)
            self.manager.current = "authing"
        else:
            print("User not found")
            self.ids.input_display.text = "Invalid ID"
            Clock.schedule_once(lambda dt: self.clear_digits(), 1.5)
