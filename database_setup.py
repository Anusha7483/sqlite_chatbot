import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("chat_assistant.db")
cursor = conn.cursor()

# Create Employees Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Department TEXT NOT NULL,
        Salary INTEGER NOT NULL,
        Hire_Date TEXT NOT NULL
    )
''')

# Create Departments Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Departments (
        ID INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Manager TEXT NOT NULL
    )
''')

# Insert sample data
cursor.executemany("INSERT INTO Employees (Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?)", [
    ("Alice", "Sales", 50000, "2021-01-15"),
    ("Bob", "Engineering", 70000, "2020-06-10"),
    ("Charlie", "Marketing", 60000, "2022-03-20"),
    ("anusha", "IT", 85000, "2018-03-20"),
    ("rindu", "Marketing", 30000, "2022-04-20"),
    ("rajath", "technical", 800000, "2023-03-20"),
    ("sagar", "technical", 60000, "2022-04-20"),
    ("sujatha", "Marketing", 40000, "2023-03-20"),
    ("sangu", "IT", 95500, "2020-03-20"),
    ("apoorva", "Sales", 34500, "2022-03-20"),
    ("kavya", "Marketing", 49500, "2023-01-20"),
    ("swapna", "Engineering", 58500, "2022-04-20"),
    ("sammi", "IT", 44600, "2020-03-20"),
    ("gauthami", "IT", 63500, "2020-03-20")






])

cursor.executemany("INSERT INTO Departments (Name, Manager) VALUES (?, ?)", [
    ("Sales", "Alice"),
    ("Engineering", "Bob"),
    ("Marketing", "Charlie"),
    ("technical", "sagar"),
    ("IT", "anusha")



])

# Commit and close connection
conn.commit()
conn.close()

print("Database setup complete! Run `python app.py` to start the server.")
