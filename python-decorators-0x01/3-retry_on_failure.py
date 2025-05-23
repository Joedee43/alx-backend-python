import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)  
        def wrapper(*args, **kwargs):
            args[0] = sqlite3.connect('users.db')
            result = func(*args, **kwargs)
            args[0].close()
        return result
        return wrapper
    return decorator
def with_db_connection(func):
    @functools.wraps(func)  
    def wrapper(*args, **kwargs):
        attempt = 0
        while attempt < retries:
            try:
                return func(*args, **kwargs)        
            except Exception as e:
                attempt += 1
                print(f"Attempt {attempt} failed: {e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    print("All retry attempts failed.")
                    raise
    return wrapper


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)