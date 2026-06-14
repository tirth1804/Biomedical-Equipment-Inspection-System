# 🏥 Project Documentation: Biomedical Equipment Inspection System (BEIS)

## 📌 Project Overview
The **Biomedical Equipment Inspection System (BEIS)** is a specialized software application developed to bridge the gap between inventory management and technical inspection in a hospital environment. It provides biomedical engineering students and technicians with a streamlined way to document device health, perform maintenance checklists, and generate professional compliance reports.

## 🎯 Problem Statement
Hospitals and clinics often struggle with:
1.  **Manual Record Keeping**: Paper-based inspection logs are easily lost and hard to track.
2.  **Inconsistent Testing**: Different technicians use different criteria for the same device.
3.  **Lack of Professional Output**: Generating a professional job card (PDF) for each inspection is a time-consuming manual process.
4.  **Static Workflows**: Most software is too rigid to add/remove specific tests during an inspection.

## 💡 Solution Provided
**BEIS** addresses these issues through:
*   **Enterprise Dashboard**: Real-time visualization of asset count, monthly inspections, and average performance scores.
*   **Dynamic Checklist Engine**: Allows the user to pre-define industry-standard tests (from `Machine.md` data) and customize them during a live inspection.
*   **Automated Seeding**: Ensures a consistent testing environment by auto-populating default medical devices and protocols on launch.
*   **Centralized SQLite Database**: Stores all inventory specs and historical inspection results for audit tracking.
*   **Automated PDF Job Cards**: Generates high-quality inspection reports using enterprise-level PDF rendering (WeasyPrint).
*   **Hospital Workflow Alignment**: Fields for Serial Number, Job Card ID, Manufacturer, Technician, and Final Sign-off.

## 🧩 Software Architecture
The application follows a modular architecture:
*   **Presentation Layer**: Built with **Streamlit** using a custom professional blue-themed "Enterprise" UI.
*   **Logic Layer**: Python-based modules for Equipment Lifecycle, Dynamic Inspection Logic, and Report Rendering.
*   **Data Layer**: **SQLite3** for lightweight, serverless persistence; includes automated seeding logic.
*   **Hardware Interface**: Hardware Abstraction Layer (HAL) for simulation and future real-world extensibility.
*   **Infrastructure**: **Docker** for "plug-and-play" deployment across different OS environments.

## ✨ Core Modules & Functionality
1.  **Dashboard Analytics**: Live metrics for operational overview (Asset count, health trends).
2.  **Equipment Management**: Manage the full lifecycle of medical devices including Manufacturer details, Operating Voltages, and Default Checklist templates.
3.  **Manual Inspection**: A form-based workflow for on-site technicians with dynamic, session-based checklist customization (add/remove tests per unit) and touch-optimized evaluation sliders.
4.  **Automated Testing Mode (IoT Simulation)**: 
    *   **Connectivity Hub**: Link virtual IoT devices via protocols like MQTT, Bluetooth, and Serial/USB.
    *   **Real-time Handshake**: Simulates secure authentication and calibration data sync with hardware.
    *   **Automated Diagnostics**: Runs predefined test suites for ECG, Ventilators, and Monitors with live progress tracking and automated pass/fail results.
5.  **Audit Logs & Reports**: A complete history of past inspections with multi-parameter filtering and one-click PDF generation.

## 🔌 Advanced Features
*   **IoT Device Linking**: A sidebar-based connection manager to simulate and manage external data sources.
*   **Modular Hardware Interface**: Built using a clean abstraction layer (`MedicalDeviceInterface`) to allow for future integration with real physical hardware.
*   **Dynamic Checklist Logic**: Ensures that while devices have "standard" tests, unique unit-level requirements are handled seamlessly without cluttering the main database schema.
*   **Seeding Mechanism**: Automatic instantiation of "Golden Images" for medical equipment categories to standardization.


## 🚀 Future Roadmap
*   **Barcode/QR Integration**: Scan a sticker on the machine to open the inspection form instantly.
*   **Calibration Alerts**: Automated notifications when a device is due for its periodic maintenance.
*   **Cloud Sync**: Migration to a central SQL server for multi-hospital deployments.

---
*Created by [Your Name] - Biomedical Engineering Project 2024*
