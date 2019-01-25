from flaskr import create_app
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()
app = create_app()


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
