from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from app.gc_bucket import GCBucket
from app.models import ItemModel
from utils.utils import non_empty_string


class Item(Resource):
    @jwt_required
    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        return item.json()

    @jwt_required
    def put(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=non_empty_string, location='form',
                            help="Name of the item (must be a non-empty string)")
        parser.add_argument('description', type=str, help="Description of the item", location='form')
        parser.add_argument('rate', type=int, location='form')
        parser.add_argument('image', type=FileStorage, location='files')
        parser.add_argument('delete_image', type=bool, location='form')
        args = parser.parse_args()
        args = {key: value for key, value in args.items() if value or key=='description'}

        if args.pop('delete_image', None):
            item.delete_image()

        if args.get('image'):
            image_url = GCBucket.save_to_google_cloud(args['image'])
            args["image"] = image_url

        item.update_fields(save=True, **args)
        return item.json(), 200

    @jwt_required
    def delete(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        item.delete()
        return {}, 200
