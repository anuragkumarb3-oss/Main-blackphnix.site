import http.server
import socketserver
import os
import sys

PORT = 5000
DIRECTORY = "public"

class SPAServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # First try to serve the file normally
        path = self.translate_path(self.path)
        if not os.path.exists(path):
            # If not found, serve index.html for SPA routing
            self.path = "/index.html"
        return super().do_GET()

if __name__ == "__main__":
    handler = SPAServer
    # Enable address reuse to avoid OSError: [Errno 98] Address already in use
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving SPA at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
