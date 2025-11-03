"""
Simulated Malicious Screen Capture - FOR DEMO PURPOSES ONLY
This script simulates what a malicious app might do (takes screenshot)
Use this to demonstrate detection of UNAUTHORIZED captures during presentation
"""

import sys
import time
from pathlib import Path
from PIL import ImageGrab
import io
import win32clipboard
from PIL import Image
import win32con

sys.path.insert(0, str(Path(__file__).parent))

def simulate_malicious_capture():
    """
    Simulates a malicious screenshot capture
    This will be detected as UNAUTHORIZED by the detector
    """
    print("=" * 70)
    print("🚨 SIMULATED MALICIOUS SCREEN CAPTURE")
    print("=" * 70)
    print()
    print("⚠️  WARNING: This is a DEMO simulation")
    print("    This script pretends to be an unauthorized capture tool")
    print("    Use this to demonstrate detection during presentation")
    print()
    print("Starting in 3 seconds...")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print()
    
    print("📸 Taking 'malicious' screenshot...")
    try:
        # Take screenshot
        screenshot = ImageGrab.grab()
        # Put it in clipboard
        output = io.BytesIO()
        screenshot.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]  # Remove BMP header
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        print(f"✓ Screenshot captured and copied to clipboard")
        print(f"✓ Screen size: {screenshot.size}")
        print()
        print("🎯 THIS SHOULD BE DETECTED AS:")
        print("   Risk Level: HIGH or CRITICAL")
        print("   Process: python.exe or pythonw.exe (if not whitelisted)")
        print("   Reason: Unknown process performing screen capture")
        print()
        print("💡 In your detector application:")
        print("   - Check the Real-Time Monitoring tab")
        print("   - You should see this detection appear")
        print("   - It will be marked as HIGH RISK (orange/red)")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("=" * 70)
    print("Demo simulation complete!")
    print("Check your detector app for the unauthorized detection alert.")
    print("=" * 70)

if __name__ == "__main__":
    print()
    input("⚠️  Make sure your detector app is running first!\n   Press ENTER when ready to simulate malicious capture...")
    print()
    simulate_malicious_capture()
