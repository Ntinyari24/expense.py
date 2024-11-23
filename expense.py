import hashlib
import sqlite3
from datetime import datetime

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Corrected SQL syntax
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

# Hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register a user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return "User created successfully."
    except sqlite3.IntegrityError:
        conn.close()
        return "Username already exists."

# Log in a user
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Hash the provided password
    hashed_password = hash_password(password)

    # Check if the user exists
    cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cur.fetchone()
    conn.close()

    # If the user exists, return the user_id, else return None
    if user:
        return user[0]  # user[0] is the user_id
    else:
        return None

# Add an expense
def add_expense(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    while True:
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter the category (e.g food,shopping): ")
            description = input("Enter a description: ")
            date = input(f"Enter the date (default is {datetime.now().strftime('%Y-%m-%d')}): ")

            if not date:
                date = datetime.now().strftime('%Y-%m-%d')

            cur.execute("INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
                        (user_id, amount, category, description, date))

            conn.commit()
            print("Expense added successfully!")
            break
        except ValueError:
            print("Please enter a valid amount.")

# View expenses
def view_expenses(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM expenses WHERE user_id=?', (user_id,))
    expenses = cur.fetchall()

    if expenses:
        for expense in expenses:
            print(f"ID: {expense[0]}, Amount: {expense[2]}, Category: {expense[3]}, Description: {expense[4]}, Date: {expense[5]}")
    else:
        print("No expenses found.")

# View total expenses
def total_expenses(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    total = result[0] if result[0] is not None else 0.0
    print(f"Total expenses: {total}")

# Expense tracker menu
def expense_tracker(user_id):
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Exit")

        option = input("Choose an option: ").strip()

        if option == "1":
            add_expense(user_id)
        elif option == "2":
            view_expenses(user_id)
        elif option == "3":
            total_expenses(user_id)
        elif option == "4":
            print("Exiting Expense Tracker.")
            break
        else:
            print("Invalid option, please try again.")

# Main function
def home():
    initialize_database()

    while True:
        option = input("Login|Signup: ").strip().capitalize()
        if option == "Login":
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            user_id = login_user(username, password)  # Pass username and password
            if user_id:
                print("Login successful!")
                print("Welcome to the Expense Tracker!")
                expense_tracker(user_id)  # Call expense tracker with the user_id
                break  # Exit the loop after transitioning to the tracker
            else:
                print("Login failed. Please check your credentials or try again.")
                
        elif option == "Signup":
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                continue

            message = register_user(username, password)
            print(message)

        else:
            print("Please enter a valid option.")

if __name__ == "__main__":
    home()
