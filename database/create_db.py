import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database/user_data.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT,
        password TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
