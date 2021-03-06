from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'andrei'
    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
    
    JWT(app, authenticate, identity)

    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(Items, '/items')
    api.add_resource(UserRegister, '/register')
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')
    return app

if __name__ == '__main__':
    app = create_app()
    db.init_app(app)
    app.run(debug=True)
