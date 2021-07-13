from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    @classmethod
    def get_parsed_body(cls, name):
        item = cls.parser.parse_args()
        item['name'] = name
        return item

    @staticmethod
    @jwt_required()
    def get(name):
        item = ItemModel.get_by_name(name)

        if item is not None:
            return item.as_dict()
        else:
            return {'message': 'No such item.'}, 404
    
    @classmethod
    @jwt_required()
    def post(cls, name):
        if ItemModel.get_by_name(name) is None:
            data = cls.get_parsed_body(name)
            data['name'] = name
            item = ItemModel(**data)
            item.save_to_db()
            return item.as_dict(), 201
        else:
            return {'message': 'Item already exists.'}, 400

    @staticmethod
    @jwt_required()
    def delete(name):
        item = ItemModel.get_by_name(name)
        if item is not None:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        else:
            return {'message': 'Item does not exist.'}, 400

    @classmethod
    @jwt_required()
    def put(cls, name):
        data = cls.get_parsed_body(name)
        data['name'] = name

        item = ItemModel.get_by_name(name)
        if item is None:
            item = ItemModel(**data)
            code = 201
        else:
            item.price = data['price']
            item.store_id = data['store_id']
            code = 200
        item.save_to_db()
        return item.as_dict(), code


class Items(Resource): 
    @staticmethod
    @jwt_required()
    def get():
        return [
            item.as_dict() for item in ItemModel.get_all()
        ]
