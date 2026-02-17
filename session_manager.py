from datetime import datetime

class KioskSession:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.user_id = None
        self.user_name = None
        self.finger_data = None
        self.is_authenticated = False
        self.alcohol_value = 0.0
        self.alcohol_status = ""   # "OK", "HIGH", or error code
        self.snapshot_path = ""
        self.start_time = None
        print("KioskSession: Reset completed.")
    
    def start(self, user_data):
        self.reset()
        self.user_id = user_data.get("user_id")
        self.user_name = user_data.get("name")
        self.finger_data = user_data.get("finger_data")
        self.is_authenticated = True
        self.start_time = datetime.now()
        print(f"KioskSession: Started for User ID {self.user_id} ({self.user_name})")
