# client

import csv
import os
import socket
import time
from datetime import datetime

import numpy as np
import tqdm

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

    ndir = './results/'+str(datetime.now())
    if not os.path.exists(ndir):
        os.makedirs(ndir)

    for measurement in MEASUREMENTS:
        # with open(measurement, 'w') as f:  # output file
        desc = measurement+'_delays'
        for server_delay in tqdm.tqdm(SERVER_DELAYS, desc=desc):
            path = os.path.join(ndir, '_'.join(
                [measurement, str(server_delay)]))
            with open(path+'.csv', 'a+') as f:
                csvwriter = csv.writer(f, delimiter=',')
                for message_size in MEASUREMENTS[measurement]:
                    tql = '_'.join([measurement, str(server_delay),
                                    'ms', str(message_size), 'bytes'])
                    tqdm.tqdm.write(tql)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((HOST, PORT))
                        # Connection Setup Phase
                        write_line(
                            s, f's {measurement} {NUMBER_OF_PROBES} {message_size} {server_delay}')
                        tqdm.tqdm.write(read_line(s))
                        # Measurement Phase
                        rtts = []
                        for i in range(NUMBER_OF_PROBES):
                            # always send xs as payload
                            msg = f'm {i+1} ' + 'x' * message_size
                            start = time.time()
                            write_line(s, msg)
                            data = read_line(s)
                            end = time.time()
                            # print((end - start)*1000, file=f)
                            tqdm.tqdm.write(data)
                            rtts.append((end-start)*1000)
                        # Connection Termination Phase
                        csvwriter.writerow(
                            [message_size, np.average(rtts), np.std(rtts)])
                        write_line(s, 't')
                        tqdm.tqdm.write(read_line(s))
