#!/usr/bin/env python
# socket_server.gy
import socket


def send_text(sending_socket, text):
    if (text and (text[-1] != '\n')):
        text += '\n'
    if not text:
        text = '\n'
    sending_socket.send(text.encode())


def get_text(recving_socket):
    buffer = ""

    socket_open = True
    while socket_open:
        data = recving_socket.recv(1024)

        if not data:
            socket_open = False

        buffer += data.decode()

        terminator_pos = buffer.find('\n')
        while (terminator_pos > -1):
            message = buffer[:terminator_pos]
            buffer = buffer[terminator_pos + 1:]
            yield message
            terminator_pos = buffer.find('\n')


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
