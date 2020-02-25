import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

drop_table = "DROP TABLE IF EXISTS users"
cursor.execute(drop_table)

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user=(1, 'user1', 'password')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)


users = [
    (2, 'user2', 'password'),
    (3, 'user3', 'password'),
    (4, 'user4', 'password')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * from users"

for row in cursor.execute(select_query):
    print(row)


connection.commit()

cursor.close()
