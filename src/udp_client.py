#!/usr/bin/env python
# udp_client.py

import socket

server_address = '127.0.0.1'
port = 20001

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = 'hello server'.encode()
udp_client.sendto(data, (server_address, port))

data_back, address_back = udp_client.recvfrom(1024)
print(f'Received back from {address_back}')
print(data_back.decode())
