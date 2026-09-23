import streamlit as st
import sqlite3
from datetime import datetime


# =========================
# LOGIN CHECK
# =========================

if not st.session_state.get("logged_in", False):
    st.warning("🔐 Please login first to access Find Blood.")
    st.stop()


# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Find Blood",
    page_icon="🔍",
    layout="wide"
)


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


/* Hide Sidebar */

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


/* Result Card */

.result-card {
    padding: 20px;
    border-radius: 15px;
    background-color: #fff5f5;
    border: 1px solid #ffd6d6;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown("""
<div class="header">

<h1>🔍 Find Blood</h1>

<p>
Search for available blood donors by blood group and city.
</p>

</div>
""", unsafe_allow_html=True)


# =========================
# SEARCH SECTION
# =========================

st.subheader("🩸 Search Available Donors")

col1, col2 = st.columns(2)


with col1:

    blood_group = st.selectbox(
        "Select Blood Group",
        [
            "All",
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


with col2:

    city = st.text_input(
        "City",
        placeholder="Enter city (optional)"
    )


search_button = st.button(
    "🔍 Search Blood",
    use_container_width=True
)


# =========================
# SEARCH DONORS
# =========================

if search_button:

    conn = get_connection()
    cursor = conn.cursor()


    # =========================
    # ALL BLOOD + ALL CITY
    # =========================

    if blood_group == "All" and city.strip() == "":

        cursor.execute("""
            SELECT
                name,
                age,
                gender,
                blood_group,
                phone,
                city,
                availability
            FROM donors
            WHERE availability = 'Available'
            ORDER BY id DESC
        """)

        donors = cursor.fetchall()


    # =========================
    # SPECIFIC BLOOD + ALL CITY
    # =========================

    elif blood_group != "All" and city.strip() == "":

        cursor.execute("""
            SELECT
                name,
                age,
                gender,
                blood_group,
                phone,
                city,
                availability
            FROM donors
            WHERE blood_group = ?
            AND availability = 'Available'
            ORDER BY id DESC
        """, (blood_group,))

        donors = cursor.fetchall()


    # =========================
    # ALL BLOOD + SPECIFIC CITY
    # =========================

    elif blood_group == "All" and city.strip() != "":

        cursor.execute("""
            SELECT
                name,
                age,
                gender,
                blood_group,
                phone,
                city,
                availability
            FROM donors
            WHERE city LIKE ?
            AND availability = 'Available'
            ORDER BY id DESC
        """, (f"%{city.strip()}%",))

        donors = cursor.fetchall()


    # =========================
    # SPECIFIC BLOOD + SPECIFIC CITY
    # =========================

    else:

        cursor.execute("""
            SELECT
                name,
                age,
                gender,
                blood_group,
                phone,
                city,
                availability
            FROM donors
            WHERE blood_group = ?
            AND city LIKE ?
            AND availability = 'Available'
            ORDER BY id DESC
        """, (
            blood_group,
            f"%{city.strip()}%"
        ))

        donors = cursor.fetchall()


    conn.close()


    # =========================
    # SAVE SEARCH ACTIVITY
    # =========================

    conn_log = get_connection()
    cursor_log = conn_log.cursor()

    cursor_log.execute(
        """
        INSERT INTO activity_logs
        (user_id, user_name, activity, date_time)
        VALUES (?, ?, ?, ?)
        """,
        (
            st.session_state.user_id,
            st.session_state.user_name,
            f"Blood Search - {blood_group}"
            + (f" - {city.strip()}" if city.strip() else ""),
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        )
    )

    conn_log.commit()
    conn_log.close()


    # =========================
    # DISPLAY RESULTS
    # =========================

    if donors:

        st.success(
            f"✅ {len(donors)} available donor(s) found."
        )

        for donor in donors:

            name = donor[0]
            age = donor[1]
            gender = donor[2]
            group = donor[3]
            phone = donor[4]
            donor_city = donor[5]
            availability = donor[6]

            st.markdown(
                f"""
                <div style="
                    background-color: white;
                    color: #222222;
                    padding: 25px;
                    border-radius: 15px;
                    border: 1px solid #dddddd;
                    margin-bottom: 20px;
                ">

                <h3 style="color: #c2185b;">
                    🩸 {name}
                </h3>

                <p style="color: #222222;">
                    <b>Blood Group:</b> {group}
                </p>

                <p style="color: #222222;">
                    <b>Age:</b> {age}
                </p>

                <p style="color: #222222;">
                    <b>Gender:</b> {gender}
                </p>

                <p style="color: #222222;">
                    <b>City:</b> {donor_city}
                </p>

                <p style="color: #222222;">
                    <b>Phone:</b> {phone}
                </p>

                <p style="color: #222222;">
                    <b>Availability:</b> {availability}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.warning(
            "⚠️ No available donor found for your search."
        )


# =========================
# IMPORTANT INFORMATION
# =========================

st.divider()

st.markdown("""
### ℹ️ Important Information

- Donor availability can change.
- Please contact the donor before proceeding.
- Blood group compatibility should be confirmed by a qualified healthcare professional or blood bank.
- This system is intended for managing donor information and requests.
""")


# =========================
# NAVIGATION
# =========================

st.divider()

st.subheader("➡️ Continue")


back_col, next_col = st.columns(2)


with back_col:

    if st.button(
        "⬅️ Back: Donor Registration",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_Donor_Registration.py"
        )


with next_col:

    if st.button(
        "Next: Request Blood ➡️",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Request_Blood.py"
        )