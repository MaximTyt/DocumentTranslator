from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep


class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/'):
            self.path = '/index.html'
            try:
                f = open(self.path[1:], encoding="utf_8").read()
                self.send_response(200)
            except:
                f = "File not found"
                self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(f, 'utf8'))

    def do_POST(self):
        if self.path.endswith('/translate'):
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/')
            self.end_headers()


def main():
    PORT = 8000
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, requestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
