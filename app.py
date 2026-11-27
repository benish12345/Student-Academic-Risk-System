import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import re

st.set_page_config(page_title="Student Academic Risk System", layout="wide", page_icon="🎓")

# ---------- DATABASE ----------
conn = sqlite3.connect("students.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (name TEXT, email TEXT PRIMARY KEY, password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS students
             (name TEXT, attendance REAL, marks REAL, study_hours REAL, assignments REAL, sleep_hours REAL, risk TEXT)''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------- LOGIN / SIGNUP ----------
if not st.session_state.logged_in:
    st.title("🎓 Student Academic Risk System")
    st.write("Welcome! Please login or create a new account to continue.")
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if not email or not password:
                st.error("Please fill all fields!")
            elif not is_valid_email(email):
                st.error("Please enter a valid email!")
            else:
                hashed = hash_password(password)
                c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed))
                user = c.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password!")

    with tab2:
        st.subheader("Create New Account")
        name = st.text_input("Full Name", key="signup_name")
        new_email = st.text_input("Email", key="signup_email")
        new_pass = st.text_input("Password", type="password", key="signup_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
        if st.button("Signup"):
            if not name or not new_email or not new_pass:
                st.error("Please fill all fields!")
            elif not is_valid_email(new_email):
                st.error("Please enter a valid email!")
            elif len(new_pass) < 6:
                st.error("Password must be at least 6 characters!")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match!")
            else:
                try:
                    hashed = hash_password(new_pass)
                    c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, new_email, hashed))
                    conn.commit()
                    st.success("Account Created! Now please Login.")
                except sqlite3.IntegrityError:
                    st.error("This email is already registered!")
    st.stop()

