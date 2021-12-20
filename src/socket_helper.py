# socket_helper.py
import socket


def send_text(sending_socket: socket.socket, text: str) -> None:
    if (text and (text[-1] != '\n')):
        text += '\n'
    if not text:
        text = '\n'
    sending_socket.send(text.encode())


def get_text(recving_socket: socket.socket) -> str:
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
            buffer = buffer[(terminator_pos + 1):]
            yield message
            terminator_pos = buffer.find('\n')
