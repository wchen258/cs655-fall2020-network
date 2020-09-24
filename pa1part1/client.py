# client

import socket

from util import base_parser, MAX_BYTE


def get_client_parser():
    parser = base_parser(True)  # with address
    return parser


if __name__ == '__main__':
    args = get_client_parser().parse_args()
    HOST = args.host
    PORT = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        msg = input()
        s.sendall(msg.encode())
        data = s.recv(MAX_BYTE)
        print(data.decode())
