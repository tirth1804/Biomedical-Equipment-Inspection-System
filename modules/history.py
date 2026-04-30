import streamlit as st
import pandas as pd
import json
from database import get_connection
from modules.reports import generate_pdf

def inspection_history():
    st.title("📜 Inspection History")
    
    conn = get_connection()
    query = '''
        SELECT i.id, i.date, e.device_name, e.model_number, i.inspected_by, i.remarks,
               i.checklist_data, e.department, i.device_id, i.serial_number, i.job_card_no,
               i.technician, e.manufacturer, e.purchase_date, e.operating_voltage, e.battery_spec
        FROM inspections i
        JOIN equipment e ON i.device_id = e.id
        ORDER BY i.date DESC
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        st.info("No inspection records found.")
        return

    # Filters
    device_filter = st.multiselect("Filter by Device", options=df['device_name'].unique())
    if device_filter:
        df = df[df['device_name'].isin(device_filter)]

    if df.empty:
        st.info("No inspections match the selected filter.")
        return

    st.dataframe(
        df[['id', 'date', 'device_name', 'inspected_by', 'remarks']],
        use_container_width=True,
        hide_index=True,
    )
    
    st.divider()
    st.subheader("View & Export Details")
    
    selected_id = st.selectbox("Select Inspection ID for Details", df['id'].tolist())
    
    if selected_id:
        record = df[df['id'] == selected_id].iloc[0]
        checklist = json.loads(record['checklist_data'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Device:** {record['device_name']}")
            st.write(f"**Model:** {record['model_number']}")
            st.write(f"**Department:** {record['department']}")
        with col2:
            st.write(f"**Date:** {record['date']}")
            st.write(f"**Inspector:** {record['inspected_by']}")
            st.write(f"**Remarks:** {record['remarks']}")
            
        st.write("**Checklist Results:**")
        # Health Score
        pass_count = sum(1 for v in checklist.values() if v == "Pass")
        total = len(checklist)
        score = (pass_count / total * 100) if total > 0 else 0
        st.info(f"Health Score: {score:.1f}%")

        st.table(pd.DataFrame(checklist.items(), columns=["Item", "Status"]))

        # PDF Generation — generate inline so download is always available
        try:
            pdf_data = generate_pdf(record, checklist)
            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name=f"Report_{record['device_name']}_{record['date']}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Could not generate PDF: {e}")
