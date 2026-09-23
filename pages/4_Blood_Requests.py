import streamlit as st
import sqlite3


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Blood Requests",
    page_icon="🆘",
    layout="wide"
)


# =========================
# LOGIN CHECK
# =========================

if not st.session_state.get("logged_in", False):

    st.warning(
        "🔐 Please login first to access Blood Requests."
    )

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


/* Header */

.header {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(135deg, #8B0000, #D32F2F);
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

.header h1 {
    color: white !important;
}

.header p {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown("""
<div class="header">

<h1>🆘 Blood Requests</h1>

<p>
View submitted blood requirements.
</p>

</div>
""", unsafe_allow_html=True)


# =========================
# LOGGED-IN USER
# =========================

st.info(
    f"👤 Logged in as: **{st.session_state.user_name}**"
)


# =========================
# GET BLOOD REQUESTS
# =========================

try:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            receiver_name,
            blood_group,
            units_required,
            hospital,
            city,
            phone,
            request_date,
            status
        FROM blood_requests
        ORDER BY id DESC
        """
    )

    requests = cursor.fetchall()

    conn.close()


except Exception as e:

    st.error(
        f"❌ Something went wrong: {e}"
    )

    requests = []


# =========================
# DISPLAY REQUESTS
# =========================

if requests:

    st.success(
        f"📋 {len(requests)} blood request(s) found."
    )

    for request in requests:

        receiver_name = request[0]
        blood_group = request[1]
        units_required = request[2]
        hospital = request[3]
        city = request[4]
        phone = request[5]
        request_date = request[6]
        status = request[7]

        if status == "Pending":
            status_message = "🟠 Pending"

        elif status == "Completed":
            status_message = "🟢 Completed"

        else:
            status_message = f"🔵 {status}"


        # Request Card

        with st.container(border=True):

            st.subheader(
                f"🩸 {blood_group} Blood Required"
            )

            st.write(
                f"**Receiver:** {receiver_name}"
            )

            st.write(
                f"**Units Required:** {units_required}"
            )

            st.write(
                f"**Hospital:** {hospital}"
            )

            st.write(
                f"**City:** {city}"
            )

            st.write(
                f"**Contact:** {phone}"
            )

            st.write(
                f"**Request Date:** {request_date}"
            )

            st.write(
                f"**Status:** {status_message}"
            )

            st.write("")


else:

    st.info(
        "📭 No blood requests have been submitted yet."
    )


# =========================
# INFORMATION
# =========================

st.divider()

st.markdown("""
### ℹ️ Important Information

- Requests shown here are submitted through the system.
- Request status may change as the blood requirement is handled.
- Contact details should be used only for genuine blood-related communication.
- Blood compatibility and transfusion decisions must be confirmed by qualified healthcare professionals or a blood bank.
""")


# =========================
# NAVIGATION
# =========================

st.divider()

back_col, next_col = st.columns(2)


with back_col:

    if st.button(
        "⬅️ Back: Request Blood",
        use_container_width=True
    ):
        st.switch_page("pages/3_Request_Blood.py")


with next_col:

    if st.button(
        "Next: Dashboard ➡️",
        use_container_width=True
    ):
        st.switch_page("pages/5_Dashboard.py")