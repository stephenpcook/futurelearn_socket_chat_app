#!/usr/bin/env python
# send_image.py

from itertools import product
from pathlib import Path
import socket
import pickle
from time import sleep
from random import randint, seed

from fl_networking_tools import ImageViewer
from PIL import Image


def do_send():
    f = Path('images/image.bmp')
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    image = Image.open(f)
    width, height = image.size

    seed(0)
    dropped = 0

    n_slowdown = 1000
    slowdownplease = []
    for pos in product(range(width), range(height)):
        if not(randint(0, 9)):
            dropped += 1
            continue
        pixel = image.getpixel(pos)
        data = pickle.dumps((pos, pixel))
        udp_client.sendto(data, ('127.0.0.1', 20001))
        for _ in range(n_slowdown):
            slowdownplease.append('Hello')
    udp_client.close()
    print(dropped)


def do_recv():
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server.bind(('0.0.0.0', 20001))
    viewer = ImageViewer()

    def get_pixel_data():
        lost_pixels = 0
        current_column = 0
        all_column_pixels = []
        column_pixels = 0
        old_pos = (0,0)
        max_column = 0
        try:
            while True:
                data, _ = udp_server.recvfrom(1024)
                pos, rgb = pickle.loads(data)
                column_pixels += 1
                viewer.put_pixel(pos, rgb)
                viewer.text = str(lost_pixels)
                # End of column, update missing pixels (does not work on last
                # column, or pixels arriving out of order)
                if (pos[0] > current_column):
                    # The most recent pixel was from the next column
                    all_column_pixels.append(column_pixels - 1)
                    # Check if we've missed an entire column
                    col_jump = current_column - pos[0]
                    if (col_jump > 1):
                        all_column_pixels.update([0] * (col_jump - 1))
                    # Check for a better estimate of the column height
                    max_column = max(old_pos[1], max_column)
                    expected_pixels = len(all_column_pixels) * max_column
                    lost_pixels = expected_pixels - sum(all_column_pixels)
                    # Setup for next column
                    current_column = pos[0]
                    # Don't forget the current pixel (so 1, not 0)
                    column_pixels = 1
                old_pos = pos
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
