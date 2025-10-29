# Software Requirements Specification (SRS)

# Screen Capture Detection System for Windows

**Project Title:** Malicious Screen Capture Detection System  
**Project Started:** 20/09/2025  
**Document Date:** 15/10/2025  
**Prepared by:** Security Research Team  
**Version:** 1.0

---

## Team Members and Their Roles

1. **Project Lead** - Overall architecture and coordination
2. **Security Researcher** - Threat analysis and detection algorithms
3. **Software Developer** - Core implementation and GUI development
4. **QA Engineer** - Testing and validation

---

## 1. Introduction

### 1.1 Purpose

The Screen Capture Detection System is a security monitoring software designed for Windows operating systems to detect and log malicious screen capture activities in real-time. The target audience includes:

- **Network Administrators** - Monitor endpoints for data exfiltration attempts
- **Security Teams** - Investigate and respond to screen capture threats
- **IT Departments** - Ensure compliance with data protection policies
- **End Users** - Protect sensitive information from unauthorized capture

**Objectives:**

- Detect unauthorized screen capture attempts in real-time
- Classify threats based on risk assessment
- Provide comprehensive logging and reporting
- Minimize false positives through intelligent whitelisting
- Maintain low system performance overhead

### 1.2 Scope

**Software Boundaries:**
The system focuses on endpoint protection against screen capture-based data exfiltration on Windows platforms.

**Key Functionalities:**

1. **Real-time Monitoring**

   - Continuous process monitoring
   - Windows API call detection
   - Behavioral analysis of running applications

2. **Threat Classification**

   - Risk-based categorization (CRITICAL, HIGH, MEDIUM, LOW)
   - Whitelist/blacklist management
   - Pattern matching and heuristic analysis

3. **Logging & Reporting**

   - Detailed event logging with timestamps
   - CSV export for analysis
   - Integration-ready log formats

4. **User Interface**

   - Modern GUI with dashboard
   - Real-time detection feed
   - Configuration management

5. **Alert System**
   - Configurable alert thresholds
   - Pop-up notifications for high-risk events
   - Optional auto-blocking capabilities

**Benefits:**

- Improved security posture against screen capture malware
- Prevention of data exfiltration through covert screen capture
- Compliance with data protection regulations (GDPR, HIPAA)
- Enhanced visibility into endpoint activities
- Reduced incident response time

### 1.3 Definitions, Acronyms, and Abbreviations

| Term       | Definition                                                      |
| ---------- | --------------------------------------------------------------- |
| **API**    | Application Programming Interface                               |
| **BitBlt** | Bit Block Transfer - Windows GDI function for bitmap operations |
| **CLI**    | Command-Line Interface                                          |
| **CSV**    | Comma-Separated Values                                          |
| **DC**     | Device Context (Windows graphics)                               |
| **DFD**    | Data Flow Diagram                                               |
| **GDI**    | Graphics Device Interface                                       |
| **GUI**    | Graphical User Interface                                        |
| **PID**    | Process Identifier                                              |
| **PoC**    | Proof of Concept                                                |
| **RBAC**   | Role-Based Access Control                                       |
| **SIEM**   | Security Information and Event Management                       |
| **UAC**    | User Account Control                                            |
| **WinAPI** | Windows Application Programming Interface                       |

### 1.4 References

1. **Microsoft Documentation**

   - Windows API Reference: https://docs.microsoft.com/en-us/windows/win32/
   - Process Security and Access Rights
   - Graphics Device Interface (GDI) Functions

2. **IEEE Standards**

   - IEEE 830-1998: Software Requirements Specifications

3. **Security Research**

   - MITRE ATT&CK Framework - Screen Capture (T1113)
   - OWASP Security Guidelines
   - CVE Database - Screen capture related vulnerabilities

4. **Python Libraries**

   - psutil documentation: https://psutil.readthedocs.io/
   - pywin32 documentation: https://github.com/mhammond/pywin32

5. **Security Blogs & Articles**
   - Krebs on Security - Data Exfiltration Techniques
   - Dark Reading - Screen Capture Malware Analysis
   - Malwarebytes Labs - Spyware Detection Methods

### 1.5 Overview

This document is structured into 9 main sections:

