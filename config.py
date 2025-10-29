"""
Configuration file for Screen Capture Detection System
Modify these settings to customize behavior
"""

# Detection Settings
DETECTION_CONFIG = {
    # Scan interval in seconds (1-10)
    'scan_interval': 1,
    
    # Enable/disable detection methods
    'enable_process_monitoring': True,
    'enable_api_monitoring': True,
    'enable_clipboard_monitoring': True,
    
    # Alert settings
    'alert_on_critical': True,
    'alert_on_high': True,
    'alert_on_medium': False,
    'alert_on_low': False,
    
    # Auto-block settings (requires admin)
    'auto_block_critical': False,
    'auto_block_high': False,
    
    # Logging settings
    'log_to_file': True,
    'log_to_console': True,
    'max_log_size_mb': 100,
    'log_retention_days': 30
}

# Whitelist - Trusted applications that won't be flagged
WHITELIST = {
    # Windows built-in tools
    'SnippingTool.exe',
    'ScreenSketch.exe',
    'mspaint.exe',
    'explorer.exe',
    'dwm.exe',
    
    # Popular legitimate screen capture tools
    'ShareX.exe',
    'Greenshot.exe',
    'LightShot.exe',
    'PicPick.exe',
    'ScreenToGif.exe',
    
    # Video recording/streaming
    'obs64.exe',
    'obs32.exe',
    'OBS.exe',
    'XSplit.Broadcaster.exe',
    'Streamlabs OBS.exe',
    
    # Communication tools
    'Discord.exe',
    'Skype.exe',
    'TEAMS.exe',
    'zoom.exe',
    'Slack.exe',
    
    # Remote desktop
    'mstsc.exe',
    'TeamViewer.exe',
    'AnyDesk.exe',
    
    # Development tools
    'Code.exe',  # VS Code
    'devenv.exe',  # Visual Studio
    'pycharm64.exe',
    
    # Add your trusted applications here
}

# Blacklist - Known malicious patterns
BLACKLIST_PATTERNS = {
    'keylogger',
    'stealer',
    'trojan',
    'backdoor',
    'rat',
    'screenlogger',
    'spyware',
    'grabber',
    'dumper',
    'logger',
    'spy',
    'hack',
    'crack',
    'inject',
}

# Suspicious keywords in command-line arguments
SUSPICIOUS_CMDLINE_KEYWORDS = {
    'screenshot',
    'screencap',
    'capture',
    'printscreen',
    'getdc',
    'bitblt',
    'screengrab',
    'snapshot',
    'imageCapture',
    'screenrecord',
}

# API calls to monitor (for future implementation)
MONITORED_APIS = {
    'BitBlt',
    'StretchBlt',
    'GetDC',
    'GetWindowDC',
    'CreateCompatibleBitmap',
    'CreateCompatibleDC',
    'PrintWindow',
    'GetDesktopWindow',
}

# GUI Settings
GUI_CONFIG = {
    'theme': 'dark',  # 'dark' or 'light'
    'window_width': 1400,
    'window_height': 800,
    'font_family': 'Segoe UI',
    'font_size': 10,
    'auto_refresh_interval': 1000,  # milliseconds
}

# Export Settings
EXPORT_CONFIG = {
    'default_format': 'csv',  # 'csv', 'json', 'xml'
    'include_headers': True,
    'timestamp_format': '%Y-%m-%d %H:%M:%S',
}

# Advanced Settings (for developers)
ADVANCED_CONFIG = {
    'max_events_in_memory': 10000,
    'cleanup_old_events': True,
    'enable_debug_mode': False,
    'verbose_logging': False,
}
