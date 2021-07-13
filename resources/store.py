from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.get_by_name(name)
        if store:
            return store.as_dict()
        return {'message': 'Store not found.'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.get_by_name(name):
            return {
                'message': 'The store already exists'
            }, 400
        else:
            store = StoreModel(name)
            store.save_to_db()
            return {
                'message': 'Store created.'
            }, 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.get_by_name(name)
        if store:
            store.delete_from_db()
            return {
                'message': 'Store deleted.'
            }
        else:
            return {
                'message': 'Store not exists.'
            }, 400


class StoreList(Resource):
    @staticmethod
    def get():
        return [
            e.as_dict() for e in StoreModel.get_all()
        ]
