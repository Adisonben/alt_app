from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock
from functions.api import get_user_by_id

class EmployeeID(MDScreen):
    
    def on_enter(self):
        self.clear_digits()
        # Ensure session is reset or ready? 
        # Ideally, we are here because we want to start a new auth flow.
        
    def add_digit(self, digit):
        if len(self.ids.input_display.text) < 6:
            self.ids.input_display.text += digit

    def clear_digits(self):
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
