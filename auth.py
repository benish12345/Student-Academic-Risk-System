
import sqlite3
import bcrypt
import os

# Create database folder if it does not exist
os.makedirs("database", exist_ok=True)

DB_NAME = "database/auth.db"


# Connect to database
def connect_db():
    return sqlite3.connect(DB_NAME)


# Create users table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Register new user
def signup_user(username, email, password):

    if not username.strip() or not email.strip() or not password:
        return False, "All fields are required."

    if "@" not in email or "." not in email:
        return False, "Please enter a valid email."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username.strip(), email.strip().lower(), hashed_password)
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."


# Login existing user
def login_user(email, password):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password FROM users WHERE email = ?",
        (email.strip().lower(),)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return False, None

    username, stored_password = user

    # Verify password
    if bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    ):
        return True, username

    return False, None


# Create database table automatically
create_table()
