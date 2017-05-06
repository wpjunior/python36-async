import json

from tornado.testing import AsyncHTTPTestCase, gen_test
from rest_mongo import get_app


class MyTest(AsyncHTTPTestCase):

    def get_app(self):
        return get_app('test-database')

    def setUp(self):
        super().setUp()
        def drop_collection_result(*args):
            self.stop()

        self.get_app().db.drop_collection('people', callback=drop_collection_result)
        self.wait()

    def test_not_found(self):
        response = self.fetch('/people/1234')

        self.assertEqual(response.code, 404)
        self.assertEqual(response.headers['content-type'], 'application/json')

        body = json.loads(response.body)
        self.assertEqual(body, {'error': 'Not found'})

    def test_create_and_get(self):
        # create
        response = self.fetch('/people', method='POST', body='{"name": "created"}')

        self.assertEqual(response.code, 201)
        self.assertEqual(response.headers['content-type'], 'application/json')

        body = json.loads(response.body)
        self.assertEqual(body['name'], 'created')

        # get
        response = self.fetch('/people/%s' % body["_id"])
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')

        body = json.loads(response.body)
        self.assertEqual(body['name'], 'created')
