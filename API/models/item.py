import sqlite3

class ItemModel:
    def __init__(self,name,price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name,'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query_select = "SELECT * from item where itemname=?"
        result = cursor.execute(query_select, (name,))
        row = result.fetchone()
        connection.commit()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        item_insert = "INSERT INTO item VALUES (?, ?)"
        # cursor.execute(item_insert, (name, request_data['price']))
        cursor.execute(item_insert, (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # print(price)

        update_item  = "UPDATE item SET price=? WHERE itemname=?"

        cursor.execute(update_item,(self.price,self.name))

        connection.commit()
        connection.close()
