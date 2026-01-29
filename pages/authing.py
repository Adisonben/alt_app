from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.clock import Clock
from functions.fingerprint import scan_fingerprint, compare_fingerprints

# def scan_fingerprint(callback):
#     # จำลอง hardware ใช้เวลา 2 วิ
#     Clock.schedule_once(lambda dt: callback(True), 2)


class Authing(MDScreen):
    failed_attempts = 0

    def on_enter(self):
        self.failed_attempts = 0
        print(f"Start fingerprint scan... (Attempt {self.failed_attempts + 1})")
        scan_fingerprint(self.on_fingerprint_done)

    def on_fingerprint_done(self, success, b64_data):
        if success:
            print(f"Fingerprint scan successful. Data length: {len(b64_data)}")
            print(f"Raw data: {b64_data}")
            # The data is now a Base64 string
            finger_data = "ndQ5w65P0//V9Qlh8JGN9xL/oiYwkBcJAhmCrh+1eC5XlQ6aPVed9MWf0L9EgQqZU6M0IwDC29RoW0T3fXFpvfeMpJzw6DOxLTpoeFahM20Da7pEzashVTzz2P850JuCA0P22s1KBnanZdv4T9encQOHf05BO3EAR1XKLXikYTUbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fA=="
            print("Comparing with stored finger data...")
            compare_fingerprints(b64_data, finger_data, self.on_match_done)
        else:
            print("Fingerprint scan failed or timed out.")
            self.show_result("Fail")

    def on_match_done(self, match, msg):
        print(f"Match Result: {match} ({msg})")
        if match:
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
    
    def start_timer(self, *args):
        # show fingerprint box
        self.ids.fingerprint_box.opacity = 1
        self.ids.fingerprint_box.disabled = False

        # hide result box
        self.ids.result_box_pass.opacity = 0
        self.ids.result_box_pass.disabled = True
        self.ids.result_box_fail.opacity = 0
        self.ids.result_box_fail.disabled = True
        
        print("Restarting fingerprint scan...")
        scan_fingerprint(self.on_fingerprint_done)

        # wait 10 seconds then call show_auth_result
        # Clock.schedule_once(self.show_result, 5)

    def show_result(self, *args):
        # hide fingerprint box
        self.ids.fingerprint_box.opacity = 0
        self.ids.fingerprint_box.disabled = True
        print(args[0])
        if args and args[0] == "Pass":
            self.ids.result_box_pass.opacity = 1
            self.ids.result_box_pass.disabled = False
            Clock.schedule_once(lambda dt: setattr(self.manager, "current", "breathing"), 1)
        else:
            self.ids.result_box_fail.opacity = 1
            self.ids.result_box_fail.disabled = False
            
            self.failed_attempts += 1
            print(f"Failed attempts: {self.failed_attempts}")
            
            if self.failed_attempts >= 3:
                print("Max attempts reached. Going home.")
                Clock.schedule_once(self.go_home, 4)
            else:
                Clock.schedule_once(self.start_timer, 4)

    def go_home(self, dt):
        # Clear state handles by on_leave automatically or we can force it here
        self.manager.current = "home"
        # # show result box
        # self.ids.result_box.opacity = 1
        # self.ids.result_box.disabled = False

    def on_leave(self):
        # Reset the state when leaving the screen
        # Hide result boxes
        self.ids.result_box_pass.opacity = 0
        self.ids.result_box_pass.disabled = True
        self.ids.result_box_fail.opacity = 0
        self.ids.result_box_fail.disabled = True
        
        # Show fingerprint box (initial state)
        self.ids.fingerprint_box.opacity = 1
        self.ids.fingerprint_box.disabled = False