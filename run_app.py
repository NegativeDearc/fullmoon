from app import app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if app.config['CONFIG_NAME'] == 'development':
    app.run(port=5000,threaded=True)
if app.config['CONFIG_NAME'] == 'production':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000,address='0.0.0.0')
    IOLoop.instance().start()