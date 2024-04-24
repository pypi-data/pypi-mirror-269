import os
from .handle import Handle
from http.server import HTTPServer


class WebServer:
    def __init__(self, host: str = '', port: int = 8000, root: str = None, handle=None):
        self._handle = handle if handle is not None else Handle
        self._host = host
        self._port = port
        self._server = None
        self._root = root if root else os.getcwd()

    @property
    def handle(self): return self._handle

    @property
    def host(self) -> str: return self._host

    @property
    def port(self) -> int: return self._port

    @property
    def server(self) -> HTTPServer:
        if self._server is None:
            self._server = HTTPServer((self.host, self.port), self.handle)
        return self._server

    def start(self):
        print(f'服务器开始运行')
        if self.host:
            print(f'- http://{self.host}:{self.port}')
        else:
            print(f'- http://127.0.0.1:{self.port}')
            print(f'- http://localhost:{self.port}')
            from ..sys import Sys
            ips = Sys.local_ips()
            for ip in ips:
                print(f'- http://{ip}:{self.port}')
            print(f'- http://{self.host}:{self.port}')

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print(f'服务器已经停止工作')
            pass

    def close(self):
        self.server.server_close()
        print(f'服务器已经停止工作')
