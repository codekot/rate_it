from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from app.gc_bucket import GCBucket
from app.models import ItemModel
from utils.utils import non_empty_string


class ItemList(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('offset', type=int, default=0)
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('name_substr', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('sort', type=str, default='-rate',
                            choices=['rate', '-rate', 'name', '-name'],
                            help="Available sort parameters: rate, -rate, name, -name")
        parser.add_argument('description', type=str)
        args = parser.parse_args()
        items = ItemModel.query
        if args['name']:
            items = items.filter_by(name=args['name'])
        if args['description']:
            items = items.filter(ItemModel.name.contains(args['description']))
        # Search for substring
        if args['name_substr']:
            items = items.filter(ItemModel.name.contains(args['name_substr']))

        # Get the total count of items
        total_count = items.count()

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
        result = [item.json() for item in items]
        return {'items': result, 'total_count': total_count}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=non_empty_string, required=True, location='form',
                            help="Name of the item is required")
        parser.add_argument('description', type=str, help="Description of the item", location='form')
        parser.add_argument('image', type=FileStorage, location='files')
        args = parser.parse_args()

        if args['image']:
            image_url = GCBucket.save_to_google_cloud(args['image'])
            args["image"]=image_url

        item = ItemModel.find_by_name(args['name'])
        if item:
            item.update_fields(rate=item.rate+1, **args)
        else:
            item = ItemModel(**args)

        try:
            item.save()
        except:
            return {'message': 'Error writing in database'}, 500
        return item.json(), 201
