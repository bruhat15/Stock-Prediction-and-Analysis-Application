import streamlit as st
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect('users.db')
    return conn

# Function to verify if the user exists
def verify_user(email, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', 
              (email, hashlib.sha256(password.encode()).hexdigest()))
    user = c.fetchone()
    conn.close()
    return user

# Function to add a new user
def add_user(username, email, password, phone_number):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email, password, phone_number) VALUES (?, ?, ?, ?)', 
              (username, email, hashlib.sha256(password.encode()).hexdigest(), phone_number))
    conn.commit()
    conn.close()

# Function to initialize the database
def init_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE,
            email TEXT PRIMARY KEY,
            password TEXT,
            phone_number TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            email TEXT,
            message TEXT,
            FOREIGN KEY(email) REFERENCES users(email)
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a message to the database
def add_message(email, message):
    conn = connect_db()
    c = conn.cursor()
    c.execute('INSERT INTO messages (email, message) VALUES (?, ?)', (email, message))
    conn.commit()
    conn.close()

# Function to create a header
def create_header():
    st.markdown(
        """
        <style>
        .header {
            padding: 10px;
            background-color: #2C3E50;
            color: white;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="header"><h1>Stock Prediction Chatbot</h1></div>', unsafe_allow_html=True)

# Function to create a footer
def create_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #2C3E50;
            color: white;
            text-align: center;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="footer">© 2024 Stock Prediction Chatbot</div>', unsafe_allow_html=True)

# Function to create a navigation bar
def create_navbar():
    st.markdown(
        """
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            background-color: #34495E;
            padding: 10px;
        }
        .navbar a {
            color: white;
            text-decoration: none;
            padding: 10px;
        }
        .navbar a:hover {
            background-color: #2980B9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def send_email(to_email, subject, body):
    from_email = "sachinkolhar4@gmail.com"
    from_password = "tojv wkxr bcod qgaw"  # Use the generated app password

    # Set up the email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    # Connect to the Gmail server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(from_email, from_password)
        server.send_message(msg)

# Example usage
send_email("sachinkolhar4@gmail.com", "Subject", "Email body")

# Main function to display the contact page
def content():
    st.title('Contact Us')
    
    # Initialize the database
    init_db()
    
    # Display header, navbar, and footer
    create_header()
    create_navbar()
    
    st.subheader("Contact Us")
    st.markdown("Feel free to reach out to us through the following methods:")
    st.markdown(
        """
        *Email:* support@stockpredictionchatbot.com  
        *Phone:* +1 (234) 567-8901  
        *Address:* 1234 Market St, Suite 567, San Francisco, CA 94103
        """
    )

    # Contact Form
    st.subheader("Send Us a Message")
    user_email = st.text_input("Email", help="Enter your registered email address")
    user_message = st.text_area("Message", help="Type your query or compliment here")
    if st.button("Go Back"):
        st.experimental_set_query_params(page="home")
        st.experimental_rerun()
    if st.button("Submit Message"):
        if '@' not in user_email or '.' not in user_email:
            st.error("Please enter a valid email address.")
        else:
            conn = connect_db()
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE email = ?', (user_email,))
            user_exists = c.fetchone()
            conn.close()
            if user_exists:
                add_message(user_email, user_message)
                st.success("Your message has been sent successfully!")

                # Send email to the owner
                owner_email = "sachinkolhar4@gmail.com"  # Replace with owner's email
                email_subject = "New Message from Contact Form"
                email_body = f"User {user_email} sent a message: {user_message}"
                send_email(owner_email, email_subject, email_body)

            else:
                st.error("This email is not registered. Please use your registered email address.")

    create_footer()

if __name__ == "__main__":
    content()