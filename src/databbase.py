import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'jugantor.db')
conn = sqlite3.connect('jugantor.db')

def create_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE jugantor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                date INTEGER,
                article_title TEXT,
                article_body TEXT,
                wordcount INTEGER,
                url TEXT
                )""")
    conn.close()

def insert_to_jugantor(year, date, article_title, article, wordcount, pagenum, url):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO jugantor (year, date, article_title, article, wordcount, pagenum, url) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                (year, date, article_title, article, wordcount, pagenum, url))
    print("Data inserted successfully")

def insert_to_table(table_name, year, date, article_title, article, wordcount, pagenum, url):
    c = conn.cursor()
    with conn:
        c.execute(f"INSERT INTO {table_name} (year, date, article_title, article, wordcount, pagenum, url) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                (year, date, article_title, article, wordcount, pagenum, url))
    print(f"Data inserted to {table_name} successfully")

def delete_all_rows(table_name):
    c = conn.cursor()
    with conn:
        c.execute(f"DELETE FROM {table_name}")
    print(f"All rows deleted from {table_name}")

def drop_table(table_name):
    c = conn.cursor()
    with conn:
        c.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Table {table_name} dropped successfully")

def remove_rows_below_wordcount_threshold(table_name, wordcount_threshold):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()

    query = f"DELETE FROM {table_name} WHERE wordcount < ?"
    
    try:
        c.execute(query, (wordcount_threshold,))
        conn.commit()
        print("Rows deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting rows: {e}")
    finally:
        conn.close()
        
# create_table()
# delete_all_rows("jugantor")
# drop_table("jugantor")

# remove_rows_below_wordcount_threshold("jugantor", 50)