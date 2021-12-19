#!/usr/bin/env python
# socket_client.py
import socket

from socket_helper import send_text, get_text


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8081))
print("Connected")

for message in get_text(client_socket):
    print(message)
print('Finished receive')

send_text(client_socket, "Thanks for letting me in")
print("Sent a reply")

client_socket.close()
