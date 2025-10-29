"""
Simple demonstration script showing the detector in action
Run this to see a quick demo of the detection capabilities
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def demo_detection():
    """Run a simple demonstration"""
    print("=" * 70)
    print("SCREEN CAPTURE DETECTOR - DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Import after path is set
    from core.detector import ScreenCaptureDetector, ScreenCaptureEvent
    
    print("Initializing detector...")
    detector = ScreenCaptureDetector()
    
    # Register a demo callback
    def on_detection(event: ScreenCaptureEvent):
        print(f"\n🚨 DETECTION ALERT!")
        print(f"   Process: {event.process_name}")
        print(f"   PID: {event.pid}")
        print(f"   Risk Level: {event.risk_level}")
        print(f"   Method: {event.method}")
        print(f"   Time: {event.timestamp.strftime('%H:%M:%S')}")
        print(f"   Window: {event.window_title}")
        print()
    
    detector.register_callback(on_detection)
    
    print("✓ Detector initialized")
    print(f"  Whitelist: {len(detector.WHITELIST)} entries")
    print(f"  Blacklist: {len(detector.BLACKLIST)} patterns")
    print()
    
    print("Starting monitoring for 10 seconds...")
    print("(Open a screen capture tool like Snipping Tool to test)")
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
    print(f"High Risk: {stats['high_risk']}")
    print(f"Medium Risk: {stats['medium_risk']}")
    print(f"Low Risk: {stats['low_risk']}")
    print()
    
    if events:
        print("Detected Events:")
        print("-" * 70)
        for event in events[-5:]:  # Show last 5
            print(f"• {event.timestamp.strftime('%H:%M:%S')} - "
                  f"{event.process_name} - {event.risk_level}")
        print()
    else:
        print("No suspicious screen capture activity detected.")
        print("(This is normal if you didn't use any screen capture tools)")
        print()
    
    print("=" * 70)
    print("Demo completed!")
    print()
    print("To run the full application with GUI:")
    print("  python main.py")
    print("=" * 70)

if __name__ == "__main__":
    try:
        demo_detection()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except ImportError as e:
        print(f"\nError: Missing dependency - {e}")
        print("\nPlease install requirements:")
        print("  pip install -r requirements.txt")
    except Exception as e:
        print(f"\nError during demo: {e}")
        print("\nPlease check that all dependencies are installed.")
    
    input("\nPress Enter to exit...")
