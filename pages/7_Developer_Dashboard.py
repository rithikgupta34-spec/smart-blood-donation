import streamlit as st
import sqlite3

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Developer Dashboard",
    page_icon="👨‍💻",
    layout="wide"
)

# =========================
# LOGIN CHECK
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔐 Please login first.")
    st.stop()

# =========================
# DEVELOPER CHECK
# =========================

if st.session_state.user_role != "Developer":
    st.error("🚫 Access Denied")
    st.write("This page is only available for the Developer.")
    st.stop()

# =========================
# DATABASE CONNECTION
# =========================

conn = sqlite3.connect("blood_donation.db")
cursor = conn.cursor()

# =========================
# PAGE HEADER
# =========================

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #8B0000, #D32F2F);
        padding: 25px;
        border-radius: 0px 0px 20px 20px;
        text-align: center;
        color: white;
    ">
        <h1>👨‍💻 Developer Dashboard</h1>
        <p>System monitoring and user activity overview</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

st.info(
    f"👋 Welcome, {st.session_state.user_name}"
)

# =========================
# SYSTEM COUNTS
# =========================

cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM donors")
total_donors = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM blood_requests")
total_requests = cursor.fetchone()[0]

cursor.execute(
    "SELECT COUNT(*) FROM activity_logs"
)
total_activities = cursor.fetchone()[0]

# =========================
# METRICS
# =========================

st.subheader("📊 System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Users",
        total_users
    )

with col2:
    st.metric(
        "🩸 Total Donors",
        total_donors
    )

with col3:
    st.metric(
        "🏥 Blood Requests",
        total_requests
    )

with col4:
    st.metric(
        "📝 Total Activities",
        total_activities
    )

st.divider()

# =========================
# REGISTERED USERS
# =========================

st.subheader("👥 Registered Users")

cursor.execute(
    """
    SELECT id, name, email, role
    FROM users
    ORDER BY id DESC
    """
)

users = cursor.fetchall()

if users:

    for user in users:

        st.write(
            f"**{user[1]}**  |  "
            f"{user[2]}  |  "
            f"Role: **{user[3]}**"
        )

else:

    st.info("No users registered yet.")

st.divider()

# =========================
# ACTIVITY LOG
# =========================

st.subheader("🕒 Recent System Activity")

cursor.execute(
    """
    SELECT user_name, activity, date_time
    FROM activity_logs
    ORDER BY id DESC
    LIMIT 20
    """
)

activities = cursor.fetchall()

if activities:

    for activity in activities:

        st.write(
            f"👤 **{activity[0]}**  →  "
            f"**{activity[1]}**  →  "
            f"🕒 {activity[2]}"
        )

else:

    st.info("No activity recorded yet.")

conn.close()

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button(
        "🏠 Back to Home",
        use_container_width=True
    ):
        st.switch_page("app.py")