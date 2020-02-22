from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = '####'
api = Api(app)

jwt=JWT(app, authenticate, identity)


items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price is required')
    #parser.add_argument('category')  In case we want to add addl arguments

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name, items),None)
        return {'item': item} if item else {'message': 'Item not found'}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items),None):
            return ({'message': f'An item with the name {name} already exists'},
             400)

        #request_data = request.get_json()
        request_data = Item.parser.parse_args()

        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items

        if not next(filter(lambda x: x['name'] == name, items),None):
            return {'message': 'Item not found'}, 404

        items =  list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item is deleted'}
        # return {'message': 'Item is deleted'} if items.pop('name', None) else {'message': 'Item does not exist'},  200

    def put(self, name):
        #request_data = request.get_json()
        '''Use parser to ensure only the valid arguments will be updated'''
        #parser.add_argument('category')
        request_data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items),None)
        if item is None:
            item = {'name' : name, 'price': request_data['price']}
            items.append(item)
        else:
            item.update(request_data)

        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  #http://127.0.0.1/5000/item/<name>
api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
