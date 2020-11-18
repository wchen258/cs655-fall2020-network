import argparse
import socket

MEASUREMENTS = {'rtt': (1, 100, 200, 400, 800, 1000),
                'tput': tuple(2**i for i in range(10, 16))}


def base_parser(with_address: bool):
    parser = argparse.ArgumentParser()
    if with_address:
        parser.add_argument('host', type=str, action='store')
    parser.add_argument('port', type=int, action='store')
    return parser


def read_line(s: socket.socket) -> str:
    ret = b''
    while True:
        byte = s.recv(1)
        if not byte:  # connection closed
            break
        ret += byte
        if byte == b'\n':  # end of message
            break
    return ret.decode()


def write_line(s: socket.socket, line: str, add_lf: bool = True):
    s.sendall(line.encode() + (b'\n' if add_lf else b''))
