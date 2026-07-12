import os
import time
from PIL import ImageGrab

# Dynamically resolve paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

def take_screenshot():
    print("=" * 50)
    print("       AUTOMATIC SCREENSHOT CAPTURE")
    print("=" * 50)
    
    # Ensure the screenshots directory exists
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    print("[*] Get ready! Taking a screenshot in 5 seconds...")
    print("[*] Arrange your VS Code terminal and graphs now!")
    
    # 5-second countdown timer
    for i in range(5, 0, -1):
        print(f"    Snap in {i}...")
        time.sleep(1)
        
    print("\n[*] SNAP! Capturing screen...")
    
    # Capture the entire screen
    screenshot = ImageGrab.grab()
    
    # Save the screenshot to the required folder
    file_path = os.path.join(SCREENSHOTS_DIR, "output_screenshot.png")
    screenshot.save(file_path)
    
    print(f"[+] Success! Screenshot saved to:\n    -> {file_path}")

if __name__ == "__main__":
    take_screenshot()
    