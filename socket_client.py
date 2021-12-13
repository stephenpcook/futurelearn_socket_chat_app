#!/usr/bin/env python
# socket_client.py
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


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8081))
print("Connected")

for message in get_text(client_socket):
    print(message)
print('Finished receive')

send_text(client_socket, "Thanks for letting me in")
print("Sent a reply")

client_socket.close()
