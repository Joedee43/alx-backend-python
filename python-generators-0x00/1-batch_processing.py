import sqlite3

def stream_users_in_batches(batch_size):
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Execute query to fetch all rows
    cursor.execute("SELECT * FROM user_data")
    
    # Fetch rows in batches using one loop
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield [dict(row) for row in batch]
    
    # Close connection
    conn.close()

def batch_processing(batch_size):
    # Process batches and filter users with age > 25 using two loops
    for batch in stream_users_in_batches(batch_size):
        # Filter users in the batch
        filtered_users = [user for user in batch if user['age'] > 25]
        # Yield each filtered user individually
        for user in filtered_users:
            print(user)  # Print to match 2-main.py output
            yield user