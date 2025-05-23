import sqlite3
import functools


#### decorator to lof SQL queries
def log_queries(func):
    @functools.wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        # Extract and log the query (first positional arg or 'query' keyword arg)
        query = args[0] if args else kwargs.get('query')
        print(f"Executing SQL query: {query}")
        
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