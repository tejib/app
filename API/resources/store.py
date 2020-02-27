from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if StoreModel.find_by_name(name):
            return ({'message': f'A store with the name {name} already exists'}, 400)

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message':'An error occured while inserting data'}, 500


        return store.json(), 201

    def delete(self, name):

        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message':'Item deleted'}

    def put(self, name):
        '''Use parser to ensure only the valid arguments will be updated'''

        store = StoreModel.find_by_name(name)

        if store is None:
            store = StoreModel(name)

        store.save_to_db()

        return store.json(), 200


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
