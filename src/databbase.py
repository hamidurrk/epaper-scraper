import sqlite3

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
    
# create_table()
# delete_all_rows("jugantor")
# drop_table("jugantor")