import sqlite3
import uuid

def generate_unique_id():
    # Generate a random UUID and extract the first 12 digits
    unique_id = str(uuid.uuid4().int)[:12]
    return unique_id

def insert_user(name, email, phone_number, password):
    user_id = generate_unique_id()
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('database/user_data.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('''
        INSERT INTO users (user_id, name, email, phone_number, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, name, email, phone_number, password))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("User data inserted successfully.")

# Example usage:
# insert_user('user', 'john@example.com', '1234567890', 'pass')





def get_all_users():
    # Connect to SQLite database
    conn = sqlite3.connect('database/user_data.db')
    cursor = conn.cursor()

    # Fetch all user data from the 'users' table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert fetched data into a list of dictionaries
    users = []
    for row in rows:
        user_data = {
            'user_id': row[0],
            'username': row[1],
            'password': row[4]
        }
        users.append(user_data)

    return users

# Example usage:
# all_users = get_all_users()
# print(all_users)
