import sqlite3


# =========================
# DATABASE CONNECTION
# =========================

def get_connection():
    return sqlite3.connect("blood_donation.db")


# =========================
# CREATE DATABASE TABLES
# =========================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # Users Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # -------------------------
    # Donors Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            blood_group TEXT,
            phone TEXT,
            city TEXT,
            last_donation_date TEXT,
            availability TEXT
        )
    """)

    # -------------------------
    # Blood Requests Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blood_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receiver_name TEXT NOT NULL,
            blood_group TEXT,
            units_required INTEGER,
            hospital TEXT,
            city TEXT,
            phone TEXT,
            request_date TEXT,
            status TEXT
        )
    """)

    # -------------------------
    # Activity Logs Table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            activity TEXT,
            date_time TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# RUN DATABASE SETUP
# =========================

create_database()