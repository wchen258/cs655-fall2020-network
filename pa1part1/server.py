# server

import socket
import threading

from util import *


def get_server_parser():
    parser = base_parser(False)  # without address
    return parser


def process_request(conn: socket.socket, addr: tuple):
    print('Connected by', addr)
    with conn:
        while True:
            msg = read_line(conn)
            if not msg:
                break
            write_line(conn, msg, False)
            if msg[-1] != '\n':
                break
    print('Connection', addr, 'closed')


if __name__ == '__main__':
    args = get_server_parser().parse_args()
    HOST = '0.0.0.0'  # bind all available IP addresses
    PORT = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:  # use multithreading to process requests simultaneously
            try:
                conn, addr = s.accept()
                threading.Thread(target=process_request, args=(conn, addr)).start()
            except:
                exit(0)
