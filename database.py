import sqlite3
import json
import os

DB_PATH = "data/app.db"

def get_connection():
    # Ensure the directory exists before connecting (Crucial for Cloud Deployment)
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            model_number TEXT,
            department TEXT,
            purchase_date DATE,
            manufacturer TEXT,
            operating_voltage TEXT,
            battery_spec TEXT,
            checklist_fields TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER,
            checklist_data TEXT,
            remarks TEXT,
            inspected_by TEXT,
            date DATE,
            serial_number TEXT,
            job_card_no TEXT,
            technician TEXT,
            FOREIGN KEY (device_id) REFERENCES equipment (id)
        )
    ''')

    # Seed default devices if table is empty
    cursor.execute("SELECT COUNT(*) FROM equipment")
    if cursor.fetchone()[0] == 0:
        default_devices = [
            ("ECG Machine", "MAC-2000", "Cardiology", "2024-01-01", "GE Healthcare", "230V", "Li-ion 14.4V",
             json.dumps(["Power-On Self Test", "Lead-Off Detection", "Baseline Stability", "Common Mode Rejection", "Heart Rate Accuracy"])),
            ("Ventilator", "Puritan Bennett 980", "ICU", "2024-01-01", "Medtronic", "230V", "Backup Lead-Acid",
             json.dumps(["Oxygen Supply Pressure", "Air Supply Pressure", "Exhalation Valve Test", "Safety Valve Test", "Battery Backup Test"])),
            ("Patient Monitor", "IntelliVue MX550", "ER", "2024-01-01", "Philips", "230V", "Rechargeable Li-ion",
             json.dumps(["Display Pixel Test", "NIBP Pump Test", "SpO2 Module Sync", "Temperature Probe Continuity", "Alarm System Audio"])),
            ("Ultrasound", "US-200", "Radiology", "2023-05-10", "GE Healthcare", "230V", "N/A",
             json.dumps(["System Boot & UI Test", "Probe Holder Board", "Image Quality Test", "DC-DC Board", "Data Storage & Connectivity", "Audio Check and Keyboard Test"])),
            ("Anesthesia Machine", "Aisys CS2", "OT", "2023-08-01", "GE Healthcare", "230V", "12V, 7Ah",
             json.dumps(["System Boot & UI Test", "Oxygen Supply Check", "Air Supply Check", "Nitrous Oxide Check", "Leak Test", "Flowmeter Accuracy Test", "Vaporizer Testing", "Breathing Circuit Check"])),
            ("Defibrillator", "HeartStart XL", "Emergency", "2024-06-28", "Philips", "230V", "12V, 2.3Ah",
             json.dumps(["Power Supply Check", "Calibration Status", "Physical Condition", "Display Working", "Alarm System"]))
        ]
        cursor.executemany('''
            INSERT INTO equipment (device_name, model_number, department, purchase_date, manufacturer, operating_voltage, battery_spec, checklist_fields)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', default_devices)
    
    conn.commit()
    conn.close()
