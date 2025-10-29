"""
Modern GUI for Screen Capture Detection System
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
from typing import List
import csv
import os

from core.detector import ScreenCaptureDetector, ScreenCaptureEvent
from utils.logger import get_logger

class ScreenCaptureDetectorApp:
    """Main application window"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture Detection System - Advanced Security Monitor")
        self.root.geometry("1400x800")
        self.root.minsize(1000, 600)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass
        
        # Initialize detector
        self.detector = ScreenCaptureDetector()
        self.detector.register_callback(self.on_detection)
        
        self.logger = get_logger(__name__)
        
        # Status variables
        self.is_monitoring = False
        self.status_var = tk.StringVar(value="● Stopped")
        self.detection_count = tk.StringVar(value="0")
        self.high_risk_count = tk.StringVar(value="0")
        self.medium_risk_count = tk.StringVar(value="0")
        
        # Setup UI
        self._setup_styles()
        self._create_widgets()
        
        # Update loop
        self.root.after(1000, self._update_stats)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        
        # Configure treeview
        style.configure("Treeview", 
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       rowheight=25)
        style.configure("Treeview.Heading",
                       background="#1e1e1e",
                       foreground="white",
                       relief="flat")
        style.map("Treeview", background=[('selected', '#0078d4')])
        
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top bar with title and controls
        self._create_top_bar(main_frame)
        
        # Statistics panel
        self._create_stats_panel(main_frame)
        
        # Main content area with tabs
        self._create_tabbed_content(main_frame)
        
        # Bottom status bar
        self._create_status_bar(main_frame)
    
    def _create_top_bar(self, parent):
        """Create top control bar"""
        top_frame = tk.Frame(parent, bg="#1e1e1e", height=80)
        top_frame.pack(fill=tk.X, pady=(0, 5))
        top_frame.pack_propagate(False)
        
        # Title
        title = tk.Label(top_frame, 
                        text="🛡️ Screen Capture Detection System",
                        font=("Segoe UI", 20, "bold"),
                        bg="#1e1e1e",
                        fg="white")
        title.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Control buttons
        button_frame = tk.Frame(top_frame, bg="#1e1e1e")
        button_frame.pack(side=tk.RIGHT, padx=20)
        
        self.start_btn = tk.Button(button_frame,
                                   text="▶ Start Monitoring",
                                   command=self.start_monitoring,
                                   bg="#28a745",
                                   fg="white",
                                   font=("Segoe UI", 11, "bold"),
                                   padx=20,
                                   pady=10,
                                   relief=tk.FLAT,
                                   cursor="hand2")
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(button_frame,
                                  text="⏸ Stop Monitoring",
                                  command=self.stop_monitoring,
                                  bg="#dc3545",
                                  fg="white",
                                  font=("Segoe UI", 11, "bold"),
                                  padx=20,
                                  pady=10,
                                  relief=tk.FLAT,
                                  cursor="hand2",
                                  state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = tk.Button(button_frame,
                             text="🗑️ Clear Logs",
                             command=self.clear_logs,
                             bg="#6c757d",
                             fg="white",
                             font=("Segoe UI", 11, "bold"),
                             padx=20,
                             pady=10,
                             relief=tk.FLAT,
                             cursor="hand2")
        clear_btn.grid(row=0, column=2, padx=5)
    
    def _create_stats_panel(self, parent):
        """Create statistics panel"""
        stats_frame = tk.Frame(parent, bg="#2b2b2b")
        stats_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Statistics cards
        stats = [
            ("Total Detections", self.detection_count, "#0078d4"),
            ("High Risk", self.high_risk_count, "#dc3545"),
            ("Medium Risk", self.medium_risk_count, "#ffc107"),
            ("Status", self.status_var, "#28a745")
        ]
        
        for label, var, color in stats:
            card = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=2)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            tk.Label(card,
                    text=label,
                    font=("Segoe UI", 10),
                    bg=color,
                    fg="white").pack(pady=(10, 5))
            
            tk.Label(card,
                    textvariable=var,
                    font=("Segoe UI", 24, "bold"),
                    bg=color,
                    fg="white").pack(pady=(0, 10))
    
    def _create_tabbed_content(self, parent):
        """Create tabbed content area"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Real-time monitoring tab
        self.monitoring_tab = self._create_monitoring_tab(notebook)
        notebook.add(self.monitoring_tab, text="🔴 Real-Time Monitoring")
        
        # Event log tab
        self.log_tab = self._create_log_tab(notebook)
        notebook.add(self.log_tab, text="📋 Event Logs")
        
        # Settings tab
        self.settings_tab = self._create_settings_tab(notebook)
        notebook.add(self.settings_tab, text="⚙️ Settings")
        
        # About tab
        self.about_tab = self._create_about_tab(notebook)
        notebook.add(self.about_tab, text="ℹ️ About")
    
    def _create_monitoring_tab(self, parent):
        """Create real-time monitoring tab"""
        frame = ttk.Frame(parent)
        
        # Live feed label
        header = tk.Label(frame,
                         text="Live Detection Feed",
                         font=("Segoe UI", 14, "bold"),
                         bg="white")
        header.pack(pady=10)
        
        # Treeview for live detections
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.live_tree = ttk.Treeview(tree_frame,
                                      columns=("Time", "Process", "PID", "Method", "Risk", "Window"),
                                      show="headings",
                                      yscrollcommand=vsb.set,
                                      xscrollcommand=hsb.set)
        
        vsb.config(command=self.live_tree.yview)
        hsb.config(command=self.live_tree.xview)
        
        # Configure columns
        columns = {
            "Time": 150,
            "Process": 200,
            "PID": 80,
            "Method": 150,
            "Risk": 100,
            "Window": 300
        }
        
        for col, width in columns.items():
            self.live_tree.heading(col, text=col, anchor=tk.W)
            self.live_tree.column(col, width=width, anchor=tk.W)
        
        self.live_tree.pack(fill=tk.BOTH, expand=True)
        
        # Export button
        export_btn = tk.Button(frame,
                              text="💾 Export to CSV",
                              command=self.export_to_csv,
                              bg="#17a2b8",
                              fg="white",
                              font=("Segoe UI", 10, "bold"),
                              padx=15,
                              pady=8,
                              relief=tk.FLAT,
                              cursor="hand2")
        export_btn.pack(pady=10)
        
        return frame
    
    def _create_log_tab(self, parent):
        """Create event log tab"""
        frame = ttk.Frame(parent)
        
        # Log text widget
        log_frame = ttk.Frame(frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(log_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame,
                               bg="#1e1e1e",
                               fg="#00ff00",
                               font=("Consolas", 10),
                               yscrollcommand=vsb.set,
                               wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        vsb.config(command=self.log_text.yview)
        
        # Initial log message
        self.log_text.insert(tk.END, "[SYSTEM] Screen Capture Detection System initialized\n")
        self.log_text.insert(tk.END, "[SYSTEM] Waiting for monitoring to start...\n\n")
        
        return frame
    
    def _create_settings_tab(self, parent):
        """Create settings tab"""
        frame = ttk.Frame(parent)
        
        settings_container = tk.Frame(frame, bg="white")
        settings_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(settings_container,
                text="Detection Settings",
                font=("Segoe UI", 16, "bold"),
                bg="white").pack(pady=10)
        
        # Alert settings
        alert_frame = tk.LabelFrame(settings_container,
                                   text="Alert Configuration",
                                   font=("Segoe UI", 11, "bold"),
                                   bg="white",
                                   padx=20,
                                   pady=20)
        alert_frame.pack(fill=tk.X, pady=10)
        
        self.alert_high_risk = tk.BooleanVar(value=True)
        tk.Checkbutton(alert_frame,
                      text="Alert on High Risk detections",
                      variable=self.alert_high_risk,
                      bg="white",
                      font=("Segoe UI", 10)).pack(anchor=tk.W, pady=5)
        
        self.alert_medium_risk = tk.BooleanVar(value=False)
        tk.Checkbutton(alert_frame,
                      text="Alert on Medium Risk detections",
                      variable=self.alert_medium_risk,
                      bg="white",
                      font=("Segoe UI", 10)).pack(anchor=tk.W, pady=5)
        
        self.auto_block = tk.BooleanVar(value=False)
        tk.Checkbutton(alert_frame,
                      text="Automatically block Critical threats (Requires Admin)",
                      variable=self.auto_block,
                      bg="white",
                      font=("Segoe UI", 10)).pack(anchor=tk.W, pady=5)
        
        # Monitoring settings
        monitor_frame = tk.LabelFrame(settings_container,
                                     text="Monitoring Configuration",
                                     font=("Segoe UI", 11, "bold"),
                                     bg="white",
                                     padx=20,
                                     pady=20)
        monitor_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(monitor_frame,
                text="Scan Interval (seconds):",
                bg="white",
                font=("Segoe UI", 10)).pack(anchor=tk.W, pady=5)
        
        self.scan_interval = tk.Scale(monitor_frame,
                                     from_=1,
                                     to=10,
                                     orient=tk.HORIZONTAL,
                                     bg="white")
        self.scan_interval.set(1)
        self.scan_interval.pack(fill=tk.X, pady=5)
        
        return frame
    
    def _create_about_tab(self, parent):
        """Create about tab"""
        frame = ttk.Frame(parent)
        
        about_container = tk.Frame(frame, bg="white")
        about_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        tk.Label(about_container,
                text="Screen Capture Detection System",
                font=("Segoe UI", 20, "bold"),
                bg="white").pack(pady=10)
        
        tk.Label(about_container,
                text="Version 1.0.0",
                font=("Segoe UI", 12),
                bg="white",
                fg="#666").pack(pady=5)
        
        info_text = """
        Advanced Security Software for Windows Environments
        
        This software monitors and detects malicious screen capture activities
        on Windows systems, helping prevent data exfiltration and privacy breaches.
        
        Features:
        • Real-time process monitoring
        • Windows API call detection
        • Risk assessment and classification
        • Comprehensive logging and reporting
        • User-friendly GUI with live monitoring
        
        Developed for: Windows 10/11, Windows Server 2019/2022
        
        © 2025 Security Research Team
        """
        
        tk.Label(about_container,
                text=info_text,
                font=("Segoe UI", 10),
                bg="white",
                justify=tk.LEFT).pack(pady=20)
        
        return frame
    
    def _create_status_bar(self, parent):
        """Create bottom status bar"""
        status_bar = tk.Frame(parent, bg="#1e1e1e", height=30)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(status_bar,
                                     text="Ready",
                                     bg="#1e1e1e",
                                     fg="white",
                                     font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        time_label = tk.Label(status_bar,
                             text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             bg="#1e1e1e",
                             fg="white",
                             font=("Segoe UI", 9))
        time_label.pack(side=tk.RIGHT, padx=10)
        
        # Update time
        def update_time():
            time_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.root.after(1000, update_time)
        
        update_time()
    
    def start_monitoring(self):
        """Start monitoring"""
        if not self.is_monitoring:
            self.detector.start()
            self.is_monitoring = True
            self.status_var.set("● Running")
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Monitoring active - Scanning for threats...")
            self.log_message("[SYSTEM] Monitoring started")
            self.logger.info("Monitoring started by user")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        if self.is_monitoring:
            self.detector.stop()
            self.is_monitoring = False
            self.status_var.set("● Stopped")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Monitoring stopped")
            self.log_message("[SYSTEM] Monitoring stopped")
            self.logger.info("Monitoring stopped by user")
    
    def clear_logs(self):
        """Clear all logs"""
        if messagebox.askyesno("Clear Logs", "Are you sure you want to clear all detection logs?"):
            self.detector.clear_events()
            for item in self.live_tree.get_children():
                self.live_tree.delete(item)
            self.log_text.delete(1.0, tk.END)
            self.log_message("[SYSTEM] Logs cleared")
            messagebox.showinfo("Success", "Logs cleared successfully")
    
    def on_detection(self, event: ScreenCaptureEvent):
        """Handle detection event"""
        # Add to treeview (thread-safe)
        self.root.after(0, self._add_to_tree, event)
        
        # Log message
        self.root.after(0, self.log_message, 
                       f"[{event.risk_level}] {event.process_name} (PID: {event.pid}) - {event.method}")
        
        # Show alert if configured
        if event.risk_level == "CRITICAL" or \
           (event.risk_level == "HIGH" and self.alert_high_risk.get()) or \
           (event.risk_level == "MEDIUM" and self.alert_medium_risk.get()):
            self.root.after(0, self._show_alert, event)
    
    def _add_to_tree(self, event: ScreenCaptureEvent):
        """Add detection to treeview"""
        values = (
            event.timestamp.strftime("%H:%M:%S"),
            event.process_name,
            event.pid,
            event.method,
            event.risk_level,
            event.window_title[:50]
        )
        
        item = self.live_tree.insert("", 0, values=values)
        
        # Color code by risk level
        if event.risk_level == "CRITICAL":
            self.live_tree.item(item, tags=('critical',))
            self.live_tree.tag_configure('critical', background='#dc3545')
        elif event.risk_level == "HIGH":
            self.live_tree.item(item, tags=('high',))
            self.live_tree.tag_configure('high', background='#fd7e14')
        elif event.risk_level == "MEDIUM":
            self.live_tree.item(item, tags=('medium',))
            self.live_tree.tag_configure('medium', background='#ffc107')
    
    def _show_alert(self, event: ScreenCaptureEvent):
        """Show alert popup"""
        messagebox.showwarning(
            "Screen Capture Detected",
            f"Risk Level: {event.risk_level}\n"
            f"Process: {event.process_name} (PID: {event.pid})\n"
            f"Method: {event.method}\n"
            f"Window: {event.window_title}\n\n"
            f"Action: Logged and monitored"
        )
    
    def log_message(self, message: str):
        """Add message to log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def _update_stats(self):
        """Update statistics display"""
        if self.is_monitoring:
            stats = self.detector.get_statistics()
            self.detection_count.set(str(stats['total_detections']))
            self.high_risk_count.set(str(stats['high_risk']))
            self.medium_risk_count.set(str(stats['medium_risk']))
        
        self.root.after(1000, self._update_stats)
    
    def export_to_csv(self):
        """Export detections to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"detections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                events = self.detector.get_recent_events(limit=10000)
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Timestamp', 'Process', 'PID', 'Method', 'Risk Level', 
                                   'Window Title', 'Executable Path'])
                    
                    for event in events:
                        writer.writerow([
                            event.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                            event.process_name,
                            event.pid,
                            event.method,
                            event.risk_level,
                            event.window_title,
                            event.executable_path
                        ])
                
                messagebox.showinfo("Export Successful", f"Detections exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Error exporting data:\n{str(e)}")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_monitoring:
            if messagebox.askokcancel("Quit", "Monitoring is active. Stop monitoring and quit?"):
                self.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
