
import streamlit as st
import sqlite3
import hashlib

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="wide"
)

# =========================
# PASSWORD HASH FUNCTION
# =========================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.block-container {
    padding-top: 3rem;
}

.login-header {
    padding: 35px;
    border-radius: 20px;
    background: linear-gradient(135deg, #8B0000, #D32F2F);
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.login-card {
    padding: 30px;
    border-radius: 18px;
    background-color: white;
    border: 1px solid #eeeeee;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("## 🩸 Smart Blood")

    st.write(
        "Blood Donation Management System"
    )

    st.divider()

    st.markdown("### 🔐 Login")

    st.write(
        "Login using your registered "
        "email and password."
    )


# =========================
# HEADER
# =========================

st.markdown("""
<div class="login-header">

<h1>🔐 Smart Blood Donation</h1>

<p>Login to your account</p>

</div>
""", unsafe_allow_html=True)


# =========================
# LOGIN FORM
# =========================

st.subheader("👤 User Login")

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

    login = st.form_submit_button(
        "🔐 Login",
        use_container_width=True
    )


# =========================
# LOGIN PROCESS
# =========================

if login:

    if email == "":
        st.error("❌ Please enter your email.")

    elif password == "":
        st.error("❌ Please enter your password.")

    else:

        try:

            conn = sqlite3.connect(
                "blood_donation.db"
            )

            cursor = conn.cursor()

            hashed_password = hash_password(
                password
            )

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

            if user:

                st.success(
                    f"✅ Welcome, {user[1]}!"
                )

                st.info(
                    f"Role: {user[3]}"
                )

            else:

                st.error(
                    "❌ Invalid email or password."
                )

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )


st.divider()

st.info(
    "💡 New users will be able to create "
    "an account through the Registration option "
    "that we will add next."
)

st.divider()

st.caption(
    "🩸 Smart Blood Donation Management System | Login"
)