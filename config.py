import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "")

KIOSK_MODE = os.getenv("KIOSK_MODE", "both").lower()
if KIOSK_MODE not in ("normal", "free", "both"):
    KIOSK_MODE = "both"
