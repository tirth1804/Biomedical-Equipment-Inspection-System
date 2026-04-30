import streamlit as st
import pandas as pd
import json
from datetime import datetime
from database import get_connection


def dashboard():
    st.title("📊 Dashboard")
    st.write("Real-time overview of your biomedical equipment system.")

    conn = get_connection()

    total_assets = pd.read_sql_query(
        "SELECT COUNT(*) as cnt FROM equipment", conn
    ).iloc[0]["cnt"]

    current_month = datetime.now().strftime("%Y-%m")
    mtd_count = pd.read_sql_query(
        "SELECT COUNT(*) as cnt FROM inspections WHERE strftime('%Y-%m', date) = ?",
        conn,
        params=(current_month,),
    ).iloc[0]["cnt"]

    all_inspections = pd.read_sql_query(
        "SELECT checklist_data FROM inspections", conn
    )

    recent_df = pd.read_sql_query(
        """
        SELECT i.id, i.date, e.device_name, i.inspected_by, i.checklist_data
        FROM inspections i
        JOIN equipment e ON i.device_id = e.id
        ORDER BY i.date DESC
        LIMIT 5
        """,
        conn,
    )

    dept_df = pd.read_sql_query(
        "SELECT department, COUNT(*) as count FROM equipment GROUP BY department",
        conn,
    )

    conn.close()

    # Average health score across all inspections
    scores = []
    for _, row in all_inspections.iterrows():
        try:
            checklist = json.loads(row["checklist_data"])
            total = len(checklist)
            if total > 0:
                passes = sum(1 for v in checklist.values() if v == "Pass")
                scores.append((passes / total) * 100)
        except Exception:
            pass
    avg_score = sum(scores) / len(scores) if scores else 0

    # --- Metric Cards ---
    c1, c2, c3 = st.columns(3)
    c1.metric("🏥 Total Assets", int(total_assets))
    c2.metric("📋 MTD Inspections", int(mtd_count))
    c3.metric("💯 Avg Health Score", f"{avg_score:.1f}%")

    st.divider()

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Recent Inspections")
        if recent_df.empty:
            st.info("No inspections recorded yet.")
        else:
            def calc_score(data):
                try:
                    c = json.loads(data)
                    t = len(c)
                    if t == 0:
                        return "N/A"
                    pct = sum(1 for v in c.values() if v == "Pass") / t * 100
                    return f"{pct:.0f}%"
                except Exception:
                    return "N/A"

            recent_df["Health Score"] = recent_df["checklist_data"].apply(calc_score)
            st.dataframe(
                recent_df[["id", "date", "device_name", "inspected_by", "Health Score"]].rename(
                    columns={
                        "id": "ID",
                        "date": "Date",
                        "device_name": "Device",
                        "inspected_by": "Inspector",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with col_right:
        st.subheader("Assets by Department")
        if dept_df.empty:
            st.info("No equipment registered.")
        else:
            st.dataframe(
                dept_df.rename(columns={"department": "Department", "count": "Devices"}),
                use_container_width=True,
                hide_index=True,
            )
