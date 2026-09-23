import streamlit as st
import sqlite3


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================
# LOGIN CHECK
# =========================

if not st.session_state.get("logged_in", False):
    st.warning("🔐 Please login first to access Dashboard.")
    st.stop()


# =========================
# DATABASE CONNECTION
# =========================

def get_connection():
    return sqlite3.connect("blood_donation.db")


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}


/* Hide Streamlit sidebar */

[data-testid="stSidebar"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}


/* Main Header */

.header {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(135deg, #8B0000, #D32F2F);
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    color: white !important;
}

.header p {
    color: white !important;
}


/* Metric Cards */

.metric-card {
    padding: 25px;
    border-radius: 18px;
    background-color: #ffffff;
    border: 1px solid #eeeeee;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    text-align: center;
    min-height: 130px;
}

.metric-card h2 {
    color: #c2185b !important;
}

.metric-card h3 {
    color: #222222 !important;
    font-size: 30px;
}

.metric-card p {
    color: #444444 !important;
    font-size: 16px;
}


/* Information Cards */

.info-card {
    padding: 22px;
    border-radius: 18px;
    background-color: #fff5f5;
    border: 1px solid #ffd6d6;
    color: #222222;
}

.info-card h3 {
    color: #8B0000 !important;
}

.info-card p {
    color: #222222 !important;
}


/* Section Headings */

h1, h2, h3 {
    color: #f5f5f5;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown("""
<div class="header">

<h1>📊 Blood Donation Dashboard</h1>

<p>
Overview of donors and blood requests in the system.
</p>

</div>
""", unsafe_allow_html=True)


# =========================
# DATABASE
# =========================

conn = get_connection()
cursor = conn.cursor()


# =========================
# TOTAL DONORS
# =========================

cursor.execute("""
    SELECT COUNT(*)
    FROM donors
""")

total_donors = cursor.fetchone()[0]


# =========================
# AVAILABLE DONORS
# =========================

cursor.execute("""
    SELECT COUNT(*)
    FROM donors
    WHERE availability = 'Available'
""")

available_donors = cursor.fetchone()[0]


# =========================
# TOTAL REQUESTS
# =========================

cursor.execute("""
    SELECT COUNT(*)
    FROM blood_requests
""")

total_requests = cursor.fetchone()[0]


# =========================
# PENDING REQUESTS
# =========================

cursor.execute("""
    SELECT COUNT(*)
    FROM blood_requests
    WHERE status = 'Pending'
""")

pending_requests = cursor.fetchone()[0]


# =========================
# BLOOD GROUP COUNTS
# =========================

cursor.execute("""
    SELECT blood_group, COUNT(*)
    FROM donors
    WHERE availability = 'Available'
    GROUP BY blood_group
    ORDER BY blood_group
""")

blood_group_data = cursor.fetchall()

conn.close()


# =========================
# METRIC CARDS
# =========================

st.subheader("📌 System Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">

        <h2>👥</h2>

        <h3>{total_donors}</h3>

        <p>Total Donors</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">

        <h2>🩸</h2>

        <h3>{available_donors}</h3>

        <p>Available Donors</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">

        <h2>🆘</h2>

        <h3>{total_requests}</h3>

        <p>Total Requests</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">

        <h2>🟠</h2>

        <h3>{pending_requests}</h3>

        <p>Pending Requests</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# BLOOD GROUP SECTION
# =========================

st.divider()

st.subheader("🩸 Available Donors by Blood Group")


if blood_group_data:

    col1, col2 = st.columns(2)

    with col1:

        for group, count in blood_group_data:

            st.markdown(
                f"""
                <div class="info-card">

                <h3>🩸 {group}</h3>

                <p>
                <b>{count}</b> available donor(s)
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")


    with col2:

        chart_data = {
            "Blood Group": [
                group
                for group, count in blood_group_data
            ],
            "Available Donors": [
                count
                for group, count in blood_group_data
            ]
        }

        st.bar_chart(
            chart_data,
            x="Blood Group",
            y="Available Donors"
        )


else:

    st.info(
        "📭 No available donors found."
    )


# =========================
# CURRENT USER
# =========================

st.divider()

st.markdown(
    f"""
    <div class="info-card">

    <h3>👤 Current User</h3>

    <p>
    <b>Name:</b> {st.session_state.user_name}
    </p>

    <p>
    <b>Role:</b> {st.session_state.user_role}
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# INFORMATION
# =========================

st.divider()

st.markdown("""
### ℹ️ About Dashboard

This dashboard provides a quick overview of:

- Registered blood donors
- Currently available donors
- Total blood requests
- Pending blood requests
- Blood group-wise donor availability

The information is retrieved from the SQLite database used by the application.
""")


# =========================
# NAVIGATION
# =========================

st.divider()

back_col, home_col = st.columns(2)


with back_col:

    if st.button(
        "⬅️ Back: Blood Requests",
        use_container_width=True
    ):
        st.switch_page("pages/4_Blood_Requests.py")


with home_col:

    if st.button(
        "🏠 Back to Home",
        use_container_width=True
    ):
        st.switch_page("app.py")