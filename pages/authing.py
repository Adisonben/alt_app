from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.clock import Clock
from functions.fingerprint import scan_fingerprint, compare_fingerprints
from functions.api import get_user_by_id

# def scan_fingerprint(callback):
#     # จำลอง hardware ใช้เวลา 2 วิ
#     Clock.schedule_once(lambda dt: callback(True), 2)


class Authing(MDScreen):
    failed_attempts = 0
    is_active = False
    _scheduled_events = []

    def on_enter(self):
        self.is_active = True
        self.failed_attempts = 0
        self._scheduled_events = []
        
        # Check if we have a candidate user from EmployeeID screen
        app = MDApp.get_running_app()
        candidate = getattr(app.session, 'candidate_user', None)
        
        if not candidate:
            print("No candidate user found. Redirecting to EmployeeID.")
            # Verify if this redirection is appropriate or if should go home
            # For now, let's redirect to employee_id input
            self.manager.current = "employeeid"
            return

        # Start Fingerprint Scan Immediately
        # Show fingerprint box (it should be visible by default now in KV, but let's ensure)
        self.ids.fingerprint_box.opacity = 1
        self.ids.fingerprint_box.disabled = False
        self.ids.result_box_pass.opacity = 0
        self.ids.result_box_pass.disabled = True
        self.ids.result_box_fail.opacity = 0
        self.ids.result_box_fail.disabled = True
        
        self.start_fingerprint_scan()

    def _schedule_once(self, callback, timeout):
        if not self.is_active:
            return
        event = Clock.schedule_once(callback, timeout)
        self._scheduled_events.append(event)
        return event

    def on_fingerprint_done(self, success, b64_data):
        if not self.is_active:
            print("Authing: on_fingerprint_done called but screen not active. Ignoring.")
            return

        if success:
            print(f"Fingerprint scan successful. Data length: {len(b64_data)}")
            print(f"Raw data: {b64_data}")
            
            app = MDApp.get_running_app()
            candidate = getattr(app.session, 'candidate_user', None)
            
            if not candidate or not candidate.get('finger_data'):
                 print("Error: No candidate user or finger data found in session.")
                 self.show_result("Fail")
                 return

            finger_data = candidate.get('finger_data')
            print("Comparing with stored finger data...")
            compare_fingerprints(b64_data, finger_data, self.on_match_done)
        else:
            print("Fingerprint scan failed or timed out.")
            self.show_result("Fail")

    def on_match_done(self, match, msg):
        if not self.is_active:
            print("Authing: on_match_done called but screen not active. Ignoring.")
            return

        print(f"Match Result: {match} ({msg})")
        if match:
             # Succcessful Match - Start Session
             app = MDApp.get_running_app()
             candidate = getattr(app.session, 'candidate_user', None)
             if candidate:
                 app.session.start(candidate)
                 # Clear temp candidate
                 app.session.candidate_user = None
                 
             self.show_result("Pass")
        else:
             self.show_result("Fail")

    def start_heartbeat(self, widget):
        # Scale up
        anim_up = Animation(size=(110, 110), duration=0.5, t="out_quad")
        # Scale down
        anim_down = Animation(size=(100, 100), duration=0.5, t="in_quad")

        anim = anim_up + anim_down
        anim.repeat = True
        anim.start(widget)
    
    def start_fingerprint_scan(self):
        print(f"Start fingerprint scan... (Attempt {self.failed_attempts + 1})")
        scan_fingerprint(self.on_fingerprint_done)

    def start_timer(self, *args):
        if not self.is_active:
            return

        print("Restarting auth flow...")
        # Since we are already on Authing page with a candidate, we just restart scan
        
        # Hide result boxes
        self.ids.result_box_pass.opacity = 0
        self.ids.result_box_pass.disabled = True
        self.ids.result_box_fail.opacity = 0
        self.ids.result_box_fail.disabled = True
        
        # Show fingerprint box
        self.ids.fingerprint_box.opacity = 1
        self.ids.fingerprint_box.disabled = False
        
        self.start_fingerprint_scan()

    def show_result(self, *args):
        if not self.is_active:
            return

        # hide fingerprint box
        self.ids.fingerprint_box.opacity = 0
        self.ids.fingerprint_box.disabled = True
        
        result = args[0] if args else "Fail"
        print(f"Showing result: {result}")
        
        if result == "Pass":
            # Ensure session is started if this was triggered manually (debug)
            app = MDApp.get_running_app()
            if not app.session.is_authenticated:
                 candidate = getattr(app.session, 'candidate_user', None)
                 if candidate:
                     print("Debug: Starting session from manual Pass")
                     app.session.start(candidate)
            
            self.ids.result_box_pass.opacity = 1
            self.ids.result_box_pass.disabled = False
            # No need to set user_id on next screen, session handles it
            self._schedule_once(lambda dt: setattr(self.manager, "current", "breathing"), 1)
        else:
            self.ids.result_box_fail.opacity = 1
            self.ids.result_box_fail.disabled = False
            
            self.failed_attempts += 1
            print(f"Failed attempts: {self.failed_attempts}")
            
            if self.failed_attempts >= 3:
                print("Max attempts reached. Going home.")
                self._schedule_once(self.go_home, 4)
            else:
                self._schedule_once(self.start_timer, 4)

    def go_home(self, dt):
        if self.is_active:
            self.manager.current = "home"

    def on_leave(self):
        # Mark as inactive immediately
        self.is_active = False

        # Cancel all scheduled events
        for event in self._scheduled_events:
            Clock.unschedule(event)
        self._scheduled_events = []
        # Reset the state when leaving the screen
        # Hide result boxes
        self.ids.result_box_pass.opacity = 0
        self.ids.result_box_pass.disabled = True
        self.ids.result_box_fail.opacity = 0
        self.ids.result_box_fail.disabled = True
        
        # Hide fingerprint box (initial state)
        self.ids.fingerprint_box.opacity = 0
        self.ids.fingerprint_box.disabled = True