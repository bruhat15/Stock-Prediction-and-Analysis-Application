import streamlit as st
import hashlib
import sqlite3
import re
import stock  # Import the stock module

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            username TEXT,
            password TEXT,
            phone_number TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new user
def add_user(username, email, password, phone_number):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute('INSERT INTO users (email, username, password, phone_number) VALUES (?, ?, ?, ?)', 
              (email, username, hashed_password, phone_number))
    conn.commit()
    conn.close()

# Function to check if the user exists
def verify_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# Function to get user info
def get_user_info(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, phone_number FROM users WHERE email = ?', (email,))
    user_info = c.fetchone()
    conn.close()
    return user_info

# Function to validate email
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Function to validate phone number
def is_valid_phone_number(phone_number):
    return len(phone_number) == 10 and phone_number.isdigit()

# Function to validate password
def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

# CSS Styling
def apply_css():
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            color: #4CAF50;
            font-size: 36px;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            color: #333;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: 10px;
        }
        .card-header {
            font-size: 18px;
            font-weight: bold;
            color: #495057;
            margin-bottom: 10px;
        }
        .price {
            color: #007bff;
            font-size: 24px;
            font-weight: bold;
        }
        .ticker-symbol {
            font-size: 20px;
            color: #6c757d;
            margin-bottom: 5px;
        }
        .graph-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }
        .graph {
            flex: 1;
            min-width: 300px;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #ffffff;
        }
        .graph h3 {
            text-align: center;
            color: #495057;
        }
        .graph .plotly-graph {
            border: none;
            box-shadow: none;
        }
        .graph-container .graph {
            flex: 1 1 calc(33% - 40px);
        }
        @media (max-width: 768px) {
            .graph-container .graph {
                flex: 1 1 100%;
            }
        }
        .card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
        }
        .card {
            flex: 1 1 calc(33% - 40px);
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .card-header {
            font-size: 18px;
            font-weight: bold;
            color: #495057;
            margin-bottom: 10px;
        }
        .price {
            color: #007bff;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Main function to handle login and signup
def login():
    
    # Apply CSS styling
    apply_css()

    # Initialize the database
    init_db()

    # State to switch between login and signup
    if "signup_mode" not in st.session_state:
        st.session_state.signup_mode = False

    # State to check if the user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.signup_mode:
        # Signup Page
        st.subheader("Signup Page")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        phone_number = st.text_input("Phone Number")

        st.info(
            "Password must be at least 8 characters long, "
            "include at least one capital letter, a number, and a special character."
        )

        if st.button("Signup"):
            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif not is_valid_phone_number(phone_number):
                st.error("Phone number must be exactly 10 digits.")
            elif not is_valid_password(password):
                st.error("Password does not meet the required criteria.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    add_user(username, email, password, phone_number)
                    st.success("Account created successfully!")
                    st.session_state.signup_mode = False  # Switch back to login after signup
                except sqlite3.IntegrityError:
                    st.error("Email already exists. Please use another one.")

        if st.button("Back to Login"):
            st.session_state.signup_mode = False

    elif not st.session_state.logged_in:
        # Login Page
        st.subheader("Login Page")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        st.markdown("password must be at least 8 characters long")
        if st.button("Login"):
            user = verify_user(email, password)
            if user:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.email = email
                st.experimental_rerun()  # Refresh to load the main content
            else:
                st.error("Invalid email or password.")

        if st.button("Signup"):
            st.session_state.signup_mode = True

    if st.session_state.logged_in:
        user_info = get_user_info(st.session_state.email)
        st.write(f"Welcome, {user_info[0]}!")
        
        stock.main()

if __name__ == "__main__":
  login()