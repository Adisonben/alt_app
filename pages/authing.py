from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.animation import Animation
from kivy.clock import Clock
from functions.fingerprint import scan_fingerprint, compare_fingerprints, check_fingerprint_device
from functions.api import get_user_by_id
from functions.audio import play_voice

SCAN_UI_TIMEOUT = 18  # seconds — UI-level guard (slightly longer than subprocess timeout)


class Authing(MDScreen):
    failed_attempts = 0
    is_active = False
    _scheduled_events = []
    _scan_timeout_event = None

    def on_enter(self):
        play_voice('voice_authing.mp3')
        self.is_active = True
        self.failed_attempts = 0
        self._scheduled_events = []
        self._scan_timeout_event = None

        # Check if we have a candidate user from EmployeeID screen
        app = MDApp.get_running_app()
        candidate = getattr(app.session, 'candidate_user', None)

        if not candidate:
            print("No candidate user found. Redirecting to EmployeeID.")
            self.manager.current = "employeeid"
            return

        # Reset all state panels
        self._show_panel("fingerprint_box")

        # Check device availability before scanning
        if not check_fingerprint_device():
            self._show_device_error(
                "ไม่พบเครื่องสแกนลายนิ้วมือ\nFingerprint scanner not found"
            )
            return

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
        # Cancel the UI timeout guard — callback arrived
        if self._scan_timeout_event:
            Clock.unschedule(self._scan_timeout_event)
            self._scan_timeout_event = None

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
        # Cancel any existing timeout guard
        if self._scan_timeout_event:
            Clock.unschedule(self._scan_timeout_event)
        # Set UI-level timeout guard
        self._scan_timeout_event = Clock.schedule_once(self._on_scan_ui_timeout, SCAN_UI_TIMEOUT)
        scan_fingerprint(self.on_fingerprint_done)

    def _on_scan_ui_timeout(self, dt):
        """Fired if the scan callback never arrives within SCAN_UI_TIMEOUT seconds."""
        if not self.is_active:
            return
        print(f"[Authing] Scan UI timeout after {SCAN_UI_TIMEOUT}s — treating as fail")
        self._scan_timeout_event = None
        self.show_result("Fail")

    def start_timer(self, *args):
        if not self.is_active:
            return
        print("Restarting auth flow...")
        self._show_panel("fingerprint_box")
        self.start_fingerprint_scan()

    def show_result(self, *args):
        if not self.is_active:
            return

        result = args[0] if args else "Fail"
        print(f"Showing result: {result}")

        if result == "Pass":
            app = MDApp.get_running_app()
            if not app.session.is_authenticated:
                candidate = getattr(app.session, 'candidate_user', None)
                if candidate:
                    print("Debug: Starting session from manual Pass")
                    app.session.start(candidate)

            self._show_panel("result_box_pass")
            self._schedule_once(lambda dt: setattr(self.manager, "current", "breathing"), 1)
        else:
            self._show_panel("result_box_fail")
            self.failed_attempts += 1
            print(f"Failed attempts: {self.failed_attempts}")

            if self.failed_attempts >= 3:
                print("Max attempts reached. Going home.")
                self._schedule_once(self.go_home, 4)
            else:
                self._schedule_once(self.start_timer, 4)

    # ── UI panel helpers ──────────────────────────────────────
    def _show_panel(self, panel_id):
        """Show one panel, hide all others in the right column."""
        panels = ["fingerprint_box", "result_box_pass", "result_box_fail", "device_error_box"]
        for pid in panels:
            if pid in self.ids:
                visible = (pid == panel_id)
                self.ids[pid].opacity = 1 if visible else 0
                self.ids[pid].disabled = not visible

    def _show_device_error(self, message):
        """Show the device error panel with a message."""
        print(f"[Authing] Device error: {message}")
        self._show_panel("device_error_box")
        if "device_error_label" in self.ids:
            self.ids.device_error_label.text = message

    def retry_device(self):
        """User pressed Retry on device error panel."""
        if not self.is_active:
            return
        print("[Authing] Retrying device check...")
        if not check_fingerprint_device():
            self._show_device_error(
                "ไม่พบเครื่องสแกนลายนิ้วมือ\nFingerprint scanner not found"
            )
            return
        self._show_panel("fingerprint_box")
        self.start_fingerprint_scan()

    def go_home(self, dt=None):
        if self.is_active:
            self.manager.current = "home"

    def go_home_from_error(self):
        """Called from device_error_box Home button."""
        self.go_home()

    def on_leave(self):
        self.is_active = False

        # Cancel scan timeout guard
        if self._scan_timeout_event:
            Clock.unschedule(self._scan_timeout_event)
            self._scan_timeout_event = None

        # Cancel all scheduled events
        for event in self._scheduled_events:
            Clock.unschedule(event)
        self._scheduled_events = []

        # Reset all panels to hidden
        panels = ["fingerprint_box", "result_box_pass", "result_box_fail", "device_error_box"]
        for pid in panels:
            if pid in self.ids:
                self.ids[pid].opacity = 0
                self.ids[pid].disabled = True