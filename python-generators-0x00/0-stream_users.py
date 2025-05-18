import sqlite3

def stream_users():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Enable row access as dictionaries
    cursor = conn.cursor()
    
    # Execute query to fetch all rows from user_data
    cursor.execute("SELECT * FROM user_data")
    
    # Fetch rows one by one using a single loop
    for row in cursor:
        # Convert row to dictionary
        yield dict(row)
    
    # Close connection
    conn.close()