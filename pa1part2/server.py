# server

import socket
import threading
import time

from util import *


def get_server_parser():
    parser = base_parser(False)  # without address
    return parser


CSP200 = '200 OK: Ready'
CSP404 = '404 ERROR: Invalid Connection Setup Message'
MP404 = '404 ERROR: Invalid Measurement Message'
CTP200 = '200 OK: Closing Connection'
CTP404 = '404 ERROR: Invalid Connection Termination Message'


def check_CSP_msg(msg: str):
    try:
        assert(msg[-1] == '\n') # LF in the end
        args = msg.split()
        assert(len(args) == 5) # 5 parts
        assert(sum(len(arg) for arg in args)+5 == len(msg)) # no more WS
        phase, measurement, number_of_probes, message_size, server_delay = args
        assert(phase == 's')
        assert(measurement in MEASUREMENTS) # rtt or tput
        number_of_probes = int(number_of_probes)
        assert(number_of_probes >= 0)
        message_size = int(message_size)
        assert(message_size in MEASUREMENTS[measurement]) # corresponding message size
        server_delay = int(server_delay)
        assert(server_delay >= 0)
        return (number_of_probes, message_size, server_delay)
    except: # assertion or conversion fails
        return False


def check_MP_msg(msg: str, sequence_number: int, message_size: int):
    try:
        assert(msg[-1] == '\n')
        args = msg.split()
        assert(args[0] == 'm')
        assert(int(args[1]) == sequence_number)
        assert(4+len(args[1])+message_size == len(msg))
        return True
    except:
        return False


def check_CTP_msg(msg: str):
    print(len(msg))
    return msg == 't\n'


def process_request(conn: socket.socket, addr: tuple):
    print('Connected by', addr)
    for _ in (True,): # one shot, support break from with
        with conn:
            # Connection Setup Phase
            msg = read_line(conn)
            valid = check_CSP_msg(msg)
            if not valid:
                write_line(conn, CSP404)
                break
            number_of_probes, message_size, server_delay = valid
            write_line(conn, CSP200)
            # Measurement Phase
            for i in range(number_of_probes):
                msg = read_line(conn)
                valid = check_MP_msg(msg, i+1, message_size)
                if not valid:
                    write_line(conn, MP404)
                    break
                time.sleep(server_delay/1000)
                write_line(conn, msg, False)
            else: # no error
                # Connection Termination Phase
                msg = read_line(conn)
                valid = check_CTP_msg(msg)
                if not valid:
                    write_line(conn, CTP404)
                    break
                write_line(conn, CTP200)
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
