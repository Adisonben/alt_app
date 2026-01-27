from kivymd.uix.screen import MDScreen
from kivy.animation import Animation
from kivy.clock import Clock
from functions.fingerprint import scan_fingerprint

# def scan_fingerprint(callback):
#     # จำลอง hardware ใช้เวลา 2 วิ
#     Clock.schedule_once(lambda dt: callback(True), 2)


class Authing(MDScreen):
    def on_enter(self):
        print("Start fingerprint scan...")
        scan_fingerprint(self.on_fingerprint_done)

    def on_fingerprint_done(self, success):
        if success:
            self.manager.current = "breathing"
        else:
            self.manager.current = "home"



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
            Clock.schedule_once(self.start_timer, 4)
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