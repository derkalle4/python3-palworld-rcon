from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import re
import threading


class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, callbacks, *args, **kwargs):
        # init our stuff
        self.callbacks = callbacks
        # init base class stuff
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        path_split = self.path.split('/')
        search_class = None
        search_func = None
        response = {'error': '404', 'message': 'not found'}
        if len(path_split) in range(2,4):
            if path_split[1]:
                search_class = re.sub(r'[^a-zA-Z0-9]', '', path_split[1])
                search_func = 'index'
            if len(path_split) == 3 and path_split[2]:
                search_func = re.sub(r'[^a-zA-Z0-9]', '', path_split[2])
        if search_class in self.callbacks:
            attribute = f"_web_{search_func}"
            print(attribute)
            if hasattr(self.callbacks[search_class], attribute):
                func = getattr(self.callbacks[search_class], attribute)
                response = func()
        self.wfile.write(json.dumps(response).encode('utf-8'))
  
class Webserver():
    def __init__(self, config, callbacks):
        self.config = config
        self.callbacks = callbacks

    def worker(self):
        if not 'web' in self.config:
            logging.info('did not find web section in config. skipping webserver.')
        if not 'port' in self.config['web']:
            logging.error('did not find port in the web section. please set a port')
        server_address = ('', self.config['web']['port'])
        # create handler
        handler = partial(HttpHandler, self.callbacks)
        httpd = HTTPServer(server_address, handler)
        try:
            logging.info(f"starting a webserver on port {self.config['web']['port']}")
            httpd.serve_forever()
        except:
            pass
    def run(self):
        server_thread = threading.Thread(target=self.worker)
        server_thread.daemon = True
        server_thread.start()