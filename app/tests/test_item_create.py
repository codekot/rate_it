import unittest

from app import create_app, db
from app.tests import TestConfig


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


    def test_create_name_only(self):
        response = self.client.post(self.URL, data={"name": 'test_name'})
        self.assertEqual(response.status_code, 201)

    def test_fail_if_name_is_empty(self):
        response = self.client.post(self.URL, data={"name": ''})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
