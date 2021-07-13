import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    @classmethod
    def get_parsed_data(cls):
        return cls.parser.parse_args()

    def post(self):
        data = self.get_parsed_data()
        if UserModel.find_by_username(data['username']) is None:
            user = UserModel(**data)
            user.save_to_db()
            return {"message": "User created successfully."}, 201
            
        else:
            return {'message': 'Error. User already exists.'}, 400
        