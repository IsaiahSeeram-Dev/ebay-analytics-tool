import sqlite3 

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn 

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT,
            price REAL,
            sold INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) 
    ''')

    conn.commit()
    conn.close()
