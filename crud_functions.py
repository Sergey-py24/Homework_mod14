import sqlite3



connection = sqlite3.connect('database_new.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')



def get_all_products():
    products = cursor.execute('SELECT title, description, price FROM Products')
    menu = []
    for i in products:
        menu += {f'Название:{i[0]} | Описание:{i[1]} |Цена:{i[2]}'}
    connection.commit()
    return menu



