from db import db

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '####'
api = Api(app)

@app.before_first_request
def create_tables():
    '''Create the tables if not exists'''
    db.create_all()

jwt=JWT(app, authenticate, identity)


# items = []

api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')  #http://127.0.0.1/5000/item/<name>
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
