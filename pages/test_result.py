from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock
from functions.api import send_test_result
from functions.printer import print_receipt
from kivy.properties import StringProperty

class TestResult(MDScreen):
    result_value = StringProperty("0")
    snapshot_path = StringProperty("")

    def on_enter(self):
        app = MDApp.get_running_app()
        session = app.session
        
        self.result_value = str(session.alcohol_value)
        self.snapshot_path = session.snapshot_path if session.snapshot_path else ""
        
        alcohol_status = getattr(session, "alcohol_status", "")
        print(f"Result = {session.alcohol_value}, Status = {alcohol_status}")
        
        # Print Receipt
        # Device ID is hardcoded for now as it's not in session
        try:
             print_receipt(
                user_id=session.user_id,
                user_name=session.user_name,
                value=session.alcohol_value,
                status=alcohol_status,
                device_id="Kiosk-001" 
             )
        except Exception as e:
            print(f"Error printing receipt: {e}")

        if session.is_authenticated:
            # Prepare data array to send
            data_to_send = [
                session.alcohol_value,
                alcohol_status,
                session.snapshot_path,
                session.user_id
            ]
            send_test_result(data_to_send)
        else:
            print("Free Mode: Skipping API call and data upload.")
        
        # Reset session and go home after delay
        Clock.schedule_once(self.finish_session, 5)

    def finish_session(self, dt):
        app = MDApp.get_running_app()
        app.session.reset()
        if self.manager:
             self.manager.current = "home"