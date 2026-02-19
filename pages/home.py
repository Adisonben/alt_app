from kivymd.uix.screen import MDScreen

class Home(MDScreen):
    def go_next(self):
        self.manager.current = "employeeid"