from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


class Handle(BaseHTTPRequestHandler):
    def __init__(self, client_address, request, server):
        super().__init__(client_address, request, server)
        self._get: dict = {}
        self._post: dict = {}
        self._cookie: dict = {}

    def do_GET(self):
        # 由于每次连接都会有GET favicon.ico，避免多余的GET处理
        if self.path == '/favicon.ico':
            from ..image import PNGIconHebill
            icon = PNGIconHebill()
            self.send_response(200)
            self.send_header('Content-type', 'image/x-icon')
            self.end_headers()
            self.wfile.write(icon.bites)
        else:
            # Refer to the reference.txt
            print(self.headers)
            headers = dict(self.headers)
            cookies = {}
            if 'Cookie' in headers:
                for key, morsel in SimpleCookie(headers['Cookie']).items():
                    cookies[key] = morsel.value
            q = urlparse(self.path).query
            get = {}
            if q:
                for p in q.split('&'):
                    k, v = p.split('=')
                    if get.get(k) is None:
                        get[k] = []
                    get[k].append(v)
            from .features.request.core import Request
            request = Request(
                cookies,
                get,
                parse_qs(self.rfile.read(
                    int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0).decode('utf-8')),
                headers
            )
            print(request.cookie)
            print(request.get)
            print(request.post)
            print(request.headers)
            # 继续相关操作
            try:
                # 发送响应状态码
                self.send_response(200)
                # 设置响应头
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # 响应内容
                self.wfile.write(b"Hello, world!")  # 将字符串转换为字节流并发送
            except ConnectionAbortedError as e:
                print("用户已经中断连接或其他异常:", e)

    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