- **Section 1**: Introduction and project overview
- **Section 2**: Overall system description and context
- **Section 3**: Detailed functional requirements
- **Section 4**: External interface specifications
- **Section 5**: Non-functional requirements
- **Section 6**: Additional requirements
- **Section 7**: Implementation details
- **Section 8**: Usability considerations
- **Section 9**: Appendices and supplementary materials

---

## 2. Overall Description

### 2.1 Product Perspective

The Screen Capture Detection System operates as a standalone Windows application that integrates deeply with the Windows operating system. It is not a replacement for antivirus software but rather a complementary security layer focused specifically on screen capture activities.

**System Context:**

- Runs on Windows 10/11 and Windows Server 2019/2022
- Utilizes Windows Management Instrumentation (WMI) for process monitoring
- Interfaces with Windows Security Center
- Can integrate with enterprise SIEM solutions

**Dependencies on Windows Services:**

- **Process Creation Notifications** - To detect new processes
- **Windows Event Log** - For system-level logging
- **Windows API** - For process interrogation and control
- **User Account Control (UAC)** - For privilege management

### 2.2 Product Functions

**Core Functions:**

1. **Process Monitoring**

   - Enumerate running processes every N seconds
   - Query process metadata (name, PID, path, command-line)
   - Track process lifecycle (creation, termination)

2. **Risk Assessment**

   - Compare process names against whitelist/blacklist
   - Analyze command-line arguments for suspicious patterns
   - Evaluate executable signature and reputation
   - Calculate risk score based on multiple factors

3. **Detection & Alerting**

   - Log all detected screen capture attempts
   - Generate alerts based on risk level
   - Provide detailed forensic information
   - Optional automatic blocking of critical threats

4. **Data Management**

   - Store events in memory and disk
   - Export logs to CSV format
   - Manage log rotation and retention
   - Provide search and filter capabilities

5. **Configuration**
   - Manage whitelist/blacklist entries
   - Configure alert thresholds
   - Set scan intervals
   - Enable/disable detection methods

### 2.3 User Classes and Characteristics

| User Class               | Access Level | Responsibilities                                                  | Technical Expertise |
| ------------------------ | ------------ | ----------------------------------------------------------------- | ------------------- |
| **System Administrator** | Full         | Configure settings, manage whitelist, review logs, export reports | Advanced            |
| **Security Analyst**     | Monitor      | Analyze detections, investigate incidents, generate reports       | Intermediate        |
| **End User**             | View         | View status, acknowledge alerts                                   | Basic               |
| **IT Manager**           | Full         | Oversee deployment, compliance monitoring                         | Intermediate        |

### 2.4 Operating Environment

**Supported Platforms:**

- Windows 10 (Build 1809 or later)
- Windows 11 (All versions)
- Windows Server 2019
- Windows Server 2022

**Hardware Requirements:**

- Processor: Intel Core i3 2.0 GHz or equivalent
- RAM: 4 GB minimum, 8 GB recommended
- Storage: 100 MB for application, 1 GB for logs
- Display: 1280x720 minimum resolution

**Software Requirements:**

- Python 3.8 or higher
- .NET Framework 4.7.2 or higher
- Administrator privileges (for full functionality)

**Required Libraries:**

- psutil 5.9.6+
- pywin32 306+
- Pillow 10.1.0+
- tkinter (included with Python)

### 2.5 Design and Implementation Constraints

**Technical Constraints:**

1. **Windows-specific** - No cross-platform support
2. **Python-based** - Requires Python runtime
3. **User-mode only** - Cannot detect kernel-mode captures
4. **Performance** - Must not exceed 5% CPU usage
5. **UAC Compliance** - Must work with User Account Control enabled

**Regulatory Constraints:**

1. Must comply with data protection laws (GDPR, CCPA)
2. Should not monitor encrypted communications
3. Must respect user privacy preferences

**Development Constraints:**

1. Must use Windows API for process monitoring
2. Limited to documented Windows functions
3. Cannot use kernel drivers (user-mode only)
4. Must be compatible with Windows Defender

### 2.6 Assumptions and Dependencies

**Assumptions:**

1. Target system has Windows 10/11 installed
2. User has administrator privileges for full features
3. Python 3.8+ is installed or can be installed
4. System has internet connectivity for initial setup
5. Windows API functions remain stable across versions

**Dependencies:**

1. **Python Runtime** - Version 3.8 or higher
2. **Windows API** - Stable across supported Windows versions
3. **Process Monitoring** - psutil library compatibility
4. **GUI Framework** - tkinter availability
5. **Third-party Libraries** - pywin32, PIL

