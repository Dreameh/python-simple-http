#!/usr/bin/env python3

import json
import cgi
import http.server
import socketserver
import sys
import os

requestHandler = http.server.BaseHTTPRequestHandler

def delete_content(name):
    with open(name, "w"):
        pass

class Server(requestHandler):
    # Set headers with content-type: 'application/json'
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # GET sends back the json object
    def do_GET(self):
        self._set_headers()
        # Read JSON file
        with open('some_json.json', 'r') as data:
            self.wfile.write(bytes(data.read(), "utf-8"))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message_str = self.rfile.read(length).decode('utf-8')
        message = json.loads(message_str) if message_str else None

        # Open destination file and append new coordinates
        with open('dest.txt', 'a') as data:
            data.write(message['lat'] + '\n' + message['long'])

        message['received'] = 'ok'
        # Send back message
        self._set_headers()
        self.wfile.write(bytes(json.dumps(message), "utf-8"))

    def do_DELETE(self):
        print("this is working")
        delete_content('dest.txt')
        self.send_response(301)

def run(server_class=http.server.HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print("Starting httpd on port:", port)
    httpd.serve_forever()

if __name__ == "__main__":
   from sys import argv

   try:
       if len(argv) == 2:
           run(port=int(argv[0]))
       else:
           run()
   except KeyboardInterrupt:
       print("Interrupted")
       try:
           sys.exit(0)
       except SystemExit:
           os._exit(0)
