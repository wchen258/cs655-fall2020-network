# server

import socket
import threading

from util import base_parser, MAX_BYTE


def get_server_parser():
    parser = base_parser(False)  # without address
    return parser


def process_request(conn: socket, addr: tuple):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(MAX_BYTE)
            if not data:
                break
            conn.sendall(data)
    print('Connection', addr, 'closed')


if __name__ == '__main__':
    args = get_server_parser().parse_args()
    HOST = '0.0.0.0'  # bind all available IP addresses
    PORT = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:  # use multithreading to process requests simultaneously
            conn, addr = s.accept()
            threading.Thread(target=process_request, args=(conn, addr)).start()
