import sqlite3
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "files", 'prothomalo.db')
conn = sqlite3.connect(DATABASE_PATH)

def create_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE prothomalo (
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

def divide_df_by_year_and_save_to_excel(df, directory, paper_name):
    folder_name = f'{paper_name}_excel'
    os.makedirs(os.path.join(directory, folder_name), exist_ok=True)
    
    unique_years = df['year'].unique()
    
    print(f'Years found: {len(unique_years)}\nYears: {unique_years}')
    
    for year in unique_years:
        year_df = df[df['year'] == year]
        
        print(f'Converting year: {year}')
        file_name = f"{paper_name}_{year}.xlsx"
        file_path = os.path.join(directory, folder_name, file_name)
        
        year_df.to_excel(file_path, index=False)

def sqlite_to_excel(database_file, table_name, sort_column, excel_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    try:
        print("Fetching data from database...")
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY {sort_column} DESC')

        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=[col[0] for col in cursor.description])
        
        df = df.drop(columns=['id'])
        
        print("Head of the data:")
        print(df.head())
        
        print("Tail of the data:")
        print(df.tail())
        
        print("DataFrame Description:")
        print(df.describe(include='all'))
        
        print("Converting to xlsx...")
        divide_df_by_year_and_save_to_excel(df, os.path.join(BASE_DIR, "files"), "jugantor")
        # df.to_excel(excel_file)
        
        print(f"Data from '{table_name}' table sorted by '{sort_column}' column has been successfully exported to '{excel_file}'.")
    
    except sqlite3.Error as e:
        print("Error:", e)
    
    finally:
        cursor.close()
        conn.close()

# create_table()
# delete_all_rows("jugantor")
# drop_table("jugantor")

# remove_rows_below_wordcount_threshold("jugantor", 50)
# sqlite_to_excel(DATABASE_PATH, 'jugantor', 'date', os.path.join(BASE_DIR, 'jugantor.xlsx'))