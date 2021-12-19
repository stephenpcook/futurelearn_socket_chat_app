#!/usr/bin/env python
# chat_app.py, Stephen C for futurelearn sockets MOOC, 2021.
import socket
import argparse


def main(as_client, port):
    if as_client:
        # Client
        print(f'Setting up as client on port {port}')
        sock = setup_as_client(port)

        s = input('You:')
        send_msg(sock, s)
    else:
        # Server
        print(f'Setting up as server on port {port}')
        sock = setup_as_server(port)

    try:
        while True:
            s_in = recv_msg(sock)
            if not s_in:
                print('Partner closed connection')
                break
            print('them: ' + s_in)
            s_out = input('You: ')
            send_msg(sock, s_out)
            if not s_out:
                print('Closing connection')
                break
    except KeyboardInterrupt:
        print('Closing connection')

    sock.close()


def setup_as_server(port=8081) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen()
    print("Waiting for connection")
    connection_socket, address = server_socket.accept()
    print(f"Client connected: {address}")
    return connection_socket


def setup_as_client(port=8081) -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", port))
    print("Connected to server")
    return client_socket


def send_msg(connection_socket, message):
    connection_socket.send(message.encode())


def recv_msg(connection_socket):
    message = connection_socket.recv(1024).decode()
    return message


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', action="store_true")
    parser.add_argument('-p', '--port', type=int, default=8081)
    print('Run options set via arguments (run with flag --help for details)')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    main(args.client, args.port)
