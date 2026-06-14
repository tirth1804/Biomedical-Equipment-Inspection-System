import streamlit as st
import time
import json
from datetime import datetime
from database import get_connection
from devices.simulated_devices import get_simulator_for_type

def automated_inspection():
    st.title("🤖 Automated Testing Mode")
    st.write("Simulate IoT-driven automated testing for biomedical equipment.")

    # --- IoT Device Connectivity Section in Sidebar ---
    st.sidebar.subheader("🔌 IoT Device Connectivity")
    
    if 'connected_devices' not in st.session_state:
        st.session_state.connected_devices = []

    # Option to connect a new device via mock protocol
    with st.sidebar.expander("🔗 Link New IoT Device"):
        new_dev_name = st.text_input("Device Name (e.g. Vent-Unit-1)")
        p_opt = ["WiFi/MQTT", "Bluetooth 5.0", "Serial/USB", "HTTP REST"]
        new_dev_type = st.selectbox("Protocol", p_opt)
        new_dev_id = st.text_input("IoT Device ID / MAC")
        if st.button("Establish Link"):
            if new_dev_name and new_dev_id:
                st.session_state.connected_devices.append({
                    "name": new_dev_name,
                    "type": new_dev_type,
                    "id": new_dev_id,
                    "status": "Online"
                })
                st.success(f"Linked to {new_dev_name} successfully.")
                st.rerun()

    # Show live connections
    if st.session_state.connected_devices:
        st.sidebar.write("---")
        st.sidebar.write("**Live IoT Sources:**")
        for dev in st.session_state.connected_devices:
            st.sidebar.info(f"🟢 {dev['name']}\n`ID: {dev['id']}`")
    else:
        st.sidebar.warning("No physical/IoT devices linked.")

    # --- Main Module Content ---
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, device_name, model_number FROM equipment")
    equipment_list = cursor.fetchall()
    conn.close()

    if not equipment_list:
        st.warning("Please add equipment in the 'Equipment Management' module first.")
        return

    # 1. UI Selection
    col1, col2 = st.columns(2)
    with col1:
        device_options = {f"{e[1]} ({e[2]})": e[0] for e in equipment_list}
        selected_device_label = st.selectbox("Assign Inventory Item", list(device_options.keys()))
        device_id = device_options[selected_device_label]
    
    with col2:
        if st.session_state.connected_devices:
            iot_sources = [f"{d['name']} ({d['type']})" for d in st.session_state.connected_devices]
            st.selectbox("IoT Source Stream", iot_sources)
        
        device_type = st.selectbox("Device Profile (for Test Suite)", ["ECG", "Ventilator", "Patient Monitor", "Other"])

    st.divider()

    # 2. Preparation
    simulator = get_simulator_for_type(device_type)
    procedures = simulator.get_test_procedures()
    
    st.subheader(f"📋 Automated Test Suite: {device_type}")
    with st.expander("Show Test Procedures"):
        for p in procedures:
            st.write(f"• {p}")

    col_s1, col_s2 = st.columns(2)
    serial_no = col_s1.text_input("Unit Serial Number", placeholder="SN-XXXX")
    inspector = col_s2.text_input("Technician / Inspector Name")

    if st.button("🚀 Execute Automated Test Sequence", type="primary"):
        if not inspector or not serial_no:
            st.error("Please provide Serial Number and Technician Name.")
            return

        # 3. Execution Simulation
        status_box = st.empty()
        status_box.warning("🔄 Initiating Secure Handshake with IoT Device...")
        time.sleep(1.2)
        status_box.info("📡 Handshake Success. Syncing Calibration Data...")
        time.sleep(1.0)

        progress_bar = st.progress(0)
        
        def update_progress(current, total, msg):
            progress = current / total
            progress_bar.progress(progress)
            status_box.text(msg)

        results = simulator.run_tests(progress_callback=update_progress)
        
        status_box.success("✅ Automated Testing Complete!")
        
        # 4. Display Results
        st.divider()
        st.subheader("📊 Live Telemetry Results")
        
        pass_count = sum(1 for status in results.values() if status == "Pass")
        total_tests = len(results)
        health_score = (pass_count / total_tests) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Tests Passed", f"{pass_count}/{total_tests}")
        c2.metric("Health Score", f"{health_score:.1f}%")
        c3.metric("Status", "Approved" if health_score > 80 else "Requires Maintenance")

        st.table([{"Test Procedure": k, "Result": v} for k, v in results.items()])

        # 5. Database Storage
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inspections (
                    device_id, checklist_data, remarks, inspected_by, date, 
                    serial_number, job_card_no, technician
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                device_id, 
                json.dumps(results), 
                f"Automated IoT Test. Profile: {device_type}. Health Score: {health_score:.1f}%", 
                inspector, 
                str(datetime.now().date()), 
                serial_no, 
                f"IOT-{int(time.time())}", 
                inspector
            ))
            conn.commit()
            conn.close()
            st.success("Test record successfully pushed to hospital database!")
        except Exception as e:
            st.error(f"Error saving results: {e}")

        st.balloons()
        st.info("Tip: You can now view and download the PDF report in the 'Inspection History' tab.")
