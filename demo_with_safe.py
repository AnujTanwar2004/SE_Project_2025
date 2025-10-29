"""
Demo with Safe Process Logging Enabled
Shows both risky and safe screen capture tools
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.detector import ScreenCaptureDetector, ScreenCaptureEvent

def demo_with_safe_logging():
    """Run demonstration with safe process logging enabled"""
    print("=" * 70)
    print("SCREEN CAPTURE DETECTOR - WITH SAFE PROCESS LOGGING")
    print("=" * 70)
    print()
    
    # Initialize detector WITH safe process logging enabled
    detector = ScreenCaptureDetector(log_safe_processes=True)
    
    print("Initializing detector with SAFE process logging enabled...")
    
    # Register callback
    def on_detection(event: ScreenCaptureEvent):
        icon = "✅" if event.risk_level == "SAFE" else "🚨"
        print(f"\n{icon} DETECTION!")
        print(f"   Process: {event.process_name}")
        print(f"   PID: {event.pid}")
        print(f"   Risk Level: {event.risk_level}")
        print(f"   Time: {event.timestamp.strftime('%H:%M:%S')}")
        if event.risk_level == "SAFE":
            print(f"   ℹ️  This is a whitelisted/legitimate tool")
        print()
    
    detector.register_callback(on_detection)
    
    print("✓ Detector initialized")
    print(f"  Whitelist: {len(detector.WHITELIST)} entries")
    print(f"  Safe logging: ENABLED")
    print()
    
    print("Starting monitoring for 10 seconds...")
    print("Try these to see different detections:")
    print("  • Open Snipping Tool → Should show as SAFE")
    print("  • Run unknown .exe → Should show as risky")
    print()
    
    detector.start()
    
    # Monitor for 10 seconds
    for i in range(10, 0, -1):
        print(f"\rTime remaining: {i} seconds...", end="", flush=True)
        time.sleep(1)
    
    print("\n")
    detector.stop()
    
    # Show statistics
    stats = detector.get_statistics()
    events = detector.get_recent_events()
    
    print("=" * 70)
    print("DETECTION SUMMARY")
    print("=" * 70)
    print(f"Total Detections: {stats['total_detections']}")
    print(f"  ✅ Safe (Whitelisted): {stats.get('safe_logged', 0)}")
    print(f"  🔴 High Risk: {stats['high_risk']}")
    print(f"  🟡 Medium Risk: {stats['medium_risk']}")
    print(f"  ⚪ Low Risk: {stats['low_risk']}")
    print()
    
    if events:
        print("Recent Events:")
        print("-" * 70)
        for event in events[-10:]:  # Show last 10
            icon = "✅" if event.risk_level == "SAFE" else "🚨"
            print(f"{icon} {event.timestamp.strftime('%H:%M:%S')} - "
                  f"{event.process_name} - {event.risk_level}")
        print()
    else:
        print("No screen capture activity detected.")
        print()
    
    print("=" * 70)
    print()
    print("Note: SAFE detections are legitimate screen capture tools")
    print("that are on the whitelist (SnippingTool, ShareX, OBS, etc.)")
    print()

if __name__ == "__main__":
    try:
        demo_with_safe_logging()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
    
    input("Press Enter to exit...")
