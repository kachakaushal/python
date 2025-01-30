import tkinter as tk
from tkinter import messagebox
import mysql.connector
import smtplib
import random

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Add your MySQL password here
    'database': 'user_db'
}

# Email configuration (for sending OTP)
EMAIL_ADDRESS = 'your_email@gmail.com'  # Replace with your email
EMAIL_PASSWORD = 'your_email_password'  # Replace with your email password
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Global variables
otp = None

# Function to connect to the database
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to send OTP via email
def send_otp(email):
    global otp
    otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = "Your OTP for Email Verification"
            body = f"Your OTP is: {otp}"
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(EMAIL_ADDRESS, email, message)
        messagebox.showinfo("OTP Sent", "OTP has been sent to your email.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {e}")

# Function to handle signup
def signup():
    username = signup_username.get()
    password = signup_password.get()
    email = signup_email.get()

    if not username or not password or not email:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Check if username or email already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                messagebox.showerror("Signup Error", "Username or email already exists!")
            else:
                # Insert new user into the database
                cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                               (username, password, email))
                conn.commit()
                send_otp(email)  # Send OTP for email verification
                messagebox.showinfo("Signup Success", "Signup successful! Please verify your email.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Function to verify OTP
def verify_otp():
    global otp
    user_otp = otp_entry.get()
    if user_otp == str(otp):
        messagebox.showinfo("Success", "Email verified successfully!")
        # Update the user's verification status in the database
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET is_verified = TRUE WHERE email = %s", (signup_email.get(),))
                conn.commit()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()
    else:
        messagebox.showerror("Error", "Invalid OTP!")

# Function to handle login
def login():
    username = login_username.get()
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                if user[4]:  # Check if the user is verified
                    messagebox.showinfo("Login Success", "Login successful!")
                else:
                    messagebox.showerror("Login Error", "Please verify your email first!")
            else:
                messagebox.showerror("Login Error", "Invalid username!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# GUI Setup
root = tk.Tk()
root.title("Login and Signup Form")

# Login Frame
login_frame = tk.LabelFrame(root, text="Login", padx=10, pady=10)
login_frame.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(login_frame, text="Username:").grid(row=0, column=0)
login_username = tk.Entry(login_frame)
login_username.grid(row=0, column=1)

tk.Button(login_frame, text="Login", command=login).grid(row=1, column=0, columnspan=2)

# Signup Frame
signup_frame = tk.LabelFrame(root, text="Signup", padx=10, pady=10)
signup_frame.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(signup_frame, text="Username:").grid(row=0, column=0)
signup_username = tk.Entry(signup_frame)
signup_username.grid(row=0, column=1)

tk.Label(signup_frame, text="Password:").grid(row=1, column=0)
signup_password = tk.Entry(signup_frame, show="*")
signup_password.grid(row=1, column=1)

tk.Label(signup_frame, text="Email:").grid(row=2, column=0)
signup_email = tk.Entry(signup_frame)
signup_email.grid(row=2, column=1)

tk.Button(signup_frame, text="Signup", command=signup).grid(row=3, column=0, columnspan=2)

# OTP Verification Frame
otp_frame = tk.LabelFrame(root, text="OTP Verification", padx=10, pady=10)
otp_frame.pack(padx=10, pady=10, fill="both", expand=True)

tk.Label(otp_frame, text="Enter OTP:").grid(row=0, column=0)
otp_entry = tk.Entry(otp_frame)
otp_entry.grid(row=0, column=1)

tk.Button(otp_frame, text="Verify OTP", command=verify_otp).grid(row=1, column=0, columnspan=2)

root.mainloop()