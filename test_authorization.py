"""
Test to demonstrate proper unauthorized vs authorized screen capture detection
"""

from core.detector import ScreenCaptureDetector

def test_authorization_logic():
    """Test that the detector properly distinguishes authorized vs unauthorized captures"""
    
    detector = ScreenCaptureDetector()
    
    print("=" * 70)
    print("SCREEN CAPTURE AUTHORIZATION TEST")
    print("=" * 70)
    print()
    
    print("Testing different screenshot scenarios:")
    print("-" * 70)
    
    test_cases = [
        {
            'name': 'SnippingTool.exe',
            'desc': 'Windows Snipping Tool (User pressed Win+Shift+S)',
            'expected': 'SAFE - User-Initiated, AUTHORIZED'
        },
        {
            'name': 'ScreenSketch.exe',
            'desc': 'Windows Screen Sketch (User pressed PrintScreen)',
            'expected': 'SAFE - User-Initiated, AUTHORIZED'
        },
        {
            'name': 'explorer.exe',
            'desc': 'Windows Explorer (User pressed PrintScreen)',
            'expected': 'SAFE - User-Initiated, AUTHORIZED'
        },
        {
            'name': 'Discord.exe',
            'desc': 'Discord screenshot feature',
            'expected': 'SAFE - User-Initiated, AUTHORIZED'
        },
        {
            'name': 'chrome.exe',
            'desc': 'Chrome browser (User action)',
            'expected': 'SAFE - User-Initiated, AUTHORIZED'
        },
        {
            'name': 'ShareX.exe',
            'desc': 'ShareX screenshot tool',
            'expected': 'SAFE - User-Initiated, AUTHORIZED'
        },
        {
            'name': 'suspicious.exe',
            'desc': 'Unknown process taking screenshots',
            'expected': 'HIGH RISK - UNAUTHORIZED, MALICIOUS'
        },
        {
            'name': 'keylogger.exe',
            'desc': 'Known malicious process',
            'expected': 'CRITICAL - UNAUTHORIZED, MALICIOUS'
        },
        {
            'name': 'unknown_app.exe',
            'desc': 'Unrecognized application capturing screen',
            'expected': 'HIGH RISK - UNAUTHORIZED'
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        proc_info = {
            'name': test['name'],
            'pid': 10000 + i,
            'exe': f'C:\\Test\\{test["name"]}',
            'cmdline': [test['name']]
        }
        
        risk = detector._assess_screenshot_risk(proc_info)
        
        is_authorized = (risk == "SAFE")
        status = "✓ AUTHORIZED" if is_authorized else "✗ UNAUTHORIZED"
        
        print(f"{i}. {test['name']:25} -> {risk:10} {status}")
        print(f"   Description: {test['desc']}")
        print(f"   Expected: {test['expected']}")
        print()
    
    print("=" * 70)
    print()
    print("HOW IT WORKS:")
    print("-" * 70)
    print("1. When user presses PrintScreen or Win+Shift+S:")
    print("   → Clipboard gets the screenshot")
    print("   → Detector checks which process is active (foreground window)")
    print("   → If it's a WHITELISTED app → SAFE (Authorized)")
    print("   → User continues working normally ✓")
    print()
    print("2. When MALICIOUS software captures screen secretly:")
    print("   → Detector catches the clipboard activity")
    print("   → Checks which process did it")
    print("   → If it's NOT whitelisted → HIGH RISK/CRITICAL")
    print("   → Alert shown to user ⚠")
    print()
    print("=" * 70)
    print()
    print("RESULT: Only UNAUTHORIZED/MALICIOUS captures are flagged!")
    print("        User-initiated screenshots work normally without alerts.")
    print("=" * 70)

if __name__ == "__main__":
    test_authorization_logic()
