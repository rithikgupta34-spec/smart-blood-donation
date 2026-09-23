import streamlit as st
import sqlite3
from datetime import date, datetime


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Donor Registration",
    page_icon="🩸",
    layout="wide"
)


# =========================
# LOGIN CHECK
# =========================

if not st.session_state.get("logged_in", False):
    st.warning("🔐 Please login first to access Donor Registration.")
    st.stop()


# =========================
# DATABASE CONNECTION
# =========================

def get_connection():
    return sqlite3.connect("blood_donation.db")


# =========================
# ADD USER ID COLUMN
# =========================

def prepare_donor_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(donors)")

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "user_id" not in columns:

        cursor.execute(
            "ALTER TABLE donors ADD COLUMN user_id INTEGER"
        )

    conn.commit()
    conn.close()


prepare_donor_table()


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}


/* Hide Streamlit Sidebar */

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


/* Form Card */

.form-card {
    padding: 25px;
    border-radius: 18px;
    background-color: #ffffff;
    border: 1px solid #eeeeee;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}


/* Form Labels */

label {
    color: #222222 !important;
}

label p {
    color: #222222 !important;
}


/* Text Input */

input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}

input::placeholder {
    color: #777777 !important;
    -webkit-text-fill-color: #777777 !important;
}


/* Select Box */

div[data-baseweb="select"] {
    color: #222222 !important;
}

div[data-baseweb="select"] * {
    color: #222222 !important;
}


/* Number Input */

div[data-testid="stNumberInput"] input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}


/* Date Input */

div[data-testid="stDateInput"] input {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
}


/* Navigation Buttons */

.nav-button {
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown("""
<div class="header">

<h1>🩸 Donor Registration</h1>

<p>
Register your information to help people find blood donors.
</p>

</div>
""", unsafe_allow_html=True)


# =========================
# LOGGED-IN USER
# =========================

st.info(
    f"👤 Logged in as: **{st.session_state.user_name}** "
    f"({st.session_state.user_role})"
)


# =========================
# DONOR FORM
# =========================

st.subheader("📝 Enter Donor Information")


with st.form("donor_registration_form"):

    col1, col2 = st.columns(2)


    # =========================
    # LEFT COLUMN
    # =========================

    with col1:

        name = st.text_input(
            "Full Name",
            placeholder="Enter donor name"
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=65,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            [
                "Select Gender",
                "Male",
                "Female",
                "Other"
            ]
        )

        blood_group = st.selectbox(
            "Blood Group",
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


    # =========================
    # RIGHT COLUMN
    # =========================

    with col2:

        phone = st.text_input(
            "Phone Number",
            placeholder="Enter 10-digit phone number"
        )

        city = st.text_input(
            "City",
            placeholder="Enter your city"
        )

        last_donation_date = st.date_input(
            "Last Donation Date",
            value=date.today()
        )

        availability = st.selectbox(
            "Current Availability",
            [
                "Available",
                "Not Available"
            ]
        )


    st.write("")

    submit_button = st.form_submit_button(
        "🩸 Register as Donor",
        use_container_width=True
    )


# =========================
# SAVE DONOR
# =========================

if submit_button:

    if name.strip() == "":
        st.error("❌ Please enter donor name.")

    elif gender == "Select Gender":
        st.error("❌ Please select gender.")

    elif blood_group == "Select Blood Group":
        st.error("❌ Please select blood group.")

    elif phone.strip() == "":
        st.error("❌ Please enter phone number.")

    elif not phone.isdigit() or len(phone) != 10:
        st.error("❌ Please enter a valid 10-digit phone number.")

    elif city.strip() == "":
        st.error("❌ Please enter city.")

    else:

        try:

            conn = get_connection()
            cursor = conn.cursor()


            # =========================
            # CHECK EXISTING DONOR
            # =========================

            cursor.execute(
                """
                SELECT id
                FROM donors
                WHERE user_id = ?
                """,
                (st.session_state.user_id,)
            )

            existing_donor = cursor.fetchone()


            if existing_donor:

                st.warning(
                    "⚠️ You have already registered as a donor."
                )


            else:

                # =========================
                # INSERT DONOR
                # =========================

                cursor.execute(
                    """
                    INSERT INTO donors
                    (
                        user_id,
                        name,
                        age,
                        gender,
                        blood_group,
                        phone,
                        city,
                        last_donation_date,
                        availability
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        st.session_state.user_id,
                        name,
                        age,
                        gender,
                        blood_group,
                        phone,
                        city,
                        str(last_donation_date),
                        availability
                    )
                )

                conn.commit()


                # =========================
                # SAVE ACTIVITY LOG
                # =========================

                cursor.execute(
                    """
                    INSERT INTO activity_logs
                    (user_id, user_name, activity, date_time)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        st.session_state.user_id,
                        st.session_state.user_name,
                        "Donor Registration",
                        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    )
                )

                conn.commit()


                st.success(
                    "✅ Donor registration completed successfully!"
                )

                st.balloons()


            conn.close()


        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )


# =========================
# INFORMATION
# =========================

st.divider()

st.markdown("""
### ℹ️ Important Information

- Please enter correct donor information.
- Keep your phone number updated.
- Update your availability when your status changes.
- Blood donation eligibility should be confirmed with a qualified healthcare professional.
""")


# =========================
# NAVIGATION
# =========================

st.divider()

st.subheader("➡️ Continue")

back_col, next_col = st.columns(2)


with back_col:

    if st.button(
        "⬅️ Back to Home",
        use_container_width=True
    ):

        st.switch_page("app.py")


with next_col:

    if st.button(
        "Next: Find Blood ➡️",
        use_container_width=True
    ):

        st.switch_page("pages/2_Find_Blood.py")