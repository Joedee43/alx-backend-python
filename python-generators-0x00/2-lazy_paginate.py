import sqlite3

def paginate_users(page_size, offset):
    connection = sqlite3.connect('users.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    connection.close()
    return result

def lazy_paginate(page_size):
    offset = 0
    # Single loop to fetch pages lazily
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop if no more rows
            break
        yield page
        offset += page_size