#!/usr/bin/env python3
import http.server, socketserver, subprocess, threading, time, os


socketserver.TCPServer.allow_reuse_address = True
PORT = 9003
COMPOSE_YML = "/opt/llm/docker-compose.yml"
INDEX_HTML = "/opt/llm/placeholder/index.html"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # serve index.html for any path
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(INDEX_HTML, "rb") as f:
            self.wfile.write(f.read())

        threading.Thread(target=start_docker, daemon=True).start()

def start_docker():
    print("Schedule docker compose command...")
    subprocess.Popen(
        ["sh", "-c", f"sleep 3 && docker compose -f {COMPOSE_YML} up -d"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp   # start new process group, detach from Python
    )

    print("Stopping placeholder server...")
    httpd.shutdown()
    httpd.server_close()
    print("Done.")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving placeholder on port {PORT}")
        httpd.serve_forever()
