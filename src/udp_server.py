#!/usr/bin/env python
# udp_server.py

import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('0.0.0.0', 20001))
data, client_address = udp_server.recvfrom(1024)

print(f'Message from {client_address}')
print(data.decode())

udp_server.sendto(data, client_address)