---

## 3. System Features and Requirements

### 3.1 Feature: Real-Time Process Monitoring

**Description:**  
Continuously monitor running processes to detect screen capture activities using Windows process enumeration and metadata analysis.

**Priority:** HIGH

**Functional Requirements:**

**FR3.1.1:** The system shall enumerate all running processes every configurable interval (default 1 second).

**FR3.1.2:** For each process, the system shall collect:

- Process name
- Process ID (PID)
- Executable path
- Command-line arguments
- Parent process ID
- User account
- Window title (if applicable)

**FR3.1.3:** The system shall compare each process against the whitelist database.

**FR3.1.4:** The system shall analyze process names for blacklist patterns.

**FR3.1.5:** The system shall examine command-line arguments for suspicious keywords.

**FR3.1.6:** The system shall assign a risk level (CRITICAL, HIGH, MEDIUM, LOW, SAFE) to each process.

**Inputs:**

- Windows process list (via psutil)
- Whitelist configuration
- Blacklist patterns

**Outputs:**

- Detection events
- Risk assessments
- Process metadata logs

**Processing:**

1. Query system for process list
2. For each process, extract metadata
3. Apply whitelist/blacklist rules
4. Analyze command-line for patterns
5. Calculate risk score
6. Generate event if suspicious

---

### 3.2 Feature: Screen Capture Detection

**Description:**  
Identify when a process is likely performing screen capture operations through behavior analysis and API monitoring.

**Priority:** CRITICAL

**Functional Requirements:**

**FR3.2.1:** The system shall detect processes with names containing screen capture keywords:

- "screenshot", "screencap", "capture", "printscreen", "screengrab", "snapshot"

**FR3.2.2:** The system shall monitor for processes with suspicious behavioral patterns:

- Hidden windows with active rendering
- Rapid bitmap operations
- Large memory allocations consistent with screen buffers

**FR3.2.3:** The system shall detect clipboard operations involving bitmap data.

**FR3.2.4:** The system shall correlate multiple indicators to improve detection accuracy.

**FR3.2.5:** The system shall maintain a detection confidence score for each event.

**Inputs:**

- Process behavior data
- Clipboard events
- Window states

**Outputs:**

- Screen capture detection events
- Confidence scores
- Behavioral indicators

---

### 3.3 Feature: Risk Classification

**Description:**  
Classify detected events into risk categories to prioritize security responses.

**Priority:** HIGH

**Functional Requirements:**

**FR3.3.1:** The system shall classify detections into four risk levels:

- **CRITICAL**: Known malware patterns (keylogger, stealer, trojan)
- **HIGH**: Unknown processes with screen capture indicators
- **MEDIUM**: Legitimate tools used suspiciously
- **LOW**: Whitelisted apps with minor anomalies

**FR3.3.2:** The system shall base classification on multiple factors:

- Process reputation (whitelist/blacklist status)
- Behavioral indicators
- User context
- Historical patterns

**FR3.3.3:** The system shall allow manual override of risk classifications.

**FR3.3.4:** The system shall update risk levels in real-time as new information becomes available.

**Inputs:**

- Process metadata
- Behavioral indicators
- Whitelist/blacklist databases
- User configuration

**Outputs:**

- Risk level assignment
- Justification/reasoning
- Recommended actions

---

### 3.4 Feature: Alert and Notification System

**Description:**  
Notify users and administrators of detected screen capture attempts based on configured thresholds.

**Priority:** HIGH

**Functional Requirements:**

**FR3.4.1:** The system shall display pop-up alerts for events meeting configured criteria.

**FR3.4.2:** Alerts shall include:

- Timestamp
- Process name and PID
- Risk level
- Window title
- Recommended actions

**FR3.4.3:** The system shall allow users to configure alert thresholds by risk level.

**FR3.4.4:** The system shall provide visual indicators (colors, icons) for different risk levels.

**FR3.4.5:** The system shall maintain an alert history.

**FR3.4.6:** The system shall support alert suppression for whitelisted processes.

**Inputs:**

- Detection events
- User alert preferences
- Risk classifications

**Outputs:**

- Pop-up notifications
- Visual alerts in GUI
- System tray notifications (optional)

---

### 3.5 Feature: Logging and Reporting

**Description:**  
Maintain comprehensive logs of all detection events for forensic analysis and compliance.

