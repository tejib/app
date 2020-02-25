import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# drop_table = "DROP TABLE IF EXISTS users"
# cursor.execute(drop_table)
#
# create_table = "CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)"
# cursor.execute(create_table)

select_query = "SELECT * from users"

for row in cursor.execute(select_query):
    print(row)

# drop_table = "DROP TABLE IF EXISTS item"
# cursor.execute(drop_table)
#
# create_table = "CREATE TABLE item (itemname text, price real)"
# cursor.execute(create_table)

select_item = "SELECT * from item"

for row in cursor.execute(select_item):
    print(row)


connection.commit()
connection.close()
