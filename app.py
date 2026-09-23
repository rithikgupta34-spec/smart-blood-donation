import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
from database import create_database

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="Smart Blood Donation",
    page_icon="🩸",
    layout="wide"
)

create_database()

# =========================
# PASSWORD HASH
# =========================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# DATABASE FUNCTIONS
# =========================

def create_user(name, email, password, role):
    conn = sqlite3.connect("blood_donation.db")
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password,
                role
            )
        )

        conn.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def login_user(email, password):
    conn = sqlite3.connect("blood_donation.db")
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT id, name, email, role
        FROM users
        WHERE email = ?
        AND password = ?
        """,
        (
            email,
            hashed_password
        )
    )

    user = cursor.fetchone()
    conn.close()

    return user

# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = ""

# =========================
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>

    /* Hide Streamlit sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .block-container {
        padding-top: 2rem;
    }

    .hero {
        padding: 40px;
        border-radius: 20px;
        background: linear-gradient(135deg, #8B0000, #D32F2F);
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 40px;
        color: white !important;
    }

    .hero p {
        color: white !important;
        font-size: 18px;
    }

    .card {
        padding: 25px;
        border-radius: 18px;
        background-color: white;
        border: 1px solid #eeeeee;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 160px;
    }

    .card h3 {
        color: #8B0000 !important;
    }

    .card p {
        color: #333333 !important;
    }

    .info-box {
        padding: 25px;
        border-radius: 18px;
        background-color: #fff5f5;
        border: 1px solid #ffd6d6;
    }

    .info-box h3 {
        color: #8B0000 !important;
    }

    .info-box p {
        color: #333333 !important;
    }

    .footer {
        text-align: center;
        color: #777777;
        margin-top: 40px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOGIN / REGISTER SCREEN
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="hero">

        <h1>🩸 Smart Blood Donation</h1>

        <p>Blood Donation Management System</p>

        <p>
        Connecting blood donors with people who need blood.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # =========================
    # LOGIN
    # =========================

    with login_tab:

        st.subheader("👋 Welcome Back")

        st.write(
            "Login to access the Blood Donation Management System."
        )

        with st.form("login_form"):

            email = st.text_input(
                "Email Address",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            login_button = st.form_submit_button(
                "🔐 Login",
                use_container_width=True
            )

        if login_button:

            if email.strip() == "":
                st.error("❌ Please enter your email.")

            elif password == "":
                st.error("❌ Please enter your password.")

            else:

                user = login_user(
                    email.strip(),
                    password
                )

                if user:

                    conn = sqlite3.connect("blood_donation.db")
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        INSERT INTO activity_logs
                        (user_id, user_name, activity, date_time)
                        VALUES (?, ?, ?, ?)
                        """,
                        (
                            user[0],
                            user[1],
                            "Login",
                            datetime.now().strftime(
                                "%d-%m-%Y %H:%M:%S"
                            )
                        )
                    )

                    conn.commit()
                    conn.close()

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.session_state.user_role = user[3]

                    st.success("✅ Login successful!")
                    st.rerun()

                else:
                    st.error("❌ Invalid email or password.")

    # =========================
    # REGISTER
    # =========================

    with register_tab:

        st.subheader("📝 Create New Account")

        st.write(
            "Register as a donor or receiver."
        )

        with st.form("register_form"):

            name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            role = st.selectbox(
                "Account Type",
                [
                    "Donor",
                    "Receiver"
                ]
            )

            register_button = st.form_submit_button(
                "📝 Create Account",
                use_container_width=True
            )

        if register_button:

            if name.strip() == "":
                st.error("❌ Please enter your name.")

            elif email.strip() == "":
                st.error("❌ Please enter your email.")

            elif password == "":
                st.error("❌ Please enter a password.")

            elif len(password) < 6:
                st.error(
                    "❌ Password must contain at least 6 characters."
                )

            else:

                success, message = create_user(
                    name.strip(),
                    email.strip(),
                    password,
                    role
                )

                if success:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "Now open the Login tab and login with your account."
                    )

                else:

                    st.error(
                        f"❌ {message}"
                    )

# =========================================================
# LOGGED-IN HOME / FIRST STEP
# =========================================================

else:

    st.markdown(
        f"""
        <div class="hero">

        <h1>🩸 Welcome, {st.session_state.user_name}!</h1>

        <p>
        Smart Blood Donation Management System
        </p>

        <p>
        Your account is successfully logged in.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔄 Blood Donation Process")

    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.markdown(
            """
            <div class="card">
            <h3>1️⃣</h3>
            <b>Donor Registration</b>
            <p>Add donor information.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step2:
        st.markdown(
            """
            <div class="card">
            <h3>2️⃣</h3>
            <b>Find Blood</b>
            <p>Search available donors.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step3:
        st.markdown(
            """
            <div class="card">
            <h3>3️⃣</h3>
            <b>Request Blood</b>
            <p>Submit blood requirements.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step4:
        st.markdown(
            """
            <div class="card">
            <h3>4️⃣</h3>
            <b>Dashboard</b>
            <p>View system information.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.info(
        "You are logged in. Click Next to start the blood donation process."
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "➡️ Next: Donor Registration",
            use_container_width=True,
            type="primary"
        ):
            st.switch_page(
                "pages/1_Donor_Registration.py"
            )

    # =========================
    # DEVELOPER ACCESS
    # =========================

    if st.session_state.user_role == "Developer":

        st.divider()

        st.subheader("👨‍💻 Developer Access")

        if st.button(
            "👨‍💻 Open Developer Dashboard",
            use_container_width=True
        ):
            st.switch_page(
                "pages/7_Developer_Dashboard.py"
            )

    # =========================
    # CURRENT USER
    # =========================

    st.divider()

    st.markdown(
        f"""
        <div class="info-box">

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

    st.divider()

    logout_col1, logout_col2, logout_col3 = st.columns([1, 2, 1])

    with logout_col2:

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.user_name = ""
            st.session_state.user_role = ""

            st.rerun()

# =========================
# FOOTER
# =========================

st.markdown(
    """
    <div class="footer">

    🩸 Smart Blood Donation Management System

    <br>

    BSc IT Final Year Project

    </div>
    """,
    unsafe_allow_html=True
)