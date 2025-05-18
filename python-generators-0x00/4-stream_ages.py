import sqlite3

def stream_user_ages():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Execute query to fetch ages
    cursor.execute("SELECT age FROM user_data")
    
    # Yield ages one by one using one loop
    for row in cursor:
        yield row[0]
    
    # Close connection
    conn.close()

def calculate_average_age():
    # Calculate running sum and count using one loop
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    # Calculate and print average
    if count == 0:
        average = 0.0  # Handle empty dataset
    else:
        average = total_age / count
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()