# ---------- AFTER LOGIN ----------
st.sidebar.title("🎓 Menu")
st.sidebar.write(f"Welcome, {st.session_state.user_email}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

page = st.sidebar.selectbox("Go to", ["Dashboard", "Home", "Predict Academic Risk", "Student Records", "About"])

def get_data():
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    if rows:
        return pd.DataFrame(rows, columns=["Name", "Attendance %", "Previous Marks %", "Study Hours", "Assignments", "Sleep Hours", "Risk"])
    else:
        return pd.DataFrame(columns=["Name", "Attendance %", "Previous Marks %", "Study Hours", "Assignments", "Sleep Hours", "Risk"])

df = get_data()

# ================= DASHBOARD =================
if page == "Dashboard":
    st.title("🎓 Student Academic Risk System")
    st.subheader("📊 Professional Dashboard")
    st.write("This dashboard gives a complete overview of all students, their performance, attendance and risk level at a glance.")

    # --- INFO BOXES ---
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**🎯 Purpose**\n\nFind weak students early before final exams.")
    with col_b:
        st.info("**👩‍🏫 For Teachers**\n\nCheck who needs extra attention and counselling.")
    with col_c:
        st.info("**📈 How it Works**\n\nAttendance + Marks + Study Hours + Assignments = Risk Score")

    st.divider()

    if df.empty:
        st.warning("No student added yet. Dashboard will show data after you add students.")
        st.info("👉 Go to 'Predict Academic Risk' page, add 3-4 students, then come back here. Dashboard will become full and professional.")
        # Demo preview for presentation
        st.subheader("📊 Dashboard Preview (After Adding Students)")
        st.write("Total Students | Average Marks | Average Attendance | High Risk Students")
        st.write("Charts, Risk Distribution and Top Risky Students will appear here automatically.")
    else:
        # --- TOP KPI CARDS ---
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Total Students", len(df))
        col2.metric("📚 Average Marks", f"{df['Previous Marks %'].mean():.1f}%")
        col3.metric("✅ Average Attendance", f"{df['Attendance %'].mean():.1f}%")
        high_risk = len(df[df["Risk"] == "High Risk"])
        col4.metric("🚨 High Risk Students", high_risk)

        st.divider()

        # --- SEARCH + FILTER ---
        st.subheader("🔍 Search & Filter Students")
        search = st.text_input("Search Student by Name")
        risk_filter = st.selectbox("Filter by Risk Level", ["All", "Low Risk", "Medium Risk", "High Risk"])

        filtered_df = df.copy()
        if search:
            filtered_df = filtered_df[filtered_df["Name"].str.contains(search, case=False, na=False)]
        if risk_filter != "All":
            filtered_df = filtered_df[filtered_df["Risk"] == risk_filter]

        # --- CHARTS ---
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.subheader("📊 Marks Comparison")
            st.bar_chart(filtered_df, x="Name", y="Previous Marks %")
        with col_chart2:
            st.subheader("📊 Attendance Comparison")
            st.bar_chart(filtered_df, x="Name", y="Attendance %")

        col_chart3, col_chart4 = st.columns(2)
        with col_chart3:
            st.subheader("⚠️ Risk Distribution")
            risk_count = df["Risk"].value_counts()
            st.bar_chart(risk_count)
            st.write(risk_count)
        with col_chart4:
            st.subheader("🚨 Top 5 Students Needing Help")
            # Lowest marks = most need help
            top_risky = df.sort_values(by="Previous Marks %").head(5)
            st.dataframe(top_risky[["Name", "Previous Marks %", "Attendance %", "Risk"]], use_container_width=True)

        st.divider()
        st.subheader("📋 All Students - Filtered Result")
        st.dataframe(filtered_df, use_container_width=True)

# ================= HOME =================
elif page == "Home":
    st.title("Student Academic Risk System")
    st.subheader("🏠 Home")
    st.write("Welcome to Student Academic Risk System. This system helps teachers to find students at risk early.")
    search = st.text_input("Search Student by Name")
    if search:
        result = df[df["Name"].str.contains(search, case=False, na=False)]
        st.dataframe(result)
    else:
        st.dataframe(df)

# ================= PREDICT =================
elif page == "Predict Academic Risk":
    st.title("Student Academic Risk System")
    st.subheader("🔮 Predict Academic Risk")
    st.write("Enter student details to predict risk. Result will be saved in Database.")
    name = st.text_input("Student Name")
    attendance = st.slider("Attendance %", 0, 100, 70)
    previous_marks = st.slider("Previous Marks %", 0, 100, 60)
    study_hours = st.slider("Study Hours per Day", 0, 10, 3)
    assignments = st.slider("Assignments Completed %", 0, 100, 70)
    sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
    if st.button("Predict Risk"):
        if not name:
            st.error("Please enter Student Name!")
        else:
            score = (attendance * 0.3) + (previous_marks * 0.3) + (assignments * 0.2) + (study_hours * 5)
            if score > 100:
                score = 100
            pass_chance = score
            fail_chance = 100 - score
            if score >= 70:
                risk = "Low Risk"
                st.success(f"{name} is at {risk} - Score: {score:.1f}")
            elif score >= 45:
                risk = "Medium Risk"
                st.warning(f"{name} is at {risk} - Score: {score:.1f}")
            else:
                risk = "High Risk"
                st.error(f"{name} is at {risk} - Score: {score:.1f}")
            st.subheader(f"📊 Prediction for {name} in Graph")
            col1, col2 = st.columns(2)
            col1.metric("Pass Chance", f"{pass_chance:.1f}%")
            col2.metric("Fail Chance", f"{fail_chance:.1f}%")
            st.progress(int(pass_chance))
            chart_data = pd.DataFrame({"Result": ["Pass Chance", "Fail Chance"], "Percentage": [pass_chance, fail_chance]})
            st.bar_chart(chart_data, x="Result", y="Percentage")
            st.info(f"Result: {name} has {fail_chance:.1f}% chance of failure and {pass_chance:.1f}% chance of passing.")
            c.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?)", (name, attendance, previous_marks, study_hours, assignments, sleep_hours, risk))
            conn.commit()
            st.success(f"{name} data saved in Database successfully! Now this student will show on Dashboard.")

# ================= RECORDS =================
elif page == "Student Records":
    st.title("Student Academic Risk System")
    st.subheader("📋 Student Records")
    if df.empty:
        st.warning("No record found. Please go to Predict page and add a student.")
    else:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download as CSV", data=csv, file_name="student_records.csv", mime="text/csv")

# ================= ABOUT =================
elif page == "About":
    st.title("Student Academic Risk System")
    st.subheader("ℹ️ About This Project")
    st.write("**Project Name:** Student Academic Risk System")
    st.write("**Made By:** Benish Seher")
    st.write("**Purpose:** To predict academic risk early so teachers can help students before final exams.")
    st.write("**Technology:** Python, Streamlit, SQLite Database, Pandas")
    st.write("**Features:** Login, Signup, Dashboard, Prediction with Graph, Student Records, Security Checks")
    st.write("**Security:** Password Hashing, Email Validation, Empty Field Check, Password Length Check, .gitignore for sensitive files.")