**Priority:** HIGH

**Functional Requirements:**

**FR3.5.1:** The system shall log every detection event with complete metadata.

**FR3.5.2:** Log entries shall include:

- ISO 8601 formatted timestamp
- Process name and PID
- Executable path
- Window title
- Risk level
- Detection method
- User account

**FR3.5.3:** The system shall write logs to both:

- File system (rotating logs)
- In-memory buffer (for GUI display)

**FR3.5.4:** The system shall support export to CSV format.

**FR3.5.5:** The system shall implement log rotation based on:

- File size (default 100 MB)
- Age (default 30 days)

**FR3.5.6:** The system shall compress archived logs.

**Inputs:**

- Detection events
- System activities
- User actions

**Outputs:**

- Log files (daily rotation)
- CSV exports
- JSON formatted logs (for SIEM integration)

---

### 3.6 Feature: Whitelist/Blacklist Management

**Description:**  
Maintain lists of known legitimate and malicious applications to reduce false positives and improve detection accuracy.

**Priority:** MEDIUM

**Functional Requirements:**

**FR3.6.1:** The system shall maintain a whitelist of trusted applications.

**FR3.6.2:** The system shall maintain a blacklist of known malicious patterns.

**FR3.6.3:** Users with admin privileges shall be able to add/remove whitelist entries.

**FR3.6.4:** The system shall ship with a default whitelist including common screen capture tools:

- Windows Snipping Tool
- Snip & Sketch
- ShareX
- Greenshot
- OBS Studio
- Discord, Teams, Zoom

**FR3.6.5:** The system shall allow wildcard patterns in whitelist/blacklist entries.

**FR3.6.6:** The system shall validate entries before adding to lists.

**Inputs:**

- User modifications
- Default configuration
- Process names

**Outputs:**

- Updated whitelist/blacklist
- Validation results

---

### 3.7 Feature: Configuration Management

**Description:**  
Provide a user-friendly interface for configuring detection parameters and system behavior.

**Priority:** MEDIUM

**Functional Requirements:**

**FR3.7.1:** The system shall provide GUI-based configuration for:

- Scan interval (1-10 seconds)
- Alert thresholds
- Auto-block settings
- Log retention policies

**FR3.7.2:** The system shall validate configuration changes before applying.

**FR3.7.3:** The system shall store configuration in a human-readable format (Python config file).

**FR3.7.4:** The system shall apply configuration changes without requiring restart.

**FR3.7.5:** The system shall provide configuration export/import functionality.

**Inputs:**

- User preferences
- Default values
- Validation rules

**Outputs:**

- Updated configuration
- Validation feedback
- Applied settings

---

## 4. External Interface Requirements

### 4.1 User Interfaces

**4.1.1 Main Dashboard**

- Window size: 1400x800 pixels (resizable, minimum 1000x600)
- Components:
  - Title bar with application name and icon
  - Control buttons (Start, Stop, Clear)
  - Statistics panel (4 cards showing metrics)
  - Tabbed interface (4 tabs)
  - Status bar with time and connection status

**4.1.2 Real-Time Monitoring Tab**

- Tabular view of detections
- Columns: Time, Process, PID, Method, Risk, Window
- Color-coding by risk level
- Sortable columns
- Export to CSV button

**4.1.3 Event Logs Tab**

- Console-style text display
- Monospace font (Consolas)
- Green text on dark background
- Auto-scroll to latest
- Search functionality (future)

**4.1.4 Settings Tab**

- Grouped settings panels
- Checkboxes for alert preferences
- Slider for scan interval
- Apply/Save buttons

**4.1.5 About Tab**

- Application name and version
- Feature summary
- Copyright information
- Contact details

**UI Requirements:**

- Must be responsive and not freeze during monitoring
- All operations must provide visual feedback
- Buttons must be clearly labeled
- Colors must be accessible (WCAG 2.1 AA compliant)

### 4.2 Hardware Interfaces

**4.2.1 Network Interface Cards (NICs)**

- Not directly interfaced
- Indirect monitoring through process network activity (future enhancement)

**4.2.2 Display Adapter**

- Required for GUI rendering
- Minimum resolution: 1280x720
- Color depth: 24-bit or higher

**4.2.3 Storage Device**

- Required for log file storage
- Minimum 1 GB free space
- Support for NTFS file system

### 4.3 Software Interfaces

**4.3.1 Windows Operating System**

