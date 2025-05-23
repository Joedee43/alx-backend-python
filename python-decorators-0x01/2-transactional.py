import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)  
    def wrapper(*args, **kwargs):
        args[0] = sqlite3.connect('users.db')
        result = func(*args, **kwargs)
        args[0].close()
        return result
    return wrapper

def transactional(func):
   def wrapper(*args, **kwargs):
     try:
            result = func(*args, **kwargs)
            conn.commit()  # Commit if no exceptions
            return result
     except Exception as e:
            conn.rollback()  # Rollback on error
            raise e  # Re-raise the exception
   return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
  cursor = conn.cursor() 
  cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
  #### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')