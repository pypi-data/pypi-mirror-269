import asyncio
import queue
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
from typing import Optional
from urllib.parse import urlparse, parse_qsl


class CodeServer(HTTPServer):
    code: Optional[str]


class RequestHandler(BaseHTTPRequestHandler):
    server: CodeServer

    def log_message(self, format, *args):
        pass  # disable logging

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Login Successful! You can now close this tab.")

        self.server.code = dict(parse_qsl(self.path)).get("code", None)


def _start_flow(redirect_uri: str, timeout=300) -> Optional[str]:
    url = urlparse(redirect_uri)
    with CodeServer((url.hostname, url.port), RequestHandler) as server:
        server.timeout = timeout
        server.handle_request()
    return server.code


async def start_oauth_flow(redirect_uri: str, timeout=300) -> Optional[str]:
    return await asyncio.to_thread(_start_flow, redirect_uri, timeout)
