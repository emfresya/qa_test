from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = {
            "cpu": random.randint(80, 98),
            "mem": f"{random.randint(80, 97)}%",
            "disk": f"{random.randint(85, 99)}%",# иногда >95
            "uptime": "1d 2h 37m 6s"
        }
        self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
    # Запускаем на 0.0.0.0, чтобы был доступен из других контейнеров
    server = HTTPServer(("0.0.0.0", 8001), Handler)
    print("Mock server running on http://0.0.0.0:8001")
    server.serve_forever()