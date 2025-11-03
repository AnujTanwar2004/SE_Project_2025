"""
Core Unauthorized Screen Capture Detection Engine
Monitors clipboard for screenshot events and identifies whether they are:
- AUTHORIZED: User-initiated (PrintScreen, Snipping Tool, whitelisted apps) - No alert
- UNAUTHORIZED: Malicious/unknown processes capturing screen - Alert shown
"""

import threading
import time
import psutil
import win32api
import win32con
import win32gui
import win32process
from datetime import datetime
from typing import Dict, List, Callable, Optional
import ctypes
from ctypes import wintypes
import logging

# Windows API constants
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

class ScreenCaptureEvent:
    """Represents a detected screen capture event"""
    def __init__(self, process_name: str, pid: int, method: str, 
                 risk_level: str, timestamp: datetime = None):
        self.process_name = process_name
        self.pid = pid
        self.method = method
        self.risk_level = risk_level  # LOW, MEDIUM, HIGH, CRITICAL
        self.timestamp = timestamp or datetime.now()
        self.window_title = ""
        self.executable_path = ""
        
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'process_name': self.process_name,
            'pid': self.pid,
            'method': self.method,
            'risk_level': self.risk_level,
            'window_title': self.window_title,
            'executable_path': self.executable_path
        }


