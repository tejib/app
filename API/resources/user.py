import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True, help='Username is required')
    parser.add_argument('password',type=str,required=True, help='Password is required')

    def post(self):
        request_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {"message": "User already exists"}, 400

        UserModel(request_data['username'], request_data['password']).save_to_db()
        return {"message": "User created successfully"}, 201

class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
