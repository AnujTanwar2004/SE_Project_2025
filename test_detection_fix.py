"""
Test script to verify that the detector only flags screen capture related processes
"""

import psutil
from core.detector import ScreenCaptureDetector

def test_process_detection():
    """Test that normal processes are not flagged"""
    detector = ScreenCaptureDetector()
    
    print("Testing Detection Logic Fix")
    print("=" * 60)
    print()
    
    # Get a sample of running processes
    test_cases = []
    
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            proc_info = proc.info
            if proc_info['name']:
                test_cases.append(proc_info)
            if len(test_cases) >= 20:  # Test first 20 processes
                break
        except:
            continue
    
    print(f"Testing {len(test_cases)} running processes:")
    print()
    
    relevant_count = 0
    safe_count = 0
    risky_count = 0
    
    for proc_info in test_cases:
        risk_level = detector._assess_process_risk(proc_info)
        name = proc_info.get('name', 'Unknown')
        
        if risk_level != "NOT_RELEVANT":
            relevant_count += 1
            status_symbol = "✓" if risk_level == "SAFE" else "⚠" if risk_level in ["LOW", "MEDIUM"] else "✗"
            print(f"{status_symbol} {name:30} -> {risk_level}")
            
            if risk_level == "SAFE":
                safe_count += 1
            elif risk_level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
                risky_count += 1
        else:
            # Process is not relevant to screen capture monitoring
            pass
    
    print()
    print("=" * 60)
    print(f"Results:")
    print(f"  Total processes checked: {len(test_cases)}")
    print(f"  Screen capture relevant: {relevant_count}")
    print(f"  - Safe (whitelisted): {safe_count}")
    print(f"  - Risky/Unknown: {risky_count}")
    print(f"  Not relevant (ignored): {len(test_cases) - relevant_count}")
    print()
    
    if relevant_count == 0:
        print("✓ PASS: No false positives - normal processes are ignored")
    else:
        print(f"ℹ INFO: {relevant_count} screen capture related processes detected")
    
    print()
    print("Testing specific scenarios:")
    print("-" * 60)
    
    # Test case 1: Normal application (should be NOT_RELEVANT)
    test_spotify = {
        'name': 'Spotify.exe',
        'pid': 12345,
        'exe': 'C:\\Users\\User\\AppData\\Roaming\\Spotify\\Spotify.exe',
        'cmdline': ['Spotify.exe']
    }
    risk = detector._assess_process_risk(test_spotify)
    print(f"Spotify.exe: {risk} {'✓ PASS' if risk in ['NOT_RELEVANT', 'SAFE'] else '✗ FAIL'}")
    
    # Test case 2: Known screen capture tool (should be SAFE)
    test_snip = {
        'name': 'SnippingTool.exe',
        'pid': 12346,
        'exe': 'C:\\Windows\\System32\\SnippingTool.exe',
        'cmdline': ['SnippingTool.exe']
    }
    risk = detector._assess_process_risk(test_snip)
    print(f"SnippingTool.exe: {risk} {'✓ PASS' if risk == 'SAFE' else '✗ FAIL'}")
    
    # Test case 3: Suspicious process (should be HIGH/CRITICAL)
    test_suspicious = {
        'name': 'unknown.exe',
        'pid': 12347,
        'exe': 'C:\\Temp\\unknown.exe',
        'cmdline': ['unknown.exe', '--screenshot', '--capture']
    }
    risk = detector._assess_process_risk(test_suspicious)
    print(f"unknown.exe with --screenshot: {risk} {'✓ PASS' if risk in ['HIGH', 'CRITICAL'] else '✗ FAIL'}")
    
    # Test case 4: Chrome browser (should be NOT_RELEVANT or SAFE)
    test_chrome = {
        'name': 'chrome.exe',
        'pid': 12348,
        'exe': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        'cmdline': ['chrome.exe', 'https://www.google.com']
    }
    risk = detector._assess_process_risk(test_chrome)
    print(f"chrome.exe: {risk} {'✓ PASS' if risk in ['NOT_RELEVANT', 'SAFE'] else '✗ FAIL'}")
    
    print()
    print("=" * 60)
    print("Test Complete!")

if __name__ == "__main__":
    test_process_detection()