class ScreenCaptureDetector:
    """
    Main detector class for monitoring UNAUTHORIZED screen capture activities
    
    How it works:
    1. Monitors Windows clipboard for screenshot events (actual captures)
    2. Identifies which process took the screenshot
    3. Checks if process is in WHITELIST (authorized/legitimate)
    4. ONLY flags unauthorized/malicious captures
    5. User screenshots with PrintScreen, Snipping Tool etc. work normally (no alerts)
    """
    
    # Known legitimate/authorized screen capture tools and applications
    # These are ALLOWED and will NOT be flagged as threats
    WHITELIST = {
        # Windows built-in screenshot tools
        'SnippingTool.exe', 'ScreenSketch.exe', 'explorer.exe', 'mspaint.exe',
        'dwm.exe', 'csrss.exe', 'winlogon.exe',  # Windows system processes
        
        # Professional screen capture/recording tools
        'ShareX.exe', 'Greenshot.exe', 'obs64.exe', 'obs32.exe', 
        'OBS Studio.exe', 'Streamlabs OBS.exe', 'Camtasia.exe',
        
        # Communication apps with screen share
        'Discord.exe', 'TEAMS.exe', 'Slack.exe', 'Zoom.exe', 'Skype.exe',
        'msteams.exe', 'Teams.exe',
        
        # Browsers (for web-based screenshots)
        'chrome.exe', 'msedge.exe', 'msedgewebview2.exe', 'firefox.exe',
        'brave.exe', 'opera.exe', 'iexplore.exe',
        
        # Development tools
        'Code.exe', 'devenv.exe', 'idea64.exe', 'pycharm64.exe',
        'VisualStudio.exe', 'sublime_text.exe',
        
        # System tools
        'powershell.exe', 'cmd.exe', 'conhost.exe', 'WindowsTerminal.exe',
        'python.exe', 'pythonw.exe', 'javaw.exe', 'java.exe',
        
        # Graphics/Media tools
        'NVIDIA Web Helper.exe', 'nvcontainer.exe', 'GeForceExperience.exe',
        'Photoshop.exe', 'GIMP.exe', 'paint.net.exe',
        
        # Common applications
        'Spotify.exe', 'notepad.exe', 'Calculator.exe', 'SystemSettings.exe',
        'notepad++.exe', 'vlc.exe', 'iTunes.exe', 'Steam.exe'
    }
    
    # Known malicious patterns
    BLACKLIST = {
        'keylogger', 'stealer', 'trojan', 'backdoor', 'rat',
        'screenlogger', 'spyware', 'grabber'
    }
    
    def __init__(self, log_safe_processes=False):
        self.running = False
        self.monitoring_thread = None
        self.callbacks: List[Callable] = []
        self.detected_events: List[ScreenCaptureEvent] = []
        self.monitored_processes: Dict[int, str] = {}
        self.logger = logging.getLogger(__name__)
        self.log_safe_processes = log_safe_processes  # New option to log whitelisted apps
        
        # Detection statistics
        self.stats = {
            'total_detections': 0,
            'high_risk': 0,
            'medium_risk': 0,
            'low_risk': 0,
            'safe_logged': 0,
            'blocked': 0
        }
        
    def start(self):
        """Start the detection engine"""
        if not self.running:
            self.running = True
            self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitoring_thread.start()
            self.logger.info("Screen Capture Detector started")
    
    def stop(self):
        """Stop the detection engine"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        self.logger.info("Screen Capture Detector stopped")
    
    def register_callback(self, callback: Callable):
        """Register a callback for detection events"""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, event: ScreenCaptureEvent):
        """Notify all registered callbacks of a detection event"""
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Error in callback: {e}")
    
    def _monitor_loop(self):
        """Main monitoring loop - monitors ACTUAL screen capture activity"""
        self.logger.info("Monitoring loop started - Tracking clipboard and active processes")
        
        # Initialize clipboard tracking
        self.last_clipboard_sequence = None
        self.clipboard_check_count = 0
        
        while self.running:
            try:
                # PRIMARY: Monitor clipboard for NEW screenshots
                self._detect_clipboard_screenshot()
                
                # SECONDARY: Monitor for screen capture tool launches (only when actually used)
                self._check_active_capture_tools()
                
                time.sleep(0.5)  # Check twice per second for responsiveness
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(2)
    
    def _check_running_processes(self):
        """Legacy method - now using clipboard and active tool detection instead"""
        # This method is deprecated in favor of _detect_clipboard_screenshot
        # and _check_active_capture_tools which detect ACTUAL capture events
        pass
    
    def _old_process_scanner(self):
        """OLD BROKEN METHOD - DO NOT USE"""
        # This was scanning ALL processes which was wrong
        # Keeping for reference only
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    proc_info = proc.info
                    pid = proc_info['pid']
                    name = proc_info['name']
                    
                    # Skip system processes
                    if pid in [0, 4] or not name:
                        continue
                    
                    # Skip already monitored processes
                    if pid in self.monitored_processes:
                        continue
                    
                    # Check for screen capture indicators
                    risk_level = self._assess_process_risk(proc_info)
                    
                    # Skip processes that are not related to screen capture
                    if risk_level == "NOT_RELEVANT":
                        continue
                    
                    # Log all screen capture tools if enabled, or only risky ones
                    should_log = (risk_level != "SAFE") or (risk_level == "SAFE" and self.log_safe_processes)
                    
                    if should_log:
                        event = ScreenCaptureEvent(
                            process_name=name,
                            pid=pid,
                            method="Process Monitoring",
                            risk_level=risk_level
                        )
                        
                        try:
                            event.executable_path = proc_info.get('exe', 'Unknown')
                        except:
                            event.executable_path = 'Access Denied'
                        
                        # Get window title if available
                        event.window_title = self._get_window_title_by_pid(pid)
                        
                        self._record_detection(event)
                        self.monitored_processes[pid] = name
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error checking processes: {e}")
    
    def _assess_process_risk(self, proc_info: Dict) -> str:
        """Assess the risk level of a process"""
        name = proc_info.get('name', '')
        name_lower = name.lower()
        exe_path = proc_info.get('exe')
        exe = exe_path.lower() if exe_path else ''
        cmdline_list = proc_info.get('cmdline', [])
        if cmdline_list is None:
            cmdline_list = []
        cmdline = ' '.join(cmdline_list).lower() if isinstance(cmdline_list, list) else str(cmdline_list).lower()
        
        # First, check if this process has ANY screen capture indicators
        # If no indicators, it's not a screen capture tool at all
        screen_capture_indicators = [
            'screenshot', 'screencap', 'capture', 'printscreen', 'print screen',
            'getdc', 'bitblt', 'screengrab', 'snapshot', 'snip', 'clip',
            'record', 'obs', 'share', 'streaming', 'broadcast'
        ]
        
        # Check if process name suggests screen capture functionality
        has_capture_indicator = any(indicator in name_lower for indicator in screen_capture_indicators)
        has_cmdline_indicator = any(indicator in cmdline for indicator in screen_capture_indicators)
        has_path_indicator = any(indicator in exe for indicator in screen_capture_indicators)
        
        # If no screen capture indicators at all, skip this process (not relevant)
        if not (has_capture_indicator or has_cmdline_indicator or has_path_indicator):
            return "NOT_RELEVANT"
        
        # Now assess risk for processes that DO have screen capture indicators
        
        # Check whitelist (case-insensitive exact match)
        if any(name_lower == white.lower() for white in self.WHITELIST):
            return "SAFE"
        
        # Check blacklist patterns
        if any(black in name_lower or black in exe or black in cmdline 
               for black in self.BLACKLIST):
            return "CRITICAL"
        
        # Unknown process with screen capture activity - HIGH risk
        if has_cmdline_indicator or has_path_indicator:
            return "HIGH"
        
        # Process name suggests screen capture but not confirmed - MEDIUM risk
        if has_capture_indicator:
            return "MEDIUM"
        
        return "LOW"
    
    def _detect_clipboard_screenshot(self):
        """Detect when a screenshot is taken and placed in clipboard"""
        try:
            import win32clipboard
            
            try:
                win32clipboard.OpenClipboard()
                
                # Get clipboard sequence number (changes when clipboard content changes)
                try:
                    sequence_number = win32clipboard.GetClipboardSequenceNumber()
                except:
                    sequence_number = None
                
                # Check if clipboard has changed
                if self.last_clipboard_sequence is not None and sequence_number is not None:
                    if sequence_number != self.last_clipboard_sequence:
                        # Clipboard changed - check if it's an image
                        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_DIB) or \
                           win32clipboard.IsClipboardFormatAvailable(win32con.CF_BITMAP):
                            # New image detected in clipboard - likely a screenshot!
                            self._handle_screenshot_detection()
                
                self.last_clipboard_sequence = sequence_number
                win32clipboard.CloseClipboard()
                
            except Exception as e:
                # Clipboard might be in use by another process
                try:
                    win32clipboard.CloseClipboard()
                except:
                    pass
                    
        except Exception as e:
            self.logger.debug(f"Clipboard check error: {e}")
    
    def _handle_screenshot_detection(self):
        """Handle detected screenshot event - identify which process took it"""
        try:
            # Get the foreground window (most likely source of screenshot)
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                window_title = win32gui.GetWindowText(hwnd)
                
                # Get process information
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                    exe_path = process.exe()
                    
                    # Assess risk
                    proc_info = {
                        'name': process_name,
                        'pid': pid,
                        'exe': exe_path,
                        'cmdline': process.cmdline()
                    }
                    
                    risk_level = self._assess_screenshot_risk(proc_info)
                    
                    # ONLY log if it's NOT SAFE (i.e., suspicious/unauthorized)
                    # Do NOT flag legitimate user-initiated screenshots
                    if risk_level != "SAFE":
                        # This is an UNAUTHORIZED screen capture - log it!
                        event = ScreenCaptureEvent(
                            process_name=process_name,
                            pid=pid,
                            method="Unauthorized Screen Capture Detected",
                            risk_level=risk_level
                        )
                        event.window_title = window_title
                        event.executable_path = exe_path
                        
                        self._record_detection(event)
                    else:
                        # Safe/authorized screenshot - optionally log if enabled
                        if self.log_safe_processes:
                            event = ScreenCaptureEvent(
                                process_name=process_name,
                                pid=pid,
                                method="Authorized Screen Capture (User-Initiated)",
                                risk_level="SAFE"
                            )
                            event.window_title = window_title
                            event.executable_path = exe_path
                            self._record_detection(event)
                    
                except psutil.NoSuchProcess:
                    pass
                    
        except Exception as e:
            self.logger.error(f"Error handling screenshot detection: {e}")
    
    def _assess_screenshot_risk(self, proc_info: Dict) -> str:
        """Assess risk when a screenshot is detected"""
        name = proc_info.get('name', '').lower()
        
        # Check if it's a whitelisted tool
        if any(name == white.lower() for white in self.WHITELIST):
            return "SAFE"
        
        # Check blacklist
        if any(black in name for black in self.BLACKLIST):
            return "CRITICAL"
        
        # Unknown process taking screenshots
        return "HIGH"
    
    def _check_active_capture_tools(self):
        """Check for screen capture tools that are currently active"""
        # Only check for processes with visible windows that might be capturing
        try:
            def callback(hwnd, results):
                if win32gui.IsWindowVisible(hwnd):
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    title = win32gui.GetWindowText(hwnd)
                    
                    # Look for screen capture keywords in window titles
                    capture_keywords = ['snip', 'screenshot', 'capture', 'screen record']
                    if title and any(keyword in title.lower() for keyword in capture_keywords):
                        results.append((pid, title))
                return True
            
            results = []
            win32gui.EnumWindows(callback, results)
            
            # Process any found capture tools
            for pid, title in results:
                if pid not in self.monitored_processes:
                    try:
                        process = psutil.Process(pid)
                        proc_info = {
                            'name': process.name(),
                            'pid': pid,
                            'exe': process.exe(),
                            'cmdline': process.cmdline()
                        }
                        
                        risk_level = self._assess_screenshot_risk(proc_info)
                        
                        if risk_level != "SAFE" or self.log_safe_processes:
                            event = ScreenCaptureEvent(
                                process_name=proc_info['name'],
                                pid=pid,
                                method="Active Screen Capture Tool",
                                risk_level=risk_level
                            )
                            event.window_title = title
                            event.executable_path = proc_info['exe']
                            
                            self._record_detection(event)
                            self.monitored_processes[pid] = proc_info['name']
                            
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                        
        except Exception as e:
            self.logger.debug(f"Error checking active capture tools: {e}")
    
    def _get_window_title_by_pid(self, pid: int) -> str:
        """Get window title for a given process ID"""
        try:
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        title = win32gui.GetWindowText(hwnd)
                        if title:
                            windows.append(title)
                return True
            
            windows = []
            win32gui.EnumWindows(callback, windows)
            return windows[0] if windows else "No Window Title"
        except:
            return "Unknown"
    
    def _record_detection(self, event: ScreenCaptureEvent):
        """Record a detection event"""
        self.detected_events.append(event)
        self.stats['total_detections'] += 1
        
        if event.risk_level == "CRITICAL":
            self.stats['high_risk'] += 1
        elif event.risk_level == "HIGH":
            self.stats['high_risk'] += 1
        elif event.risk_level == "MEDIUM":
            self.stats['medium_risk'] += 1
        elif event.risk_level == "SAFE":
            self.stats['safe_logged'] += 1
        else:
            self.stats['low_risk'] += 1
        
        log_level = logging.INFO if event.risk_level == "SAFE" else logging.WARNING
        self.logger.log(log_level, f"Screen capture detected: {event.process_name} (PID: {event.pid}) - Risk: {event.risk_level}")
        self._notify_callbacks(event)
    
    def get_recent_events(self, limit: int = 100) -> List[ScreenCaptureEvent]:
        """Get recent detection events"""
        return self.detected_events[-limit:]
    
    def get_statistics(self) -> Dict:
        """Get detection statistics"""
        return self.stats.copy()
    
    def clear_events(self):
        """Clear all recorded events"""
        self.detected_events.clear()
        self.monitored_processes.clear()
        self.logger.info("Detection events cleared")
