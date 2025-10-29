"""Quick test to verify whitelist is working correctly"""
from core.detector import ScreenCaptureDetector

detector = ScreenCaptureDetector()

# Test cases
test_cases = [
    ('SnippingTool.exe', 'SAFE'),
    ('Code.exe', 'SAFE'),
    ('chrome.exe', 'SAFE'),
    ('powershell.exe', 'SAFE'),
    ('malware.exe', 'SAFE'),  # Unknown process should be SAFE
    ('keylogger.exe', 'CRITICAL'),
    ('stealer.exe', 'CRITICAL'),
]

print("Testing Whitelist/Blacklist Detection:")
print("=" * 60)

all_passed = True
for name, expected in test_cases:
    result = detector._assess_process_risk({
        'name': name,
        'exe': f'C:\\Test\\{name}',
        'cmdline': []
    })
    
    status = "✓ PASS" if result == expected else "✗ FAIL"
    if result != expected:
        all_passed = False
    
    print(f"{status} | {name:25} | Expected: {expected:10} | Got: {result}")

print("=" * 60)
if all_passed:
    print("✓ All tests passed!")
else:
    print("✗ Some tests failed!")
