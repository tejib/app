import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from users where username=?"
        result = cursor.execute(query, (username,))

        row = result.fetchone()
        if row:
            #user = User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_userid(cls, _id):
        connection =  sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from users where id=?"
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        if row:
            #user = User(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True, help='Username is required')
    parser.add_argument('password',type=str,required=True, help='Password is required')

    def post(self):
        request_data = UserRegister.parser.parse_args()

        if User.find_by_username(request_data['username']):
            return {"message": "User already exists"}, 400
        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "INSERT INTO users VALUES (NULL, ?, ?) "
            cursor.execute(query,(request_data['username'], request_data['password']))
            connection.commit()
            connection.close()
            return {"message": "User created successfully"}, 201
