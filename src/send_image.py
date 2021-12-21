#!/usr/bin/env python
# send_image.py

from itertools import product
from pathlib import Path
import socket
import pickle

from fl_networking_tools import ImageViewer
from PIL import Image


def do_send():
    f = Path('images/image.bmp')
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    image = Image.open(f)
    width, height = image.size

    for pos in product(range(width), range(height)):
        pixel = image.getpixel(pos)
        data = pickle.dumps((pos, pixel))
        udp_client.sendto(data, ('127.0.0.1', 20001))
    udp_client.close()


def do_recv():
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind(('0.0.0.0', 20001))
    viewer = ImageViewer()

    def get_pixel_data():
        lost_pixels = 0
        last_pos = (-1, -1)
        try:
            while True:
                data, _ = udp_server.recvfrom(1024)
                pos, rgb = pickle.loads(data)
                lost_pixel = (((pos[0] - last_pos[0]) > 1)
                              or ((pos[1] - last_pos[1]) > 1))
                if lost_pixel:
                    lost_pixels += 1
                viewer.put_pixel(pos, rgb)
                viewer.text = str(lost_pixels)
                last_pos = pos
        except KeyboardInterrupt:
            pass

    viewer.start(get_pixel_data)

    udp_server.close()


def main():
    mode = ''
    while mode not in ['1', '2']:
        mode = input('Server [1] or client [2]:')
    mode_switch = {'1': do_recv, '2': do_send}
    mode_switch[mode]()


if __name__ == "__main__":
    main()