- Interface: Windows API (Win32)
- Purpose: Process enumeration, window management
- Data exchanged: Process information, window titles
- Communication: Direct API calls via pywin32

**4.3.2 Python Runtime**

- Interface: Python 3.8+ interpreter
- Purpose: Application execution environment
- Data exchanged: Python bytecode, runtime data

**4.3.3 psutil Library**

- Interface: Python module API
- Purpose: Cross-platform process and system monitoring
- Functions used:
  - `psutil.process_iter()` - Enumerate processes
  - `psutil.Process()` - Query process information

**4.3.4 pywin32 Library**

- Interface: Python-wrapped Windows API
- Purpose: Windows-specific functionality
- Modules used:
  - `win32api` - General Windows API
  - `win32gui` - GUI-related functions
  - `win32process` - Process management

**4.3.5 Windows Event Log (Future)**

- Interface: Windows Event Log API
- Purpose: System-wide event logging
- Data format: Event Log XML schema

**4.3.6 SIEM Integration (Future)**

- Interface: Syslog or REST API
- Purpose: Forward events to security information systems
- Protocols: Syslog (UDP 514), HTTPS
- Data format: JSON or CEF

### 4.4 Communication Interfaces

**4.4.1 Inter-Process Communication**

- Method: Python threading
- Purpose: Communicate between detection engine and GUI
- Data: Detection events, commands

**4.4.2 File I/O**

- Protocol: Standard file operations
- Purpose: Log storage and configuration management
- Formats: CSV, JSON, plain text

**4.4.3 Network Communication (Future Enhancement)**

- Protocols: HTTPS for cloud reporting
- Purpose: Upload detection statistics
- Encryption: TLS 1.3

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

**NFR5.1.1:** The system shall use less than 5% CPU on average during monitoring.

**NFR5.1.2:** The system shall use less than 100 MB of RAM during normal operation.

**NFR5.1.3:** The system shall detect screen capture attempts within 2 seconds of occurrence.

**NFR5.1.4:** The system shall enumerate all processes in less than 500 milliseconds.

**NFR5.1.5:** The GUI shall respond to user input within 100 milliseconds.

**NFR5.1.6:** The system shall handle up to 10,000 detection events in memory without degradation.

**NFR5.1.7:** Log file I/O shall not block the detection engine.

### 5.2 Security Requirements

**NFR5.2.1:** The system shall require administrator privileges for:

- Auto-blocking processes
- Modifying system-wide settings
- Accessing logs of other users

**NFR5.2.2:** The system shall store logs with appropriate ACLs to prevent unauthorized access.

**NFR5.2.3:** The system shall not expose sensitive information in error messages.

**NFR5.2.4:** Configuration files shall be protected from unauthorized modification.

**NFR5.2.5:** The system shall validate all user inputs to prevent injection attacks.

**NFR5.2.6:** The system shall operate without requiring network access (air-gapped environments).

**NFR5.2.7:** The system itself shall not perform screen captures except for diagnostic purposes.

### 5.3 Reliability and Availability

**NFR5.3.1:** The system shall have 99.9% uptime during monitoring periods.

**NFR5.3.2:** The system shall gracefully handle exceptions without crashing.

**NFR5.3.3:** If the detection engine crashes, it shall restart automatically.

**NFR5.3.4:** The system shall maintain log integrity even during abnormal shutdown.

**NFR5.3.5:** The system shall operate continuously for at least 30 days without restart.

**NFR5.3.6:** The system shall recover from transient errors (e.g., process access denied) without stopping.

### 5.4 Maintainability

**NFR5.4.1:** The codebase shall follow PEP 8 Python style guidelines.

**NFR5.4.2:** All modules shall have docstrings explaining their purpose.

**NFR5.4.3:** Configuration shall be externalized (not hardcoded).

**NFR5.4.4:** The system shall support logging at multiple verbosity levels (DEBUG, INFO, WARNING, ERROR).

**NFR5.4.5:** The system shall be modular with clear separation of concerns:

- Core detection engine
- GUI layer
- Logging subsystem
- Configuration management

**NFR5.4.6:** Updates shall not require database migrations (file-based storage).

### 5.5 Portability

**NFR5.5.1:** The system shall run on Windows 10 and Windows 11 without modification.

**NFR5.5.2:** The system shall support both 32-bit and 64-bit Windows installations.

