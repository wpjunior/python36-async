import json
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import (
    Application,
    RequestHandler,
)

from tornado.httpclient import AsyncHTTPClient


async def get_http_result():
    url = 'https://raw.githubusercontent.com/backstage/functions/master/package.json'
    response = await AsyncHTTPClient().fetch(url, validate_cert=False)
    data = json.loads(response.body)
    return {
        'heey': data['name'],
    }


from tornado import gen

class HelloWorldHandler(RequestHandler):

    async def get(self):
        result01, result02 = await gen.multi([
            get_http_result(),
            get_http_result(),
        ])
        self.write(json.dumps([result01, result02]))



if __name__ == "__main__":
    app = Application([
        (r"/", HelloWorldHandler),
    ])
    app.listen(8888)
    IOLoop.current().start()
