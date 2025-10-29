"""
Core Screen Capture Detection Engine
Monitors Windows API calls and process behaviors to detect screen capture activities
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
    """Main detector class for monitoring screen capture activities"""
    
    # Known legitimate screen capture tools
    WHITELIST = {
        'SnippingTool.exe', 'ScreenSketch.exe', 'ShareX.exe', 
        'Greenshot.exe', 'mspaint.exe', 'explorer.exe',
        'obs64.exe', 'obs32.exe', 'Discord.exe', 'TEAMS.exe',
        'Code.exe', 'chrome.exe', 'msedge.exe', 'msedgewebview2.exe',
        'firefox.exe', 'powershell.exe', 'cmd.exe', 'conhost.exe',
        'WindowsTerminal.exe', 'nvcontainer.exe', 'NVIDIA Web Helper.exe',
        'WMIRegistrationService.exe', 'python.exe', 'pythonw.exe'
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
        """Main monitoring loop"""
        self.logger.info("Monitoring loop started")
        
        while self.running:
            try:
                # Monitor for screen capture processes
                self._check_running_processes()
                
                # Monitor for suspicious API usage patterns
                self._check_api_patterns()
                
                # Monitor clipboard for captured images
                self._check_clipboard()
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(2)
    
    def _check_running_processes(self):
        """Check running processes for screen capture indicators"""
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
        
        # Check whitelist (case-insensitive exact match)
        if any(name_lower == white.lower() for white in self.WHITELIST):
            return "SAFE"
        
        # Check blacklist patterns
        if any(black in name_lower or black in exe or black in cmdline 
               for black in self.BLACKLIST):
            return "CRITICAL"
        
        # Check for suspicious indicators
        suspicious_indicators = [
            'screenshot', 'screencap', 'capture', 'printscreen',
            'getdc', 'bitblt', 'screengrab', 'snapshot'
        ]
        
        if any(indicator in cmdline for indicator in suspicious_indicators):
            return "HIGH"
        
        # Check for hidden windows with screen capture capabilities
        if 'python' in name_lower and ('screenshot' in cmdline or 'capture' in cmdline):
            return "MEDIUM"
        
        return "SAFE"
    
    def _check_api_patterns(self):
        """Monitor for suspicious Windows API usage patterns"""
        # This would require kernel-mode driver or API hooking
        # For PoC, we'll simulate detection of common APIs
        pass
    
    def _check_clipboard(self):
        """Check clipboard for captured screen images"""
        try:
            import win32clipboard
            from PIL import ImageGrab
            
            # Try to detect if clipboard contains a bitmap
            try:
                win32clipboard.OpenClipboard()
                if win32clipboard.IsClipboardFormatAvailable(win32con.CF_BITMAP):
                    # Clipboard has a bitmap, could be a screenshot
                    # We'd need to track which process put it there
                    pass
                win32clipboard.CloseClipboard()
            except:
                pass
                
        except Exception as e:
            pass  # Clipboard monitoring is optional
    
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