**NFR5.5.3:** The system shall work with Python 3.8, 3.9, 3.10, 3.11, and 3.12.

**NFR5.5.4:** The system shall not depend on specific hardware configurations.

**NFR5.5.5:** The system shall be deployable via simple file copy (no installer required).

---

## 6. Other Requirements

### 6.1 Legal and Compliance

**REQ6.1.1:** The system shall comply with applicable data protection regulations (GDPR, CCPA).

**REQ6.1.2:** The system shall provide notice to users that monitoring is active.

**REQ6.1.3:** The system shall allow users to opt-out where legally required.

**REQ6.1.4:** Documentation shall clearly state intended use and limitations.

### 6.2 Internationalization

**REQ6.2.1:** The system shall use UTF-8 encoding for all text.

**REQ6.2.2:** GUI text shall be externalizable for future translation (English only in v1.0).

**REQ6.2.3:** Date/time formats shall respect locale settings.

### 6.3 Documentation

**REQ6.3.1:** The system shall include a comprehensive README file.

**REQ6.3.2:** The system shall include a user guide with screenshots.

**REQ6.3.3:** The code shall include inline comments for complex logic.

**REQ6.3.4:** API documentation shall be generated from docstrings.

---

## 7. Implementation/Proof-of-Concept (PoC)

### 7.1 Architecture Overview

**Component Structure:**

```
Screen Capture Detector
│
├── Main Application (main.py)
│   └── Entry point, initialization
│
├── Core Detection Engine (core/detector.py)
│   ├── Process monitoring thread
│   ├── Risk assessment engine
│   ├── Event management
│   └── Statistics tracking
│
├── GUI Layer (gui/main_window.py)
│   ├── Main window
│   ├── Tabbed interface
│   ├── Real-time tree view
│   └── Event callbacks
│
└── Utilities (utils/)
    └── Logging system (logger.py)
```

### 7.2 Detection Algorithm

**Pseudocode:**

```
WHILE monitoring_active:
    processes = enumerate_all_processes()

    FOR EACH process IN processes:
        IF process.pid IN already_checked:
            CONTINUE

        metadata = extract_process_metadata(process)
        risk_level = assess_risk(metadata)

        IF risk_level != SAFE:
            event = create_detection_event(metadata, risk_level)
            log_event(event)
            notify_gui(event)

            IF risk_level == CRITICAL AND auto_block_enabled:
                terminate_process(process)

        mark_as_checked(process.pid)

    SLEEP(scan_interval)
END WHILE
```

### 7.3 Risk Assessment Logic

**Risk Scoring:**

```python
def assess_risk(process_info):
    score = 0

    # Check whitelist (immediate return)
    if process_name in WHITELIST:
        return "SAFE"

    # Check blacklist patterns
    for pattern in BLACKLIST:
        if pattern in process_name.lower():
            return "CRITICAL"

    # Check command-line for suspicious keywords
    cmdline = process_info['cmdline'].lower()
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in cmdline:
            score += 30

    # Check for hidden windows
    if has_hidden_window(process):
        score += 20

    # Check process reputation
    if not is_signed(process):
        score += 15

    # Convert score to risk level
    if score >= 60:
        return "CRITICAL"
    elif score >= 40:
        return "HIGH"
    elif score >= 20:
        return "MEDIUM"
    else:
        return "LOW"
```

### 7.4 Technology Stack

- **Language:** Python 3.8+
- **GUI:** Tkinter (built-in)
- **Process Monitoring:** psutil 5.9.6
- **Windows API:** pywin32 306
- **Image Processing:** Pillow 10.1.0
- **Logging:** Python logging module
- **Data Export:** CSV module

### 7.5 Deployment Model

**Standalone Executable (Future):**

- Use PyInstaller to create .exe
- Bundle Python runtime
- Single-file deployment option

**Python Script (Current):**

- Requires Python installation
- Install dependencies via pip
- Run directly from source

---

## 8. Usability Burden

### 8.1 Learning Curve

**Estimated Time to Proficiency:**

- Basic use (start/stop monitoring): 5 minutes
- Intermediate use (configure alerts): 15 minutes
- Advanced use (whitelist management): 30 minutes

**Mitigation:**

- Intuitive GUI with clear labels
- Sensible defaults
- Comprehensive user guide
- Tooltips on hover (future enhancement)

### 8.2 System Requirements

**Burden on Users:**

