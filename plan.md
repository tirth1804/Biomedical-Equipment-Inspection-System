You are a senior Python full-stack developer.

I want you to build a complete web application for biomedical students to manage machine inventory and inspection reports. The users are non-technical, so the UI must be very simple and intuitive.

---

### Tech Stack Requirements

* Backend + UI: Python using Streamlit
* Database: SQLite (no external DB setup)
* PDF Reports: WeasyPrint (preferred) or ReportLab
* Deployment: Should be compatible with Streamlit Cloud
* Containerization: Docker (must be included)
* Keep everything lightweight and free to run

---

### Application Overview

This app is a "Biomedical Equipment Inspection System" with the following modules:

---

### 1. Login Page

* Simple password-based login (no complex authentication)
* Use Streamlit session state to manage login
* Hardcode one username/password for now

---

### 2. Equipment Management Module

Features:

* Add new device
* View device list
* Edit existing device

Device fields:

* id (auto)
* device_name
* model_number
* department
* purchase_date

---

### 3. Inspection Module (Main Feature)

Workflow:

1. Select a device from dropdown
2. Show checklist (predefined items)
3. For each checklist item → dropdown:

   * Pass
   * Fail
   * Not Tested
4. Add:

   * Remarks (text)
   * Inspected By (text)
   * Date (auto-filled, editable)

Checklist example:

* Power supply check
* Calibration status
* Physical condition
* Display working
* Alarm system

Store checklist as JSON in database.

Database table:

* id
* device_id (foreign key)
* checklist_data (JSON)
* remarks
* inspected_by
* date

---

### 4. Inspection History Module

Features:

* Filter by device
* Show all past inspections in table
* View details of each inspection

---

### 5. Report Generation

* Generate PDF report for each inspection
* Include:

  * Device details
  * Checklist results
  * Remarks
  * Inspector name
  * Date
* Add a "Download PDF" button

---

### UI Requirements

* Clean and minimal design using Streamlit
* Sidebar navigation:

  * Login
  * Equipment Management
  * New Inspection
  * Inspection History
* Use forms for inputs
* Use tables for displaying data

---

### Code Structure

Organize code into:

* app.py (main entry)
* database.py (SQLite operations)
* modules/

  * auth.py
  * equipment.py
  * inspection.py
  * reports.py

---

### Additional Features (if easy)

* Auto-generate "Device Health Score" based on checklist
* Simple charts (pass/fail count)
* Success/error messages

---

### Docker Requirements (VERY IMPORTANT)

Create a complete Docker setup so the app can run anywhere.

Include:

1. Dockerfile:

   * Use python:3.10-slim
   * Install system dependencies required for WeasyPrint (like libcairo, pango, etc.)
   * Copy project files
   * Install requirements.txt
   * Expose port 8501
   * Run Streamlit app

2. .dockerignore:

   * **pycache**/
   * *.pyc
   * *.db
   * .git

3. docker-compose.yml:

   * One service: app
   * Map port 8501:8501
   * Mount volume for SQLite database persistence

4. Ensure SQLite database file is stored in a persistent volume (e.g., /app/data/app.db)

---

### Important Constraints

* Keep code beginner-friendly and well-commented
* Avoid overengineering
* No external paid services
* Everything should run locally, via Docker, and on Streamlit Cloud

---

### Output Expectation

1. Full working code
2. Database schema creation
3. requirements.txt
4. Dockerfile
5. docker-compose.yml
6. .dockerignore
7. Step-by-step instructions to:

   * Run locally (without Docker)
   * Run with Docker
   * Deploy on Streamlit Cloud

---

### Development Instructions

Start by generating:

1. Project folder structure
2. requirements.txt
3. database.py
4. app.py
5. modules (one by one)
6. report generation
7. Docker setup (Dockerfile, docker-compose.yml)

Do not skip steps. Ensure everything is connected, clean, and runnable.
