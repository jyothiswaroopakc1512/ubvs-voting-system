import sqlite3

# Create the database and tables
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table for voters
c.execute('''CREATE TABLE IF NOT EXISTS voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    father_name TEXT,
    aadhar_number TEXT,
    address TEXT,
    biometric TEXT
)''')

# Create table for officers
c.execute('''CREATE TABLE IF NOT EXISTS officers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    aadhar TEXT,
    employee_id TEXT,
    biometric TEXT
)''')

# Create table for votes
c.execute('''CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    voter_id INTEGER,
    candidate TEXT,
    FOREIGN KEY (voter_id) REFERENCES voters(id)
)''')

conn.commit()
conn.close()
print("Database and tables created successfully.")
