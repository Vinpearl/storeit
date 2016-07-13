#! /usr/bin/env python

import SocketServer, sys
from BaseHTTPServer import BaseHTTPRequestHandler

port = int(sys.argv[1])
print('listening on port {}'.format(port))

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('get: sending 200')
        self.send_response(200)

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print('post: sent 200')

    def do_PUT(self):
        print('put: sending 200')
        self.send_response(200)

httpd = SocketServer.TCPServer(("", int(port)), MyHandler)
httpd.serve_forever()
