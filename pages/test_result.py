from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.clock import Clock
from functions.api import send_test_result
from kivy.properties import StringProperty

class TestResult(MDScreen):
    result_value = StringProperty("0")
    snapshot_path = StringProperty("")

    def on_enter(self):
        app = MDApp.get_running_app()
        session = app.session
        
        self.result_value = str(session.alcohol_value)
        self.snapshot_path = session.snapshot_path if session.snapshot_path else ""
        
        print(f"Result = {session.alcohol_value}")
        
        if session.is_authenticated:
            # Prepare data array to send
            data_to_send = [
                session.alcohol_value, 
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