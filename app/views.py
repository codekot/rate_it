import os

from dotenv import load_dotenv
from flask_restful import Resource, reqparse
from google.cloud import storage
from werkzeug.datastructures import FileStorage

from app.models import ItemModel
from . import db

load_dotenv()
CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')


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
                            choices=['rate', '-rate', 'name', '-name'],
                            help="Available sort parameters: rate, -rate, name, -name")
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

    def post(self):
        #{"name": "First", "description": "main item", "image": "some.jpg", "rate": 200}
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="Name of the item (required)", required=True)
        parser.add_argument('description', type=str, help="Description of the item")
        parser.add_argument('image', type=str)
        args = parser.parse_args()

        if ItemModel.find_by_name(args['name']):
            return {'message': "An item with name '{}' already exists.".format(args['name'])}, 400

        item = ItemModel(**args)
        try:
            db.session.add(item)
            db.session.commit()
        except:
            return {'message': 'Error writing in database'}, 500
        return item.json(), 201


class SearchItem(Resource):
    def get(self, name):
        result = []
        search = ItemModel.find_all()
        for item in search:
            if name.lower() in item.name.lower():
                result.append(item.json())
        return {'items': result}

class Images(Resource):
    def save_to_google_cloud(self, image):
        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        print(image.filename)
        blob = bucket.blob(image.filename)

        blob.upload_from_string(
            image.read(),
            content_type=image.content_type
        )

        # The public URL can be used to directly access the uploaded file via HTTP.
        return blob.public_url


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('item_image', type=FileStorage, location='files')
        parser.add_argument('item_name', type=str, help="Name of the item (required)", required=True)
        args = parser.parse_args()
        item_image = args['item_image']
        if not item_image:
            return {'message': 'No file uploaded'}, 400
        image_url = self.save_to_google_cloud(item_image)
        print(image_url)
        #item_image.save("new_item.jpg")
