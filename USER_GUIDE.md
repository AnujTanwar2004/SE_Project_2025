# Screen Capture Detection System - User Guide

## Quick Start Guide

### First Time Setup

1. **Install Python** (if not already installed)

   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Minimum version: Python 3.8

2. **Install Dependencies**

   - Double-click `install.bat`
   - OR open PowerShell and run: `pip install -r requirements.txt`

3. **Run the Application**
   - Double-click `run.bat`
   - OR open PowerShell and run: `python main.py`

---

## Main Interface Overview

### Dashboard (Top Bar)

- **Title**: Shows application name
- **Start Monitoring**: Begin real-time detection
- **Stop Monitoring**: Pause detection
- **Clear Logs**: Remove all recorded events

### Statistics Panel

Four cards displaying:

1. **Total Detections**: All detected events
2. **High Risk**: Critical and high-risk threats
3. **Medium Risk**: Medium-risk detections
4. **Status**: Current monitoring state

---

## Tabs Explained

### 1. 🔴 Real-Time Monitoring

**Purpose**: View live screen capture detection events

**Columns**:

- **Time**: When the event was detected
- **Process**: Name of the process performing screen capture
- **PID**: Process ID (useful for advanced users)
- **Method**: Detection method used
- **Risk**: CRITICAL, HIGH, MEDIUM, or LOW
- **Window**: Title of the window being captured

**Color Coding**:

- 🔴 Red: CRITICAL risk
- 🟠 Orange: HIGH risk
- 🟡 Yellow: MEDIUM risk
- ⚪ White: LOW risk

**Actions**:

- Click "💾 Export to CSV" to save detections to a file

---

### 2. 📋 Event Logs

**Purpose**: View detailed text logs of all system activities

**Information Logged**:

- System start/stop events
- Detection events with full details
- Errors and warnings
- User actions

**Format**: Console-style logging with timestamps

---

### 3. ⚙️ Settings

**Alert Configuration**:

- ✅ **Alert on High Risk**: Show popup for high-risk detections
- ✅ **Alert on Medium Risk**: Show popup for medium-risk detections
- ✅ **Auto-block Critical Threats**: Automatically terminate malicious processes (requires admin)

**Monitoring Configuration**:

- **Scan Interval**: How often to check for threats (1-10 seconds)
  - Lower = faster detection, higher CPU usage
  - Higher = slower detection, lower CPU usage
  - Recommended: 1-2 seconds

---

### 4. ℹ️ About

**Information Displayed**:

- Software version
- Feature list
- System requirements
- Copyright information

---

## Common Use Cases

### Scenario 1: Monitor for Data Theft

**Goal**: Detect if malware is capturing sensitive documents

**Steps**:

1. Start the application
2. Click "Start Monitoring"
3. Open sensitive documents
4. If any suspicious process tries to capture, you'll see an alert
5. Check the "Real-Time Monitoring" tab for details

### Scenario 2: Verify Legitimate Software

**Goal**: Ensure your screen recording tool is recognized

**Steps**:

1. Start monitoring
2. Use your screen recording tool (e.g., OBS, ShareX)
3. Check if it appears in detections
4. If it's marked as HIGH risk but it's legitimate:
   - Note the process name
   - Add it to the whitelist (see Configuration section)

### Scenario 3: Security Audit

**Goal**: Review all screen capture activity over time

**Steps**:

1. Run monitoring for a day/week
2. Go to "Real-Time Monitoring"
3. Click "Export to CSV"
4. Open the CSV in Excel
5. Analyze patterns and suspicious activity

---

## Understanding Risk Levels

### CRITICAL ⚠️

- **Definition**: Known malware patterns detected
- **Examples**: Processes with "keylogger", "stealer", "trojan" in name
- **Action**: Immediately investigate, consider terminating process
- **Auto-blocked**: If enabled in settings

### HIGH ⚠️

