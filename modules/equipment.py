import streamlit as st
import pandas as pd
import json
from database import get_connection

DEFAULT_CHECKLIST = ["Power supply check", "Calibration status", "Physical condition"]


def equipment_management():
    st.title("🛠️ Equipment Management")

    tab1, tab2 = st.tabs(["View / Edit Equipment", "Add New Device"])

    with tab1:
        st.subheader("Inventory List")
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM equipment", conn)
        conn.close()

        if df.empty:
            st.info("No equipment found. Add some in the next tab.")
        else:
            # Display a clean table — show checklist count instead of raw JSON
            display_df = df[["id", "device_name", "model_number", "department", "manufacturer", "operating_voltage", "battery_spec", "purchase_date"]].copy()
            display_df.columns = ["ID", "Device", "Model", "Department", "Manufacturer", "Voltage", "Battery", "Purchase Date"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            st.divider()

            # Edit / Delete section
            device_to_edit = st.selectbox(
                "Select Device to Edit or Delete",
                df["id"].tolist(),
                format_func=lambda x: f"{df[df['id']==x]['device_name'].values[0]} (ID {x})",
            )

            device_data = df[df["id"] == device_to_edit].iloc[0]

            with st.form(f"edit_form_{device_to_edit}"):
                st.subheader("Edit Device Details")
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Device Name", value=str(device_data["device_name"] or ""))
                    new_model = st.text_input("Model Number", value=str(device_data["model_number"] or ""))
                    new_dept = st.text_input("Department", value=str(device_data["department"] or ""))
                    new_mfr = st.text_input("Manufacturer", value=str(device_data["manufacturer"] or ""))
                with col2:
                    new_volts = st.text_input("Operating Voltage", value=str(device_data["operating_voltage"] or ""))
                    new_bat = st.text_input("Battery Spec", value=str(device_data["battery_spec"] or ""))
                    # Safely parse purchase_date — handle None / NaN
                    raw_date = device_data["purchase_date"]
                    try:
                        parsed_date = pd.to_datetime(raw_date).date()
                    except Exception:
                        parsed_date = pd.Timestamp.today().date()
                    new_date = st.date_input("Purchase Date", value=parsed_date)

                current_fields = (
                    json.loads(device_data["checklist_fields"])
                    if device_data["checklist_fields"]
                    else DEFAULT_CHECKLIST
                )
                new_fields_str = st.text_area(
                    "Checklist Fields (comma separated)", value=", ".join(current_fields)
                )
                new_fields = [x.strip() for x in new_fields_str.split(",") if x.strip()]

                if st.form_submit_button("Update Device"):
                    if new_name:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            """
                            UPDATE equipment
                            SET device_name=?, model_number=?, department=?, purchase_date=?,
                                manufacturer=?, operating_voltage=?, battery_spec=?, checklist_fields=?
                            WHERE id=?
                            """,
                            (
                                new_name, new_model, new_dept, str(new_date),
                                new_mfr, new_volts, new_bat,
                                json.dumps(new_fields), device_to_edit,
                            ),
                        )
                        conn.commit()
                        conn.close()
                        st.success("Device updated successfully!")
                        st.rerun()
                    else:
                        st.error("Device Name is required.")

            # Delete — outside the form to avoid accidental submit
            st.divider()
            with st.expander("⚠️ Delete This Device", expanded=False):
                st.warning(
                    f"Deleting **{device_data['device_name']}** will also remove all linked inspection records. This cannot be undone."
                )
                confirm_name = st.text_input("Type the device name to confirm deletion", key="delete_confirm")
                if st.button("Delete Device", type="primary", key="delete_btn"):
                    if confirm_name == device_data["device_name"]:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM inspections WHERE device_id = ?", (device_to_edit,))
                        cursor.execute("DELETE FROM equipment WHERE id = ?", (device_to_edit,))
                        conn.commit()
                        conn.close()
                        st.success("Device and all linked inspections deleted.")
                        st.rerun()
                    else:
                        st.error("Device name does not match. Deletion cancelled.")

    with tab2:
        st.subheader("Register New Equipment")
        with st.form("add_device_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Device Name")
                model = st.text_input("Model Number")
                dept = st.text_input("Department")
                mfr = st.text_input("Manufacturer")
            with col2:
                volts = st.text_input("Operating Voltage")
                bat = st.text_input("Battery Spec")
                p_date = st.date_input("Purchase Date")

            checklist_fields_str = st.text_area(
                "Initial Checklist Fields (comma separated)",
                value=", ".join(DEFAULT_CHECKLIST),
            )
            checklist_fields = [x.strip() for x in checklist_fields_str.split(",") if x.strip()]

            if st.form_submit_button("Add Device"):
                if name:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO equipment (device_name, model_number, department, purchase_date,
                                              manufacturer, operating_voltage, battery_spec, checklist_fields)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (name, model, dept, str(p_date), mfr, volts, bat, json.dumps(checklist_fields)),
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"'{name}' added successfully!")
                    st.rerun()
                else:
                    st.error("Device Name is required.")
