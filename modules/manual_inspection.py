import streamlit as st
import json
from datetime import datetime
from database import get_connection

def inspection_module():
    st.title("📋 New Inspection")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, device_name, model_number, checklist_fields FROM equipment")
    devices = cursor.fetchall()
    conn.close()
    
    if not devices:
        st.warning("Please add a device in Equipment Management first.")
        return

    # Use Device Name and Model for selection instead of showing IDs
    device_options = {f"{d[1]} - {d[2]}": (d[0], d[3]) for d in devices}
    selected_device_key = st.selectbox("Select Device to Inspect", list(device_options.keys()))
    device_id, checklist_fields_json = device_options[selected_device_key]
    
    # Load predefined checklist for this device
    base_checklist = json.loads(checklist_fields_json) if checklist_fields_json else []
    
    # Initialize session state for dynamic fields if not present
    state_key = f"dynamic_fields_{device_id}"
    if state_key not in st.session_state:
        st.session_state[state_key] = base_checklist.copy()

    st.divider()
    
    with st.expander("🛠️ Customize Checklist for this Session", expanded=False):
        st.write("Add or remove specific tests for this unique inspection unit.")
        
        # Add new field
        new_field_col, add_btn_col = st.columns([3, 1])
        new_field_name = new_field_col.text_input("New specialized test name", key=f"new_field_input_{device_id}")
        if add_btn_col.button("Add Test", key=f"add_btn_{device_id}", use_container_width=True):
            if new_field_name and new_field_name not in st.session_state[state_key]:
                st.session_state[state_key].append(new_field_name)
                st.rerun()

        # Remove fields
        if st.session_state[state_key]:
            field_to_remove = st.multiselect("Remove tests (not required for this unit)", 
                                            options=st.session_state[state_key],
                                            key=f"remove_multi_{device_id}",
                                            help="Select items you want to skip/remove for this specific inspection.")
            if st.button("Apply Removals", key=f"remove_btn_{device_id}"):
                st.session_state[state_key] = [f for f in st.session_state[state_key] if f not in field_to_remove]
                st.rerun()

    with st.form("inspection_form"):
        st.subheader("General Information")
        col1, col2 = st.columns(2)
        with col1:
            serial_no = st.text_input("Serial Number")
            job_card = st.text_input("Job Card No")
        with col2:
            tech = st.text_input("Technician")
            date = st.date_input("Inspection Date", value=datetime.now())
            
        st.divider()
        st.subheader("Checklist Results")
        results = {}
        active_fields = st.session_state[state_key]
        
        if not active_fields:
            st.info("No checklist items. Add some above.")
        else:
            cols = st.columns(2)
            for i, item in enumerate(active_fields):
                with cols[i % 2]:
                    results[item] = st.selectbox(f"{item}", ["Pass", "Fail", "Not Tested"], key=f"check_{device_id}_{i}")
        
        st.divider()
        remarks = st.text_area("Observations / Remarks")
        inspected_by = st.text_input("Inspected By (Final Sign-off)")
        
        if st.form_submit_button("Submit Inspection"):
            if inspected_by:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO inspections (
                        device_id, checklist_data, remarks, inspected_by, date, 
                        serial_number, job_card_no, technician
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (device_id, json.dumps(results), remarks, inspected_by, str(date), serial_no, job_card, tech))
                conn.commit()
                conn.close()
                st.success("Inspection recorded successfully!")
                # Clear session state for next time
                if state_key in st.session_state:
                    del st.session_state[state_key]
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter the inspector's name.")
