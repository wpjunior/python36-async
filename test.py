import unittest
from tornado.testing import AsyncTestCase, gen_test
from http_client_example import get_http_result


class MyTest(AsyncTestCase):

    @gen_test
    async def test_ok(self):
        result = await get_http_result()
        self.assertEqual(result, {'heey': 'backstage-functions'})
