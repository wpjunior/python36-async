import json
import uuid

from tornado.ioloop import IOLoop
from tornado.web import (
    Application,
    RequestHandler,
)
from motor.motor_tornado import MotorClient


class CollectionNameMixin(object):

    @property
    def collection_name(self):
        raise NotImplementedError

    def set_default_headers(self):
        self.set_header('content-type', 'application/json')

    @property
    def collection(self):
        return self.application.db[self.collection_name]


class BaseCollectionHandler(CollectionNameMixin, RequestHandler):

    async def get(self):
        result = []
        async for document in self.collection.find({}):
            result.append(document)

        self.write(json.dumps(result))

    async def post(self):
        body = json.loads(self.request.body)
        body['_id'] = str(uuid.uuid4())

        await self.collection.insert_one(body)

        self.write(json.dumps(body))


class BaseResourceHandler(CollectionNameMixin, RequestHandler):

    async def get(self, resource_id):
        result = await self.collection.find_one({"_id": resource_id})

        if not result:
            self.set_status(404)
            self.write('{"error": "Not found"}')
            return

        self.write(json.dumps(result))

    async def put(self, resource_id):
        body = json.loads(self.request.body)
        result = await self.collection.update_one(
            {'_id': resource_id},
            {'$set': body}
        )

        await self.get(resource_id)

    async def delete(self, resource_id):
        where = {'_id': resource_id}
        result = await self.collection.delete_many(where)
        if result.deleted_count == 0:
            self.set_status(404)
            self.write('{"error": "Not found"}')
            return

        self.set_status(204)


class PeopleCollectionHandler(BaseCollectionHandler):
    collection_name = 'people'


class PeopleResourceHandler(BaseResourceHandler):
    collection_name = 'people'


def get_app(db_name='blah'):
    app = Application([
        (r"/people", PeopleCollectionHandler),
        (r"/people/(.*)", PeopleResourceHandler),
    ])
    app.db = MotorClient()[db_name]
    return app


if __name__ == "__main__":
    get_app().listen(8888)
    IOLoop.current().start()
