from flask import Flask 
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

# from db import db
# from models import ItemModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
db = SQLAlchemy(app)
api = Api(app)


class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category = db.Column(db.String())
    description = db.Column(db.Text())
    created_date = db.Column(db.String())
    last_edit_date = db.Column(db.String())
    image = db.Column(db.String())
    rate = db.Column(db.Integer)

    def json(self):
        return {
        'id': self.id,
        'name': self.name,
        'category': self.category,
        'description': self.description,
        'created_date': self.created_date,
        'last_edit_date': self.last_edit_date,
        'image': self.image,
        'rate': self.rate
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    color = db.Column(db.Integer())

class Item(Resource):
    def get(self):
        return {'item': 'some item'}

class ItemList(Resource):
    def get(self):
        items = [item.json() for item in ItemModel.find_all()]
        return {'items': items}, 200

class SearchItem(Resource):
    def get(self, name):
        result = []
        search = ItemModel.find_all()
        for item in search:
            if name.lower() in item.name.lower():
                result.append(item.json())
        if result:
            return {'items': result}
        else:
            return {'items': 'not found'}


api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')
api.add_resource(SearchItem, '/search/<string:name>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)