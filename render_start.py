"""
Render Web Service entry point.
- Starts an HTTP health server immediately so Render's port check always passes.
- Runs the bot (magic.py) as a subprocess with auto-restart on crash.
- Sets DISABLE_HEALTH_SERVER=1 so magic.py does NOT try to bind the same port.
"""
import os
import sys
import time
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK - Bot is running")

    def log_message(self, format, *args):
        pass


def start_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"[render_start] Health server listening on port {port}", flush=True)
    server.serve_forever()


def run_bot():
    bot_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "magic.py")
    restart_delay = 5

    # Pass all current env vars, but tell magic.py not to start its own health server
    env = os.environ.copy()
    env["DISABLE_HEALTH_SERVER"] = "1"

    while True:
        print("[render_start] Starting bot (magic.py)...", flush=True)
        proc = subprocess.Popen([sys.executable, bot_script], env=env)
        exit_code = proc.wait()
        print(
            f"[render_start] Bot exited with code {exit_code}. "
            f"Restarting in {restart_delay}s...",
            flush=True,
        )
        time.sleep(restart_delay)


if __name__ == "__main__":
    # Start HTTP server in background daemon thread — stays alive always.
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Run bot in main thread with infinite restart loop.
    run_bot()
