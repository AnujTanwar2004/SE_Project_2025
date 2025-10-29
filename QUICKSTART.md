# 🚀 QUICK START GUIDE

## Screen Capture Detection System

### ⚡ 3-Step Installation

#### Step 1: Install Dependencies

Open PowerShell in the project directory:

```powershell
pip install -r requirements.txt
```

Or double-click: **`install.bat`**

---

#### Step 2: Run the Application

```powershell
python main.py
```

Or double-click: **`run.bat`**

---

#### Step 3: Start Monitoring

1. Click **"▶ Start Monitoring"** button
2. Watch for real-time detections
3. Check the different tabs for logs and settings

---

## ✅ System Requirements

- ✔️ Windows 10 or 11
- ✔️ Python 3.8 or higher
- ✔️ 4 GB RAM minimum
- ✔️ Administrator rights (recommended)

---

## 📦 What's Included

```
screen_capture_detector/
│
├── 📄 main.py              ← Run this to start
├── 📄 requirements.txt     ← Dependencies list
├── 📄 README.md           ← Full documentation
├── 📄 USER_GUIDE.md       ← Detailed user guide
├── 📄 SRS_DOCUMENT.md     ← Technical specifications
├── 📄 config.py           ← Configuration settings
├── 📄 test_system.py      ← Test the installation
│
├── 📂 core/               ← Detection engine
│   └── detector.py
│
├── 📂 gui/                ← User interface
│   └── main_window.py
│
├── 📂 utils/              ← Utilities
│   └── logger.py
│
├── 📂 logs/               ← Auto-generated logs
│
├── 🪟 install.bat         ← Windows installer
└── 🪟 run.bat             ← Quick launcher
```

---

## 🎯 Main Features

### 🔴 Real-Time Monitoring

- Detect screen capture attempts as they happen
- Color-coded risk levels (Critical, High, Medium, Low)
- Process details with PID and window titles

### 📊 Statistics Dashboard

- Total detections counter
- High/Medium risk breakdowns
- Current monitoring status

### 📋 Comprehensive Logging

- Timestamped event logs
- Export to CSV for analysis
- Console-style text logs

### ⚙️ Configurable Settings

- Adjust scan intervals (1-10 seconds)
- Enable/disable alerts by risk level
- Auto-block critical threats (requires admin)

---

## 🧪 Test Your Installation

Run the test script to verify everything works:

```powershell
python test_system.py
```

This will check:

- ✔️ Python modules installed
- ✔️ Detector initialization
- ✔️ GUI components
- ✔️ Logging system
- ✔️ Process monitoring

---

## 🎨 GUI Overview

### Top Bar

- **Title**: Application name and icon
- **Start/Stop Buttons**: Control monitoring
- **Clear Logs**: Remove all events

### Statistics Cards (4 panels)

1. **Total Detections** - All detected events
2. **High Risk** - Critical and high-risk threats
3. **Medium Risk** - Moderate threats
4. **Status** - Current state (Running/Stopped)

### Tabs (4 sections)

1. **🔴 Real-Time Monitoring** - Live detection feed
2. **📋 Event Logs** - Detailed text logs
3. **⚙️ Settings** - Configure behavior
4. **ℹ️ About** - Application info

---

## 🚨 Common Issues & Solutions

### Issue: "Module not found"

**Solution:**

```powershell
pip install --upgrade -r requirements.txt
```

### Issue: "Access Denied" errors

**Solution:** Run PowerShell as Administrator

### Issue: High CPU usage

**Solution:** Increase scan interval in Settings (2-3 seconds)

### Issue: False positives

**Solution:** Add trusted apps to whitelist in `core/detector.py`

---

## 🔒 Security Notes

- **Run as Administrator** for full functionality
- All logs stored **locally** (no cloud uploads)
- Whitelist legitimate apps to reduce alerts
- Combine with antivirus for best protection

---

## 📚 Need More Help?

- 📖 **Full Documentation**: See `README.md`
- 👤 **User Guide**: See `USER_GUIDE.md`
- 🔬 **Technical Details**: See `SRS_DOCUMENT.md`
- 🐛 **Report Issues**: Contact your administrator

---

## 🎓 How It Works

The system monitors Windows processes every second looking for:

- ❌ Known malware patterns (keylogger, stealer)
- ⚠️ Suspicious command-line arguments (screenshot, capture)
- 🔍 Processes not in whitelist performing screen operations
- 📸 Clipboard monitoring for captured images

### Risk Levels Explained

| Level    | Icon | Meaning                         | Action                  |
| -------- | ---- | ------------------------------- | ----------------------- |
| CRITICAL | 🔴   | Known malware                   | Immediate investigation |
| HIGH     | 🟠   | Suspicious activity             | Review within 30 min    |
| MEDIUM   | 🟡   | Unusual but possibly legitimate | Review daily            |
| LOW      | ⚪   | Minor anomaly                   | Monitor for patterns    |

---

## 💡 Pro Tips

1. **Start monitoring when handling sensitive data**
2. **Review logs daily for patterns**
3. **Export to CSV for Excel analysis**
4. **Add your trusted tools to whitelist**
5. **Adjust scan interval based on workload**

---

## 📞 Support

For issues or questions:

- Check the logs folder for error details
- Run `test_system.py` to diagnose problems
- Review documentation files

---

**Version 1.0.0** | 18 October 2025 | Made with 🛡️ for Windows Security

---

## 🏁 Ready to Start?

1. ✅ Dependencies installed? → Run `install.bat`
2. ✅ Tested the system? → Run `test_system.py`
3. ✅ Ready to monitor? → Run `run.bat` or `python main.py`
4. ✅ Click **"▶ Start Monitoring"** and you're protected! 🎉

**Stay secure!** 🛡️
