
import subprocess
import sys
import os

def print_result(user_name, status, value):
    """
    Calls the external printer script using subprocess to avoid USB conflicting
    with the main application process.
    """
    try:
        # Resolve the path to the script
        # Assuming this file is in functions/ and script is in bin/
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(base_dir, 'bin', 'printer_script.py')
        
        # Prepare the command
        # python bin/printer_script.py "User Name" "PASS" "0.00"
        # Use sys.executable to ensure we use the same python interpreter
        cmd = [sys.executable, script_path, str(user_name), str(status), str(value)]
        
        print(f"Executing printer command: {cmd}")
        
        # Run subprocess
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True,
            timeout=15 # Timeout to prevent hanging
        )
        
        if result.returncode == 0:
            print(f"Print success: {result.stdout}")
            return True
        else:
            print(f"Print script failed with code {result.returncode}")
            print(f"Stderr: {result.stderr}")
            print(f"Stdout: {result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        print("Print script timed out")
        return False
    except Exception as e:
        print(f"Error calling print subprocess: {e}")
        return False