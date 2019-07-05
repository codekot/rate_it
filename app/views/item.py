import logging

from utils.jwt_required import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from app.gc_bucket import GCBucket
from app.models import ItemModel
from utils.identify_user import identify_user
from utils.utils import non_empty_string

logger = logging.getLogger()


class Item(Resource):
    @jwt_required
    @identify_user
    def get(self, item_id, current_user):
        item = ItemModel.find_by_id(item_id, user_id=current_user.id)
        if not item:
            return {"message": "Item not found"}, 404

        return item.json()

    @jwt_required
    @identify_user
    def put(self, item_id, current_user):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=non_empty_string, location='form',
                            help="Name of the item (must be a non-empty string)")
        parser.add_argument('description', type=str, help="Description of the item", location='form')
        parser.add_argument('rate', type=int, location='form')
        parser.add_argument('image', type=FileStorage, location='files')
        parser.add_argument('delete_image', type=bool, location='form')
        args = parser.parse_args()
        args = {key: value for key, value in args.items() if value or key=='description'}

        item = ItemModel.find_by_id(item_id, user_id=current_user.id)
        if not item:
            return {"message": "Item not found"}, 404

        if args.pop('delete_image', None):
            item.delete_image()

        if args.get('image'):
            try:
                image_url = GCBucket.save_to_google_cloud(args['image'])
            except Exception as exc:
                logger.error("Cannot save image. Exception message: {}".format(str(exc)))
                image_url = None
            if image_url:
                args['image'] = image_url
            else:
                args.pop('image', None)

        item.update_fields(save=True, **args)
        return item.json(), 200

    @jwt_required
    @identify_user
    def delete(self, item_id, current_user):
        item = ItemModel.find_by_id(item_id, user_id=current_user.id)
        if not item:
            return {"message": "Item not found"}, 404

        item.delete()
        return {}, 200
