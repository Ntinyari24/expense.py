
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
cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            category TEXT,
            description TEXT,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(rowid)
            
)
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

def add_expense(user_id):
    conn = sqlite3.cursor()
    cur = conn.cursor()

    while True:
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter the category (e.g food,shopping)")
            description = input("Enter a description: ")
            date = input(f"Enter the date (default is{datetime.now().strftime('%Y-%m-%d')})")

            if not date:
                date = datetime.now().strftime('%Y-%m-%d')

            cur.execute(
                "INSERT INTO expenses WHERE (user_id, amount, category, description, date) VALUES (?,?,?, ?)" ,
                        (user_id, amount, category, description, date))  

            conn.commit()
            print("Expense added successfully!") 
            break
        except ValueError:
            print("Please enter a valid amount.")




def view_expenses(user_id):

    cur.execute('SELECT * FROM expenses WHERE user_id=?', (user_id,))
    expenses = cur.fetchall()


    for expense in expenses:
        print(f"ID: {expense[0]},Amount:{expense[2]}, Category:{expense[4]}, Description:{expense[4]}, Date{expense[5]}")
    else:
         print ('No expenses found')


def total_expenses(user_id):
    cur.execute("SELECT SUM (amount) FROM expenses WHERE user_id = ?", (user_id,))
    result =cur.fetchone()
    total = result[0] if result[0] is not None else 0.0
    print(f"Total expenses: {total}")

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
            print("Invalid option, please try again")          




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




