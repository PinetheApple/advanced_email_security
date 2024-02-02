from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
sys.path.append('../')


class MyHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        from processing.predict_input import analyze_email
        analyzed_email = analyze_email(post_data)
        self._set_headers()
        self.wfile.write(json.dumps(
            {'phishing': analyzed_email[0], 'spam': analyzed_email[1], 'links': analyzed_email[2]}).encode('utf-8'))


def run_server(server_class=HTTPServer, handler_class=MyHandler, port=12345):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


run_server()
