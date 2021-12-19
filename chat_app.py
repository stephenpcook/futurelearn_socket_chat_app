#!/usr/bin/env python
# chat_app.py

import socket
import logging
import argparse

from socket_helper import send_text, get_text


def setup_as_server(port=8081) -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen()
    logging.info("Waiting for connection")
    connection_socket, address = server_socket.accept()
    logging.info(f"Client connected: {address}")
    return connection_socket


def setup_as_client(port=8081) -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", port))
    logging.info("Connected")


def message_out(connection_socket):
    s = input('Input: ')
    send_text(connection_socket, s)


def message_in(connection_socket):
    for in_message in get_text(connection_socket):
        print(in_message)


def get_args():
    parser = argparse.ArgumentParser(description='Chat application')
    chat_type = parser.add_mutually_exclusive_group()
    chat_type.add_argument('-s',
                           '--server',
                           default=True,
                           dest='server',
                           action='store_true',
                           help='Start app as server [default]')
    chat_type.add_argument('-c',
                           '--client',
                           dest='server',
                           action='store_false',
                           help='Start app as client')
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        nargs='?',
                        default=8081,
                        help='Port to use [default:8081]')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Report more info')

    return parser.parse_args()


def main(args):
    port = args.port
    as_server = args.server

    if as_server:
        connection_socket = setup_as_server(port)
    else:
        connection_socket = setup_as_client(port)
        message_out(connection_socket)

    try:
        while True:
            message_in(connection_socket)

            message_out(connection_socket)
            # If the connection drops, we want to close out the code
    except KeyboardInterrupt:
        pass

    connection_socket.close()


if __name__ == "__main__":
    args = get_args()
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)

    main(args)
