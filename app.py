from flask import Flask 
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

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

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()


class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    color = db.Column(db.Integer())


class Item(Resource):
    def get(self, item_id):
        return ItemModel.find_by_id(item_id).json()


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
        return {'items': result}
        


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<int:item_id>')
api.add_resource(SearchItem, '/search/<string:name>')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
