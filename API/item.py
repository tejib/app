import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')
    #parser.add_argument('category')  In case we want to add addl arguments

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # item = next(filter(lambda x: x['name'] == name, items),None)
        # return {'item': item} if item else {'message': 'Item not found'}, 200 if item else 404

        item = self.find_by_name(name)

        if item:
            return item
        return {'message': 'Item not found'}

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
            return {'item': {'name' : row[0], 'price': row[1]}}


    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items),None):
        #     return ({'message': f'An item with the name {name} already exists'},
        #      400)

        #request_data = request.get_json()

        if self.find_by_name(name):
            return ({'message': f'An item with the name {name} already exists'}, 400)

        request_data = self.parser.parse_args()

        # item = {'name': name, 'price': request_data['price']}
        # items.append(item)

        # item = {'name': name, 'price': request_data['price']}

        try:
            self.insert(name, request_data['price'])
        except:
            return {'message':'An error occured while inserting data'}, 500

        return self.find_by_name(name), 201

    @classmethod
    def insert(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        item_insert = "INSERT INTO item VALUES (?, ?)"
        # cursor.execute(item_insert, (name, request_data['price']))
        cursor.execute(item_insert, (name, price))
        connection.commit()
        connection.close()

    def delete(self, name):
        # global items

        # if not next(filter(lambda x: x['name'] == name, items),None):
        #     return {'message': 'Item not found'}, 404
        #
        # items =  list(filter(lambda x: x['name'] != name, items))
        # return {'message' : 'Item is deleted'}
        # return {'message': 'Item is deleted'} if items.pop('name', None) else {'message': 'Item does not exist'},  200

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_item = "DELETE FROM item WHERE itemname=?"

        cursor.execute(delete_item, (name,))
        connection.commit()
        connection.close()

        return {'message':'Item deleted'}



    def put(self, name):
        #request_data = request.get_json()
        '''Use parser to ensure only the valid arguments will be updated'''
        #parser.add_argument('category')
        request_data = Item.parser.parse_args()

        #item = next(filter(lambda x: x['name'] == name, items),None)

        # if item is None:
        #     item = {'name' : name, 'price': request_data['price']}
        #     items.append(item)
        # else:
        #     item.update(request_data)

        # print(request_data['price'])

        if self.find_by_name(name):
            try:
                self.update(name, request_data['price'])
            except:
                return {'message':'An error occured'}, 500
        else:
            try:
                self.insert(name, request_data['price'])
            except:
                return {'message':'An error occured'}, 500


        return self.find_by_name(name), 200


    @classmethod
    def update(cls, name, price):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # print(price)

        update_item  = "UPDATE item SET price=? WHERE itemname=?"

        cursor.execute(update_item,(price,name))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        # return {'items': items}
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query_items = 'SELECT * from item'

        for row in cursor.execute(query_items):
            items.append(dict(name=row[0], price= row[1]))

        connection.close()

        return  {'items': items}
