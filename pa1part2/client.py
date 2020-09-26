# client

import socket
import time

from util import *


def get_client_parser():
    parser = base_parser(True)  # with address
    return parser


SERVER_DELAYS = (0, 1, 10, 20, 50, 100)
NUMBER_OF_PROBES = 15

if __name__ == '__main__':
    args = get_client_parser().parse_args()
    HOST = args.host
    PORT = args.port

    for measurement in MEASUREMENTS:
        with open(measurement, 'w') as f:  # output file
            for server_delay in SERVER_DELAYS:
                for message_size in MEASUREMENTS[measurement]:
                    print(measurement, server_delay,
                          'ms', message_size, 'bytes')
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((HOST, PORT))
                        # Connection Setup Phase
                        write_line(
                            s, f's {measurement} {NUMBER_OF_PROBES} {message_size} {server_delay}')
                        print(read_line(s), end='')
                        # Measurement Phase
                        for i in range(NUMBER_OF_PROBES):
                            # always send xs as payload
                            msg = f'm {i+1} ' + 'x' * message_size
                            start = time.time()
                            write_line(s, msg)
                            data = read_line(s)
                            end = time.time()
                            print((end - start)*1000, file=f)
                            print(data, end='')
                        # Connection Termination Phase
                        write_line(s, 't')
                        print(read_line(s), end='')
