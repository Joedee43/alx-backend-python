import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries
def log_queries(func):
    @functools.wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        # Extract and log the query (first positional arg or 'query' keyword arg)
        insec = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"Executing SQL query is a {insec}: {args[0]}")
        
        # Execute the original function and return its result
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")