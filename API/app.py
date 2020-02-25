from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = '####'
api = Api(app)

jwt=JWT(app, authenticate, identity)


# items = []

api.add_resource(Item, '/item/<string:name>')  #http://127.0.0.1/5000/item/<name>
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
