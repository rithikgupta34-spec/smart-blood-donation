import streamlit as st
import sqlite3
from datetime import date, datetime


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Request Blood",
    page_icon="🆘",
    layout="wide"
)


# =========================
# LOGIN CHECK
# =========================

if not st.session_state.get("logged_in", False):
    st.warning("🔐 Please login first to access Blood Request.")
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


/* MAIN HEADER */

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


/* FORM LABELS */

label {
    color: #222222 !important;
}

label p {
    color: #222222 !important;
}


/* TEXT INPUT */

input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}

input::placeholder {
    color: #777777 !important;
    -webkit-text-fill-color: #777777 !important;
}


/* SELECT BOX */

div[data-baseweb="select"] {
    color: #222222 !important;
}

div[data-baseweb="select"] * {
    color: #222222 !important;
}

div[data-baseweb="select"] input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}


/* NUMBER INPUT */

div[data-testid="stNumberInput"] input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}

div[data-testid="stNumberInput"] button {
    color: #222222 !important;
}


/* DATE INPUT */

div[data-testid="stDateInput"] input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}

div[data-testid="stDateInput"] svg {
    color: #555555 !important;
}


/* FORM INPUT BACKGROUND */

div[data-baseweb="input"] {
    color: #222222 !important;
}

div[data-baseweb="input"] input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}


/* INFORMATION CARD */

.info-card {
    padding: 20px;
    border-radius: 15px;
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


/* BUTTON */

button {
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown("""
<div class="header">

<h1>🆘 Request Blood</h1>

<p>
Submit a blood requirement request.
</p>

</div>
""", unsafe_allow_html=True)


# =========================
# LOGGED-IN USER
# =========================

st.info(
    f"👤 Request submitted by: **{st.session_state.user_name}**"
)


# =========================
# REQUEST FORM
# =========================

st.subheader("📝 Blood Request Details")


with st.form("blood_request_form"):

    col1, col2 = st.columns(2)


    # LEFT COLUMN

    with col1:

        receiver_name = st.text_input(
            "Receiver Name",
            value=st.session_state.user_name,
            placeholder="Enter receiver name"
        )

        blood_group = st.selectbox(
            "Required Blood Group",
            [
                "Select Blood Group",
                "A+",
                "A-",
                "B+",
                "B-",
                "AB+",
                "AB-",
                "O+",
                "O-"
            ]
        )

        units_required = st.number_input(
            "Units Required",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )

        request_date = st.date_input(
            "Request Date",
            value=date.today()
        )


    # RIGHT COLUMN

    with col2:

        hospital = st.text_input(
            "Hospital Name",
            placeholder="Enter hospital name"
        )

        city = st.text_input(
            "City",
            placeholder="Enter city"
        )

        phone = st.text_input(
            "Contact Number",
            placeholder="Enter 10-digit phone number"
        )


    st.write("")

    submit_button = st.form_submit_button(
        "🆘 Submit Blood Request",
        use_container_width=True
    )


# =========================
# SAVE REQUEST
# =========================

if submit_button:

    if receiver_name.strip() == "":
        st.error("❌ Please enter receiver name.")

    elif blood_group == "Select Blood Group":
        st.error("❌ Please select required blood group.")

    elif hospital.strip() == "":
        st.error("❌ Please enter hospital name.")

    elif city.strip() == "":
        st.error("❌ Please enter city.")

    elif phone.strip() == "":
        st.error("❌ Please enter contact number.")

    elif not phone.isdigit() or len(phone) != 10:
        st.error("❌ Please enter a valid 10-digit phone number.")

    else:

        try:

            conn = get_connection()
            cursor = conn.cursor()


            # SAVE BLOOD REQUEST

            cursor.execute(
                """
                INSERT INTO blood_requests
                (
                    receiver_name,
                    blood_group,
                    units_required,
                    hospital,
                    city,
                    phone,
                    request_date,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    receiver_name,
                    blood_group,
                    units_required,
                    hospital,
                    city,
                    phone,
                    str(request_date),
                    "Pending"
                )
            )

            conn.commit()


            # SAVE ACTIVITY LOG

            cursor.execute(
                """
                INSERT INTO activity_logs
                (
                    user_id,
                    user_name,
                    activity,
                    date_time
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    st.session_state.user_id,
                    st.session_state.user_name,
                    f"Blood Request - {blood_group}",
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                )
            )

            conn.commit()
            conn.close()


            # SUCCESS MESSAGE

            st.success(
                "✅ Blood request submitted successfully!"
            )

            st.info(
                "Your request is currently marked as Pending."
            )

            st.balloons()


        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )


# =========================
# INFORMATION
# =========================

st.divider()

st.markdown("""
<div class="info-card">

<h3>ℹ️ Important Information</h3>

<p>
Please provide accurate hospital, city, blood group
and contact details.
</p>

<p>
Blood availability and compatibility should be confirmed
with a qualified healthcare professional or blood bank.
</p>

</div>
""", unsafe_allow_html=True)


# =========================
# NAVIGATION
# =========================

st.divider()

back_col, next_col = st.columns(2)

with back_col:

    if st.button(
        "⬅️ Back: Find Blood",
        use_container_width=True
    ):
        st.switch_page("pages/2_Find_Blood.py")


with next_col:

    if st.button(
        "Next: Blood Requests ➡️",
        use_container_width=True
    ):
        st.switch_page("pages/4_Blood_Requests.py")