- Must install Python 3.8+ if not present
- Must install dependencies (3 packages)
- Should have administrator privileges for full features

**Mitigation:**

- Provide install.bat script for automated setup
- Include portable Python distribution (future)
- Degrade gracefully without admin rights

### 8.3 Performance Impact

**Potential Burden:**

- Continuous CPU/memory usage
- Disk I/O for logging
- Potential interference with legitimate screen capture tools

**Mitigation:**

- Optimized scanning interval (1-second default)
- Asynchronous I/O for logging
- Comprehensive whitelist to prevent false positives
- Configurable performance settings

### 8.4 False Positives

**Burden:**

- Users may receive alerts for legitimate software
- May need to configure whitelist

**Mitigation:**

- Pre-populated whitelist with common tools
- Easy whitelist management in GUI
- Clear explanations in alerts
- Risk level categorization to prioritize real threats

---

## 9. Appendices

### 9.1 Appendix A: Use Case Diagram

```
                    ┌────────────────┐
                    │  Administrator │
                    └────────┬───────┘
                             │
                             │ manages
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐      ┌──────────────┐    ┌──────────────┐
    │Configure│      │View Detections│    │Export Reports│
    │ Settings│      │   & Logs     │    │              │
    └─────────┘      └──────────────┘    └──────────────┘
                             │
                             │ uses
                             │
                    ┌────────┴────────┐
                    │ Detector System │
                    └────────┬────────┘
                             │
                             │ monitors
                             │
                    ┌────────▼────────┐
                    │ Windows Processes│
                    └─────────────────┘
```

### 9.2 Appendix B: Data Flow Diagram (Level 0)

```
External          ┌──────────────────────────────┐
Entities          │                              │
                  │   Screen Capture Detector    │
    ┌──────┐      │                              │      ┌──────┐
    │      │─────▶│  1. Monitor Processes        │─────▶│      │
    │ OS   │      │  2. Assess Risk              │      │ Logs │
    │      │◀─────│  3. Generate Alerts          │◀─────│      │
    └──────┘      │  4. Record Events            │      └──────┘
                  │                              │
    ┌──────┐      │                              │      ┌──────┐
    │      │─────▶│                              │─────▶│      │
    │ User │      │                              │      │ GUI  │
    │      │◀─────│                              │◀─────│      │
    └──────┘      └──────────────────────────────┘      └──────┘
```

### 9.3 Appendix C: Sample UI Mockup

_See actual GUI implementation in the running application_

Key UI elements:

1. Top control bar with start/stop buttons
2. Statistics cards (4 metrics)
3. Tabbed interface with 4 tabs
4. Tree view for real-time detections
5. Console-style log viewer
6. Settings panel with checkboxes and sliders

### 9.4 Appendix D: Glossary of Technical Terms

**API Hooking:** Intercepting function calls to monitor or modify behavior

**Behavioral Analysis:** Monitoring actions and patterns rather than signatures

**BitBlt:** Windows GDI function for transferring bitmap data between device contexts

**Device Context (DC):** Windows structure representing a drawing surface

**False Positive:** Alert triggered by legitimate activity (not a real threat)

**Heuristic Analysis:** Detection based on behavioral patterns rather than known signatures

**Process Enumeration:** Listing all currently running processes

**Risk Classification:** Categorizing threats by severity level

**Screen Capture:** Taking a snapshot of all or part of the screen

**Whitelist:** List of trusted applications that won't trigger alerts

### 9.5 Appendix E: Risk Matrix

| Risk Level | Characteristics    | Response Time | Auto-Block       |
| ---------- | ------------------ | ------------- | ---------------- |
| CRITICAL   | Known malware      | Immediate     | Yes (if enabled) |
| HIGH       | Unknown suspicious | < 30 seconds  | Optional         |
| MEDIUM     | Unusual legitimate | < 5 minutes   | No               |
| LOW        | Minor anomaly      | Review daily  | No               |

### 9.6 Appendix F: Change Log

**Version 1.0.0 (18 October 2025)**

- Initial release
- Core detection engine implemented
- Modern GUI with tabbed interface
- Real-time monitoring with color-coded alerts
- CSV export functionality
- Configurable settings
- Comprehensive logging
- User guide and documentation

---

**Document Status:** FINAL  
**Approval Date:** 15 October 2025  
**Next Review:** January 2026

---

_This SRS document is a living document and will be updated as the project evolves._