- **Definition**: Suspicious screen capture by unknown process
- **Examples**: Unfamiliar .exe files capturing screen
- **Action**: Investigate process origin and purpose

### MEDIUM ⚠️

- **Definition**: Potentially legitimate but unusual activity
- **Examples**: Python scripts, development tools
- **Action**: Verify if you initiated the activity

### LOW ℹ️

- **Definition**: Whitelisted apps with minor anomalies
- **Examples**: Legitimate tools behaving slightly unusual
- **Action**: Generally safe, monitor for patterns

---

## Troubleshooting

### Problem: No detections appearing

**Solutions**:

1. Ensure monitoring is started (green "Running" status)
2. Try using a screen capture tool (Windows Snipping Tool)
3. Check if the tool is whitelisted
4. Review logs tab for errors

### Problem: Too many false positives

**Solutions**:

1. Increase scan interval in Settings
2. Add trusted applications to whitelist
3. Disable "Alert on Medium Risk"

### Problem: Application won't start

**Solutions**:

1. Verify Python installation: `python --version`
2. Reinstall dependencies: Run `install.bat`
3. Check logs folder for error details
4. Run as Administrator

### Problem: High CPU usage

**Solutions**:

1. Increase scan interval to 3-5 seconds
2. Close other resource-intensive applications
3. Ensure you have latest Python version

---

## Advanced Features

### Exporting Data for Analysis

1. Click "Export to CSV"
2. Open in Excel or Python/R
3. Filter by risk level
4. Create pivot tables for patterns
5. Generate charts for reporting

### Running as Windows Service

For always-on protection:

1. Install NSSM (Non-Sucking Service Manager)
2. Use NSSM to create a service pointing to `main.py`
3. Configure service to start automatically

### Integrating with SIEM

1. Configure logs to output JSON format
2. Use log forwarding to send to Splunk/ELK
3. Create dashboards and alerts

---

## Best Practices

1. **Run as Administrator**: For full functionality
2. **Regular Log Reviews**: Check weekly for patterns
3. **Keep Whitelist Updated**: Add legitimate tools
4. **Export Regularly**: Maintain historical records
5. **Combine with AV**: Use alongside antivirus software
6. **Document Incidents**: Note unusual detections
7. **Test Periodically**: Verify detection is working

---

## Keyboard Shortcuts

Currently not implemented, but planned for future:

- `Ctrl+S`: Start monitoring
- `Ctrl+T`: Stop monitoring
- `Ctrl+E`: Export to CSV
- `Ctrl+C`: Clear logs

---

## Privacy & Security

### What Data is Collected?

- Process names and IDs
- Window titles
- Executable paths
- Timestamps of capture attempts
- Detection methods and risk assessments

### Where is Data Stored?

- Locally in `logs/` folder
- CSV exports in user-selected location
- No cloud storage or external transmission

### Who Can Access the Data?

- Only users with access to the computer
- Administrator accounts have full access
- Standard users can only see their session data

---

## FAQ

**Q: Will this slow down my computer?**
A: Minimal impact (<5% CPU) with default settings.

**Q: Can it detect all screen capture malware?**
A: Detects most common methods, but sophisticated malware may evade detection.

**Q: Is it legal to use this software?**
A: Yes, for monitoring your own systems or with proper authorization.

**Q: Does it work on Windows 7?**
A: Not officially supported. Use Windows 10/11 for best results.

**Q: Can I customize the whitelist?**
A: Yes, edit `core/detector.py` and modify the WHITELIST set.

**Q: Will it block legitimate screen capture?**
A: No, it only monitors and alerts. Blocking is optional and requires admin rights.

---

## Support & Updates

For help:

- Check README.md for detailed documentation
- Review log files in `logs/` folder
- Open an issue on the project repository

For updates:

- Check the project repository regularly
- Subscribe to release notifications
- Follow security advisories

---

**Last Updated**: 12 October 2025
**Version**: 1.0.0
