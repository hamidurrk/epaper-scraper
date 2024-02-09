import sqlite3

conn = sqlite3.connect('jugantor.db')

c = conn.cursor()

c.execute("""CREATE TABLE jugantor (
            id integer primary key,
            year integer,
            date integer,
            article_title text,
            article text,
            wordcount integer,
            pagenum integer,
            url text
            )""")

def insert_emp(year, date, article_title, article, wordcount, pagenum, url):
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO jugantor VALUES (:first, :last, :pay)", {'year': year, 'date': date, 'article_title': article_title, 'article': article, 'wordcount': wordcount, 'pagenum': pagenum, 'url': url})
    conn.close()
    
def get_article_by_word(lastname):
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
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


insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name('Doe')
print(emps)

update_pay(emp_2, 95000)
remove_emp(emp_1)

emps = get_emps_by_name('Doe')
print(emps)

conn.close()