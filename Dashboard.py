import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Dashboard", layout="wide")

# ============ DATA LOAD ============
def get_data():
    try:
        conn = sqlite3.connect("database/auth.db")
        df = pd.read_sql("SELECT * FROM students", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame(columns=["StudentID","Name","Class","Gender","Age","Absences","Midterm_Score","Final_Score","Final_Percentage","Risk_Level"])

df = get_data()

# ============ DASHBOARD ============
st.markdown('<div class="main-title">📊 Academic Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Live overview of student performance, attendance & risk levels</div>', unsafe_allow_html=True)

if df.empty:
    st.warning("⚠️ No student data found. Please add students from Add Student page.")
else:
    total_students = len(df)
    avg_final = round(df["Final_Percentage"].mean(), 1) if "Final_Percentage" in df.columns else 0
    avg_attendance = round(100 - (df["Absences"].mean() / 30 * 100), 1) if "Absences" in df.columns else 0
    high_risk = len(df[df["Risk_Level"] == "High"]) if "Risk_Level" in df.columns else 0

    # INFO BOXES
    st.markdown(f"""
    <div class="info-row">
        <div class="info-box">👨‍🎓<br><b>{total_students}</b><br>Total Students</div>
        <div class="info-box">📈<br><b>{avg_final}%</b><br>Avg Final Score</div>
        <div class="info-box">✅<br><b>{avg_attendance}%</b><br>Avg Attendance</div>
        <div class="info-box">⚠️<br><b>{high_risk}</b><br>High Risk Students</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Top KPI Cards")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", total_students)
    col2.metric("Avg Final %", f"{avg_final}%")
    col3.metric("Avg Attendance", f"{avg_attendance}%")
    col4.metric("High Risk", high_risk)

    st.markdown("---")

    # SEARCH + FILTER
    st.markdown("### 🔍 Search + Filter")
    c1, c2 = st.columns([2, 1])
    search = c1.text_input("Search by Name or ID")
    risk_filter = c2.selectbox("Filter by Risk", ["All", "Low", "Medium", "High"])

    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df["Name"].str.contains(search, case=False, na=False) | filtered_df["StudentID"].astype(str).str.contains(search, na=False)]
    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df["Risk_Level"] == risk_filter]

    # CHARTS
    st.markdown("### 📊 Charts")
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("**Students by Class**")
        st.bar_chart(df["Class"].value_counts())
    with ch2:
        st.markdown("**Risk Level Distribution**")
        st.bar_chart(df["Risk_Level"].value_counts())

    st.markdown("### 📋 All Students Data")
    st.dataframe(filtered_df, use_container_width=True)