import os
from uuid import uuid4

from dotenv import load_dotenv
from flask_restful import Resource, reqparse
from google.cloud import storage
from werkzeug.datastructures import FileStorage

from flask_jwt_extended import create_access_token

from app.models import ItemModel, UserModel
from . import db

load_dotenv()
CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')


class Item(Resource):
    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        return item.json()

    def put(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="Name of the item (required)", location='form')
        parser.add_argument('description', type=str, help="Description of the item", location='form')
        parser.add_argument('rate', type=int, location='form')
        parser.add_argument('image', type=FileStorage, location='files')
        parser.add_argument('delete_image', type=bool, location='form')
        args = parser.parse_args()
        args = {key: value for key, value in args.items() if value}

        if args.pop('delete_image', None):
            item.delete_image()

        if args.get('image'):
            image_url = self.save_to_google_cloud(args['image'])
            args["image"] = image_url

        item.update_fields(save=True, **args)
        return {}, 200

    def delete(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if not item:
            return {"message": "Item not found"}, 404

        item.delete()
        return {}, 200


class ItemList(Resource):

    def save_to_google_cloud(self, image):
        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Change filename to unique
        filename = uuid4().hex
        image.filename = filename

        # Create a new blob and upload the file's content.
        blob = bucket.blob(image.filename)

        blob.upload_from_string(
            image.read(),
            content_type=image.content_type
        )

        # The public URL can be used to directly access the uploaded file via HTTP.
        return blob.public_url

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
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help="Name of the item (required)", required=True, location='form')
        parser.add_argument('description', type=str, help="Description of the item", location='form')
        parser.add_argument('image', type=FileStorage, location='files')
        args = parser.parse_args()

        if args['image']:
            image_url = self.save_to_google_cloud(args['image'])
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
        return item.json_response(), 201


class SearchItem(Resource):
    def get(self, name):
        result = []
        search = ItemModel.find_all()
        for item in search:
            if name.lower() in item.name.lower():
                result.append(item.json())
        return {'items': result}


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username field (required)")
        parser.add_argument('password', type=str, required=True, help="Password field (required)")
        args = parser.parse_args()

        if UserModel.find_by_username(args['username']):
            return {"message": "A user with that username already exist"}, 400

        user = UserModel(username=args['username'])
        user.set_password(args['password'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username field (required)")
        parser.add_argument('password', type=str, required=True, help="Password field (required)")
        args = parser.parse_args()

        user = UserModel.find_by_username(args["username"])

        if user and user.check_password(args["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token}, 200

        return {"message": "Invalid password or username"}

