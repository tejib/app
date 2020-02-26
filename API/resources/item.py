import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')
    #parser.add_argument('category')  In case we want to add addl arguments

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}


    def post(self, name):
        if ItemModel.find_by_name(name):
            return ({'message': f'An item with the name {name} already exists'}, 400)

        request_data = self.parser.parse_args()

        item = ItemModel(name, request_data['price'])

        try:
            item.insert()
        except:
            return {'message':'An error occured while inserting data'}, 500


        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_item = "DELETE FROM item WHERE itemname=?"

        cursor.execute(delete_item, (name,))
        connection.commit()
        connection.close()

        return {'message':'Item deleted'}



    def put(self, name):
        '''Use parser to ensure only the valid arguments will be updated'''
        request_data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            try:
                ItemModel(name, request_data['price']).update()
            except:
                return {'message':'An error occured in update'}, 500
        else:
            try:
                ItemModel(name, request_data['price']).insert()
            except:
                return {'message':'An error occured in insert'}, 500


        return ItemModel.find_by_name(name).json(), 200


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
