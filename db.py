import sqlite3

class DataBase:
    def __init__(self):
        pass
    def save_user(self, name, age):
        conn = sqlite3.connect("usere.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        conn.commit()
        conn.close()
        