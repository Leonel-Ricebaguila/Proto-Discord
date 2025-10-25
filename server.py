"""Simple HTTP server for Render web service health checks."""
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple handler that responds to health checks."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Discord bot is running!')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress HTTP server logs."""
        pass  # Suppress logs to keep console clean


def start_server(port=10000):
    """Start HTTP server in background thread."""
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f'✓ HTTP server started on port {port} for health checks')
    return server


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    start_server(port)
    print(f'Health check server running on http://0.0.0.0:{port}')
    
    # Keep running
    import time
    while True:
        time.sleep(3600)

