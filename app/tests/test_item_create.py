import os
import unittest

import requests
from dotenv import load_dotenv

from app import create_app, db
from app.tests import TestConfig

load_dotenv()
CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')


class CreateItemCase(unittest.TestCase):

    URL = '/api/items'

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_fail_empty_data(self):
        response = self.client.post(self.URL, data={"name": ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': {'name': 'Name of the item is required'}})

    def test_fail_empty_name(self):
        response = self.client.post(self.URL, data={"name": ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': {'name': 'Name of the item is required'}})

    def test_create_name_only(self):
        name = 'test name'
        response = self.client.post(self.URL, data={"name": name})
        self.assertEqual(response.status_code, 201)
        json = response.json
        self.assertIn('id', json)
        self.assertEqual(json.get('name'), name)
        self.assertEqual(json.get('description'), None)
        self.assertEqual(json.get('image'), None)
        self.assertEqual(json.get('rate'), 1)

    def test_create_with_description(self):
        name = 'test name'
        description = 'test description'
        response = self.client.post(self.URL, data={"name": name, 'description': description})
        self.assertEqual(response.status_code, 201)
        json = response.json
        self.assertIn('id', json)
        self.assertEqual(json.get('name'), name)
        self.assertEqual(json.get('description'), description)
        self.assertIsNone(json.get('image'))
        self.assertEqual(json.get('rate'), 1)

    def test_create_with_image(self):
        # Path where image should be stored
        storage_path = 'https://storage.googleapis.com/{}/'.format(CLOUD_STORAGE_BUCKET)
        name = 'test name'
        image = open("test_image.png", 'rb')
        # Get image data to compare it later
        image_data = image.read()
        # Rewind the file reader cursor
        image.seek(0)
        response = self.client.post(self.URL,
                                    data={"name": name, 'image': image},
                                    content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        json = response.json
        self.assertIn('id', json)
        self.assertEqual(json.get('name'), name)
        self.assertIsNone(json.get('description'))
        self.assertEqual(json.get('rate'), 1)
        # Check image
        image_value = json.get('image')
        image_is_str = isinstance(image_value, str)
        # 'image' field value is a string
        self.assertTrue(image_is_str)
        if not image_is_str: return
        # Image is stored at the cloud storage
        stored_in_storage = image_value.startswith(storage_path)
        self.assertTrue(stored_in_storage)
        if not stored_in_storage: return
        # Image data at the storage is the same as in local file
        self.assertEqual(image_data, requests.get(image_value).content)

    def test_create_with_description_image(self):
        name = 'test name'
        description = 'test description'
        image = open("test_image.png", 'rb')
        response = self.client.post(self.URL,
                                    data={"name": name, 'description': description, 'image': image},
                                    content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        json = response.json
        self.assertIn('id', json)
        self.assertEqual(json.get('name'), name)
        self.assertEqual(json.get('description'), description)
        self.assertEqual(json.get('rate'), 1)
        self.assertIsInstance(json.get('image'), str)


if __name__ == '__main__':
    unittest.main()
