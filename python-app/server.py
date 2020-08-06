import http.server
import socketserver
import random
import time

from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram

REQUESTS = Counter("python_app_hello_world_requests_total",
                   "Hello World requested.")
EXCEPTIONS = Counter('python_app_hello_world_exceptions_total',
                     'Exceptions serving Hello World.')
SALES = Counter('python_app_hello_world_sales_total', "Euros made serving..")

INPROGRESS = Gauge("python_app_hello_world_inprogress",
                   "Number of hello world in progress")
LAST = Gauge("python_app_hello_world_time_seconds",
             "The last time a hello world was served")

LATENCY = Summary('python_app_hello_world_latency_seconds',
                  'Time taken for a hello world')

LATENCY_HISTO = Histogram("python_app_hello_world_latency_seconds_hosto",
                          "Time requests for latency")

PORT = 8001


class MyHandler(http.server.BaseHTTPRequestHandler):
    @EXCEPTIONS.count_exceptions()
    @INPROGRESS.track_inprogress()
    @LATENCY.time()
    @LATENCY_HISTO.time()
    def do_GET(self):
        REQUESTS.inc()
        euros = random.random()
        time.sleep(int(random.random() * 5))
        SALES.inc(euros)
        print("[python_app] Getting request..")
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Hello World for {} euros".format(euros).encode())
        LAST.set_to_current_time()


Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    start_http_server(8000)
    httpd.serve_forever()


# Shell command to make requsets for 100 times with delay
# for i in {1..100}; do echo $i; curl http://192.168.29.228:8001/ ; sleep `expr  $i  % 11`s;  done
