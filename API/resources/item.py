from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')
    parser.add_argument('store_id', type=int, required=True, help='StoreId is required')
    #parser.add_argument('category')  In case we want to add addl arguments

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return ({'message': f'An item with the name {name} already exists'}, 400)

        request_data = self.parser.parse_args()

        item = ItemModel(name, request_data['price'], request_data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message':'An error occured while inserting data'}, 500


        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'Item deleted'}

    def put(self, name):
        '''Use parser to ensure only the valid arguments will be updated'''
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    def get(self):
        # return {'items': items}
        # Longer way. Using list comprehension is simpler
        #items = []
        # for item in ItemModel.item_list():
        #     items.append(dict(name=item.name, price=item.price))
        #
        # return  {'items': items}

        return {'items': [item.json() for item in ItemModel.query.all()]}
