
import json

def get_user_by_id(employee_id):
    """
    Mock API to get user details by Employee ID.
    Returns a dict with user info if found, else None.
    """
    # Mock data for testing
    if employee_id == "123456":
         # Use the sample finger data from the original authing.py for testing success
        finger_data = "ndQ5w65P0//V9Qlh8JGN9xL/oiYwkBcJAhmCrh+1eC5XlQ6aPVed9MWf0L9EgQqZU6M0IwDC29RoW0T3fXFpvfeMpJzw6DOxLTpoeFahM20Da7pEzashVTzz2P850JuCA0P22s1KBnanZdv4T9encQOHf05BO3EAR1XKLXikYTUbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fBstyeuvDV9gKmT/R/Bs+XwbLcnrrw1fYCpk/0fwbPl8Gy3J668NX2AqZP9H8Gz5fA=="
        return {
            "user_id": "123456",
            "name": "Test User",
            "finger_data": finger_data
        }
    return None


def send_test_result(data):
    # TODO: Connect to actual API
    # requests.post("http://api.server.com/result", json=data)
    print(f"Mock sending data to API: {data}")

