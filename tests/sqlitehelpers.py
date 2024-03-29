import sqlite3

conn = sqlite3.connect('jugantor.db')

def create_table():
    conn = sqlite3.connect('jugantor.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE jugantor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                date INTEGER,
                article_title TEXT,
                article TEXT,
                wordcount INTEGER,
                pagenum INTEGER,
                url TEXT
                )""")
    conn.close()

def insert_to_jugantor(year, date, article_title, article, wordcount, pagenum, url):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO jugantor VALUES (:year, :date, :article_title, :article, :wordcount, :pagenum, :url)", 
                  {'year': year, 'date': date, 'article_title': article_title, 'article': article, 'wordcount': wordcount, 'pagenum': pagenum, 'url': url})
    conn.close()
    
def get_article_by_word(lastname):
    c = conn.cursor()
    c.execute("SELECT * FROM jugantor WHERE last=:last", {'last': lastname})
    return c.fetchall()
    
def update_entry(emp, pay):
    c = conn.cursor()
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})
    conn.close()

def remove_entry(emp):
    c = conn.cursor()
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})
    conn.close()

conn.close()

create_table()