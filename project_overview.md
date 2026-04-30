# 🏥 Biomedical Equipment Inspection System (BEIS) - Project Abstract

## 🌟 Project Motto
> **"Bridging Technology and Patient Safety through Precision Engineering."**

This project was conceived to digitalize the critical workflow of biomedical equipment maintenance. Our goal is to replace archaic paper-based logs with a high-integrity, automated diagnostic platform that ensures every life-saving machine in a hospital is verified, calibrated, and compliant.

---

## 🏗️ Technical Architecture & Stack

### 💻 Programming Environment
*   **Primary Language**: **Python 3.10+**
    *   *Why?* For its massive ecosystem of hardware simulation, data processing, and rapid prototyping capabilities.
*   **Operating System Agnostic**: Developed to run seamlessly on **macOS, Linux, and Windows** via containerization.

### 🖼️ Core Frameworks
*   **UI/UX Framework**: [**Streamlit**](https://streamlit.io/)
    *   Used to build a reactive "Enterprise Portal" providing a professional dashboard and real-time telemetry visuals.
*   **Data Persistence**: [**SQLite3**](https://sqlite.org/)
    *   A lightweight, serverless relational database used for local persistence of hospital inventory and audit logs.
*   **Reporting Engine**: [**WeasyPrint**](https://weasyprint.org/) & [**Jinja2**](https://palletsprojects.com/p/jinja/)
    *   Transforms inspection data into industry-standard PDF Job Cards with high-fidelity typography and layouts.

### 🤖 Simulation & Hardware Logic
*   **HAL (Hardware Abstraction Layer)**: Custom Python Object-Oriented (OOP) implementation.
*   **Protocols Simulated**: Virtual MQTT, Bluetooth Low Energy (BLE), and USB-Serial handshakes for IoT-ready diagnostics.

---

## 🛠️ Software & Tools Used
| Tool | Purpose |
| :--- | :--- |
| **VS Code** | Primary IDE for development and system refactoring. |
| **Docker & Docker Compose** | Total project containerization to eliminate "it works on my machine" issues. |
| **Git & GitHub** | Version control for code integrity and collaborative tracking. |
| **Pylance & Black** | Static type checking and PEP8 code formatting for production-level quality. |

---

## 💡 Key Innovation Highlights
1.  **Dynamic Checklist Customizer**: Unlike static forms, BEIS allows technicians to add or remove specific tests on-the-fly during a live session, adapting to the machine's immediate condition.
2.  **IoT Connectivity Hub**: A simulated environment that mimics real-world device handshakes, essential for training future biomedical IoT specialists.
3.  **Automated Health Scoring**: Proprietary algorithm that calculates a "Device Health Score" based on pass/fail ratios from multiple diagnostic cycles.
4.  **White-Label Enterprise Look**: Custom CSS injection to provide a standalone portal experience, hiding standard platform branding for professional hospital use.

---

## 🚀 Impact Statement
This system transforms a reactive maintenance department into a **proactive compliance center**. By centralizing asset data and automating the generation of signed PDF certificates, BEIS ensures that biomedical engineers spend more time on hardware precision and less time on administrative paperwork.

---
*Developed for: Biomedical Engineering Academic Showcase 2024 / Professional Industry Implementation*
