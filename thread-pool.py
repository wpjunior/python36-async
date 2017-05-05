import time

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import (
    Application,
    RequestHandler,
)
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class ThreadPoolHandler(RequestHandler):

    _thread_pool = ThreadPoolExecutor(10)

    @gen.coroutine
    def get(self):
        result = yield self.sync_job()
        self.write(result)

    @run_on_executor(executor='_thread_pool')
    def sync_job(self):
        time.sleep(1)
        return 'ok'

if __name__ == "__main__":
    app = Application([
        (r"/", ThreadPoolHandler),
    ], debug=True)
    app.listen(8888)
    IOLoop.current().start()
