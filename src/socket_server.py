#!/usr/bin/env python
# socket_server.gy
import socket

from socket_helper import send_text, get_text


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8081))
server_socket.listen()
print("Waiting for connection")
connection_socket, address = server_socket.accept()
print(f"Client connected: {address}")

message = "Hello, thanks for connecting"
send_text(connection_socket, message)

for in_message in get_text(connection_socket):
    print(in_message)

connection_socket.close()
server_socket.close()
