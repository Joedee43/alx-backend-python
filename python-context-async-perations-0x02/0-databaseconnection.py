import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def __exit__(self, *args):
        self.conn.close()

# Usage
with DatabaseConnection('users.db') as conn:
    print(conn.execute("SELECT * FROM users").fetchall())