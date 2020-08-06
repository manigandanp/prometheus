import http.server
import socketserver
import random

from prometheus_client import start_http_server
from prometheus_client import Counter

REQUESTS = Counter("python_app_hello_world_requests_total", "Hello World requested.")
EXCEPTIONS = Counter('python_app_hello_world_exceptions_total', 'Exceptions serving Hello World.')

PORT = 8001

class MyHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    REQUESTS.inc()
    print("[python_app] Getting request..")
    # with EXCEPTIONS.count_exceptions():
    #     if random.random() < 0.2:
    #         raise Exception
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Hello Mani")

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    start_http_server(8000)
    httpd.serve_forever()