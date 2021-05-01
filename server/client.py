#!/usr/bin/env python3

import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 3000        # The port used by the server

m = {"type": "connect", "payload": {"name": "Philipp"}}

data = json.dumps(m)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(data+'\n',encoding="utf-8"))
    s.sendall(bytes(data+'\n',encoding="utf-8"))
    s.sendall(bytes(data+'\n',encoding="utf-8"))
    data = s.recv(1024)

print('Received', repr(data))