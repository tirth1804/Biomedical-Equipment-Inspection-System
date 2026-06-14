# 🏥 Biomedical Equipment Inspection System (BEIS)

**BEIS** is a specialized web-based management platform designed for biomedical engineers and students to maintain hospital inventory and document device safety and performance through professional inspection reports.

## 🚀 Key Features

*   **🔒 Secure Access**: Simplified administrative dashboard with session management.
*   **📂 Equipment Inventory**: Comprehensive lifecycle tracking (Device Specs, Dept, Manufacturer, Voltage/Battery Specs).
*   **� Enterprise Dashboard**: Live analytics for Total Assets, MTD Inspections, and Average Unit Health Scores.
*   **�📋 Dual Inspection Workflows**:
    *   **Manual Mode**: Form-based entry with dynamic, session-level checklist customization (add/remove tests on-the-fly) and modern touch-friendly sliders.
    *   **Automated Mode (IoT Simulation)**: Simulated hardware interface for ECG, Ventilators, and Monitors via virtual MQTT/Bluetooth/Serial protocols with live progress tracking.
*   **🔌 IoT Connectivity Hub**: Sidebar-based device manager to link and track virtual hardware sources with secure handshake simulation.
*   **📜 History & Analytics**: Full audit trail of past inspections with "Device Health Score" calculations and compliance filtering.
*   **🌱 Automated Seeding**: System-wide auto-initialization of core medical device data (ECG, Ventilators, Monitors) on first launch.

*   **📄 Professional PDF Reporting**: Generates industry-standard job cards (including Serial No, Job Card IDs, and Technician sign-offs) using WeasyPrint and Jinja2 templates.
*   **🐳 Production Ready**: Fully containerized with Docker and Docker Compose for persistent local storage.

## 🛠️ Tech Stack

*   **Frontend/Backend**: [Streamlit](https://streamlit.io/) (Python)
*   **Database**: SQLite (Local & Persistent)
*   **PDF Engine**: WeasyPrint & Jinja2 Templates
*   **Infrastructure**: Docker

## 📥 Installation & Running

### Option 1: Using Docker (Recommended)
```bash
docker-compose up --build
```
Access at: `http://localhost:8501`

### Option 2: Local Installation
1. Install Python 3.10+
2. Install system dependencies for WeasyPrint (e.g., `brew install pango` on macOS)
3. `pip install -r requirements.txt`
4. `streamlit run app.py`

## 👤 Credentials
*   **Username**: `admin`
*   **Password**: `biomed2024`
