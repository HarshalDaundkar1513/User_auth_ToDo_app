import sqlite3
from flask import g

# # Connect to the database (or create it if it doesn't exist)
# conn = sqlite3.connect('LoginApp.db')
# cursor = conn.cursor()

# # Create the Users table
# # cursor.execute('''
# # CREATE TABLE Users (
# #     UserID INTEGER PRIMARY KEY AUTOINCREMENT,
# #     UserName TEXT NOT NULL,
# #     UserEmail TEXT NOT NULL UNIQUE,
# #     Password TEXT NOT NULL,
# #     Login_Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
# # )
# # ''')

# # Commit the changes and close the connection
# conn.commit()
# conn.close()


def open_database():
    sql = sqlite3.connect('LoginApp.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_database():
    if not hasattr(g, 'login_db'):
        g.login_db = open_database()
        return g.login_db
    