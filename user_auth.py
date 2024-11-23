
import sqlite3
import hashlib
from datetime import datetime


conn = sqlite3.connect('user_system.db')
cur = conn.cursor()

cur.execute(""" 
            

            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
);
""")

conn.commit()
print("Database initialized successfully.")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_hashed_password):
    return hash_password(input_password) == stored_hashed_password

def register():
    while True:
        username = input("Create username: ")
        password = input("Create password: ")
        password1 = input("Confirm password: ")

        # Check if passwords match
        if password != password1:
            print("Passwords don't match. Please try again.")
            continue

        # Check password length
        if len(password) < 8:
            print("Password too short. It must be at least 8 characters long.")
            continue

        # Check if username already exists
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            print("Username already exists. Please try a different one.")
            continue

       # Insert the new user into the database
        hashed_password = hash_password(password)
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Registration successful!")
        break



def login_user():
    conn = sqlite3.cursor()
    cur = conn.cursor()

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    while True:
        username = input("Enter your Username: ")
        password = input("Enter your password: ")

        # Fetch user from the database
        cur.execute("SELECT * FROM users WHERE username = ? AND password =?", (username,hashed_password))
        result = cur.fetchone()

        if result is None:
            print("Username does not exist. Please register or try again.")
            continue

        # Check if the password matches
        hashed_password = result[1]
        if verify_password(password, hashed_password):
            print("Login successful!")
            return result[0]  # Returning the user_id
        else:
            print("Incorrect password! Please try again.")

  




def home():
    while True:
        option = input("Login|Signup:").strip().capitalize()
        if option == "Login":
           user_id= login_user()
           if user_id:
                print("Welcome to the Expense Tracker!")
                expense_tracker(user_id)
           break

        elif option == "Signup":
           register()
           break

        else:
           print("Please enter a valid option") 


if __name__=="__main__":
    home()




