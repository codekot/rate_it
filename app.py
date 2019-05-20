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
        parser = reqparse.RequestParser()
        parser.add_argument('offset', type=int, default=0)
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('name_substr', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('sort', type=str, default='-rate', 
                            choices=['rate', '-rate', 'name', '-name'])
        parser.add_argument('description', type=str)
        args = parser.parse_args()
        items = ItemModel.query
        if args['name']:
            items = items.filter_by(name=args['name'])
        if args['name_substr']:
            items = items.filter(ItemModel.name.contains(args['name_substr']))
        if args['description']:
            items = items.filter(ItemModel.name.contains(args['description']))
        if args['sort']:
            is_desc = args['sort'].startswith('-')
            sort_field = args['sort'][1:] if is_desc else args['sort']
            sort_field = ItemModel.__table__.columns[sort_field]
            sort_field = sort_field.desc() if is_desc else sort_field.asc()
            items = items.order_by(sort_field)
        if args['offset']:
            items = items.offset(args['offset'])
        if args['limit']:
            items = items.limit(args['limit'])
        items = items.all()
        result = [item.json() for item in items]
        return {'items': result}, 200


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
