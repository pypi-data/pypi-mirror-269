import os
import socket
import sys


class Sys:
    @staticmethod
    def local_ips():
        ips = set()
        # 获取当前主机名
        hostname = socket.gethostname()  # 获取主机的所有地址信息
        addr_info = socket.getaddrinfo(hostname, None)
        for addr in addr_info:
            ip_address = addr[4][0]  # 提取IP地址
            ips.add(ip_address)
        return ips

    @staticmethod
    def python_exe_path():
        if len(sys.argv) > 0:
            python_script_path = sys.argv[0]
            return os.path.abspath(python_script_path)
        return None
