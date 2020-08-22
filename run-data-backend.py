#!/usr/bin/env python
# -*- coding: utf-8 -*-
from server import app
<<<<<<< HEAD
# from gevent.wsgi import WSGIServer
from gevent.pywsgi import WSGIServer

=======
from gevent.pywsgi import WSGIServer
>>>>>>> master
# app.config['STATIC_FOLDER'] = './client/assets'

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
